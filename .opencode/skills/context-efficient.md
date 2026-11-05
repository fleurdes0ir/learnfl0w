# context-efficient: Preserve Context Budget

Project has 200K token budget. Use efficiently.

## Search before reading

```bash
# Find files
find . -name "*client*" -type f

# Grep for patterns
grep -r "class.*Client" backend/app/

# Read specific lines
sed -n '50,80p' app/services/auth.py
```

## Read line ranges

Use `read` with `offset` and `limit`. Never open:
- Lockfiles (package-lock.json, poetry.lock)
- Generated files (openapi.yaml if large)
- Seed CSVs (thousands of lines)

## Filter command output

```bash
# Not this
pytest

# This
pytest -q | tail -20

# Or
pytest backend/tests/api/test_auth.py::test_register
```

## Narrow tests while iterating

Run single test file or function during dev. `make check` once at end.

## Tool result handling

- Success + expected → note result, move on
- Error → show relevant excerpt only
- Large output → grep/tail/head

## One task per session

At natural breakpoint write `.opencode/handoff.md` and start fresh or compact.

## Report diffs

Summarize changes. Don't paste code back unless asked.

```
Changed:
- auth.py: add type hints to verify_token
- dependencies.py: fix Callable return type
```

Not:
```python
def verify_token(token: str...) -> dict[str, object]:
    [entire function]
```
