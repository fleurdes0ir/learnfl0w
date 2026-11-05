---
description: Implement one task from a spec
---

Implement this task: $ARGUMENTS

Rules:
1. Find the task in its `docs/specs/SPEC-*.md`. If no spec covers it, stop and tell me.
2. Read only the docs the spec links to. State a short plan first.
3. Implement the task with tests, keeping the diff small.
4. Update `docs/api/openapi.yaml` and docs if contracts or behavior change.
5. Run `make check`, report the real result, and tick the task in the spec.
