# frontend/AGENTS.md

Applies to everything under `frontend/`. Root `AGENTS.md` rules also apply.

## Rules

- Next.js App Router, TypeScript `strict`, no `any`. Prefer server components; mark client components explicitly (`"use client"`).
- Feature code lives in `src/features/<feature>/` (components, hooks, api, types). Shared UI in `src/components/`.
- API types come from `docs/api/openapi.yaml` via `npm run gen:api` (output in `src/lib/api/schema.d.ts`). Do not hand-write response types that exist in the contract.
- Streaming chat uses `fetch` + `ReadableStream` (needs the `Authorization` header, so not `EventSource`). Parse events exactly as the OpenAPI spec defines.
- Roadmap rendering uses `@xyflow/react`. Node types: `stage`, `course`, `material`, `certification`. Layout must be computed from the roadmap JSON (stages left to right); no hardcoded positions.
- Store the access token in memory only; refresh through the refresh endpoint. Never store tokens in `localStorage`.
- UI language: Indonesian. Keep strings in one place (`src/lib/i18n/id.ts`) for easy editing.
- Accessibility: keyboard navigation, visible focus, sufficient contrast, labels on every control. Mobile width from 360 px.
- Always show a clear label that AI-generated content is AI-generated.

## Testing

- Unit/component tests with Vitest + Testing Library. Mock the API with fixtures derived from the OpenAPI examples.
- Test: loading, empty, error, and success states for every data-driven view.
