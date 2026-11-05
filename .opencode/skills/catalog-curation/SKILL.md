---
name: catalog-curation
description: Add or update certifications, learning materials, courses, or career-path templates in data/seed. Use for any catalog data change. Never invent URLs.
---

# Catalog curation

Files: `data/seed/*.csv|json` (see `data/seed/README.md`). The catalog is the only source of recommendations.

## Hard rules

- **Never write a URL from memory or from model output.** A human must open every link, confirm it works and matches, then supply it. If asked to "find" certifications or materials, you may propose candidate names for a human to verify; leave `url` empty and mark `status = needs_review`.
- Never delete rows. Set `status = inactive`.

## Steps

1. Add rows using the existing header. Codes are unique and sequential: `CERT-001`, `MAT-001`.
2. Enums: `cost_type` in `free|paid|freemium`; `level` in `beginner|intermediate|advanced`; `status` in `active|needs_review|inactive`; material `format` in `video|article|course|book|lab`.
3. Multi-value fields use `|` (`CP-05|CP-01`). Career path codes must exist in `career_paths.json`.
4. `last_verified_at` is the date a human verified the link (`YYYY-MM-DD`).
5. Description 50 to 150 words (it is embedded for retrieval).
6. Run `make seed` twice and confirm it is idempotent. Then reindex embeddings.

## Targets

At least 3 certifications and 5 materials per career path. Report coverage per path when finishing.
