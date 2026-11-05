# Coding Standards

> **Status:** Active | **Owner:** LearnFl0w | **Updated:** 2026-10-31
> Loaded into every OpenCode session via `opencode.json`. Keep it short and enforceable.

## General

- Small, focused functions and modules. Prefer clarity over cleverness.
- Code, identifiers, comments, and commit messages are in **English**. User-facing strings are in Indonesian.
- No dead code, no commented-out blocks, no `TODO` without an issue reference.
- Every behavior change comes with a test.
- Do not log secrets, tokens, message content, or personal data.

## Python (backend)

- Python 3.12. Type hints on all public functions. `mypy --strict` clean on `app/`.
- Format and lint with `ruff` (`ruff format`, `ruff check`). Line length 100.
- Async everywhere: `async def` routes and `AsyncSession`. Never block the event loop.
- Layering: `api` -> `services` -> `models`. Routes only parse, call a service, and shape the response.
- Pydantic v2 schemas for all I/O. Never return ORM objects. Never expose `password_hash`.
- Settings via `app/core/config.py` only. No `os.environ` elsewhere.
- Errors: raise domain exceptions in services; map them to RFC 7807 problem responses in one handler. No bare `except`.
- Naming: `snake_case` functions and modules, `PascalCase` classes, `UPPER_SNAKE` constants.
- Database: Alembic migrations only; never edit an applied migration. Use explicit transactions in services that touch several tables.
- Imports: standard library, third-party, first-party; no wildcard imports.

## TypeScript (frontend)

- `strict` mode; no `any`; prefer `unknown` and narrow.
- ESLint (`next/core-web-vitals`, `next/typescript`) and Prettier. Zero warnings in CI.
- Server components by default; `"use client"` only when state, effects, or browser APIs are needed.
- Feature folders: `src/features/<feature>/{components,hooks,api,types}`.
- API types come from `docs/api/openapi.yaml` (`npm run gen:api`). Do not duplicate them by hand.
- Naming: `PascalCase` components, `camelCase` functions and variables, `kebab-case` file names for non-components.
- Styling: consistent design tokens; no inline magic numbers for colors or spacing.
- Accessibility is a requirement, not a polish step: labels, focus states, keyboard support, contrast.

## API design

- Contract first: change `docs/api/openapi.yaml` before code.
- Plural nouns, versioned under `/api/v1`. Use `PUT` for replace, `POST` for create or actions, `DELETE` for removal.
- Pagination with `page` and `page_size`. Errors as `application/problem+json`.
- Never break a published field silently; add fields instead of changing meaning.

## Security

- Validate all input at the boundary. Authorize in the backend on every endpoint.
- Passwords: Argon2id. Tokens: short-lived JWT, rotating refresh tokens.
- Secrets from environment or Secret Manager only. `.env` is never committed.
- Treat LLM output and user text as untrusted data. Validate before use or display.

## AI code

- The backend never calls an LLM directly. LLM work happens in Langflow flows, reached only through `backend/app/ai/langflow/client.py`. Embedding SDKs only in `backend/app/ai/embeddings/`.
- Prompts live inside Langflow flows (exported to `langflow/flows/`). No catalog names, URLs, or secrets inside flows.
- The dialog manager (`backend/app/ai/dialog/`) is pure logic with no I/O.
- Every roadmap item must be verified against the catalog before it is stored or shown; candidates are a closed set prepared by FastAPI.

## Dependencies

- Add a dependency only with a stated reason in the PR. Prefer the standard library and existing dependencies.
- Pin versions through lockfiles; do not edit lockfiles by hand.

## Reviews

- Each PR is reviewed by the other team member (or the `reviewer` agent plus a human).
- A PR is ready when `make check` is green, acceptance criteria are met, and docs are updated.
