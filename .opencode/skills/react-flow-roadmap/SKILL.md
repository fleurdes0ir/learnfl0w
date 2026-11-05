---
name: react-flow-roadmap
description: Render and lay out the career roadmap with React Flow (@xyflow/react) from roadmap JSON, with node types, status styles, and accessibility. Use for SPEC-007 work.
---

# Roadmap viewer (React Flow)

Input: `docs/api/roadmap.schema.json` (generated TS types from OpenAPI).

## Design

- A **pure layout function** `layoutRoadmap(roadmap) -> { nodes, edges }` in `src/features/roadmap/layout.ts`. No positions are stored or hardcoded; unit-test it.
- Stages run left to right by `order`. Nodes inside a stage are stacked vertically, grouped by type (course, material, certification).
- Custom node types registered once (`course`, `material`, `certification`, `stage`); memoize them.
- Status styling for courses: `completed`, `in_progress`, `not_taken`, `not_applicable` (never color alone; add an icon or label).
- Defaults: `fitView`, zoom and pan on, `nodesDraggable={false}`, `nodesConnectable={false}`.
- A detail panel shows reason, provider, cost, level, and the link.

## Behavior

- External links open in a new tab with `rel="noopener noreferrer"` and send a `reference_click` event.
- Mark node complete calls `putRoadmapProgress`.
- `source = template` shows a "versi dasar" notice.
- Keyboard: nodes focusable, Enter opens detail, Escape closes.
- Performance target: 60 nodes render in <= 2 s on a mid-range device.

## Tests

Layout (order, no overlaps, orphan handling), each node type renders, empty/error states, keyboard open and close.
