# ADR-0008: Roadmap sebagai Structured Output dengan Roadmap Templat Cadangan

> **Status:** Diterima
> **Tanggal:** 2026-10-31 | **Pengambil keputusan:** Anaya

## Konteks

Roadmap harus logis, terhubung ke katalog, dan dapat dirender sebagai graf. Keluaran bebas dari LLM rawan halusinasi dan format rusak.

## Opsi yang Dipertimbangkan

### Opsi A: LLM menulis roadmap bebas (teks)
- Kekurangan: sulit divalidasi dan dirender.

### Opsi B: Structured output (JSON Schema) + verifikasi katalog + templat cadangan
- Kelebihan: dapat divalidasi otomatis; ID dan tautan diverifikasi; selalu ada hasil.
- Kekurangan: perlu skema, validator, dan templat per jalur yang dikurasi.

## Keputusan

**Opsi B.** LLM hanya memilih dan mengurutkan item katalog; keluaran divalidasi terhadap `roadmap.schema.json` dan Pydantic, setiap `ref_id` diverifikasi. Gagal dua kali berarti **roadmap templat** per jalur (`career_paths.template_stages`) yang dipersonalisasi secara deterministik.

## Konsekuensi

- Positif: 0 entitas fiktif, perilaku dapat diuji.
- Negatif: templat harus dirawat Admin; kreativitas LLM sengaja dibatasi.
