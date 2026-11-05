# SPEC-004: Katalog dan Panel Admin

> **Status:** Siap
> **Pemilik:** Anaya, Bastian | **Milestone:** M1 sampai M3 | **Prioritas:** Must
> **PRD:** FR-ADM-01 sampai 07, FR-CAT-01 sampai 04 | **ADR terkait:** ADR-0003, ADR-0007

## 1. Konteks

Katalog (mata kuliah, jalur karir, sertifikasi, materi) adalah **satu-satunya sumber** rekomendasi AI. Admin mengelola dan memverifikasinya; pengguna dapat mencari dan melaporkan tautan rusak.

## 2. Lingkup

**Dalam lingkup:** seed awal dari `data/seed/`, CRUD katalog untuk Admin (soft delete), impor CSV, embedding dan reindex, pencari sertifikasi dan materi, laporan tautan rusak, pemeriksa tautan terjadwal, log audit.

**Di luar lingkup:** scraping otomatis, kurasi oleh AI.

## 3. Persyaratan

| ID | Persyaratan |
|---|---|
| R-1 | Seed memuat 19 matkul terkurasi (+ 11 non-pemetaan), 11 jalur karir, dan pemetaan matkul ke jalur |
| R-2 | Admin dapat membuat, mengubah, dan menonaktifkan (`status`) item katalog; tidak ada hapus fisik |
| R-3 | Setiap perubahan katalog memicu embedding ulang item terkait |
| R-4 | Sertifikasi dan materi punya `last_verified_at`; item tidak diverifikasi lebih dari 90 hari ditandai `needs_review` |
| R-5 | Pencarian dengan filter: jalur, biaya, tingkat, format, bahasa |
| R-6 | Pengguna dapat melaporkan tautan rusak; Admin meninjau laporan |
| R-7 | Job terjadwal memeriksa URL (HEAD/GET) dan menandai yang mati sebagai `needs_review` |
| R-8 | Perubahan katalog tercatat pada `audit_logs` |
| R-9 | Target isi katalog: minimal 3 sertifikasi dan 5 materi per jalur |

## 4. Kontrak

- Endpoint: `listCareerPaths`, `listCertifications`, `listMaterials`, `createLinkReport`, `adminListCatalog`, `adminCreateCatalogItem`, `adminUpdateCatalogItem`, `adminDeactivateCatalogItem`, `adminReindex`, `adminRunLinkCheck`, `adminListLinkReports`.
- DB: `courses`, `career_paths`, `course_career_map`, `certifications`, `learning_materials`, `link_reports`, `audit_logs`.
- UI: halaman katalog (pengguna), panel admin (tabel, form, impor CSV, tinjau laporan).

## 5. Acceptance Criteria

- [ ] AC-1: Given database kosong, When `make seed`, Then katalog dasar termuat tanpa duplikasi (idempoten).
- [ ] AC-2: Given Admin menonaktifkan sebuah sertifikasi, When AI mencari sertifikasi, Then item itu tidak pernah dikembalikan.
- [ ] AC-3: Given Admin mengubah deskripsi materi, When selesai, Then embedding diperbarui dan perubahan tercatat pada log audit.
- [ ] AC-4: Given URL mati, When job pemeriksa berjalan, Then item ditandai `needs_review`.
- [ ] AC-5: Given pengguna melaporkan tautan rusak, When Admin membuka daftar laporan, Then laporan terlihat dengan konteks item.

## 6. Tugas

- [ ] T-1 [Anaya] Model dan migrasi katalog; skrip seed idempoten
- [ ] T-2 [Anaya] Layanan embedding (Vertex AI) dan reindex
- [ ] T-3 [Anaya] Endpoint katalog publik dan admin, log audit
- [ ] T-4 [Anaya] Pemeriksa tautan sebagai job (dijalankan lokal lewat skrip; Cloud Run Job + Cloud Scheduler dipasang pada M5, SPEC-010)
- [ ] T-5 [Bastian] Halaman pencarian katalog dan tombol lapor tautan
- [ ] T-6 [Bastian] Panel admin: CRUD, impor CSV, tinjau laporan
- [ ] T-7 [Anaya, Bastian] Kurasi data: sertifikasi dan materi per jalur

## 7. Strategi Uji

Seed berulang; filter pencarian; akses Admin vs Mahasiswa; reindex dipicu saat ubah data.

## 8. Catatan dan Risiko

Kualitas katalog menentukan kualitas roadmap. **Jangan** menambahkan URL dari ingatan model; verifikasi setiap tautan secara manual sebelum dimasukkan.
