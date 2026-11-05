# SPEC-006: Saran Jalur, Generasi Roadmap, dan Guardrails

> **Status:** Siap
> **Pemilik:** Anaya | **Milestone:** M3 | **Prioritas:** Must
> **PRD:** FR-MAP-01, 03 sampai 06, 08, 12; AC-R-01 sampai AC-R-10 | **ADR terkait:** ADR-0008, ADR-0010

## 1. Konteks

Setelah ringkasan disetujui, sistem menawarkan jalur lalu membuat roadmap berstruktur yang logis dan sepenuhnya bersumber dari katalog. FastAPI menyiapkan **himpunan kandidat tertutup**; flow Langflow hanya memilih dan mengurutkan.

## 2. Lingkup

**Dalam lingkup:** peringkat jalur kandidat, flow `path-advisor` dan `roadmap-builder` (dua varian), penyusun kandidat tertutup, validator (skema, graf, ID, tautan, personalisasi), retry, roadmap templat cadangan, penyimpanan dan versi roadmap, output guardrails.

**Di luar lingkup:** tampilan (SPEC-007).

## 3. Persyaratan

| ID | Persyaratan |
|---|---|
| R-1 | Jalur kandidat diperingkat FastAPI; `path-advisor` mengembalikan 1 sampai 3 `{code, reason}` dan setiap `code` diverifikasi terhadap daftar baku |
| R-2 | Kandidat roadmap (matkul, sertifikasi, materi) disiapkan FastAPI; hanya item `active` dan sesuai filter biaya serta tingkat |
| R-3 | `roadmap-builder` hanya boleh memakai `ref_id` dari kandidat; keluaran memenuhi `docs/api/roadmap.schema.json` dan model Pydantic |
| R-4 | Setiap `ref_id` ada di katalog dan `status = active`; node tidak valid dibuang; URL hanya dari katalog |
| R-5 | Graf berupa DAG, tanpa node yatim, urutan fondasi ke lanjutan |
| R-6 | Matkul yang sudah ditempuh berstatus `completed` dan bukan tugas baru |
| R-7 | Setiap tahap punya minimal 1 materi; roadmap punya minimal 1 sertifikasi sesuai `budget_pref` |
| R-8 | Estimasi waktu realistis terhadap `hours_per_week` dan `internship_target` |
| R-9 | Validasi gagal: retry maksimal 2 kali dengan `feedback_errors`, lalu roadmap templat |
| R-10 | Roadmap berversi; `source` bernilai `ai` atau `template` |
| R-11 | Tidak ada klaim gaji, lowongan, atau kelulusan |

## 4. Kontrak

- Endpoint: `listRoadmaps`, `getRoadmap`, event SSE `roadmap_ready`.
- Flow: [langflow-flows.md](../api/langflow-flows.md) (`path-advisor`, `roadmap-builder`). Skema: `docs/api/roadmap.schema.json`.
- DB: `roadmaps`, `career_paths.template_stages`, `ai_runs`.

## 5. Acceptance Criteria

- [ ] AC-1: Given persona lengkap, When roadmap dibuat, Then memenuhi seluruh AC-R pada PRD 15.1.
- [ ] AC-2: Given flow mengembalikan `ref_id` di luar kandidat, When validasi, Then node dibuang dan kejadian dicatat.
- [ ] AC-3: Given flow gagal dua kali, When validasi, Then roadmap templat dihasilkan dan `source = template`.
- [ ] AC-4: Given `budget_pref = free`, When roadmap dibuat, Then tidak ada sertifikasi berbayar tanpa penanda jelas.
- [ ] AC-5: Given pengujian waktu, When diukur, Then roadmap selesai ≤ 40 detik (P95).
- [ ] AC-6: Given Langflow tidak tersedia, When roadmap diminta, Then roadmap templat dihasilkan dengan keterangan "versi dasar".

## 6. Tugas

- [ ] T-1 [Anaya] Model Pydantic dan JSON Schema roadmap
- [ ] T-2 [Anaya] Templat per jalur (`template_stages`) untuk 11 jalur
- [ ] T-3 [Anaya] Peringkat jalur dan penyusun kandidat tertutup
- [ ] T-4 [Anaya] Flow `path-advisor` dan `roadmap-builder` (dua varian), ekspor
- [ ] T-5 [Anaya] Validator (skema, DAG, ID, tautan, personalisasi)
- [ ] T-6 [Anaya] Retry, fallback templat, penyimpanan versi
- [ ] T-7 [Anaya] Evaluasi pada 20 persona (grounding 100%, skema ≥ 98%)

## 7. Strategi Uji

Unit untuk setiap aturan validator dengan kasus buruk (siklus, node yatim, ID palsu, URL palsu, matkul sudah lulus); evaluasi persona; uji fallback dan Langflow mati.

## 8. Catatan dan Risiko

Templat jalur dikurasi manual dan menjadi jaring pengaman utama.
