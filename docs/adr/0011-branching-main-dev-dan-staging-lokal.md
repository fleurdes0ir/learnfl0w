# ADR-0011: Branching `main` dan `dev` dengan Staging Lokal

> **Status:** Diterima
> **Tanggal:** 2026-11-03 | **Pengambil keputusan:** Anaya, Bastian

## Konteks

Tim dua orang bekerja paralel pada backend dan frontend. Staging dilakukan di lokal, dan deployment cloud hanya di akhir. Dibutuhkan alur cabang yang umum di industri dan mudah ditegakkan CI.

## Opsi yang Dipertimbangkan

### Opsi A: `main` + `dev` + cabang kerja `feat/`, `fix/`, `chore/`
- Kelebihan: `dev` menjadi tempat integrasi dan staging lokal; `main` hanya berisi kode yang siap rilis dan menjadi sumber deployment; nama cabang jelas.
- Kekurangan: satu PR tambahan untuk rilis (`dev` ke `main`).

### Opsi B: Trunk-based (hanya `main`)
- Kelebihan: paling sederhana.
- Kekurangan: tidak ada tempat integrasi atau staging yang stabil; `main` mudah terganggu.

## Keputusan

**Opsi A.** `main` dan `dev` terproteksi; cabang kerja dibuat dari `dev` dan digabung dengan squash; rilis lewat PR `dev` ke `main` (merge commit) dan diberi tag `v*`. Perbaikan kritis memakai `fix/` dari `main`, lalu digabung balik ke `dev`. CI (`branch-policy`) menolak nama cabang atau target yang salah.

## Konsekuensi

- Positif: alur jelas, staging lokal punya cabang acuan, riwayat rilis rapi.
- Negatif: disiplin back-merge setelah hotfix.
- Tindak lanjut: [git-workflow.md](../engineering/git-workflow.md), `branch-policy.yml`.
