---
name: lean-coding
description: Write the smallest correct change. Use BEFORE writing code for any feature or fix, and when asked to simplify, trim, or avoid over-engineering. Cuts code, review effort, and tokens.
---

# Lean coding

Goal: the smallest change that fully meets the acceptance criteria. Walk this ladder and stop at the first rung that works.

1. **Needed?** If the spec or acceptance criteria do not require it, do not build it. Note it as a follow-up instead.
2. **Already in the repo?** Search for an existing function, component, or pattern (grep first). Reuse or extend it.
3. **Standard library or framework built-in?** Use it.
4. **Already-installed dependency?** Use it.
5. **A few lines?** Write them inline.
6. Only then write new code, as small as possible. A **new dependency** needs a reason in the PR: size, maintenance, license, and why the rungs above failed.

## Rules

- No speculative abstractions: no helper used once, no wrapper around a single call, no config flag nobody asked for, no new layer.
- Do not rewrite working code. Prefer deleting code over adding code.
- Keep the diff inside the task. Unrelated cleanup goes into a separate change.
- If a requirement is ambiguous, ask **one** short question instead of building options.

## Never trimmed

Input validation, authorization, error handling, accessibility, tests, and security checks stay, even when the change is small.

## Report

When finished, state: what changed, what you deliberately did not build, and any follow-up worth an issue.
