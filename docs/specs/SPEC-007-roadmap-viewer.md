# SPEC-007: Roadmap Viewer

> **Status:** Siap
> **Pemilik:** Bastian | **Milestone:** M3 | **Prioritas:** Must
> **PRD:** FR-MAP-02 sampai 07, 09 | **ADR terkait:** ADR-0008

## 1. Konteks

Roadmap ditampilkan sebagai diagram node-edge interaktif mirip roadmap.sh, dengan detail matkul, materi, dan sertifikasi.

## 2. Lingkup

**Dalam lingkup:** render graf dengan React Flow, layout otomatis dari JSON, panel detail node, status matkul, penanda progres, klik referensi dicatat.

**Di luar lingkup:** ekspor PDF/gambar (Could), editor roadmap.

## 3. Persyaratan

| ID | Persyaratan |
|---|---|
| R-1 | Tahap disusun kiri ke kanan; node dikelompokkan per tahap; layout dihitung dari data (tanpa posisi hardcode) |
| R-2 | Tipe node: `stage`, `course`, `material`, `certification` dengan gaya berbeda |
| R-3 | Node matkul menampilkan semester, status (`completed`, `in_progress`, `not_taken`, `not_applicable`), dan nilai |
| R-4 | Node sertifikasi menampilkan penyedia, biaya (gratis/berbayar), tingkat, tautan |
| R-5 | Node materi menampilkan judul, format, bahasa, durasi, tingkat, tautan |
| R-6 | Setiap node menampilkan alasan rekomendasi ("mengapa ini?") |
| R-7 | Pengguna dapat menandai node selesai; progres tersimpan |
| R-8 | Klik tautan membuka tab baru dan mengirim event analitik |
| R-9 | Tersedia tombol "laporkan tautan rusak" |
| R-10 | Responsif (≥ 360 px) dan dapat dioperasikan dengan keyboard |
| R-11 | Roadmap sumber `template` menampilkan keterangan "versi dasar" |

## 4. Kontrak

- Endpoint: `getRoadmap`, `putRoadmapProgress`, `createEvent`, `createLinkReport`.
- Skema: `roadmap.schema.json`.

## 5. Acceptance Criteria

- [ ] AC-1: Given roadmap 60 node, When dirender, Then selesai ≤ 2 detik di perangkat menengah.
- [ ] AC-2: Given node matkul `completed`, When dilihat, Then menampilkan nilai dan tidak tampil sebagai tugas baru.
- [ ] AC-3: Given klik tautan, When dibuka, Then tab baru terbuka dan event tercatat.
- [ ] AC-4: Given layar 360 px, When dibuka, Then graf dapat di-pan dan di-zoom dan panel detail dapat dibaca.
- [ ] AC-5: Given fixture roadmap dari OpenAPI, When dirender pada test, Then tidak ada error dan seluruh tipe node muncul.

## 6. Tugas

- [ ] T-1 [Bastian] Fungsi layout dari JSON ke posisi node (teruji)
- [ ] T-2 [Bastian] Komponen node per tipe dan panel detail
- [ ] T-3 [Bastian] Penanda progres dan sinkronisasi API
- [ ] T-4 [Bastian] Event analitik klik dan laporan tautan
- [ ] T-5 [Bastian] Aksesibilitas dan responsif
- [ ] T-6 [Bastian] Test komponen (Vitest) dengan fixture

## 7. Strategi Uji

Fixture dari contoh OpenAPI; keadaan kosong, error, dan templat; uji layout untuk graf dengan banyak cabang.

## 8. Catatan dan Risiko

Layout otomatis pada graf lebar dapat sulit dibaca; mulai dengan layout berlapis per tahap.
