# Architecture Decision Records

Catatan keputusan arsitektur dalam format MADR ringkas. Gunakan `/new-adr` di OpenCode atau salin [`0000-template.md`](0000-template.md).

| ADR | Judul | Status |
|---|---|---|
| [0001](0001-monorepo.md) | Satu monorepo | Diterima |
| [0002](0002-serverless-cloud-run.md) | Arsitektur serverless di Cloud Run | Diterima |
| [0003](0003-cloud-sql-pgvector.md) | PostgreSQL + pgvector pada Cloud SQL | Diterima |
| [0004](0004-agent-langgraph-slot-filling.md) | Agent LangGraph dengan slot-filling | Digantikan oleh ADR-0010 |
| [0005](0005-llm-gateway-9router-dengan-fallback-vertex.md) | LLM via 9router dengan fallback Vertex AI | Diterima |
| [0006](0006-autentikasi-internal-email-password-jwt.md) | Autentikasi internal (email, password, JWT) | Diterima |
| [0007](0007-embedding-vertex-ai.md) | Embedding melalui Vertex AI | Diusulkan |
| [0008](0008-roadmap-structured-output-dan-templat-fallback.md) | Roadmap structured output + templat cadangan | Diterima |
| [0009](0009-transkrip-input-manual-dan-csv.md) | Transkrip via input manual dan CSV | Diterima |
| [0010](0010-langflow-dan-fastapi-untuk-lapisan-ai.md) | Langflow + FastAPI untuk lapisan AI | Diterima |
| [0011](0011-branching-main-dev-dan-staging-lokal.md) | Branching `main`/`dev` dan staging lokal | Diterima |
| [0012](0012-deployment-di-akhir.md) | Deployment cloud di akhir | Diterima |

**Aturan:** ADR yang sudah diterima tidak diedit isinya; keputusan baru yang menggantikan dibuat sebagai ADR baru dan status lama diubah menjadi `Digantikan oleh ADR-XXXX`.
