# ADR-0001: Satu Monorepo untuk Frontend, Backend, dan Infra

> **Status:** Diterima
> **Tanggal:** 2026-10-31 | **Pengambil keputusan:** Anaya, Bastian

## Konteks

Tim terdiri dari dua orang dan bekerja paralel pada frontend dan backend dengan kontrak API bersama. Pengembangan banyak dibantu AI coding agent yang membutuhkan konteks lintas bagian.

## Faktor Keputusan

- Kontrak API dan dokumen harus selalu sinkron dengan kode.
- Agent perlu melihat spec, kontrak, dan kode dalam satu workspace.
- Overhead pengelolaan repositori harus minimal.

## Opsi yang Dipertimbangkan

### Opsi A: Monorepo
- Kelebihan: satu PR dapat mengubah kontrak, backend, dan frontend; konteks agent lengkap; satu pengaturan CI.
- Kekurangan: pipeline perlu dipisah per layanan agar tidak membangun semuanya setiap saat.

### Opsi B: Dua repositori (frontend dan backend)
- Kelebihan: pemisahan akses jelas.
- Kekurangan: kontrak API mudah menyimpang; dokumen terpecah; dua pengaturan CI.

## Keputusan

Memakai **monorepo** dengan folder `backend/`, `frontend/`, `infra/`, `docs/`, dan `data/`. Workflow CI memakai filter path agar hanya layanan yang berubah yang diuji dan dibangun.

## Konsekuensi

- Positif: konsistensi kontrak, onboarding sederhana.
- Negatif: perlu disiplin filter path pada CI dan kepemilikan kode (`CODEOWNERS`).
