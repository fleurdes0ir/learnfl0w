# SPEC-003: Profil dan Transkrip

> **Status:** Siap
> **Pemilik:** Anaya, Bastian | **Milestone:** M1 sampai M2 | **Prioritas:** Must
> **PRD:** FR-PRO-01 sampai 05 | **ADR terkait:** ADR-0009

## 1. Konteks

Personalisasi roadmap membutuhkan profil dan transkrip (mata kuliah dan nilai). V1 memakai input manual atau CSV.

## 2. Lingkup

**Dalam lingkup:** onboarding profil, persetujuan data, input transkrip manual, impor CSV dengan pratinjau dan validasi, penyimpanan matkul non-pemetaan dengan `is_mappable = false`.

**Di luar lingkup:** parsing PDF, integrasi SIAKAD.

## 3. Persyaratan

| ID | Persyaratan |
|---|---|
| R-1 | Profil: semester, minat, skill, waktu belajar per minggu, target magang, preferensi biaya |
| R-2 | Persetujuan pemrosesan data (`consent_at`) wajib sebelum konsultasi |
| R-3 | Transkrip manual: pilih matkul dari katalog dan nilai (A, AB, B, BC, C, D, E) |
| R-4 | CSV `nama_matkul,nilai,semester` dengan pratinjau; baris tidak valid ditandai, hanya baris valid disimpan setelah konfirmasi |
| R-5 | Nama matkul dicocokkan toleran terhadap katalog; bila tidak persis sama, tawarkan pilihan terdekat |
| R-6 | Matkul di luar 19 terkurasi tetap disimpan tetapi diabaikan mesin pemetaan |
| R-7 | Perubahan profil atau transkrip menawarkan pembaruan roadmap |

## 4. Kontrak

- Endpoint: `getProfile`, `putProfile`, `listCourses`, `getTranscript`, `putTranscript`, `importTranscriptCsv`.
- DB: `student_profiles`, `transcript_entries`.
- UI: wizard onboarding, form transkrip, unggah CSV dengan pratinjau.

## 5. Acceptance Criteria

- [ ] AC-1: Given pengguna baru, When login pertama, Then diarahkan ke onboarding sampai profil dan persetujuan lengkap.
- [ ] AC-2: Given CSV dengan satu baris tidak valid, When diunggah, Then pratinjau menandai baris itu dan penyimpanan hanya memuat baris valid.
- [ ] AC-3: Given matkul non-pemetaan pada transkrip, When roadmap dibuat, Then matkul itu tidak muncul sebagai node.
- [ ] AC-4: Given pengguna lain, When mengakses transkrip pengguna ini, Then 403 atau 404.

## 6. Tugas

- [ ] T-1 [Anaya] Model, migrasi, dan service profil serta transkrip
- [ ] T-2 [Anaya] Parser CSV dengan validasi dan pencocokan nama
- [ ] T-3 [Anaya] Endpoint dan test
- [ ] T-4 [Bastian] Wizard onboarding dan form transkrip
- [ ] T-5 [Bastian] Unggah CSV dengan pratinjau dan penanganan error

## 7. Strategi Uji

CSV valid, kosong, delimiter salah, nilai tidak dikenal, nama matkul mirip; akses lintas pengguna.

## 8. Catatan dan Risiko

Skala nilai diasumsikan huruf (A, AB, B, BC, C, D, E); dapat disesuaikan lewat konfigurasi (PRD A-05).
