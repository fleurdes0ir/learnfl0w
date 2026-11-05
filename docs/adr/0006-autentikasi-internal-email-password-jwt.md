# ADR-0006: Autentikasi Internal (Email, Password, JWT)

> **Status:** Diterima
> **Tanggal:** 2026-10-31 | **Pengambil keputusan:** Anaya

## Konteks

Hanya ada dua peran (Mahasiswa dan Admin). Proyek bersifat akademik dan tidak ingin bergantung pada penyedia identitas pihak ketiga.

## Opsi yang Dipertimbangkan

### Opsi A: Login internal (tabel `users`, hash password, JWT)
- Kelebihan: tanpa ketergantungan eksternal, sederhana, penuh kendali.
- Kekurangan: keamanan password menjadi tanggung jawab tim.

### Opsi B: Google OAuth atau Firebase Auth
- Kelebihan: password dikelola pihak lain.
- Kekurangan: ketergantungan eksternal dan konfigurasi tambahan.

## Keputusan

**Login internal.**
- Password: **Argon2id**, kebijakan minimum panjang password.
- Access token JWT berumur pendek (30 menit); refresh token acak, disimpan sebagai hash, **dirotasi** setiap dipakai.
- Frontend menyimpan access token di memori saja.
- Peran **Admin** ditetapkan lewat allowlist email (`ADMIN_EMAILS`).
- Rate limit pada endpoint login dan registrasi.

## Konsekuensi

- Positif: sederhana dan mandiri.
- Negatif: perlu pengujian keamanan (brute force, token reuse), dan tidak ada pemulihan password otomatis pada V1.
- Tindak lanjut: [SPEC-002](../specs/SPEC-002-auth-dan-rbac.md).
