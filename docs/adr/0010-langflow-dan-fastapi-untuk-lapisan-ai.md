# ADR-0010: Langflow + FastAPI untuk Lapisan AI

> **Status:** Diterima
> **Tanggal:** 2026-11-03 | **Pengambil keputusan:** Anaya, Bastian
> **Menggantikan:** [ADR-0004](0004-agent-langgraph-slot-filling.md)

## Konteks

Rencana awal membangun agent dengan kode LangChain dan LangGraph kustom. Tim memilih memakai **Langflow** (flow visual) agar prompt dan alur LLM dapat disusun dan diubah lebih cepat, dengan **FastAPI** sebagai backend tunggal. Kebutuhan tetap: konsultasi hybrid, anti-halusinasi (rekomendasi hanya dari katalog), roadmap terstruktur, dan fallback LLM.

## Faktor Keputusan

- Iterasi prompt dan alur harus cepat (tenggat 8 Des 2026, tim 2 orang).
- Kontrol, keamanan, dan kemampuan uji tidak boleh turun.
- Harus berjalan stabil sebagai layanan serverless di cloud.

## Opsi yang Dipertimbangkan

### Opsi A: Langflow untuk alur LLM, FastAPI untuk data dan aturan
- Kelebihan: prompt dan alur disusun visual; kode agent berkurang; dialog manager, validasi, dan guardrails tetap berupa kode yang dapat diuji.
- Kekurangan: Langflow berat untuk serverless; flow JSON sulit di-*review*; dua varian per flow; versi harus dipin.

### Opsi B: Agent LangChain/LangGraph kustom di backend (ADR-0004)
- Kelebihan: seluruh logika berupa kode; satu layanan lebih sedikit.
- Kekurangan: iterasi prompt lebih lambat; lebih banyak kode untuk dikelola.

### Opsi C: Langflow saja sebagai backend (tanpa logika di FastAPI)
- Kelebihan: paling sedikit kode.
- Kekurangan: validasi, RBAC, dan guardrails sulit dijamin; tidak cocok untuk data aplikasi.

## Keputusan

**Opsi A.** Pembagian:
- **FastAPI:** auth, data, dialog manager deterministik, retrieval katalog, himpunan kandidat tertutup, guardrails, validasi roadmap, roadmap templat, circuit breaker, pencatatan `ai_runs`.
- **Langflow (privat, stateless):** empat flow (`slot-extractor`, `consultant-reply`, `path-advisor`, `roadmap-builder`), masing-masing dengan varian `router` dan `vertex`.
- Flow disusun di lokal, diekspor sebagai JSON ke `langflow/flows/`, dimuat lewat image kustom dengan versi Langflow yang dipin.
- Tool katalog untuk agent adalah endpoint internal FastAPI (`X-Internal-Token`).

## Konsekuensi

- Positif: iterasi cepat pada prompt; logika kritis tetap teruji; fallback LLM tetap berjalan lewat varian flow.
- Negatif / risiko: startup dan memori Langflow di Cloud Run (R-19); diff JSON sulit ditinjau (R-20); varian dapat menyimpang (R-21); latensi dua panggilan per giliran (R-23).
- Tindak lanjut: [SPEC-011](../specs/SPEC-011-flow-langflow-dan-klien-fastapi.md), kontrak [langflow-flows.md](../api/langflow-flows.md), validasi CI `flows-check`.

## Referensi

- [PRD bagian 8](../product/PRD.md), [ai-design.md](../architecture/ai-design.md)
