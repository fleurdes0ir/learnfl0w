---
name: context-efficiency
description: Keep sessions cheap and focused (search before read, targeted tests, one task per session, compaction, handoff notes). Use at the start of any non-trivial task or when a session grows long.
---

# Context efficiency

## Reading

- Locate with grep or glob first; read line ranges, not whole files.
- Do not open: lockfiles, generated files (`frontend/src/lib/api/schema.d.ts`), `data/seed/*.csv`, build output, or large logs. Use `head`, `wc -l`, or a targeted query.
- Do not re-read a file already in context unless it changed.
- Load only the docs the spec links to. Load only the skills you need.

## Running commands

- Filter output: `| tail -n 30`, `pytest -q -x`, `ruff check --output-format concise`.
- While iterating run the narrowest test (`pytest tests/test_x.py::test_y -q`); run `make check` once at the end.

## Working

- Plan first (Plan agent), then build. One task from one spec per session.
- For wide exploration (many files), delegate to a subagent and ask for a summary only.
- Keep replies short: report the diff summary and check results. Do not paste code back.

## Long sessions

1. Finish or park the current sub-task.
2. Write the handoff note (below).
3. Run `/compact` (alias `/summarize`) at that natural breakpoint, or start a fresh session and read the handoff.

## Handoff note

File: `.opencode/handoff.md` (git-ignored). Max 30 lines: **Goal**, **Done**, **Decisions**, **Files touched**, **Next steps**, **Open questions**. Read it at the start of a session if it exists. Update it at the end.
