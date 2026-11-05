---
name: debug-fix
description: Diagnose and fix a bug systematically (reproduce, hypothesize, minimal fix, regression test). Use for failing tests, errors, or unexpected behavior.
---

# Debug and fix

1. **Reproduce.** Get the exact error, input, and environment. Write the smallest failing test or command. If it cannot be reproduced, say so and ask for details.
2. **Read the evidence.** Read the stack trace bottom-up and only the relevant log lines (filter, do not dump).
3. **Hypothesize.** List at most 3 likely causes, most likely first. Prefer causes that explain all symptoms.
4. **Test one hypothesis at a time** with minimal instrumentation (an assertion, a targeted log without personal data). Remove instrumentation afterwards.
5. **Fix the root cause**, not the symptom. Keep the diff minimal (skill `lean-coding`).
6. **Regression test** that fails before and passes after the fix.
7. **Verify:** narrow test, then `make check`. Report what was wrong, why, and what changed.

## Rules

- Do not change unrelated code while debugging.
- Do not silence errors (`except: pass`, skipping tests, loosening assertions).
- If the cause is a design problem, stop and propose it (and an ADR if needed) instead of patching around it.
