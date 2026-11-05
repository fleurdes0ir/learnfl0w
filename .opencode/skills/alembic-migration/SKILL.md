---
name: alembic-migration
description: Create and review Alembic migrations (PostgreSQL, pgvector, reversible, no edits to applied migrations). Use whenever a model or schema changes.
---

# Alembic migration

## Steps

1. Change models in `backend/app/models/` and import them in `app/models/__init__.py`.
2. Generate: `cd backend && alembic revision --autogenerate -m "short message"`.
3. **Review the generated file by hand.** Autogenerate misses or mangles: vector columns, CHECK constraints, GIN indexes, server defaults, enum-like text columns.
4. Conventions (see `docs/architecture/data-model.md`): uuid PKs, `created_at`/`updated_at` as `timestamptz`, enum-like values as `text` + `CHECK`, soft delete via `status`, `snake_case` plural table names, explicit constraint and index names.
5. Vector columns use `pgvector.sqlalchemy.Vector(dim)`; also store `embedding_model` next to `embedding`.
6. Make `downgrade()` real whenever practical.
7. Test on a fresh database: `alembic upgrade head`, then `downgrade -1`, then `upgrade head` again.
8. Update `docs/architecture/data-model.md` if the model changed.

## Rules

- Never edit a migration that has been applied or merged. Add a new one.
- Keep data migrations separate from schema migrations. Seed data is not a migration (`make seed`).
- Destructive changes (drop column/table) need a note in the PR and, if non-trivial, an ADR.
