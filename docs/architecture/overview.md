# Gambaran Arsitektur

> **Status:** Draft | **Pemilik:** Anaya | **Diperbarui:** 2026-11-03
> Rujukan rinci: [PRD bagian 5](../product/PRD.md) dan [ADR](../adr/README.md).

## 1. Tujuan dan Batasan

Sistem membantu mahasiswa TI memetakan karir lewat konsultasi AI dan roadmap node-edge. Batasan utama:

- **Pengembangan dan staging di lokal** (Docker Compose); **deployment ke GCP serverless di akhir** (28 Nov sampai 3 Des 2026);
- harus **lancar saat demo 8 Des 2026** (PRD 14.6);
- lapisan AI memakai **Langflow** yang dipanggil oleh **FastAPI**; LLM utama lewat **9router** (Tailscale) dengan fallback **Vertex AI**;
- rekomendasi **berbasis katalog terkurasi** (himpunan kandidat tertutup).

## 2. Konteks Sistem

```mermaid
flowchart LR
    S[Mahasiswa] -->|konsultasi, roadmap| SYS[IT Career Compass]
    A[Admin] -->|kelola katalog, dashboard| SYS
    SYS -->|LLM utama| R[9router<br/>homelab via Tailscale]
    SYS -->|LLM fallback + embedding| V[Vertex AI]
    SYS -->|data| SQL[(PostgreSQL)]
```

## 3. Container

```mermaid
flowchart TB
    U[Browser] -->|HTML/JS| FE[frontend<br/>Next.js]
    U -->|REST + SSE| BE[backend<br/>FastAPI]
    BE --> DB[(PostgreSQL + pgvector<br/>db app)]
    BE -->|run flow| LF[langflow<br/>privat]
    LF -->|tools katalog| BE
    LF --> LDB[(db langflow)]
    LF -->|varian router| TS((Tailscale)) --> R[9router]
    LF -.->|varian vertex| V[Vertex AI]
    BE --> V
    JOB[job: link-check, reindex] --> DB
```

| Container | Tanggung jawab | Lokal | Cloud (di akhir) |
|---|---|---|---|
| `frontend` | UI, viewer roadmap, panel admin | Compose | Cloud Run (publik) |
| `backend` | API, auth, dialog manager, retrieval, guardrails, validator | Compose | Cloud Run (publik) |
| `langflow` | Flow LLM (4 flow x 2 varian) | Compose | Cloud Run **privat** (+ sidecar Tailscale) |
| `db` | PostgreSQL + pgvector (database `app` dan `langflow`) | Compose | Cloud SQL |
| `job` | Pemeriksa tautan, reindex | `make` / skrip | Cloud Run Job + Scheduler |

## 4. Modul Backend

| Modul | Lokasi | Tanggung jawab |
|---|---|---|
| API | `backend/app/api/v1/` | Routing, validasi input, dependensi auth |
| Services | `backend/app/services/` | Logika bisnis (profil, transkrip, roadmap, katalog, analitik) |
| Auth | `backend/app/auth/` | Hash password, JWT, refresh token, RBAC |
| AI | `backend/app/ai/` | `dialog/` (dialog manager), `langflow/` (klien + circuit breaker), `guardrails/`, `tools/`, `embeddings/`, `schemas/` |
| DB | `backend/app/db/`, `models/` | Sesi async, model SQLAlchemy |

Alur ketergantungan: `api` -> `services` -> `models`. Modul `ai` hanya dipanggil dari `services`.

## 5. Alur Runtime Utama

### 5.1 Satu Giliran Konsultasi

```mermaid
sequenceDiagram
    participant B as Browser
    participant API as Backend
    participant DM as Dialog manager
    participant LF as Langflow
    participant DB as PostgreSQL
    B->>API: POST /sessions/{id}/messages
    API->>DB: muat profil, slot, tahap, pesan terakhir
    API->>API: input guardrails
    API->>LF: slot-extractor (JSON)
    LF-->>API: slots_update, intent
    API->>DM: next_step(...)
    DM-->>API: tahap + aksi
    API->>LF: consultant-reply (stream)
    LF->>API: tool katalog (X-Internal-Token)
    LF-->>API: token
    API-->>B: SSE token (URL non-katalog dihapus)
    API->>DB: simpan pesan, slot, tahap, ai_runs
```

### 5.2 Pembuatan Roadmap

```mermaid
sequenceDiagram
    participant API as Backend
    participant DB as PostgreSQL
    participant LF as Langflow
    API->>DB: kandidat tertutup (matkul, sertifikasi, materi)
    API->>LF: roadmap-builder (JSON)
    LF-->>API: roadmap
    API->>API: validasi (skema, DAG, ref_id, personalisasi)
    alt valid
        API->>DB: simpan roadmap (ai)
    else gagal 2 kali
        API->>DB: simpan roadmap templat
    end
```

### 5.3 Fallback LLM

`LangflowClient` memanggil varian utama (`router`). Setelah 3 kegagalan beruntun, circuit breaker terbuka dan panggilan dialihkan ke varian `vertex` selama 60 detik sebelum dicoba lagi. Detail: [ai-design.md](ai-design.md) dan [ADR-0005](../adr/0005-llm-gateway-9router-dengan-fallback-vertex.md).

## 6. Prinsip Lintas-Modul

| Aspek | Keputusan |
|---|---|
| State | Stateless; sumber kebenaran percakapan di PostgreSQL (FastAPI); flow tanpa state |
| Konfigurasi | Variabel environment lewat `Settings`; rahasia di Secret Manager (cloud) |
| Keamanan | Argon2id, JWT berumur pendek, RBAC di backend, rate limit, log tanpa PII; Langflow privat |
| Observabilitas | Log terstruktur, tabel `ai_runs`, uptime check dan alert (cloud) |
| Kontrak | API publik `docs/api/openapi.yaml`; flow `docs/api/langflow-flows.md` |
| Keandalan | Kontrol REL-01 sampai REL-14 pada PRD 14.6 |

## 7. Lingkungan

| Lingkungan | Platform | Cabang | Catatan |
|---|---|---|---|
| Local | Docker Compose | `feat/`, `fix/`, `chore/` | `make up`; Langflow UI di port 7860 untuk menyusun flow |
| Staging lokal | Docker Compose + `docker-compose.staging.yml` | `dev` | `make staging-up`, `make smoke`; meniru cloud |
| Cloud (GCP) | Cloud Run, Cloud SQL, Vertex AI | `main` | **Dideploy di akhir** (28 Nov sampai 3 Des) |

Panduan deploy: [deployment.md](deployment.md). Alur cabang: [git-workflow.md](../engineering/git-workflow.md).
