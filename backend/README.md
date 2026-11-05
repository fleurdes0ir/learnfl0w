# Backend

API, dialog manager, dan klien Langflow untuk IT Career Compass (FastAPI, SQLAlchemy async). Alur LLM dijalankan oleh Langflow (lihat `../langflow/`).

Aturan pengembangan: [AGENTS.md](AGENTS.md) dan [docs/engineering/coding-standards.md](../docs/engineering/coding-standards.md). Kontrak API: [docs/api/openapi.yaml](../docs/api/openapi.yaml).

## Struktur

```text
app/
├── main.py            # factory aplikasi FastAPI
├── api/               # routes (health di root, v1 di /api/v1)
├── core/              # konfigurasi (Settings), logging
├── db/                # base model, sesi async
├── models/            # model SQLAlchemy
├── schemas/           # model Pydantic (I/O)
├── services/          # logika bisnis
├── auth/              # hash password, JWT, RBAC
└── ai/                # dialog/ (dialog manager), langflow/ (klien + circuit breaker), guardrails/, tools/, embeddings/, schemas/
migrations/            # Alembic
scripts/               # seed dan skrip bantu
tests/                 # pytest (tests/ai: dialog, circuit breaker, klien Langflow, evaluasi)
```

## Menjalankan Tanpa Docker

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp ../.env.example ../.env        # lalu isi nilainya
uvicorn app.main:app --reload --port 8080
```

Dokumentasi interaktif: <http://localhost:8080/docs>.

## Perintah

| Perintah | Fungsi |
|---|---|
| `pytest -q` | Menjalankan test |
| `ruff check . && ruff format --check .` | Lint dan cek format |
| `mypy app` | Cek tipe |
| `alembic revision --autogenerate -m "pesan"` | Membuat migrasi |
| `alembic upgrade head` | Menerapkan migrasi |
| `python -m scripts.seed` | Memuat data katalog |
