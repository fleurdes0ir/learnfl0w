# SPEC-009: Dashboard Admin

> **Status:** Siap
> **Pemilik:** Anaya (data), Bastian (UI) | **Milestone:** M4 | **Prioritas:** Should
> **PRD:** RPT-01 sampai RPT-13, AC-08

## 1. Konteks

Admin melihat tren karir yang diminati mahasiswa dan kesehatan sistem. Data bersifat agregat dan anonim.

## 2. Lingkup

**Dalam lingkup:** dashboard tren (jalur populer, tren mingguan, distribusi semester, matkul paling sering muncul, sertifikasi/materi paling banyak diklik, celah kompetensi, funnel, kepuasan), dashboard operasional (latensi, error, fallback LLM, token dan biaya, kesehatan tautan), filter, ekspor CSV agregat.

**Di luar lingkup:** dashboard untuk peran lain, ringkasan email (Could).

## 3. Persyaratan

| ID | Persyaratan |
|---|---|
| R-1 | Hanya peran `admin` yang dapat mengakses |
| R-2 | Segmen dengan kurang dari 5 pengguna disembunyikan |
| R-3 | Filter: rentang tanggal, semester, jalur karir |
| R-4 | Ekspor CSV untuk data agregat |
| R-5 | Data tertunda maksimal 15 menit |
| R-6 | Metrik operasional: latensi P50/P95, tingkat error LLM, tingkat fallback, tingkat roadmap templat, token dan estimasi biaya harian, kesehatan tautan |

## 4. Kontrak

- Endpoint: `adminTrends`, `adminOps`.
- UI: halaman `/admin/dashboard` dengan kartu dan grafik.

## 5. Acceptance Criteria

- [ ] AC-1: Given mahasiswa, When mengakses endpoint dashboard, Then 403.
- [ ] AC-2: Given segmen kurang dari 5 pengguna, When dashboard dibuka, Then segmen disembunyikan.
- [ ] AC-3: Given filter semester dipilih, When data dimuat, Then seluruh grafik mengikuti filter.
- [ ] AC-4: Given tombol ekspor, When diklik, Then CSV agregat terunduh tanpa data individu.

## 6. Tugas

- [ ] T-1 [Anaya] Query agregasi dan endpoint
- [ ] T-2 [Anaya] Metrik operasional dari log dan tabel
- [ ] T-3 [Bastian] Halaman dashboard, grafik, filter, ekspor
- [ ] T-4 [Anaya] Data sintetis berlabel untuk demo bila data pilot sedikit

## 7. Strategi Uji

Uji ambang k-anonymity, filter, otorisasi, dan format CSV.

## 8. Catatan dan Risiko

Data pilot kecil; sediakan mode data sintetis yang jelas berlabel agar tidak menyesatkan.
