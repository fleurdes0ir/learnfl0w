# ADR-0005: LLM via 9router (Tailscale) dengan Fallback Otomatis ke Vertex AI

> **Status:** Diterima (jalur utama divalidasi pada Gate G1)
> **Tanggal:** 2026-10-31 | **Pengambil keputusan:** Anaya, Bastian

## Konteks

Tim memiliki API combo sendiri di 9router yang berjalan di homelab rekan dan dijangkau lewat Tailscale. Aplikasi di Cloud Run harus tetap lancar saat demo walaupun homelab atau koneksi bermasalah.

## Opsi yang Dipertimbangkan

### Opsi A: 9router saja
- Kelebihan: memakai model combo sendiri.
- Kekurangan: titik kegagalan tunggal (homelab, koneksi, kuota).

### Opsi B: Vertex AI saja
- Kelebihan: paling andal, memakai kredit GCP, tanpa jaringan tambahan.
- Kekurangan: tidak memakai combo sendiri.

### Opsi C: 9router sebagai utama, Vertex AI sebagai fallback otomatis
- Kelebihan: memakai combo sendiri dan tetap tahan gangguan.
- Kekurangan: dua jalur untuk diuji; sidecar Tailscale perlu validasi.

## Keputusan

**Opsi C**, diwujudkan sebagai dua varian setiap flow Langflow (`router` dan `vertex`) yang dipilih oleh `LangflowClient` di FastAPI lewat *circuit breaker* (buka setelah 3 kegagalan beruntun, coba lagi setiap 60 detik). Sidecar Tailscale berada pada layanan Langflow. Konektivitas diuji di lokal sejak M1 dan di Cloud Run pada jendela deployment (M5). Bila gagal, **varian Vertex AI menjadi jalur utama**.

## Konsekuensi

- Positif: ketahanan tinggi, penyedia dapat ditukar lewat konfigurasi.
- Negatif: perilaku model dapat sedikit berbeda antar penyedia; evaluasi AI dijalankan pada keduanya.
- Tindak lanjut: `/healthz/llm` melaporkan status kedua jalur.
