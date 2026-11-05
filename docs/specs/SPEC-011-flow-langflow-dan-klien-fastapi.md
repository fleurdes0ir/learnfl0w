# SPEC-011: Flow Langflow dan Klien FastAPI

> **Status:** Siap
> **Pemilik:** Anaya | **Milestone:** M1 sampai M3 | **Prioritas:** Must
> **PRD:** Bagian 8 (8.2, 8.3, 8.8, 8.9) | **ADR terkait:** ADR-0005, ADR-0010

## 1. Konteks

Fondasi lapisan AI: Langflow berjalan di Docker Compose, flow diekspor ke repositori, dan FastAPI memanggilnya lewat satu klien dengan circuit breaker dan fallback varian.

## 2. Lingkup

**Dalam lingkup:** layanan Langflow di Compose (database `langflow`, API key, variabel global), image kustom dengan flow, `LangflowClient` (non-stream dan stream, pencarian ID flow dari nama, circuit breaker per varian), validasi flow di CI, pencatatan `ai_runs`, `/healthz/llm`, verifikasi perilaku Langflow versi yang dipin.

**Di luar lingkup:** isi flow (SPEC-005, SPEC-006); deployment Langflow ke cloud (SPEC-010).

## 3. Persyaratan

| ID | Persyaratan |
|---|---|
| R-1 | Versi Langflow dipin (`LANGFLOW_VERSION`); tag image diverifikasi ada |
| R-2 | Langflow memakai database `langflow` pada PostgreSQL yang sama; `LANGFLOW_AUTO_LOGIN=false` |
| R-3 | Flow dimuat dari `langflow/flows/` lewat image (cadangan: `import_flows.py`) |
| R-4 | Setiap flow punya dua varian `router` dan `vertex` dengan antarmuka identik |
| R-5 | `LangflowClient` mencari `flow_id` dari nama, memakai `x-api-key` (dan ID token di cloud), timeout dan retry sesuai konfigurasi |
| R-6 | Circuit breaker per varian: buka setelah 3 kegagalan beruntun, coba lagi setelah 60 detik |
| R-7 | Streaming hanya pindah varian sebelum byte pertama |
| R-8 | Keluaran flow divalidasi Pydantic; keluaran tidak valid dihitung gagal |
| R-9 | CI `flows-check`: kedua varian ada, JSON valid, tanpa rahasia, paritas struktur |
| R-10 | Setiap panggilan dicatat pada `ai_runs` tanpa isi pesan |
| R-11 | `/healthz/llm` melaporkan status Langflow dan circuit tiap varian |

## 4. Kontrak

- Flow: [langflow-flows.md](../api/langflow-flows.md). Tool internal: [internal-tools.openapi.yaml](../api/internal-tools.openapi.yaml).
- Kode: `backend/app/ai/langflow/` (`client.py`, `circuit.py`), `langflow/`.

## 5. Acceptance Criteria

- [ ] AC-1: Given `make up`, When Langflow siap, Then `/health_check` hijau dan database `langflow` terpakai.
- [ ] AC-2: Given varian `router` gagal berturut-turut, When panggilan berikutnya, Then `LangflowClient` memakai `vertex` dan `fallback_used = true`.
- [ ] AC-3: Given flow tanpa varian kedua, When `make flows-check`, Then gagal.
- [ ] AC-4: Given JSON flow berisi kunci API, When `make flows-check`, Then gagal.
- [ ] AC-5: Given versi Langflow terpilih, When diverifikasi, Then variabel muat flow, endpoint daftar flow, format stream, dan bentuk respons terkonfirmasi dan dicatat di `langflow/README.md`.

## 6. Tugas

- [ ] T-1 [Anaya] Compose Langflow lokal, API key, variabel global (M1)
- [ ] T-2 [Anaya] Kerangka `LangflowClient`, circuit breaker, tes unit (sudah ada; lengkapi)
- [ ] T-3 [Anaya] Verifikasi perilaku Langflow versi dipin dan catat hasilnya (M1)
- [ ] T-4 [Anaya] `ai_runs` dan `/healthz/llm`
- [ ] T-5 [Anaya] `flows-check` di CI dan `make check`

## 7. Strategi Uji

`httpx.MockTransport` untuk klien (fallback, circuit); `validate_flows.py` dengan flow contoh baik dan buruk; uji manual Langflow lokal.

## 8. Catatan dan Risiko

Perubahan versi Langflow dapat mengubah API atau format stream (R-13); peningkatan versi hanya lewat PR dengan evaluasi persona.
