# Testing Strategy

> **Status:** Active | **Owner:** LearnFl0w | **Updated:** 2026-10-31

## Goals

- Catch regressions early and cheaply; keep the suite fast and deterministic.
- Prove the acceptance criteria in each spec.
- Protect the riskiest parts: authorization, AI grounding, data privacy.

## Test Pyramid

| Level | Tooling | Scope | Target |
|---|---|---|---|
| Unit | pytest, Vitest | Pure logic: validators, layout, CSV parsing, guardrails | Majority of tests, milliseconds each |
| Integration | pytest + real PostgreSQL (pgvector image) | Routes + services + DB, auth and RBAC | Every endpoint |
| Component | Vitest + Testing Library | UI states: loading, empty, error, success | Every data-driven view |
| AI evaluation | pytest (`backend/tests/ai/`) | Personas, grounding, schema validity, injection | Run on prompt or agent changes |
| End-to-end smoke | curl or Playwright (optional) | Health and one full consultation | After each deploy |

## Rules

1. **Real database for DB tests.** Do not use SQLite for code that relies on PostgreSQL or pgvector features.
2. **Never call real Langflow or LLMs in unit tests.** Use `httpx.MockTransport` or a fake `LangflowClient`. Live runs only with `RUN_LIVE_LLM=1`.
3. **Every endpoint:** happy path, validation error, unauthenticated, wrong role, cross-user access.
4. **Deterministic tests:** no sleeping, no reliance on wall-clock or random without seeds.
5. **Independent tests:** each test sets up its own data and cleans up.
6. **Bug fixes** start with a failing test that reproduces the bug.

## Coverage

- Backend: at least 70% line coverage; critical modules (`auth`, `ai/guardrails`, `services/roadmap`) aim for 90%.
- Frontend: coverage reported, not gated; component states required for all data views.

## AI Evaluation Suite

Location: `backend/tests/ai/`. Personas in `personas/*.json` (20 synthetic students with profile, transcript, expected path candidates).

| Metric | Target |
|---|---|
| Schema validity | at least 98% |
| Grounding (all `ref_id` and URLs exist in catalog) | 100% |
| Graph rules (DAG, no orphans, order) | 100% |
| Completed courses never recommended as new work | 100% |
| Budget preference respected | 100% |
| Injection and off-topic handled | 100% |

Manual relevance review (rubric 1 to 5, average at least 4) is done by both team members before the demo.

## Reliability Checks (before demo)

- Fallback test: make the primary flow variant fail and confirm the consultation still works; stop Langflow and confirm the template roadmap is returned.
- Local staging gate: `make staging-up && make smoke` on branch `dev` before every release PR.
- Light load test: 20 concurrent sessions, no errors, latency within targets.
- Deploy test: broken revision triggers automatic rollback.
- Full demo rehearsal at least twice.

## CI

`make check` runs lint, typecheck, and tests. CI repeats it on every PR with a PostgreSQL service container.
