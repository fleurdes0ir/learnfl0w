# Indeks Dokumentasi

> **Status:** Aktif | **Pemilik:** LearnFl0w | **Diperbarui:** 2026-10-31

Semua dokumentasi proyek berada di folder ini, dikelompokkan per topik. File komunitas (`README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`) tetap di root repositori.

## Peta Dokumen

| Folder | Isi | Untuk siapa |
|---|---|---|
| [`product/`](product/PRD.md) | PRD: visi, scope, kebutuhan fungsional dan non-fungsional | Semua |
| [`architecture/`](architecture/overview.md) | Gambaran sistem, model data, desain AI, deployment | Developer |
| [`adr/`](adr/0000-template.md) | Architecture Decision Record: alasan keputusan teknis | Developer |
| [`specs/`](specs/README.md) | Spec per fitur dengan acceptance criteria dan tugas | Developer, AI agent |
| [`api/`](api/openapi.yaml) | Kontrak API (OpenAPI), JSON Schema roadmap, kontrak flow Langflow, API tool internal | Backend, Frontend, AI |
| [`engineering/`](engineering/coding-standards.md) | Standar kode, strategi test, alur Git, setup OpenCode dan skills ([opencode-setup](engineering/opencode-setup.md)) | Developer, AI agent |
| [`operations/`](operations/runbook.md) | Runbook, checklist demo | Tim deployment |

## Urutan Membaca (Anggota Baru)

1. [PRD](product/PRD.md) bagian 1 sampai 3
2. [Gambaran arsitektur](architecture/overview.md)
3. [Daftar spec](specs/README.md)
4. [Standar kode](engineering/coding-standards.md)

## Konvensi Dokumen

- **Format:** Markdown, satu topik per file, nama file `kebab-case`.
- **Header:** setiap dokumen diawali baris `Status | Pemilik | Diperbarui`.
- **Status:** `Draft`, `Aktif`, `Usang`. ADR memakai `Diusulkan`, `Diterima`, `Digantikan`.
- **Diagram:** ditulis sebagai kode (Mermaid), bukan gambar.
- **Tautan:** relatif terhadap file, bukan URL absolut.
- **Bahasa:** `AGENTS.md`, `.opencode/`, dan `docs/engineering/` dalam bahasa Inggris (dibaca oleh agent dan terkait kode). Dokumen lain dalam bahasa Indonesia.
- **Sumber kebenaran:**
  - perilaku produk: PRD dan spec,
  - kontrak HTTP: `api/openapi.yaml`,
  - alasan keputusan: ADR.
  Bila ada konflik, perbaiki dokumen yang salah pada PR yang sama.
