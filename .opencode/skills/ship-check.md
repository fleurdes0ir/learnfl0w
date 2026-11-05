# ship-check: Definition of Done

Before saying "done" or creating PR.

## Code checks

```bash
cd backend
ruff check .
ruff format --check .
mypy app
pytest -q
```

Or:
```bash
make check  # runs all: lint, typecheck, test
```

## Acceptance criteria

- [ ] All AC in spec checked off
- [ ] New behavior has tests
- [ ] No new lint/type errors
- [ ] No leftover TODO without issue reference

## Contract sync

If API changed:
- [ ] `docs/api/openapi.yaml` updated
- [ ] Related docs updated (langflow-flows.md, data-model.md)

## Commit

```bash
git add -A
git commit -m "feat(spec-011): add langflow client with circuit breaker

- LangflowClient with router/vertex fallback
- CircuitBreaker per variant (3 fail → open, 60s retry)
- /healthz/llm endpoint
- AC-1, AC-2 passing
"
```

Conventional Commits: `feat|fix|chore(scope): description`

## PR

```bash
gh pr create --base dev --head feat/spec-011-langflow \
  --title "feat(spec-011): langflow client and circuit breaker" \
  --body "$(cat <<EOF
Summary: LangflowClient with fallback and circuit breaker

Acceptance Criteria:
- [x] AC-1: Langflow health check works
- [x] AC-2: Circuit breaker switches variants on failure
- [ ] AC-3: flows-check validation (next PR)

Test: make check passes
EOF
)"
```

## Report

State what passed. Example:

```
✅ ruff check clean
✅ mypy: no issues  
✅ pytest: 45 passed
✅ AC-1, AC-2 verified

Ready for review.
```

Not: "I assume it works" or paste full output.
