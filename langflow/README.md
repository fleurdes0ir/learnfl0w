# Langflow

Lapisan AI IT Career Compass. Flow disusun secara visual di Langflow, diekspor sebagai JSON ke repositori, dan dipanggil oleh backend FastAPI. Keputusan: [ADR-0010](../docs/adr/0010-langflow-dan-fastapi-untuk-lapisan-ai.md). Kontrak input/output: [docs/api/langflow-flows.md](../docs/api/langflow-flows.md).

## Pembagian Tugas

| Langflow (folder ini) | FastAPI (`backend/`) |
|---|---|
| Alur LLM: prompt, model, tool | Auth, data, dialog manager, retrieval katalog |
| Varian `router` (9router) dan `vertex` | Circuit breaker, pemilihan varian, validasi output, roadmap templat |

Langflow bersifat **stateless** dan **privat** di cloud (hanya backend yang boleh memanggil).

## Struktur

```text
langflow/
├── Dockerfile              # image kustom: versi dipin + flow dari flows/
├── flows.manifest.json     # daftar flow, mode, status (planned | exported)
├── flows/                  # hasil ekspor: <flow>__router.json, <flow>__vertex.json
└── scripts/
    ├── validate_flows.py   # dipakai CI dan `make flows-check`
    └── import_flows.py     # cadangan: impor flow lewat API
```

## Flow V1

| Flow | Mode | Spec |
|---|---|---|
| `slot-extractor` | non-stream | SPEC-005 |
| `consultant-reply` | stream | SPEC-005 |
| `path-advisor` | non-stream | SPEC-006 |
| `roadmap-builder` | non-stream | SPEC-006 |

## Menyusun Flow (Lokal)

1. `cp .env.example .env`, isi `LANGFLOW_*`, `ROUTER_*`, `VERTEX_*`, `INTERNAL_TOOL_TOKEN`.
2. `make up`, buka <http://localhost:7860>, login dengan `LANGFLOW_SUPERUSER`.
3. Buat API key (Settings > API keys) dan simpan ke `.env` sebagai `LANGFLOW_API_KEY`.
4. Susun flow mengikuti kontrak. Kunci dan URL **tidak** ditulis di komponen; pakai **variabel global** (`ROUTER_BASE_URL`, `ROUTER_API_KEY`, `INTERNAL_TOOL_TOKEN`, `VERTEX_PROJECT`, `VERTEX_LOCATION`).
5. Buat varian kedua dengan menduplikasi flow dan **hanya** mengganti komponen model (`__router` memakai model kompatibel OpenAI dengan basis URL 9router; `__vertex` memakai Vertex AI).
6. Ekspor kedua flow (JSON) ke `flows/` dengan nama `<flow>__<variant>.json`, ubah `status` menjadi `exported` pada `flows.manifest.json`.
7. Jalankan `make flows-check` dan evaluasi persona (`pytest backend/tests/ai`).
8. Buka PR ke `dev`. Diff JSON ditinjau seperti kode.

## Aturan

- Satu flow, satu tanggung jawab; prompt singkat dan spesifik.
- Tidak ada nama sertifikasi, materi, atau URL di prompt. Data katalog selalu datang dari input atau tool.
- Tidak ada rahasia di JSON (CI memeriksanya).
- Versi Langflow **dipin** (`LANGFLOW_VERSION`). Peningkatan versi lewat PR dengan evaluasi persona.
- Penyusunan UI hanya di lokal. UI Langflow tidak diekspos di cloud.

## Hal yang Perlu Diverifikasi pada Versi yang Dipin

Beberapa nama variabel dan endpoint berikut berasal dari dokumentasi Langflow dan perlu dikonfirmasi pada versi terpilih saat M1:

- `LANGFLOW_LOAD_FLOWS_PATH` (memuat flow saat startup); cadangan: `scripts/import_flows.py`.
- `LANGFLOW_VARIABLES_TO_GET_FROM_ENVIRONMENT` (variabel global dari environment).
- `GET /api/v1/flows/` (daftar flow untuk mencari ID dari nama).
- Format event streaming `POST /api/v1/run/{flow}?stream=true`.
- Struktur respons non-stream untuk mengambil teks atau JSON keluaran.
- Health check: gunakan `/health_check` (bukan `/health`).
