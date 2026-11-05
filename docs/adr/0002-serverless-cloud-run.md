# ADR-0002: Arsitektur Serverless di GCP dengan Cloud Run

> **Status:** Diterima
> **Tanggal:** 2026-10-31 | **Pengambil keputusan:** Anaya, Bastian

## Konteks

Proyek adalah tugas UAS Cloud Computing dengan tenggat 8 Desember 2026 dan kredit GCP gratis. Aplikasi harus berjalan lancar di cloud tanpa hambatan dan sudah dikemas dalam Docker.

## Faktor Keputusan

- Dapat didemokan sebagai arsitektur serverless cloud-native.
- Biaya rendah saat idle; tidak ada server yang dikelola.
- Tetap memakai container (Docker) dan mendukung streaming SSE.
- Risiko *cold start* harus dapat dikendalikan saat demo.

## Opsi yang Dipertimbangkan

### Opsi A: Cloud Run (container serverless)
- Kelebihan: Docker apa adanya, scale-to-zero, revisi dan rollback bawaan, SSE didukung, min-instances untuk menghindari cold start.
- Kekurangan: sidecar Tailscale butuh konfigurasi khusus; koneksi DB harus dijaga (banyak instance).

### Opsi B: VM Compute Engine + Docker Compose
- Kelebihan: Tailscale di host sederhana, perilaku mudah ditebak.
- Kekurangan: bukan serverless, perlu patching dan pengelolaan server.

### Opsi C: Cloud Functions / App Engine
- Kelebihan: terkelola penuh.
- Kekurangan: kurang cocok untuk aplikasi stateful-streaming berbasis container; kontrol runtime lebih terbatas.

## Keputusan

Memakai **Cloud Run** untuk frontend dan backend, Cloud Run Jobs + Cloud Scheduler untuk tugas terjadwal, dan Cloud SQL sebagai database.

## Konsekuensi

- Positif: memenuhi tujuan UAS, biaya terkendali, rollback cepat.
- Negatif: perlu `min-instances = 1` pada masa demo dan pool koneksi DB kecil.
- Tindak lanjut: deployment dilakukan di akhir (28 Nov sampai 3 Des) lewat jendela deployment; staging di lokal ([ADR-0012](0012-deployment-di-akhir.md)).

## Referensi

- [PRD 5 dan 14.6](../product/PRD.md), [deployment.md](../architecture/deployment.md)
