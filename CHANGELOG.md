# Changelog

Semua perubahan penting pada proyek ini dicatat di sini.
Format mengikuti [Keep a Changelog](https://keepachangelog.com/id-ID/1.1.0/) dan proyek ini menggunakan [Semantic Versioning](https://semver.org/lang/id/).

## [Unreleased]

### Added
- Struktur repositori awal, dokumentasi (PRD, arsitektur, ADR, spec), konfigurasi OpenCode, dan kerangka CI/CD.
- Layanan Langflow (`langflow/`): image kustom, manifest flow, skrip validasi dan impor; kontrak flow dan API tool internal.
- Dialog manager deterministik, `LangflowClient`, dan circuit breaker beserta tes unit.
- Staging lokal (`docker-compose.staging.yml`, `make staging-up`, `make smoke`).
- Strategi branching `main` / `dev` / `feat/` `fix/` `chore/` dan pemeriksaan `branch-policy` di CI.
- ADR-0010 (Langflow + FastAPI), ADR-0011 (branching), ADR-0012 (deployment di akhir); SPEC-011.

### Changed
- Lapisan AI memakai Langflow + FastAPI; kode agent LangChain/LangGraph kustom tidak dipakai (menggantikan ADR-0004).
- Deployment cloud dipindah ke akhir (28 Nov sampai 3 Des 2026); `deploy.yml` hanya manual atau tag `v*`.
- Target latensi AI disesuaikan karena dua panggilan LLM per giliran (token pertama 4 detik, respons penuh 12 detik, roadmap 40 detik).
- PRD menjadi versi 0.5; SPEC-010 menjadi deployment cloud dan kesiapan demo.

### Removed
- `backend/app/ai/agent`, `ai/llm`, `ai/prompts`; skill `langgraph-node` (diganti `langflow-flow`).
