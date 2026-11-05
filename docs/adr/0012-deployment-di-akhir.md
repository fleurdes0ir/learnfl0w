# ADR-0012: Deployment Cloud di Akhir, Staging di Lokal

> **Status:** Diterima
> **Tanggal:** 2026-11-03 | **Pengambil keputusan:** Anaya, Bastian
> **Menggantikan:** keputusan *walking skeleton* deploy pada Minggu 1

## Konteks

Tim ingin fokus pada fitur dan kualitas AI lebih dulu, menghemat kredit GCP, dan menghindari pekerjaan deploy berulang saat arsitektur AI berubah ke Langflow.

## Opsi yang Dipertimbangkan

### Opsi A: Deployment di akhir (28 Nov sampai 3 Des), staging di lokal
- Kelebihan: fokus fitur; kredit hemat; satu kali deploy.
- Kekurangan: masalah cloud (IAM, jaringan, memori Langflow, Tailscale) baru terlihat di akhir.

### Opsi B: Deploy kerangka sejak Minggu 1
- Kelebihan: risiko cloud terlihat dini.
- Kekurangan: menghabiskan kredit lebih awal; pekerjaan berulang saat arsitektur berubah.

## Keputusan

**Opsi A**, dengan mitigasi risiko: staging lokal yang meniru cloud (`make staging-up`, `make smoke`), dokumen deployment dan runbook disiapkan sejak awal, jendela deployment 6 hari ditambah buffer 3 hari, perkiraan sumber daya Langflow dari `docker stats`, dan **rencana B** (varian Vertex AI sebagai jalur utama, demo cadangan dari staging lokal, rekaman layar).

## Konsekuensi

- Positif: kecepatan pengembangan fitur, biaya terkendali.
- Negatif: risiko R-24 (masalah cloud terlambat terlihat); pemotongan scope dilakukan pada fitur Should, bukan jendela deployment.
- Tindak lanjut: [deployment.md](../architecture/deployment.md), PRD 20.1.
