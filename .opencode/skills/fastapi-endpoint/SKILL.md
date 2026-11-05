---
name: fastapi-endpoint
description: Add or change a FastAPI endpoint (contract-first, thin route, service, schemas, RBAC, tests). Use for any new or modified HTTP endpoint in backend/.
---

# FastAPI endpoint

## Steps

1. Read the spec (`docs/specs/SPEC-*.md`) and the operation in `docs/api/openapi.yaml`. If the operation is missing or wrong, update the OpenAPI file first (operationId, request/response schemas, 401/403/404/422 as relevant) and confirm before coding.
2. **Schemas** in `app/schemas/`: separate input and output models. Never expose `password_hash` or secrets.
3. **Service** in `app/services/<area>.py`: all business logic, typed args, `AsyncSession`, raises domain exceptions.
4. **Route** in `app/api/v1/<area>.py`: thin (parse, call service, shape response). Use auth dependencies (`get_current_user`, `require_role`). Register in `app/api/v1/router.py`.
5. **Authorization:** check role in the backend and ownership for user data. Cross-user access returns 404 (or 403 for admin routes).
6. **Errors:** domain exception -> RFC 7807 via the global handler. No bare `except`.
7. **Tests** (real PostgreSQL): happy path, 422, 401, 403, cross-user access. See skill `write-tests`.
8. Run `make check`. Tick the spec task. If the contract changed, follow skill `api-contract-sync`.

## Pitfalls

- SQL or business rules inside the route function.
- Returning ORM objects instead of schemas.
- Blocking calls inside `async def`.
- Streaming endpoints that buffer the whole response (SSE must stream).
- Forgetting pagination (`page`, `page_size`) on list endpoints.
