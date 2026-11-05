import httpx
import pytest

from app.ai.langflow.client import (
    FlowOutputError,
    LangflowClient,
    LangflowUnavailableError,
    extract_json,
    extract_text,
    flow_name,
)
from app.core.config import Settings


def run_payload(text: str) -> dict:
    return {"outputs": [{"outputs": [{"results": {"message": {"text": text}}}]}]}


def make_client(handler) -> LangflowClient:
    settings = Settings(
        llm_provider="router",
        llm_fallback_provider="vertex",
        langflow_api_key="test-key",
        llm_circuit_failure_threshold=2,
    )
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="http://langflow")
    return LangflowClient(settings, http=http)


def test_flow_name_convention() -> None:
    assert flow_name("slot-extractor", "router") == "slot-extractor__router"


def test_extract_text_and_json() -> None:
    assert extract_text(run_payload("halo")) == "halo"
    assert extract_json(run_payload('{"intent": "provide_info"}')) == {"intent": "provide_info"}


def test_extract_rejects_bad_shapes() -> None:
    with pytest.raises(FlowOutputError):
        extract_text({"outputs": []})
    with pytest.raises(FlowOutputError):
        extract_json(run_payload("bukan json"))


FLOWS = [
    {"name": "slot-extractor__router", "id": "r1"},
    {"name": "slot-extractor__vertex", "id": "v1"},
]


async def test_falls_back_to_vertex_when_router_fails() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/v1/flows/":
            return httpx.Response(200, json=FLOWS)
        if request.url.path.endswith("/r1"):
            return httpx.Response(500)
        return httpx.Response(200, json=run_payload("{}"))

    client = make_client(handler)
    result = await client.run("slot-extractor", "{}", "session-1")
    assert result.variant == "vertex" and result.fallback_used is True


async def test_raises_when_all_variants_fail() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/v1/flows/":
            return httpx.Response(200, json=FLOWS)
        return httpx.Response(503)

    client = make_client(handler)
    with pytest.raises(LangflowUnavailableError):
        await client.run("slot-extractor", "{}", "session-1")


async def test_open_circuit_skips_primary_variant() -> None:
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/v1/flows/":
            return httpx.Response(200, json=FLOWS)
        calls.append(request.url.path)
        if request.url.path.endswith("/r1"):
            return httpx.Response(500)
        return httpx.Response(200, json=run_payload("{}"))

    client = make_client(handler)
    for _ in range(2):  # threshold is 2: opens the router circuit
        await client.run("slot-extractor", "{}", "s")
    calls.clear()
    await client.run("slot-extractor", "{}", "s")
    assert all(path.endswith("/v1") for path in calls)
