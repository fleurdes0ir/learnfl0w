## Cabang

- Dari: `feat/` | `fix/` | `chore/` (atau `dev` untuk rilis)
- Ke: `dev` (rilis: `main`; perbaikan kritis: `main`)

## Ringkasan

<!-- Apa yang berubah dan mengapa, dalam 2 sampai 4 kalimat. -->

## Terkait

- Spec / Issue: SPEC-XXX, #nomor
- ADR (bila ada): ADR-XXXX

## Jenis Perubahan

- [ ] feat
- [ ] fix
- [ ] chore (tooling, dependensi, CI, dokumentasi, refactor)

## Checklist

- [ ] `make check` hijau
- [ ] Test ditambahkan atau diperbarui
- [ ] `docs/api/openapi.yaml` diperbarui bila endpoint berubah
- [ ] Flow Langflow diekspor dan evaluasi AI dijalankan bila flow berubah
- [ ] Dokumen terkait (spec, ADR, arsitektur) diperbarui
- [ ] Migrasi database disertakan bila skema berubah
- [ ] Tidak ada rahasia, data pribadi, atau URL katalog hardcoded
- [ ] Dependensi baru dijelaskan alasannya (bila ada)

## Cara Menguji

<!-- Langkah untuk memverifikasi, termasuk `make staging-up` / `make smoke` bila relevan. Sertakan tangkapan layar untuk perubahan UI. -->

## Risiko dan Rollback

<!-- Dampak yang mungkin terjadi dan cara mengembalikan. -->
