# Data Seed

Data awal katalog yang dimuat oleh `make seed` (lihat [SPEC-004](../../docs/specs/SPEC-004-katalog-dan-admin.md)). Skrip seed harus **idempoten**: dapat dijalankan berulang tanpa duplikasi.

| File | Isi | Status |
|---|---|---|
| `courses.csv` | 19 mata kuliah terkurasi (`is_mappable=true`) dan 11 non-pemetaan (`false`) | Siap; deskripsi perlu dicek terhadap silabus |
| `course_career_map.csv` | Pemetaan matkul ke jalur karir dengan `relevance` 1 sampai 3 | Seed awal (disetujui), dapat diubah Admin |
| `career_paths.json` | 11 jalur karir baku beserta `template_stages` | Draf templat; perlu dikurasi |
| `certifications.csv` | Sertifikasi | **Kosong (hanya header)** |
| `learning_materials.csv` | Materi belajar | **Kosong (hanya header)** |

## Aturan Pengisian Katalog

- Target: minimal **3 sertifikasi** dan **5 materi** per jalur karir.
- **Jangan menambahkan URL dari ingatan atau dari hasil AI.** Buka setiap tautan secara manual, pastikan aktif dan sesuai, lalu isi `last_verified_at` (format `YYYY-MM-DD`).
- `cost_type`: `free`, `paid`, atau `freemium`. `level`: `beginner`, `intermediate`, `advanced`.
- `career_path_codes` dan `topic_tags` dipisah dengan tanda `|` (contoh: `CP-05|CP-01`).
- `status`: `active`, `needs_review`, atau `inactive`.
- `code` unik: `CERT-001`, `MAT-001`, dan seterusnya.

## Catatan Pemetaan

`relevance`: `3` untuk jalur utama sebuah matkul, `2` untuk jalur pendukung. Pemetaan ini adalah titik awal dan harus ditinjau Admin setelah silabus dicek.
