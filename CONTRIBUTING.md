# Panduan Kontribusi

Dokumen ini berlaku untuk seluruh anggota tim dan juga untuk AI coding agent.

## Prinsip

1. **Spec-first:** setiap fitur punya spec di `docs/specs/`. Tidak ada kode fitur tanpa spec.
2. **Perubahan kecil:** satu Pull Request mengerjakan satu tugas dalam spec.
3. **Docs sebagai kode:** bila perilaku berubah, dokumen ikut diperbarui pada PR yang sama.
4. **Hijau sebelum merge:** `make check` dan CI harus lolos.
5. **Staging di lokal, deployment di akhir:** `dev` dijalankan sebagai staging lokal; deployment cloud hanya pada jendela akhir (28 Nov sampai 3 Des 2026).

## Strategi Cabang

Dua cabang permanen: **`main`** (rilis dan sumber deployment) dan **`dev`** (integrasi dan staging lokal). Pekerjaan dilakukan di cabang pendek **`feat/`**, **`fix/`**, dan **`chore/`**.

| Cabang | Fungsi | Dari | Ke |
|---|---|---|---|
| `main` | Rilis dan demo | | |
| `dev` | Integrasi dan staging lokal | `main` | `main` |
| `feat/<topik>` | Fitur baru | `dev` | `dev` |
| `fix/<topik>` | Perbaikan bug | `dev` (kritis: `main`) | `dev` (kritis: `main`, lalu `dev`) |
| `chore/<topik>` | Tooling, dependensi, CI, dokumentasi, refactor | `dev` | `dev` |

Perubahan dokumentasi memakai `chore/docs-<topik>` dengan commit bertipe `docs:`.

## Alur Kerja

1. `git switch dev && git pull`.
2. Buat cabang kerja: `feat/spec-005-dialog-manager`.
3. Kerjakan dengan commit kecil (Conventional Commits). Jalankan `make check`.
4. Buka Pull Request **ke `dev`** dengan templat yang tersedia.
5. Minta review silang (Anaya meninjau PR Bastian, dan sebaliknya).
6. Squash merge ke `dev`. Cabang dihapus.
7. Jalankan `make staging-up` lalu `make smoke` untuk memeriksa `dev` secara terpadu.
8. Rilis: PR `dev` ke `main` (merge commit) setelah gate, lalu beri tag `v*`.

Detail: [docs/engineering/git-workflow.md](docs/engineering/git-workflow.md). CI menolak PR dengan nama cabang atau target yang salah.

## Conventional Commits

Format: `<type>(<scope>): <deskripsi singkat, imperatif>`

```text
feat(chat): add dialog manager state machine
fix(roadmap): reject nodes with unknown ref_id
docs(adr): record decision on langflow
chore(ci): validate langflow flows
```

Type: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `perf`.
Scope yang dianjurkan: `auth`, `profile`, `chat`, `roadmap`, `catalog`, `admin`, `ai`, `flows`, `ui`, `infra`, `ci`, `docs`.

## Checklist Pull Request

- [ ] Terkait spec atau issue (cantumkan ID)
- [ ] Cabang berawalan `feat/`, `fix/`, atau `chore/`, dan target PR benar
- [ ] `make check` hijau
- [ ] Test ditambahkan atau diperbarui
- [ ] Kontrak API (`docs/api/openapi.yaml`) diperbarui bila endpoint berubah
- [ ] Flow Langflow diekspor ke `langflow/flows/` dan evaluasi AI dijalankan bila flow berubah
- [ ] Dokumen terkait (spec, ADR, arsitektur) diperbarui
- [ ] Tidak ada rahasia, data pribadi, atau URL katalog hardcoded
- [ ] Migrasi database disertakan bila skema berubah

## Standar Kode

Lihat [docs/engineering/coding-standards.md](docs/engineering/coding-standards.md) dan [docs/engineering/testing-strategy.md](docs/engineering/testing-strategy.md).

## Bekerja dengan AI Agent (OpenCode)

- Agent membaca `AGENTS.md`; jangan menyalin isi PRD ke sana.
- Beri agent satu spec dan satu tugas per sesi. Skill proyek ada di `.opencode/skills/` (daftar dan panduan hemat token: [opencode-setup](docs/engineering/opencode-setup.md)).
- Gunakan agent **Plan** untuk rencana, tinjau rencananya, baru jalankan **Build**.
- Tinjau setiap diff seperti kode rekan tim. Pengirim PR bertanggung jawab atas isinya.
- Jangan menempelkan rahasia (API key, token, password) ke prompt.

## Melaporkan Masalah Keamanan

Lihat [SECURITY.md](SECURITY.md).
