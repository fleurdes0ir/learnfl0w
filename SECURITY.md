# Kebijakan Keamanan

## Melaporkan Kerentanan

Jangan membuka issue publik untuk masalah keamanan. Hubungi tim LearnFl0w secara langsung (kontak: **isi alamat email tim**) dengan menyertakan:

- deskripsi masalah dan dampaknya,
- langkah untuk mereproduksi,
- versi atau commit yang terdampak.

Kami berusaha menanggapi dalam 3 hari kerja.

## Praktik Dasar

- Rahasia disimpan di Secret Manager (cloud) atau `.env` yang tidak di-commit (lokal).
- `.env.example` hanya berisi nama variabel dan nilai contoh.
- Password disimpan sebagai hash Argon2id; token JWT berumur pendek.
- Pemindaian rahasia berjalan pada pre-commit dan CI.
- Percakapan dan data pribadi tidak dicatat pada log.

## Versi yang Didukung

Hanya cabang `main`.
