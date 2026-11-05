# SPEC-008: Riwayat, Umpan Balik, dan Progres

> **Status:** Siap
> **Pemilik:** Anaya, Bastian | **Milestone:** M3 sampai M4 | **Prioritas:** Must (riwayat, rating), Should (versi, hapus)
> **PRD:** FR-HIS-01 sampai 03, FR-MAP-09, FR-MAP-10, FR-CAT-04

## 1. Konteks

Pengguna kembali ke sesi dan roadmap sebelumnya, memberi umpan balik, dan melacak progres.

## 2. Lingkup

**Dalam lingkup:** daftar sesi dan roadmap, versi roadmap, rating dan komentar, hapus sesi atau data, pencatatan event analitik (klik referensi).

**Di luar lingkup:** notifikasi email (Could).

## 3. Persyaratan

| ID | Persyaratan |
|---|---|
| R-1 | Daftar sesi dan roadmap milik pengguna, terbaru lebih dulu, dengan paginasi |
| R-2 | Pengguna dapat membuka versi roadmap sebelumnya |
| R-3 | Rating 1 sampai 5 dan komentar opsional pada sesi dan roadmap |
| R-4 | Pengguna dapat menghapus sesi (beserta pesan) dan roadmap miliknya |
| R-5 | Event analitik memakai ID pseudonim dan tidak memuat isi percakapan |
| R-6 | Notifikasi in-app "Roadmap siap" dan pengingat sesi tidak selesai |

## 4. Kontrak

- Endpoint: `listSessions`, `deleteSession`, `listRoadmaps`, `getRoadmap`, `putRoadmapProgress`, `createFeedback`, `createEvent`.
- DB: `feedback`, `roadmap_progress`, `analytics_events`.

## 5. Acceptance Criteria

- [ ] AC-1: Given beberapa sesi, When membuka riwayat, Then hanya milik pengguna dan terurut terbaru.
- [ ] AC-2: Given rating diberikan, When disimpan, Then dapat dibaca kembali dan terhitung pada dashboard.
- [ ] AC-3: Given sesi dihapus, When diperiksa, Then pesan terkait ikut terhapus.
- [ ] AC-4: Given event klik, When disimpan, Then tidak memuat isi pesan atau identitas langsung.

## 6. Tugas

- [ ] T-1 [Anaya] Endpoint riwayat, versi, hapus, feedback, event
- [ ] T-2 [Anaya] Pseudonimisasi ID analitik
- [ ] T-3 [Bastian] Halaman riwayat, rating, hapus, notifikasi in-app

## 7. Strategi Uji

Akses lintas pengguna, cascade hapus, paginasi, validasi rating.

## 8. Catatan dan Risiko

Pilih fungsi pseudonim yang stabil (HMAC dengan secret) agar tren dapat dihitung tanpa identitas.
