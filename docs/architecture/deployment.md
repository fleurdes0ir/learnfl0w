# Deployment (GCP Serverless, Dilakukan di Akhir)

> **Status:** Draft | **Pemilik:** Anaya | **Diperbarui:** 2026-11-03
> Rujukan: [PRD 5, 14.6, dan 20](../product/PRD.md), [ADR-0002](../adr/0002-serverless-cloud-run.md), [ADR-0010](../adr/0010-langflow-dan-fastapi-untuk-lapisan-ai.md).
> Perintah `gcloud` adalah acuan; verifikasi flag terhadap dokumentasi terbaru sebelum dijalankan.

## 1. Prinsip: Deployment di Akhir

Pengembangan dan staging berjalan **di lokal** (Docker Compose). Resource GCP dibuat dan dideploy **sekali** pada jendela **28 Nov sampai 3 Des 2026** dari cabang `main`. Sebelum jendela itu, **jangan** membuat resource GCP atau menjalankan `deploy.yml`.

| Tanggal | Kegiatan |
|---|---|
| 28 sampai 29 Nov | Persiapan resource: project, API, Artifact Registry, Cloud SQL (database `app` dan `langflow`), service account, Workload Identity, secret |
| 30 Nov | Deploy pertama (urutan di bagian 8), membuat API key Langflow, smoke test |
| 30 Nov sampai 1 Des | Validasi Langflow di Cloud Run dan Tailscale ke 9router; putuskan jalur LLM utama |
| 1 Des | `min-instances = 1` untuk frontend, backend, Langflow; alert dan uptime check aktif |
| 1 sampai 3 Des | Pilot di cloud (minimal 5 mahasiswa), perbaikan |
| 4 Des | Code freeze (Gate G3) |

**Rencana B** bila Tailscale atau Langflow di Cloud Run bermasalah: `LLM_PROVIDER=vertex` (tanpa Tailscale), demo cadangan dari staging lokal, dan rekaman layar.

## 2. Pra-Deploy (Selesai Sebelum 28 Nov)

- [ ] Staging lokal hijau: `make staging-up` dan `make smoke`
- [ ] Evaluasi AI memenuhi target; `make flows-check` hijau
- [ ] Rilis `dev` -> `main` digabung; tag `v*` dibuat
- [ ] Perkiraan sumber daya Langflow dari `docker stats` (memori, CPU)
- [ ] Daftar variabel dan secret pada dokumen ini lengkap
- [ ] Akun GCP, billing, dan kredit aktif; budget alert direncanakan
- [ ] Pemilik homelab siap menguji Tailscale dari Cloud Run

## 3. Sumber Daya

| Sumber daya | Nama (usulan) | Catatan |
|---|---|---|
| Project GCP | `learnfl0w-cloud` | Billing budget 50/80/100% |
| Region | `asia-southeast2` (Jakarta) | Cadangan: `asia-southeast1` |
| Artifact Registry | `learnfl0w` (Docker) | Image `backend`, `frontend`, `langflow`, `job` |
| Cloud SQL | `learnfl0w-db` (PostgreSQL 16) | Satu instance; database `learnfl0w` (app) dan `langflow`; ekstensi `vector` pada database app |
| Cloud Run | `learnfl0w-backend`, `learnfl0w-frontend`, `learnfl0w-langflow` (privat) | Lihat bagian 6 |
| Cloud Run job | `learnfl0w-jobs` | Link checker, reindex |
| Cloud Scheduler | `link-check-weekly` | Memicu job |
| Service account | `sa-backend`, `sa-frontend`, `sa-langflow`, `sa-jobs`, `sa-deployer` | Hak akses minimum |

## 4. Persiapan Awal (28 sampai 29 Nov)

```bash
export PROJECT_ID=learnfl0w-cloud REGION=asia-southeast2

gcloud config set project $PROJECT_ID
gcloud services enable run.googleapis.com artifactregistry.googleapis.com \
  sqladmin.googleapis.com secretmanager.googleapis.com aiplatform.googleapis.com \
  cloudscheduler.googleapis.com iamcredentials.googleapis.com

gcloud artifacts repositories create learnfl0w \
  --repository-format=docker --location=$REGION

gcloud sql instances create learnfl0w-db \
  --database-version=POSTGRES_16 --edition=ENTERPRISE \
  --tier=db-f1-micro --region=$REGION
gcloud sql databases create learnfl0w --instance=learnfl0w-db
gcloud sql databases create langflow --instance=learnfl0w-db
# Pada database learnfl0w:  CREATE EXTENSION IF NOT EXISTS vector;
```

### Workload Identity Federation untuk GitHub Actions

```bash
gcloud iam workload-identity-pools create github --location=global
gcloud iam workload-identity-pools providers create-oidc github-provider \
  --location=global --workload-identity-pool=github \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository=='OWNER/REPO'"

gcloud iam service-accounts add-iam-policy-binding \
  sa-deployer@$PROJECT_ID.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github/attribute.repository/OWNER/REPO"
```

Peran minimum:
- `sa-deployer`: `roles/run.admin`, `roles/artifactregistry.writer`, `roles/iam.serviceAccountUser` (pada service account runtime).
- `sa-backend`: `roles/cloudsql.client`, `roles/secretmanager.secretAccessor`, `roles/aiplatform.user` (embedding), dan `roles/run.invoker` pada layanan Langflow.
- `sa-langflow`: `roles/cloudsql.client`, `roles/secretmanager.secretAccessor`, `roles/aiplatform.user` (varian `vertex`).

## 5. Variabel GitHub dan Rahasia

**Repository variables:** `GCP_PROJECT_ID`, `GCP_REGION`, `AR_REPOSITORY`, `WIF_PROVIDER`, `WIF_SERVICE_ACCOUNT`, `CLOUDSQL_INSTANCE`, `BACKEND_URL`, `FRONTEND_URL`, `MIN_INSTANCES` (`0`, lalu `1` mulai 1 Des), `LLM_PROVIDER` (`router` atau `vertex`).

**Secret Manager:**

| Secret | Dipakai oleh | Catatan |
|---|---|---|
| `database-url` | backend, job | `postgresql+psycopg://USER:PASS@/learnfl0w?host=/cloudsql/INSTANCE` |
| `jwt-secret` | backend | Acak, minimal 32 byte |
| `admin-emails` | backend | Email Admin, dipisah koma |
| `langflow-api-key` | backend | Dibuat di Langflow setelah deploy pertama |
| `internal-tool-token` | backend, Langflow | Token tool internal (`X-Internal-Token`) |
| `langflow-database-url` | Langflow | `postgresql://USER:PASS@/langflow?host=/cloudsql/INSTANCE` |
| `langflow-secret-key` | Langflow | Tetap; kunci enkripsi variabel Langflow |
| `langflow-superuser`, `langflow-superuser-password` | Langflow | Akun admin Langflow |
| `router-api-key` | Langflow | API key 9router |
| `tailscale-auth-key` | Langflow (sidecar) | Ephemeral, bertag; rotasi berkala |

## 6. Konfigurasi Cloud Run

| Parameter | Backend | Frontend | Langflow |
|---|---|---|---|
| Akses | Publik | Publik | **Privat** (hanya `sa-backend`) |
| min-instances | 0, lalu **1** (1 sampai 8 Des) | 0, lalu **1** | 0, lalu **1** (wajib) |
| max-instances | 3 | 3 | 2 |
| CPU | Always allocated | Request-based | Always allocated |
| Memori | 1 GiB | 512 MiB | 2 GiB atau lebih (hasil `docker stats`) |
| Concurrency | 20 | 80 | 10 |
| Timeout | 300 s | 60 s | 300 s |
| Port | 8080 | 8080 | 7860 |
| Cloud SQL | `--add-cloudsql-instances` | tidak ada | `run.googleapis.com/cloudsql-instances` |
| Health | `/healthz` | `/api/health` | `/health_check` |

Langflow didefinisikan lewat [`infra/cloud-run/langflow.service.yaml`](../../infra/cloud-run/langflow.service.yaml) (template). Variabel penting backend: `APP_ENV=cloud`, `CORS_ORIGINS`, `LANGFLOW_BASE_URL`, `LANGFLOW_USE_ID_TOKEN=true`, `LLM_PROVIDER`, `LLM_FALLBACK_PROVIDER=vertex`, `VERTEX_PROJECT`, `VERTEX_LOCATION`, `EMBEDDING_PROVIDER=vertex`. Daftar lengkap: [`.env.example`](../../.env.example).

## 7. Alur CI/CD

- **CI** (`ci.yml`, `branch-policy.yml`): setiap PR ke `dev` dan `main`; juga push ke keduanya. Berjalan sejak awal.
- **CD** (`deploy.yml`): hanya dari `main`, dipicu manual (`workflow_dispatch`) atau tag `v*`, pada jendela deployment. Urutan: autentikasi WIF -> build dan push image (backend, Langflow, frontend) -> deploy Langflow -> deploy backend -> smoke test (rollback otomatis bila gagal) -> deploy frontend.

## 8. Deploy Pertama (Urutan Khusus)

Ada ketergantungan melingkar (backend butuh API key Langflow; frontend butuh URL backend). Lakukan sekali:

1. Deploy Langflow (workflow atau `gcloud run services replace`); beri `roles/run.invoker` pada `sa-backend`.
2. Buka UI Langflow lewat proxy: `gcloud run services proxy learnfl0w-langflow --region $REGION`, login superuser, buat **API key**, simpan ke secret `langflow-api-key`. Pastikan flow termuat (8 flow: 4 x 2 varian). Bila tidak, jalankan `langflow/scripts/import_flows.py` terhadap alamat proxy.
3. Deploy backend; catat URL; isi variabel `BACKEND_URL`.
4. Deploy frontend; catat URL; isi `FRONTEND_URL`; deploy ulang backend agar CORS memuat URL frontend.
5. `bash scripts/smoke.sh` dengan `BACKEND_URL` dan `FRONTEND_URL` cloud (`SKIP_LANGFLOW=1`), lalu satu sesi konsultasi lewat UI.

## 9. Konektivitas ke 9router (Tailscale Sidecar pada Langflow)

- Sidecar Tailscale berjalan pada layanan **Langflow** (bukan backend) karena panggilan model berasal dari flow varian `router`.
- Butuh CPU always allocated dan auth key ephemeral bertag dari Secret Manager.
- **Status: divalidasi pada jendela deployment (30 Nov sampai 1 Des).** Template sidecar ada (dikomentari) pada `langflow.service.yaml`; konfigurasi pendukung di `infra/tailscale/`.
- Bila tidak stabil: `LLM_PROVIDER=vertex` menjadi jalur utama ([ADR-0005](../adr/0005-llm-gateway-9router-dengan-fallback-vertex.md)).

## 10. Pemantauan dan Biaya

- Uptime check pada frontend dan backend; alert ke webhook tim.
- Billing budget 50/80/100% dan `max-instances` sebagai pagar biaya; estimasi dihitung pada M4.
- Backup: Cloud SQL automated backup harian + ekspor manual ke Cloud Storage sebelum hari demo.
- Prosedur operasional: [runbook](../operations/runbook.md).
