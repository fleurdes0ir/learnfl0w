"""AI service layer - flow calls and logging."""

import time
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.langflow.client import LangflowClient, LangflowUnavailableError, RunResult
from app.models.ai import AiRun


class AiService:
    """Wraps LangflowClient. Logs every call to ai_runs."""

    def __init__(self, client: LangflowClient, session: AsyncSession):
        self.client = client
        self.session = session

    async def run_flow(
        self,
        flow: str,
        input_value: str,
        session_id: str,
        conversation_id: str | None = None,
        tweaks: dict[str, object] | None = None,
    ) -> RunResult:
        """Call a non-stream flow and log the result."""
        start = time.monotonic()
        try:
            result = await self.client.run(flow, input_value, session_id, tweaks=tweaks)
            status = "success"
        except (LangflowUnavailableError, Exception):
            status = "failure"
            raise
        finally:
            latency_ms = int((time.monotonic() - start) * 1000)
            log_entry = AiRun(
                conversation_id=conversation_id,
                flow_name=flow,
                variant=result.variant if status == "success" else "unknown",
                status=status,
                latency_ms=latency_ms,
                fallback_used=result.fallback_used if status == "success" else False,
            )
            self.session.add(log_entry)
            await self.session.flush()

        return result

    async def stream_flow(
        self,
        flow: str,
        input_value: str,
        session_id: str,
        conversation_id: str | None = None,
        tweaks: dict[str, object] | None = None,
    ) -> AsyncIterator[str]:
        """Stream a flow and log when complete."""
        start = time.monotonic()
        variant = "unknown"
        status = "success"
        try:
            async for chunk in self.client.stream(flow, input_value, session_id, tweaks=tweaks):
                yield chunk
        except (LangflowUnavailableError, Exception):
            status = "failure"
            raise
        finally:
            latency_ms = int((time.monotonic() - start) * 1000)
            # ponytail: variant tracked in SPEC-005; stream doesn't expose it yet
            log_entry = AiRun(
                conversation_id=conversation_id,
                flow_name=flow,
                variant=variant,
                status=status,
                latency_ms=latency_ms,
                fallback_used=False,
            )
            self.session.add(log_entry)
            await self.session.flush()
