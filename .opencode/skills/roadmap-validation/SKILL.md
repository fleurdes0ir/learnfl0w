---
name: roadmap-validation
description: Add or change roadmap validation rules and run the AI persona evaluation (schema, catalog ids, URLs, DAG, personalization). Use when touching roadmap generation or guardrails.
---

# Roadmap validation

Rules live in `backend/app/ai/guardrails/`. Order of checks:

1. **Schema:** `docs/api/roadmap.schema.json` + Pydantic model.
2. **Catalog ids:** every `ref_id` exists and `status = active`; drop invalid nodes.
3. **URLs:** only from the catalog; remove any URL the LLM produced.
4. **Graph:** DAG (no cycles), no orphan nodes, stages ordered foundation -> advanced.
5. **Personalization:** completed courses are `completed` and never new work; budget preference respected; at least 1 material per stage and 1 certification.
6. **Timing:** estimated weeks realistic for `hours_per_week` and `internship_target`.

## Adding a rule

1. Write a failing test with a bad-roadmap fixture (one violation per fixture).
2. Implement the rule; return structured errors (`code`, `node_id`, `message`) usable as retry feedback.
3. Keep the rule deterministic and free of LLM calls.

## Evaluation

- Personas: `backend/tests/ai/personas/*.json` (target 20).
- Run `pytest tests/ai -q` (fake LLM). `RUN_LIVE_LLM=1` uses a real LLM and costs money; ask first.
- Targets: schema validity >= 98%, grounding 100%, graph rules 100%.
- After 2 failed retries the system returns the template roadmap (`source = template`). Never skip this fallback.
