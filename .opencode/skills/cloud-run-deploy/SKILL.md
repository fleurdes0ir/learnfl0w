---
name: cloud-run-deploy
description: Deploy, verify, roll back, and troubleshoot the GCP Cloud Run services (backend, frontend, Langflow, jobs), including secrets, min-instances, and the LLM variant switch. Use only for deployment or ops tasks inside the deployment window.
---

# Cloud Run deploy and ops

Read: `docs/architecture/deployment.md` and `docs/operations/runbook.md`. Do not run commands against GCP unless the user asked and confirmed the project and region.

## Timing

Deployment is at the **end** of the project: window **2026-11-28 to 2026-12-03**. Before the window, do not create GCP resources or run the deploy workflow. Rehearse with local staging instead: `make staging-up && make smoke` (branch `dev`).

## Normal path (preferred)

1. Gate G2 passed; release PR `dev` -> `main` merged; `make check` and CI are green.
2. Run `.github/workflows/deploy.yml` from `main` (manual `workflow_dispatch` or a `v*` tag). It builds backend, Langflow, and frontend images, deploys Langflow (private), then backend, smoke-tests `/healthz`, rolls back on failure, then deploys the frontend.
3. Verify: `/healthz`, `/healthz/llm` (Langflow and both variants), and one consultation through the UI.

## Manual operations

- **Rollback:** `gcloud run services update-traffic <service> --region $REGION --to-revisions=<REV>=100` (backend, frontend, or Langflow).
- **Switch LLM variant:** the backend chooses the variant: `gcloud run services update learnfl0w-backend --update-env-vars LLM_PROVIDER=vertex`, then check `/healthz/llm`.
- **Secrets:** via Secret Manager and `--set-secrets` (or `secretKeyRef` in `infra/cloud-run/langflow.service.yaml`). Never pass secret values as plain env vars or commit them.
- **Langflow stays private:** only `sa-backend` has `roles/run.invoker`. Never make it public.
- **Cost guard:** keep `max-instances` low; `min-instances = 1` only from 1 to 8 Dec 2026.

## Rules

- No manual change to cloud config without writing it back into `deploy.yml`, `infra/`, or `docs/`.
- After code freeze (2026-12-04) only critical fixes (`fix/` from `main`) with a rollback plan.
- Report exact command output; never claim success without checking health endpoints.
