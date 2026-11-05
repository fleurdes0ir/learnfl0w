# Runbook

> **Status:** Draft | **Pemilik:** Anaya | **Diperbarui:** 2026-10-31
> Perintah memakai variabel `PROJECT_ID` dan `REGION` (lihat [deployment.md](../architecture/deployment.md)). Verifikasi flag terhadap dokumentasi `gcloud` terbaru.

## 1. Kontak dan Akses

| Peran | Siapa | Akses |
|---|---|---|
| Deployment | Anaya | GCP, GitHub, Secret Manager |
| Frontend | Bastian | GitHub, GCP (baca) |
| Pemilik homelab (9router/Tailscale) | rekan | Isi kontak di sini |

## 2. Memeriksa Kesehatan

```bash
curl -s https://BACKEND_URL/healthz
curl -s https://BACKEND_URL/healthz/llm
gcloud run services describe learnfl0w-backend --region $REGION --format="value(status.url)"
gcloud logging read 'resource.type="cloud_run_revision" severity>=ERROR' --limit 20
```

## 3. Rollback Backend atau Frontend

```bash
gcloud run revisions list --service learnfl0w-backend --region $REGION
gcloud run services update-traffic learnfl0w-backend --region $REGION \
  --to-revisions=REVISION_SEBELUMNYA=100
```

Target: selesai dalam 5 menit. Verifikasi dengan `/healthz` setelahnya.

## 4. LLM Utama atau Langflow Bermasalah

Gejala: `/healthz/llm` menunjukkan `router` error atau circuit `open`; respons lambat.

1. Periksa apakah varian `vertex` aktif dan responsif (`/healthz/llm`).
2. Bila perlu paksa varian lain (backend yang memilih varian flow):
   ```bash
   gcloud run services update learnfl0w-backend --region $REGION \
     --update-env-vars LLM_PROVIDER=vertex
   ```
3. Bila Langflow sendiri mati: periksa log dan revisi `learnfl0w-langflow` (memori, startup, koneksi database `langflow`); rollback revisi bila perlu. Selama Langflow mati, roadmap jatuh ke roadmap templat.
4. Hubungi pemilik homelab; periksa 9router dan status node Tailscale (sidecar ada pada layanan Langflow).
5. Setelah pulih, kembalikan `LLM_PROVIDER=router` dan verifikasi `/healthz/llm`.

## 5. Database

- **Backup otomatis:** Cloud SQL harian. Lihat dan pulihkan dari konsol atau `gcloud sql backups list --instance learnfl0w-db`.
- **Ekspor manual sebelum demo:**
  ```bash
  gcloud sql export sql learnfl0w-db gs://BUCKET/backup-$(date +%F).sql --database=learnfl0w
  ```
- **Koneksi habis:** turunkan `max-instances`, periksa pool (`pool_size <= 5`), restart revisi.

## 6. Rotasi Rahasia

1. Buat versi baru secret di Secret Manager.
2. Deploy ulang revisi backend agar memakai versi terbaru.
3. Rotasi `jwt-secret` mengakhiri seluruh sesi pengguna (dapat diterima; informasikan bila perlu).

## 7. Lonjakan Biaya

1. Buka Billing dan periksa layanan penyebab.
2. Turunkan `max-instances`, matikan `min-instances` di luar jam penting.
3. Periksa pemakaian token LLM pada dashboard operasional.

## 8. Insiden Saat Demo

1. Cek `/healthz` dan `/healthz/llm`.
2. Bila LLM bermasalah: paksa `vertex` (bagian 4).
3. Bila revisi terbaru bermasalah: rollback (bagian 3).
4. Bila semuanya gagal: gunakan **rekaman demo cadangan**.

## 9. Pemeliharaan Rutin

| Frekuensi | Tugas |
|---|---|
| Mingguan | Tinjau laporan tautan rusak dan item `needs_review` |
| Mingguan | Periksa biaya dan sisa kredit GCP |
| Per rilis | Jalankan smoke test dan catat di CHANGELOG |
