---
name: refactor-safe
description: Refactor without changing behavior (tests first, small steps, one kind of change per commit). Use when restructuring, renaming, or splitting code.
---

# Safe refactoring

1. **State the goal** in one sentence and the behavior that must not change.
2. **Safety net first.** Run the relevant tests; they must be green. If coverage is missing, add characterization tests for current behavior before touching code. If that is too risky or large, stop and tell the user.
3. **Small steps.** One kind of change at a time (rename, extract, move, delete dead code). Run the tests after each step.
4. **Use tooling** for renames and moves (editor or `ruff`/TypeScript refactors), not blind find-and-replace.
5. **No behavior change.** Do not mix in features or bug fixes; note them separately.
6. **Layering stays intact:** `api -> services -> models`; `ai/` only called from services; LLM calls only through Langflow (`app/ai/langflow/`); embedding SDK only in `app/ai/embeddings/`.
7. **Finish:** `make check`, update docs/imports, and commit refactor separately from feature work.

Signs to stop: tests turn red and the cause is unclear, the diff keeps growing, or the change needs a contract or schema change (that is no longer a pure refactor).
