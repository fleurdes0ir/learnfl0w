# AGENTS.md

Rules for AI coding agents (OpenCode) working in this repository. Keep this file short; details live in `docs/`.

## Project

IT Career Compass (team LearnFl0w): an AI career-mapping platform for IT students. A student completes a guided AI consultation and receives a node-edge roadmap linking campus courses, learning materials, and certifications. University project (Cloud Computing final exam), demo deadline **2026-12-08**. Development and staging run **locally** (Docker Compose); the serverless GCP deployment happens **at the end** (2026-11-28 to 2026-12-03).

## Source of truth

Read the relevant document **before** coding. Load them on demand, do not read everything.

| Need | File |
|---|---|
| Product requirements | `docs/product/PRD.md` |
| Feature to build | `docs/specs/SPEC-*.md` (index: `docs/specs/README.md`) |
| HTTP contract | `docs/api/openapi.yaml`, `docs/api/roadmap.schema.json` |
| Data model | `docs/architecture/data-model.md` |
| AI design | `docs/architecture/ai-design.md` |
| Langflow flow contracts | `docs/api/langflow-flows.md`, `docs/api/internal-tools.openapi.yaml`, `langflow/README.md` |
| System design, deploy | `docs/architecture/overview.md`, `docs/architecture/deployment.md` |
| Past decisions | `docs/adr/` |
| Backend rules (when working in `backend/`) | `backend/AGENTS.md` |
| Frontend rules (when working in `frontend/`) | `frontend/AGENTS.md` |
| Code style details | `docs/engineering/coding-standards.md` |

If code and docs disagree, **stop and ask**. Update the docs in the same change when behavior changes.

## Tech stack

- Backend: Python 3.12, FastAPI, SQLAlchemy 2 async (psycopg 3), Alembic, Pydantic v2. The AI layer is **Langflow** (visual flows), called by FastAPI through `app/ai/langflow/`.
- Frontend: Next.js (App Router), TypeScript strict, React Flow (`@xyflow/react`).
- AI layer: Langflow (pinned version, private service) with `router` (9router) and `vertex` (Vertex AI) variants of every flow.
- Data: PostgreSQL 16 + pgvector. No other datastore.
- Cloud: GCP Cloud Run, Cloud SQL, Vertex AI, Secret Manager. CI/CD: GitHub Actions.

## Commands

```bash
make up          # start local stack (db, langflow, backend, frontend)
make staging-up  # production-like local staging (run from branch dev)
make smoke       # health checks for all services
make flows-check # validate exported Langflow flows
make check       # lint + typecheck + tests  (must pass before you say "done")
make test        # all tests
make lint        # ruff + eslint
make format      # ruff format + prettier
make migrate     # alembic upgrade head
make seed        # load data/seed into the database
```

Backend only: `cd backend && pytest -q`, `ruff check .`. Frontend only: `cd frontend && npm run typecheck && npm run lint && npm test`.

## Repo map

- `backend/app/api/v1/` HTTP routes (thin). `services/` business logic. `models/` SQLAlchemy. `schemas/` Pydantic.
- `backend/app/auth/` password hashing, JWT, RBAC dependencies.
- `backend/app/ai/` `dialog/` (deterministic dialog manager), `langflow/` (client + circuit breaker), `guardrails/`, `tools/`, `embeddings/`, `schemas/`. Backend code never calls an LLM directly.
- `langflow/` Dockerfile, exported flows (`flows/`), manifest, validation scripts.
- `frontend/src/app/` routes. `features/<name>/` feature code. `components/` shared UI. `lib/` API client, utils.
- `data/seed/` catalog seed files. `infra/` deploy config. `docs/` documentation.

## Workflow

1. **Spec first.** Do not implement a feature that has no `docs/specs/SPEC-*.md`. Propose a spec instead.
2. Use the **Plan** agent to propose an approach; wait for approval; then use **Build**.
3. One task from a spec per change. Keep diffs small and focused.
4. Write or update tests together with the code.
5. Run `make check`. Report the actual result, never assume it passed.
6. Branching: branch from `dev` as `feat/`, `fix/`, or `chore/`; PR into `dev`; release by PR `dev` -> `main`. Never commit directly to `main` or `dev`. See `docs/engineering/git-workflow.md`.
7. Commit with Conventional Commits (`feat(chat): ...`). Do not commit unless asked.

## Conventions

- Python: type hints everywhere, `ruff` for lint and format, async endpoints and DB calls, no business logic in routes.
- TypeScript: `strict`, no `any`, API types generated from `docs/api/openapi.yaml` (`npm run gen:api`).
- Errors: return RFC 7807 problem JSON (see OpenAPI `Problem`). No bare `except`.
- Config: read via `app/core/config.py` (`Settings`). Never read `os.environ` elsewhere.
- Names: English for code and identifiers. Indonesian only for user-facing text and product docs.

## Hard rules (never)

- Never commit secrets, tokens, or real `.env` files. Use `.env.example` for new variables.
- Never hardcode certification, material, or course names/URLs in code or prompts. They come from the catalog tables only.
- Never trust LLM output. Validate with Pydantic and verify every `ref_id` against the catalog before use or display.
- Never log message content, passwords, tokens, or personal data.
- Never call an LLM from backend code. LLM work happens only inside Langflow flows, reached through `app/ai/langflow/`. Embedding SDKs only in `app/ai/embeddings/`.
- Never put secrets, API keys, or URLs of catalog items in flow JSON or prompts. Use Langflow global variables.
- Never edit applied Alembic migrations or lockfiles by hand. Add a new migration.
- Never add a dependency without stating why in the PR description.
- Never weaken auth, RBAC, rate limits, or guardrails to make a test pass.

## AI feature rules

- Roadmap content = selection and ordering of catalog items, plus short rationale. No invented entities or links.
- If validation fails twice, fall back to the career-path template roadmap (see `ai-design.md`).
- Prompts live inside Langflow flows, exported as JSON to `langflow/flows/` (`<flow>__router.json`, `<flow>__vertex.json`). Changing a flow requires `make flows-check` and the AI eval suite (`backend/tests/ai/`).
- The consultation stage and next action are decided by the dialog manager in code (`app/ai/dialog/`), not by the LLM. Roadmap candidates are a closed set prepared by FastAPI.

## Skills

Project skills live in `.opencode/skills/`. Load only what the task needs:

- Before writing any code: `lean-coding`. On long or wide tasks: `context-efficiency`.
- Endpoint: `fastapi-endpoint`, `api-contract-sync`. Schema change: `alembic-migration`. UI: `nextjs-feature`, `react-flow-roadmap`.
- Flow or roadmap work: `langflow-flow`, `roadmap-validation`. Catalog data: `catalog-curation`.
- Tests, bugs, restructuring: `write-tests`, `debug-fix`, `refactor-safe`. Risky changes: `security-review`.
- Deploy or ops (only in the deployment window): `cloud-run-deploy`. Finishing a change: `ship-change`.

## Efficiency

- Search before reading; read line ranges; never open lockfiles, generated files, or seed CSVs.
- Filter command output; run the narrowest test while iterating and `make check` once at the end.
- One task per session. At a natural breakpoint write `.opencode/handoff.md` and compact or start fresh.
- Report diff summary and check results only; do not paste code back.

## Definition of done

- Acceptance criteria in the spec are met and checked off.
- `make check` is green; new behavior has tests.
- `docs/api/openapi.yaml` and related docs updated when contracts change.
- No new lint or type errors, no leftover TODO without an issue reference.

## When unsure

Ask a short question instead of guessing, especially about product behavior, security, cost, or anything touching production.
