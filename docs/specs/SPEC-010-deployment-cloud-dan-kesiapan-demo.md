# SPEC-010: Deployment Cloud, Keandalan, dan Kesiapan Demo

> **Status:** Siap
> **Pemilik:** Anaya | **Milestone:** M5 (28 Nov sampai 3 Des) | **Prioritas:** Must
> **PRD:** 14.6 (REL-01 sampai REL-14), NFR-O-01, NFR-O-04 sampai NFR-O-06, Bagian 20.1 | **ADR terkait:** ADR-0002, ADR-0005, ADR-0012

## 1. Konteks

Deployment ditempatkan **di akhir**. Spec ini mencakup pembuatan resource GCP, deploy pertama (frontend, backend, **Langflow privat**), validasi Tailscale ke 9router, kontrol keandalan, pilot di cloud, dan kesiapan demo 8 Des 2026. Prasyarat proyek: berjalan di cloud dengan baik, benar, dan lancar.

## 2. Lingkup

**Dalam lingkup:** resource GCP (Cloud SQL, Cloud Run, Artifact Registry, Secret Manager, Workload Identity), CD dari `main`, Langflow privat dan sidecar Tailscale, min-instances, health check, uptime check dan alert, fallback teruji, smoke test dan rollback, budget alert, backup, runbook, pilot di cloud, gladi demo, code freeze.

**Di luar lingkup:** multi-region, environment cloud staging terpisah.

## 3. Persyaratan

| ID | Persyaratan |
|---|---|
| R-1 | Seluruh checklist pra-deploy (PRD 20.7) selesai sebelum 28 Nov |
| R-2 | Resource dibuat sesuai [deployment.md](../architecture/deployment.md); rahasia hanya di Secret Manager |
| R-3 | Langflow berjalan sebagai layanan **privat**; hanya `sa-backend` yang boleh memanggil |
| R-4 | Deploy pertama mengikuti urutan khusus (deployment.md bagian 8); flow termuat (4 x 2 varian) |
| R-5 | `min-instances = 1` untuk frontend, backend, Langflow pada 1 sampai 8 Des 2026 |
| R-6 | Startup dan liveness probe aktif; deploy gagal otomatis dibatalkan; rollback ≤ 5 menit |
| R-7 | Uptime check dan alert ke webhook tim; billing budget 50/80/100% |
| R-8 | Tailscale sidecar ke 9router divalidasi; bila gagal, `LLM_PROVIDER=vertex` menjadi jalur utama |
| R-9 | Fallback teruji dengan mematikan jalur utama dan dengan mematikan Langflow (roadmap templat) |
| R-10 | Pool DB kecil, retry dengan backoff; Cloud SQL backup harian dan ekspor sebelum demo |
| R-11 | Runbook dan checklist demo selesai ([runbook](../operations/runbook.md), [demo-checklist](../operations/demo-checklist.md)) |
| R-12 | Pilot minimal 5 mahasiswa di cloud; code freeze 4 Des; gladi demo penuh minimal 2 kali; rekaman cadangan |

## 4. Kontrak

- Endpoint: `getHealth`, `getLlmHealth`.
- Infra: [deployment.md](../architecture/deployment.md), `.github/workflows/deploy.yml`, `infra/cloud-run/langflow.service.yaml`.

## 5. Acceptance Criteria

- [ ] AC-1: Given aplikasi dibuka tanpa pemanasan, When pertama kali, Then halaman dan respons pertama ≤ 5 detik tanpa error.
- [ ] AC-2: Given 9router dimatikan, When pesan dikirim, Then respons tetap datang lewat varian `vertex`.
- [ ] AC-3: Given Langflow dimatikan, When roadmap diminta, Then roadmap templat dihasilkan dan sesi tetap tersimpan.
- [ ] AC-4: Given revisi rusak ter-deploy, When smoke test gagal, Then rollback otomatis.
- [ ] AC-5: Given 20 sesi bersamaan, When uji beban ringan, Then tidak ada error dan latensi sesuai target.
- [ ] AC-6: Given Langflow di cloud, When diakses tanpa kredensial dari internet, Then ditolak.
- [ ] AC-7: Given hari demo, When checklist dijalankan, Then seluruh butir lolos.

## 6. Tugas

- [ ] T-1 [Anaya] Pra-deploy: perkiraan sumber daya Langflow (`docker stats`), checklist, daftar variabel dan secret
- [ ] T-2 [Anaya] Resource GCP, service account, Workload Identity, secret (28 sampai 29 Nov)
- [ ] T-3 [Anaya] Deploy pertama dan API key Langflow (30 Nov)
- [ ] T-4 [Anaya] Validasi Langflow di Cloud Run dan Tailscale sidecar (30 Nov sampai 1 Des)
- [ ] T-5 [Anaya] min-instances, probe, uptime check, alert, budget
- [ ] T-6 [Anaya] Uji fallback, uji Langflow mati, uji beban ringan, uji rollback
- [ ] T-7 [Anaya] Backup, ekspor, uji pemulihan
- [ ] T-8 [Anaya, Bastian] Pilot di cloud, runbook, gladi demo, rekaman cadangan

## 7. Strategi Uji

Uji kekacauan sederhana (matikan 9router, putuskan Tailscale, matikan Langflow, restart instance), uji beban ringan, simulasi demo end-to-end di cloud.

## 8. Catatan dan Risiko

Risiko utama R-24: masalah cloud baru terlihat di akhir. **Rencana B:** varian `vertex` sebagai jalur utama, demo cadangan dari staging lokal, rekaman layar. Gate G3 (4 Des): setelah code freeze hanya perbaikan kritis.
