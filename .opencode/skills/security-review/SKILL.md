---
name: security-review
description: Security checklist for reviewing a change (auth, RBAC, input validation, prompt injection, secrets, logging, rate limits, LLM output trust). Use before merging risky changes and at the G3 gate.
---

# Security review

Review the diff against this checklist and report **Blocking / Should fix / Nit** with file and line.

## Access control
- Every endpoint enforces role in the backend; user data checks ownership (no IDOR).
- Admin endpoints require `admin`. Analytics and exports contain no individual data; segments under 5 users are hidden.

## Authentication
- Argon2id hashing; JWT short-lived; refresh tokens hashed, rotated, reuse revokes all sessions.
- Login and register are rate limited. Error messages do not reveal whether an email exists.

## Input and output
- All input validated with Pydantic at the boundary. SQL only through the ORM or bound parameters.
- Responses never include `password_hash`, tokens, or internal ids that should be private.
- CORS limited to the frontend origin.

## AI-specific
- User text and transcript data are treated as data, never as instructions.
- LLM output is validated; every `ref_id` and URL checked against the catalog.
- Tools are read-only. No tool can change data or reach arbitrary URLs.
- Langflow is private (Cloud Run IAM + API key); `/internal/tools/*` requires `X-Internal-Token`; no secrets in flow JSON; `LANGFLOW_AUTO_LOGIN=false`.

## Secrets and logging
- No secrets in code, images, logs, or `.env.example`.
- Logs contain no message content, passwords, tokens, or personal data.

## Dependencies
- New dependency has a stated reason; versions pinned by lockfile; no known critical vulnerability.

Finish with a short verdict: safe to merge or not, and why.
