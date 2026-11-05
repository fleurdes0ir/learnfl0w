# SPEC-005: Konsultasi AI (Dialog Manager, Slot-Filling, Streaming)

> **Status:** Siap
> **Pemilik:** Anaya (dialog manager, flow), Bastian (UI chat) | **Milestone:** M2 | **Prioritas:** Must
> **PRD:** FR-CHAT-01 sampai 09, NFR-P-01, NFR-P-02 | **ADR terkait:** ADR-0005, ADR-0010

## 1. Konteks

Mahasiswa menjalani percakapan terarah (hybrid) yang mengumpulkan informasi lalu menawarkan 1 sampai 3 jalur karir sebelum roadmap dibuat. Tahap dan aksi diputuskan **dialog manager di FastAPI**; Langflow hanya mengekstrak slot dan menulis balasan.

## 2. Lingkup

**Dalam lingkup:** dialog manager (`app/ai/dialog/`), flow `slot-extractor` dan `consultant-reply` (varian `router` dan `vertex`), tool katalog internal, input guardrails, endpoint SSE, UI chat.

**Di luar lingkup:** `path-advisor` dan `roadmap-builder` (SPEC-006), tool tren pasar kerja (V2).

## 3. Persyaratan

| ID | Persyaratan |
|---|---|
| R-1 | Satu sesi = satu `conversation`; dapat dilanjutkan jika belum selesai |
| R-2 | Slot wajib: `interests`, `current_skills`, `work_style`, `hours_per_week`, `internship_target`, `budget_pref` |
| R-3 | Slot yang sudah ada di profil tidak ditanyakan ulang, hanya dikonfirmasi |
| R-4 | `slot-extractor` mengembalikan `slots_update`, `intent`, `chosen_path`; keluaran divalidasi Pydantic |
| R-5 | Dialog manager memutuskan tahap dan aksi (`ask_slot`, `summarize`, `offer_paths`, `answer_question`, `redirect`, `generate_roadmap`) tanpa LLM |
| R-6 | Ringkasan profil dikonfirmasi pengguna sebelum jalur ditawarkan |
| R-7 | Pertanyaan di luar topik dijawab singkat lalu diarahkan kembali |
| R-8 | Respons di-*stream* lewat SSE (`token`, `tool_status`, `slots`, `error`, `done`); URL non-katalog dihapus dari aliran |
| R-9 | Batas: 25 giliran per sesi, 5 sesi per hari per pengguna |
| R-10 | Circuit breaker per varian flow; fallback ke `vertex` setelah 3 kegagalan beruntun |
| R-11 | State (tahap, slot, pesan) disimpan di PostgreSQL; sesi dapat dilanjutkan oleh instance lain |
| R-12 | Tool `certification_finder` dan `material_finder` berupa endpoint internal (`X-Internal-Token`), hanya baca |

## 4. Kontrak

- Endpoint publik: `createSession`, `listSessions`, `getSession`, `deleteSession`, `postMessage` (SSE).
- Flow: [langflow-flows.md](../api/langflow-flows.md) (`slot-extractor`, `consultant-reply`). Tool: [internal-tools.openapi.yaml](../api/internal-tools.openapi.yaml).
- DB: `conversations` (termasuk `state`), `messages`, `ai_runs`.
- UI: halaman chat, indikator mengetik dan status tool, tombol berhenti dan ulang, label "dihasilkan AI".

## 5. Acceptance Criteria

- [ ] AC-1: Given profil lengkap, When sesi dimulai, Then hanya slot yang kurang yang ditanyakan.
- [ ] AC-2: Given pesan di luar topik, When diproses, Then respons singkat dan percakapan kembali ke slot.
- [ ] AC-3: Given varian `router` gagal 3 kali, When pesan berikutnya, Then respons tetap datang lewat `vertex` tanpa kehilangan state.
- [ ] AC-4: Given prompt injection, When diproses, Then instruksi diabaikan dan kejadian dicatat tanpa isi pesan.
- [ ] AC-5: Given pengujian waktu, When diukur, Then token pertama ≤ 4 detik (P95), respons penuh ≤ 12 detik (P95).
- [ ] AC-6: Given sesi dihentikan lalu dibuka kembali, Then percakapan berlanjut dari tahap dan slot terakhir.
- [ ] AC-7: Given semua transisi tahap, When diuji unit, Then seluruh cabang dialog manager tercakup.

## 6. Tugas

- [ ] T-1 [Anaya] Dialog manager `app/ai/dialog/state.py` dan layanan percakapan (sudah ada kerangka dan tes unit)
- [ ] T-2 [Anaya] Flow `slot-extractor` dan `consultant-reply` (dua varian), ekspor, `flows-check`
- [ ] T-3 [Anaya] Endpoint internal tool dan token internal
- [ ] T-4 [Anaya] Input guardrails, rate limit, filter URL pada aliran
- [ ] T-5 [Anaya] Endpoint SSE yang memetakan event Langflow ke event kita; pencatatan `ai_runs`
- [ ] T-6 [Bastian] UI chat dengan streaming via `fetch` + `ReadableStream`
- [ ] T-7 [Anaya] Persona uji dan evaluasi (`backend/tests/ai/`)

## 7. Strategi Uji

Uji unit dialog manager dan circuit breaker; klien Langflow dengan `httpx.MockTransport`; 20 persona sintetis; uji fallback dengan varian yang sengaja gagal; uji SSE end-to-end di staging lokal.

## 8. Catatan dan Risiko

Format event streaming dan struktur respons Langflow diverifikasi pada versi yang dipin (SPEC-011 T-3). Prompt tidak boleh memuat nama sertifikasi atau URL.
