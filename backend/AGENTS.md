# backend/AGENTS.md

Applies to everything under `backend/`. Root `AGENTS.md` rules also apply.

## Layering

`api/v1` (HTTP, validation, auth deps) -> `services` (business logic) -> `models` (DB). `ai/` is called only from services.
Routes stay thin: parse input, call a service, shape the response. No SQL in routes.

## Rules

- Async everywhere (`async def`, `AsyncSession`). Do not block the event loop; wrap CPU-bound work.
- Pydantic v2 models in `schemas/`; never return ORM objects directly. `password_hash` must never appear in any response model.
- Settings only through `app/core/config.py`.
- DB access uses one `AsyncSession` per request via dependency. Keep pool small (serverless): `pool_size<=5`.
- Streaming chat endpoint returns `text/event-stream` with the event types defined in `docs/api/openapi.yaml`. Never buffer the stream.
- Conversation state (stage, slots, messages) lives in PostgreSQL. Never keep it in process memory (Cloud Run is stateless). Langflow flows are stateless; send context on every call.
- Roles: `student`, `admin`. Admin is granted by `ADMIN_EMAILS` allowlist at login/registration time.
- Auth: Argon2id password hashing, short-lived JWT access token, rotating refresh token, login rate limit.

## AI layer (Langflow + FastAPI)

- Only `app/ai/langflow/client.py` talks to Langflow. It picks the flow variant (`router` or `vertex`) with a circuit breaker per variant. Never call an LLM provider directly.
- Contracts for every flow: `docs/api/langflow-flows.md`. Validate every flow output with a Pydantic model in `app/ai/schemas/`; invalid output counts as a failure (retry, then fallback).
- The dialog manager (`app/ai/dialog/state.py`) is pure logic: stage, slots, intent -> next stage and action. Keep it free of I/O so it stays unit-testable.
- Retrieval over the catalog (pgvector, filters, `status = active`) is done in FastAPI. Roadmap candidates are a **closed set**; the LLM may only pick from it. After generation, verify every `ref_id` and URL against the catalog.
- Internal tool endpoints for Langflow live under `/internal/tools/*`, require `X-Internal-Token`, are read-only, and are not part of the public OpenAPI (`docs/api/internal-tools.openapi.yaml`).
- Embeddings only through `app/ai/embeddings/` (Vertex AI by default).
- Record every flow call in `ai_runs` (flow, variant, latency, tokens, fallback). Never store message content there.

## Testing

- `pytest` with `pytest-asyncio`. Use a real PostgreSQL (pgvector image) for DB tests, not SQLite.
- Never call real Langflow or LLMs in unit tests: use `httpx.MockTransport` or a fake `LangflowClient`. AI evals in `tests/ai/` use fakes unless `RUN_LIVE_LLM=1`.
- Every endpoint: happy path, validation error, auth failure, permission failure.
- Dialog manager: cover every stage transition. Circuit breaker: closed, open, half-open.

## Migrations

`alembic revision --autogenerate -m "<message>"`, review the generated file, then `make migrate`. Keep migrations reversible when practical. The Langflow database (`langflow`) is managed by Langflow, not by Alembic.
