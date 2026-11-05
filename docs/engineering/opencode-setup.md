# OpenCode Setup, Skills, and Token Efficiency

> **Status:** Active | **Owner:** LearnFl0w | **Updated:** 2026-10-31

How this repository is prepared for AI-assisted development with [OpenCode](https://opencode.ai).

## 1. What Lives Where

| Path | Purpose | Loaded |
|---|---|---|
| `AGENTS.md` | Short, always-on rules (stack, commands, hard rules, workflow) | Every session |
| `backend/AGENTS.md`, `frontend/AGENTS.md` | Area rules | On demand (root `AGENTS.md` points to them) |
| `opencode.json` | OpenCode config (compaction) | Every session |
| `.opencode/agents/` | Subagents: `reviewer` (read-only), `tester` | When invoked |
| `.opencode/commands/` | Slash commands: `/new-spec`, `/new-adr`, `/implement`, `/check` | When invoked |
| `.opencode/skills/<name>/SKILL.md` | Reusable procedures | Description always advertised; body loaded on demand |
| `.opencode/handoff.md` | Session handoff note (git-ignored) | When you create it |

Principle: keep `AGENTS.md` short; put procedures in skills; put facts in `docs/` and let the agent read only what a spec links to.

## 2. Skills Catalog

Skill names match their folder names. Descriptions are written to say *when* to use the skill.

| Group | Skill | Use for | Main owner |
|---|---|---|---|
| Project | `fastapi-endpoint` | Add or change an endpoint | Anaya |
| Project | `alembic-migration` | Schema changes and migrations | Anaya |
| Project | `langflow-flow` | Langflow flows, variants, FastAPI client contract | Anaya |
| Project | `roadmap-validation` | Roadmap rules and persona evaluation | Anaya |
| Project | `catalog-curation` | Seed data changes (never invent URLs) | Both |
| Project | `nextjs-feature` | Frontend features | Bastian |
| Project | `react-flow-roadmap` | Roadmap viewer | Bastian |
| Project | `cloud-run-deploy` | Deploy, rollback, ops | Anaya |
| Project | `security-review` | Security checklist before merge | Both |
| Token | `lean-coding` | Smallest correct change (YAGNI ladder) | Both |
| Token | `context-efficiency` | Cheap sessions, handoff, compaction | Both |
| Codebase | `api-contract-sync` | Keep OpenAPI, backend, frontend types in sync | Both |
| Codebase | `write-tests` | pytest and Vitest patterns | Both |
| Codebase | `debug-fix` | Systematic bug fixing | Both |
| Codebase | `refactor-safe` | Behavior-preserving refactors | Both |
| Codebase | `ship-change` | Quality gate, docs sync, commit and PR | Both |

Adding a skill: create `.opencode/skills/<name>/SKILL.md` with frontmatter `name` and `description` only (name: lowercase letters, digits, single hyphens, matches the folder; description: specific, up to 1024 characters). Put long material in `references/` and scripts in `scripts/` inside the skill folder. Do not add a README inside `.opencode/skills/`.

Troubleshooting a skill that does not appear: check the frontmatter, that `name` equals the folder name, that the name is unique, and that agent permissions do not deny it.

Skill descriptions are always in context, so keep the set small. Add a skill only when a procedure repeats.

## 3. Token Efficiency Practices

1. **Short always-on context.** `AGENTS.md` stays under about 200 lines. Nothing else is force-loaded.
2. **Search before reading.** Use grep or line ranges. Skip lockfiles, generated files (`schema.d.ts`), seed CSVs, build output.
3. **Filter command output** (`tail`, `-q -x`, concise formats). Narrow tests while iterating, `make check` once at the end.
4. **One task per session**, starting from a spec. Use the Plan agent first, then Build.
5. **Compact at breakpoints.** Run `/compact` (alias `/summarize`) after finishing a sub-task, or start a fresh session and read `.opencode/handoff.md`.
6. **Compaction config** in `opencode.json` is enabled. Tune per the current OpenCode docs for your version; fields differ between versions.
7. **Lean code is cheaper code.** Use `lean-coding` before writing anything; smaller diffs cost fewer tokens to write, review, and fix.
8. **Cheaper model for light work.** OpenCode supports a `small_model` setting for low-complexity operations. Set it in your own (global) config using a model id from your provider; it is not committed here because ids are provider-specific.

## 4. Optional: Third-Party Token Tools

Not installed by default. If you want to try one, treat it as third-party code that runs on your machine.

- **ponytail** (YAGNI-style plugin and skills that push the agent toward less code; an OpenCode plugin entry exists per its README). Its own benchmark reports large reductions in lines of code and smaller reductions in tokens; independent hands-on reports show smaller savings on from-scratch work and more on edits to existing code. It may also ask extra clarifying questions.
- Context or command-output compressors exist as well; evaluate them the same way.

Before enabling any of them:
1. Confirm the official repository and owner (there are many forks).
2. Read the plugin source: plugins execute code inside OpenCode and inject text into every turn.
3. Pin an exact version or commit that is at least two weeks old.
4. Try it on a throwaway branch and compare diff size, tokens, and quality with `lean-coding` alone.
5. Add it to `opencode.json` only if it clearly helps; record the decision in an ADR.

`lean-coding` in this repo gives the same intent (smallest correct change) without third-party code.

## 5. Daily Workflow

1. `git pull`; open OpenCode in the repo (or in `backend/` or `frontend/`).
2. Pick a spec task. If `.opencode/handoff.md` exists, read it.
3. `/implement <task>` (Plan first, review the plan, then Build).
4. `make check`. Use `@reviewer` for a second look on risky changes (skill `security-review`).
5. `ship-change`: docs, changelog, Conventional Commit, PR.
6. Update `.opencode/handoff.md` if you stop mid-task.
