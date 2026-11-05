---
name: langflow-flow
description: Create or change a Langflow flow (slot-extractor, consultant-reply, path-advisor, roadmap-builder), its router/vertex variants, the JSON export, and the FastAPI client contract. Use for any AI flow, prompt, or Langflow integration change.
---

# Langflow flow work

Read: `docs/api/langflow-flows.md` (contract), `langflow/README.md`, and the flow section of `docs/architecture/ai-design.md`. Search exported JSON; do not read it in full.

## Steps

1. Spec first (`SPEC-005`, `SPEC-006`, `SPEC-011`). If the contract changes, update `docs/api/langflow-flows.md` and the Pydantic models in `backend/app/ai/schemas/` first.
2. Author the flow in local Langflow (`make up`, UI on port 7860). Keys and URLs only through global variables.
3. Keep both variants identical except the model component. Name them `<flow>__router` and `<flow>__vertex`.
4. Export the JSON to `langflow/flows/` and set `status: exported` in `langflow/flows.manifest.json`.
5. Run `make flows-check`, then the persona evaluation (`pytest backend/tests/ai`).
6. Backend side: only `app/ai/langflow/client.py` calls Langflow. Add a typed wrapper that validates the output with Pydantic; unit-test with `httpx.MockTransport`.

## Rules

- Flows are stateless: all context arrives in `input_value` JSON.
- No catalog names or URLs in prompts. Catalog data comes from the input or from internal tools.
- Non-stream flows return JSON only. The stream flow returns plain Indonesian text without URLs.
- Never put secrets in flow JSON (CI scans for them).
- Do not hand-edit exported JSON except to resolve a merge conflict; then re-import and re-export.
- Langflow version is pinned. Upgrades go through a PR plus evaluation.

## Done

Both variants exported, manifest updated, `make flows-check` and AI tests green, contract doc and spec updated.
