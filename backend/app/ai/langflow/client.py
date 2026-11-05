"""Client for the private Langflow service. The only module that talks to Langflow.

Flows are named `<flow>__<variant>` (variant: router | vertex). The primary variant comes from
`LLM_PROVIDER`; the fallback from `LLM_FALLBACK_PROVIDER`. A circuit breaker per variant decides
which one to call. Endpoint details and response shapes must be verified against the pinned
Langflow version (see langflow/README.md, SPEC-011 T-3).
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from typing import Any

import httpx

from app.ai.langflow.circuit import CircuitBreaker
from app.core.config import Settings

IdTokenProvider = Callable[[], Awaitable[str]]


class LangflowUnavailableError(RuntimeError):
    """Raised when no flow variant could be reached."""


class FlowOutputError(ValueError):
    """Raised when a flow response does not contain the expected output."""


@dataclass(frozen=True)
class RunResult:
    variant: str
    payload: dict[str, Any]
    fallback_used: bool

    @property
    def text(self) -> str:
        return extract_text(self.payload)


def flow_name(flow: str, variant: str) -> str:
    return f"{flow}__{variant}"


def extract_text(payload: dict[str, Any]) -> str:
    """Return the chat output text from a non-stream `run` response (verify shape per version)."""
    try:
        text = payload["outputs"][0]["outputs"][0]["results"]["message"]["text"]
    except (KeyError, IndexError, TypeError) as exc:
        raise FlowOutputError("unexpected Langflow response shape") from exc
    if not isinstance(text, str):
        raise FlowOutputError("flow output is not text")
    return text


def extract_json(payload: dict[str, Any]) -> dict[str, Any]:
    """Parse the JSON object a non-stream flow returns as text."""
    raw = extract_text(payload).strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FlowOutputError("flow output is not valid JSON") from exc
    if not isinstance(data, dict):
        raise FlowOutputError("flow output JSON is not an object")
    return data


class LangflowClient:
    def __init__(
        self,
        settings: Settings,
        http: httpx.AsyncClient | None = None,
        id_token_provider: IdTokenProvider | None = None,
    ) -> None:
        self._settings = settings
        self._http = http or httpx.AsyncClient(base_url=settings.langflow_base_url)
        self._id_token_provider = id_token_provider
        self._flow_ids: dict[str, str] = {}
        self.breakers: dict[str, CircuitBreaker] = {
            variant: CircuitBreaker(
                failure_threshold=settings.llm_circuit_failure_threshold,
                reset_seconds=settings.llm_circuit_reset_seconds,
            )
            for variant in {settings.llm_provider, settings.llm_fallback_provider}
        }

    def variants_in_order(self) -> list[str]:
        order = [self._settings.llm_provider, self._settings.llm_fallback_provider]
        seen: list[str] = []
        for variant in order:
            if variant not in seen and self.breakers[variant].allow():
                seen.append(variant)
        return seen

    async def _headers(self) -> dict[str, str]:
        headers = {"x-api-key": self._settings.langflow_api_key}
        if self._id_token_provider is not None:
            headers["Authorization"] = f"Bearer {await self._id_token_provider()}"
        return headers

    async def _resolve_flow_id(self, name: str) -> str:
        if name not in self._flow_ids:
            response = await self._http.get("/api/v1/flows/", headers=await self._headers())
            response.raise_for_status()
            self._flow_ids = {f["name"]: f["id"] for f in response.json()}
        try:
            return self._flow_ids[name]
        except KeyError as exc:
            raise FlowOutputError(f"flow not found in Langflow: {name}") from exc

    def _body(self, input_value: str, session_id: str, tweaks: dict[str, Any] | None) -> dict[str, Any]:
        body: dict[str, Any] = {
            "input_value": input_value,
            "input_type": "chat",
            "output_type": "chat",
            "session_id": session_id,
        }
        if tweaks:
            body["tweaks"] = tweaks
        return body

    async def run(
        self,
        flow: str,
        input_value: str,
        session_id: str,
        *,
        timeout: float | None = None,
        tweaks: dict[str, Any] | None = None,
    ) -> RunResult:
        """Run a non-stream flow, falling back to the other variant when needed."""
        primary = self._settings.llm_provider
        for variant in self.variants_in_order():
            breaker = self.breakers[variant]
            try:
                flow_id = await self._resolve_flow_id(flow_name(flow, variant))
                response = await self._http.post(
                    f"/api/v1/run/{flow_id}",
                    json=self._body(input_value, session_id, tweaks),
                    headers=await self._headers(),
                    timeout=timeout or self._settings.langflow_timeout_seconds,
                )
                response.raise_for_status()
            except (httpx.HTTPError, FlowOutputError):
                breaker.record_failure()
                continue
            breaker.record_success()
            return RunResult(variant, response.json(), fallback_used=variant != primary)
        raise LangflowUnavailableError(f"no variant of flow '{flow}' is available")

    async def stream(
        self, flow: str, input_value: str, session_id: str, *, tweaks: dict[str, Any] | None = None
    ) -> AsyncIterator[str]:
        """Yield raw event lines from a streaming flow. Fails over only before the first byte."""
        for variant in self.variants_in_order():
            breaker = self.breakers[variant]
            started = False
            try:
                flow_id = await self._resolve_flow_id(flow_name(flow, variant))
                async with self._http.stream(
                    "POST",
                    f"/api/v1/run/{flow_id}",
                    params={"stream": "true"},
                    json=self._body(input_value, session_id, tweaks),
                    headers=await self._headers(),
                    timeout=self._settings.langflow_timeout_seconds,
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        started = True
                        yield line
                breaker.record_success()
                return
            except (httpx.HTTPError, FlowOutputError):
                breaker.record_failure()
                if started:
                    raise LangflowUnavailableError("stream interrupted") from None
        raise LangflowUnavailableError(f"no variant of flow '{flow}' is available")
