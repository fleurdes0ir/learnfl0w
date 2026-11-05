---
name: write-tests
description: Write or improve pytest and Vitest tests (real PostgreSQL, fake LLM, component states, deterministic). Use when adding behavior, fixing a bug, or when coverage is missing.
---

# Write tests

Read `docs/engineering/testing-strategy.md` if unsure about scope.

## Backend (pytest)

- Real PostgreSQL (pgvector image) via fixtures; each test sets up its own data and rolls back.
- Helper fixtures: authenticated client for `student` and `admin`, user factory, fake `LangflowClient` or `httpx.MockTransport` (never call real Langflow or an LLM; `RUN_LIVE_LLM=1` only for AI evals, with permission).
- Every endpoint: happy path, validation error (422), unauthenticated (401), wrong role (403), cross-user access (404/403).
- Naming: `test_<unit>_<scenario>_<expected>`. Use `pytest.mark.parametrize` for input variants.
- Deterministic: no sleeping, no wall-clock reliance (freeze or inject time), seed any randomness.

## Frontend (Vitest + Testing Library)

- Test behavior through the DOM (roles, labels), not implementation details.
- Cover loading, empty, error, and success. Mock `fetch` with fixtures derived from OpenAPI examples.
- Keyboard interaction for interactive components.

## Quality bar

- Bug fix: write the failing test first, then fix.
- A good test fails when the behavior breaks: briefly break the code to confirm.
- Never weaken an assertion to make a test pass; say so if production code must change.
- Run the narrow test while iterating, then `make check`.
