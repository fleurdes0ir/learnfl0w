# Checklist Demo (8 Desember 2026)

> **Status:** Draft | **Pemilik:** Anaya, Bastian | **Diperbarui:** 2026-10-31

## H-7 (1 Des)

- [ ] `min-instances = 1` aktif untuk backend, frontend, dan Langflow
- [ ] Staging lokal tetap siap sebagai demo cadangan (`make staging-up`)
- [ ] Uptime check dan alert aktif
- [ ] Billing budget aktif; sisa kredit cukup
- [ ] Akun demo: satu Mahasiswa (profil dan transkrip terisi) dan satu Admin
- [ ] Katalog terisi dan tautan terverifikasi
- [ ] Data pilot atau data sintetis berlabel untuk dashboard

## H-4 (4 Des): Code Freeze

- [ ] Seluruh Must selesai; CI hijau di `main`
- [ ] Tag `v1.0.0` dibuat
- [ ] Evaluasi AI memenuhi target (grounding 100%, skema ≥ 98%)
- [ ] Uji fallback LLM lulus (9router dimatikan)
- [ ] Ekspor database dan backup tersimpan

## H-2 sampai H-1 (6 sampai 7 Des)

- [ ] Latihan demo penuh ke-1 dan ke-2 (catat waktu)
- [ ] Rekaman layar cadangan selesai
- [ ] Runbook dibaca bersama
- [ ] Skenario demo dan urutan bicara disepakati
- [ ] Perangkat, koneksi internet, dan cadangan hotspot disiapkan

## Hari H (8 Des)

- [ ] 10 menit sebelum: akses `/healthz` dan `/healthz/llm`, jalankan satu sesi uji (pemanasan)
- [ ] Buka frontend, login sebagai Mahasiswa dan Admin di dua jendela
- [ ] Rekaman cadangan siap dibuka
- [ ] Tab konsol GCP (logs, revisions) siap untuk rollback darurat

## Skenario Demo (usulan, ±10 menit)

1. Masalah dan solusi (1 menit)
2. Arsitektur serverless: Cloud Run, Cloud SQL, CI/CD, fallback LLM (2 menit)
3. Login, profil, transkrip (1 menit)
4. Konsultasi AI dengan streaming (2 menit)
5. Roadmap interaktif: matkul, materi, sertifikasi, klik referensi (2 menit)
6. Admin: katalog dan dashboard tren (1 menit)
7. Keandalan: health check, rollback, fallback (1 menit)
