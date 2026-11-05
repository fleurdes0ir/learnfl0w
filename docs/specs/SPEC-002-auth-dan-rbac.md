# SPEC-002: Autentikasi dan RBAC

> **Status:** Siap
> **Pemilik:** Anaya (backend), Bastian (UI) | **Milestone:** M1 | **Prioritas:** Must
> **PRD:** FR-AUTH-01 sampai 05, NFR-S-02, NFR-S-11 | **ADR terkait:** ADR-0006

## 1. Konteks

Dua peran: Mahasiswa dan Admin. Login internal dengan email dan password, token JWT berumur pendek, dan refresh token berotasi.

## 2. Lingkup

**Dalam lingkup:** registrasi, login, refresh, logout, hapus akun, RBAC pada setiap endpoint, penetapan Admin via `ADMIN_EMAILS`, rate limit login, halaman login dan registrasi.

**Di luar lingkup:** pemulihan password otomatis, login sosial, verifikasi email.

## 3. Persyaratan

| ID | Persyaratan |
|---|---|
| R-1 | Registrasi dengan email unik dan password (minimal 10 karakter); password di-hash Argon2id |
| R-2 | Login mengembalikan access token (30 menit) dan refresh token (7 hari) |
| R-3 | Refresh **merotasi** token: token lama dicabut; pemakaian ulang token lama mencabut seluruh sesi pengguna |
| R-4 | Email yang ada di `ADMIN_EMAILS` mendapat peran `admin`; selain itu `student` |
| R-5 | Setiap endpoint memeriksa peran di backend; tidak bergantung pada UI |
| R-6 | Rate limit: maksimal 5 percobaan login gagal per 15 menit per kombinasi email dan IP |
| R-7 | `DELETE /me` menghapus akun dan seluruh data terkait |
| R-8 | `password_hash` dan token tidak pernah muncul pada log atau respons selain yang semestinya |

## 4. Kontrak

- Endpoint: `register`, `login`, `refresh`, `logout`, `getMe`, `deleteMe`.
- DB: `users`, `auth_refresh_tokens`.
- UI: halaman `/login`, `/register`, penjaga rute per peran, penyimpanan token di memori.

## 5. Acceptance Criteria

- [ ] AC-1: Given email baru, When registrasi dengan password valid, Then akun dibuat dan password tersimpan sebagai hash Argon2id.
- [ ] AC-2: Given kredensial benar, When login, Then menerima token dan `role` sesuai.
- [ ] AC-3: Given mahasiswa, When memanggil endpoint admin, Then 403.
- [ ] AC-4: Given refresh token dipakai dua kali, When pemakaian kedua, Then 401 dan seluruh refresh token pengguna dicabut.
- [ ] AC-5: Given 5 login gagal beruntun, When percobaan ke-6, Then 429.
- [ ] AC-6: Given akun dihapus, When data diperiksa, Then profil, transkrip, sesi, dan roadmap ikut terhapus.

## 6. Tugas

- [ ] T-1 [Anaya] Model `users`, `auth_refresh_tokens`, migrasi
- [ ] T-2 [Anaya] Hash password, JWT, dependensi `get_current_user` dan `require_role`
- [ ] T-3 [Anaya] Endpoint auth, rate limit, hapus akun
- [ ] T-4 [Anaya] Test keamanan (token reuse, brute force, akses lintas peran)
- [ ] T-5 [Bastian] Halaman login/registrasi, klien API dengan refresh otomatis, penjaga rute

## 7. Strategi Uji

Integrasi pada PostgreSQL asli; uji negatif untuk setiap endpoint (tanpa token, token kedaluwarsa, peran salah).

## 8. Catatan dan Risiko

Secret JWT berasal dari Secret Manager. Rotasi secret menyebabkan semua sesi berakhir (dapat diterima).
