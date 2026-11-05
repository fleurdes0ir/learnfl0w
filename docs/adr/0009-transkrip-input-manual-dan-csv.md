# ADR-0009: Transkrip via Input Manual dan CSV pada V1

> **Status:** Diterima
> **Tanggal:** 2026-10-31 | **Pengambil keputusan:** Anaya, Bastian

## Konteks

Personalisasi roadmap membutuhkan data mata kuliah dan nilai mahasiswa. Format transkrip kampus bervariasi dan parsing PDF/OCR rawan salah serta memakan waktu.

## Opsi yang Dipertimbangkan

### Opsi A: Parsing PDF/OCR
- Kekurangan: akurasi tidak pasti, waktu pengembangan besar, tenggat ketat.

### Opsi B: Input manual dan unggah CSV
- Kelebihan: sederhana, akurat, mudah diuji; ada pratinjau dan validasi sebelum simpan.
- Kekurangan: usaha pengguna sedikit lebih besar.

## Keputusan

**Opsi B** pada V1. Templat CSV: `nama_matkul,nilai,semester`. Mata kuliah di luar 19 yang terkurasi disimpan dengan `is_mappable = false` dan diabaikan mesin pemetaan. Parsing PDF ditunda ke V2.

## Konsekuensi

- Positif: risiko kecil, cepat selesai.
- Negatif: pencocokan nama matkul perlu pencocokan toleran (nama mirip ditawarkan sebagai pilihan).
