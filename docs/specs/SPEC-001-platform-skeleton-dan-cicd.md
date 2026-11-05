# SPEC-001: Kerangka Platform Lokal, CI, dan Staging Lokal

> **Status:** Siap
> **Pemilik:** Anaya | **Milestone:** M0 sampai M1 | **Prioritas:** Must
> **PRD:** NFR-O-02, NFR-O-03, NFR-O-09 | **ADR terkait:** ADR-0001, ADR-0011, ADR-0012

## 1. Konteks

Fondasi teknis yang berjalan **sepenuhnya di lokal**: Docker Compose (db, Langflow, backend, frontend), CI pada setiap PR, proteksi cabang `main` dan `dev`, dan **staging lokal** yang meniru cloud. Deployment cloud **tidak** termasuk di sini (lihat SPEC-010, jendela 28 Nov sampai 3 Des).

## 2. Lingkup

**Dalam lingkup:** repositori dan cabang (`main`, `dev`), Docker Compose lokal, Dockerfile backend/frontend/Langflow, `/healthz`, CI (lint, typecheck, test, validasi flow, build image), `branch-policy`, profil `staging`, `make smoke`.

**Di luar lingkup:** resource GCP, CD, Tailscale di cloud (SPEC-010); fitur bisnis.

## 3. Persyaratan

| ID | Persyaratan |
|---|---|
| R-1 | `make up` menjalankan db, Langflow, backend, frontend secara lokal |
| R-2 | Backend `GET /healthz` melaporkan aplikasi dan database; frontend `GET /api/health`; Langflow `/health_check` |
| R-3 | CI menjalankan lint, typecheck, test, `flows-check`, dan build image untuk PR ke `dev` dan `main` |
| R-4 | `branch-policy` menolak cabang selain `feat/`, `fix/`, `chore/` ke `dev`, dan selain `dev` atau `fix/` ke `main` |
| R-5 | `main` dan `dev` terproteksi (PR, 1 persetujuan, status check, metode merge sesuai `git-workflow.md`) |
| R-6 | `make staging-up` menjalankan profil `staging` (image dan variabel meniru cloud, batas memori); `make smoke` memeriksa semua layanan |
| R-7 | Rahasia hanya di `.env` lokal (tidak di-commit); `.env.example` lengkap |

## 4. Kontrak

- Endpoint: `getHealth`, `getLlmHealth` (OpenAPI).
- Cabang dan rilis: [git-workflow.md](../engineering/git-workflow.md).

## 5. Acceptance Criteria

- [ ] AC-1: Given repo baru, When `cp .env.example .env && make up`, Then db, Langflow, backend, frontend sehat dan `/healthz` bernilai `ok`.
- [ ] AC-2: Given PR dari `feat/x` ke `dev`, When CI berjalan, Then lint, test, dan build lolos untuk layanan yang berubah.
- [ ] AC-3: Given PR dari `docs/x` ke `dev`, When `branch-policy` berjalan, Then PR ditolak.
- [ ] AC-4: Given cabang `dev`, When `make staging-up && make smoke`, Then seluruh layanan sehat.

## 6. Tugas

- [ ] T-1 [Anaya] Repo, cabang `main` dan `dev`, proteksi cabang
- [ ] T-2 [Anaya] `docker-compose.yml`, `docker-compose.staging.yml`, Dockerfile, `Makefile`, `scripts/smoke.sh`
- [ ] T-3 [Anaya] `ci.yml` dan `branch-policy.yml`
- [ ] T-4 [Bastian] Inisialisasi Next.js, halaman awal, `/api/health`, Dockerfile frontend
- [ ] T-5 [Anaya] Dokumentasi `.env.example` dan README

## 7. Strategi Uji

Jalankan `make up` pada mesin bersih; buka PR uji dengan nama cabang salah; jalankan `make staging-up` dan `make smoke`.

## 8. Catatan dan Risiko

Deployment baru di akhir (R-24); staging lokal yang meniru cloud adalah mitigasi utamanya.
