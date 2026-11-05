---
name: ship-change
description: Finish and hand over a change (quality gate, docs sync, Conventional Commit, PR description, changelog). Use when work is done and ready to commit or open a PR.
---

# Ship a change

## Before committing

1. `make check` is green (report the real result).
2. Acceptance criteria met; tick tasks in `docs/specs/SPEC-*.md`; update the status column in `docs/specs/README.md` if a spec is finished.
3. Docs synced: `docs/api/openapi.yaml` (skill `api-contract-sync`), `data-model.md`, `ai-design.md`, ADR for new decisions (`/new-adr`).
4. `CHANGELOG.md` under `[Unreleased]` for user-visible changes.
5. No secrets, no personal data, no hardcoded catalog names or URLs, no leftover debug code.

## Commit

Conventional Commits: `type(scope): imperative description` (<= 72 chars). Types: `feat fix docs test refactor chore ci perf`. Scopes: `auth profile chat roadmap catalog admin ai flows ui infra ci docs`. One logical change per commit. **Do not commit or push unless the user asked.**

## Pull request

Use `.github/PULL_REQUEST_TEMPLATE.md`. Fill: summary, spec or issue, how to test, risk and rollback, new dependencies with reasons. Branch from `dev` as `feat/`, `fix/`, or `chore/` (for example `feat/spec-005-dialog-manager`); PR **into `dev`**, squash merge, PR title follows Conventional Commits. Release PR is `dev` -> `main` (merge commit) after a gate. CI rejects wrong branch names or targets.

## After code freeze (2026-12-04)

Only critical fixes: `fix/` branch from `main`, PR into `main`, then back-merge into `dev`. Describe the risk and the rollback plan in the PR.
