---
name: nextjs-feature
description: Build a frontend feature in Next.js (feature folder, typed API client, loading/empty/error states, i18n, accessibility, tests). Use for any UI work in frontend/.
---

# Next.js feature

## Steps

1. Read the spec and the OpenAPI operations it uses. Run `npm run gen:api` if the contract changed.
2. Create `src/features/<feature>/` with `components/`, `hooks/`, `api/`, `types/` as needed. Shared pieces go to `src/components/`.
3. Server components by default; add `"use client"` only for state, effects, or browser APIs.
4. Use generated API types. Do not hand-write response types that exist in the contract.
5. Cover four states for every data view: loading, empty, error, success.
6. Put all Indonesian strings in `src/lib/i18n/id.ts`.
7. Accessibility: labels, visible focus, keyboard support, contrast, 360 px width.
8. Show the AI label (`id.aiLabel`) wherever AI-generated content appears.
9. Tests with Vitest + Testing Library for each state (see skill `write-tests`).
10. Run `npm run lint && npm run typecheck && npm test`.

## Rules

- Access token lives in memory only; never in `localStorage` or `sessionStorage`.
- Streaming chat uses `fetch` + `ReadableStream` with the `Authorization` header (not `EventSource`).
- No `any`. No inline magic numbers for colors or spacing; use shared tokens.
