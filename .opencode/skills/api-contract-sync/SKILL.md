---
name: api-contract-sync
description: Keep docs/api/openapi.yaml, backend routes, and frontend generated types in sync (contract-first). Use whenever an endpoint, request, response, or error shape changes.
---

# API contract sync

Source of truth: `docs/api/openapi.yaml` (and `docs/api/roadmap.schema.json`).

## Steps

1. Change the contract **first**: operationId, parameters, schemas, responses (including 401/403/404/422/429 where relevant). Never change the meaning of an existing field; add fields instead.
2. Backend: implement or adjust routes and schemas to match (skill `fastapi-endpoint`).
3. Contract test: `backend/tests/test_openapi_contract.py` compares the paths, methods, and operationIds of `app.openapi()` with `docs/api/openapi.yaml`. If the test does not exist yet, create a small one.
4. Frontend: `cd frontend && npm run gen:api` regenerates `src/lib/api/schema.d.ts`. Commit the generated file; never edit it by hand.
5. Update fixtures used by frontend tests so they match the new examples.
6. Mention the contract change in the PR description.

## Checks

- No endpoint exists in code but not in the contract (or the reverse).
- Pagination (`page`, `page_size`) and RFC 7807 errors are used consistently.
- SSE event types match the description on `postMessage`.
