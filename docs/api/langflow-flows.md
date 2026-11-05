# Kontrak Flow Langflow

> **Status:** Draft | **Pemilik:** Anaya | **Diperbarui:** 2026-11-03
> Kontrak antara backend FastAPI (`backend/app/ai/langflow/`) dan flow di [`langflow/flows/`](../../langflow/README.md). Ubah dokumen ini lebih dulu sebelum mengubah flow atau klien.

## Konvensi

- Nama flow di Langflow: `<flow>__<variant>`, varian `router` atau `vertex`. Kedua varian punya **antarmuka yang sama**.
- Panggilan: `POST {LANGFLOW_BASE_URL}/api/v1/run/{flow_id}` dengan header `x-api-key` (dan ID token Cloud Run di cloud). Backend mencari `flow_id` dari nama flow.
- Flow **stateless**: seluruh konteks dikirim pada setiap panggilan sebagai JSON pada `input_value`. Keluaran non-stream berupa JSON murni (tanpa teks pembuka atau blok kode).
- Backend memvalidasi semua keluaran dengan Pydantic. Keluaran yang tidak valid dianggap gagal (retry atau fallback).
- Bahasa keluaran untuk pengguna: Indonesia.

## 1. `slot-extractor` (non-stream)

Input (`input_value`, JSON):

```json
{
  "message": "Saya suka ngoprek server dan jaringan",
  "recent_messages": [{ "role": "assistant", "content": "..." }, { "role": "user", "content": "..." }],
  "current_slots": { "interests": ["jaringan"], "hours_per_week": null },
  "stage": "collecting",
  "valid_path_codes": ["CP-01", "CP-02", "CP-03"]
}
```

Output:

```json
{
  "slots_update": { "interests": ["server", "jaringan"], "work_style": "praktik langsung" },
  "intent": "provide_info",
  "chosen_path": null
}
```

- `intent` salah satu dari: `provide_info`, `confirm_summary`, `correct_summary`, `choose_path`, `ask_question`, `off_topic`.
- `chosen_path` hanya terisi bila `intent = choose_path` dan nilainya ada pada `valid_path_codes`; selain itu `null`.
- `slots_update` hanya memuat slot yang berubah: `interests`, `current_skills`, `work_style`, `hours_per_week`, `internship_target`, `budget_pref`.

## 2. `consultant-reply` (stream)

Input:

```json
{
  "stage": "collecting",
  "instruction": { "kind": "ask_slot", "slot": "hours_per_week" },
  "known_slots": { "interests": ["jaringan"] },
  "missing_slots": ["hours_per_week", "internship_target"],
  "recent_messages": [{ "role": "user", "content": "..." }],
  "candidate_paths": []
}
```

- `instruction.kind`: `ask_slot`, `summarize`, `offer_paths`, `answer_question`, `redirect`, `finish`.
- Output: teks Indonesia, ringkas, ramah, satu pertanyaan per giliran. **Tanpa URL.** Referensi katalog hanya lewat tool (`certification_finder`, `material_finder`), dan nama yang disebut harus berasal dari hasil tool.
- Tool dipanggil ke endpoint internal FastAPI: [`internal-tools.openapi.yaml`](internal-tools.openapi.yaml).

## 3. `path-advisor` (non-stream)

Input: `{ "slots": {...}, "candidate_paths": [{ "code": "CP-05", "name": "...", "description": "...", "score": 0.82 }] }`

Output:

```json
{ "paths": [{ "code": "CP-05", "reason": "Kamu menyukai server dan jaringan..." }] }
```

- 1 sampai 3 item; `code` harus berasal dari `candidate_paths`. Backend menolak kode lain.

## 4. `roadmap-builder` (non-stream)

Input (himpunan kandidat **tertutup**):

```json
{
  "career_path_code": "CP-05",
  "slots": { "hours_per_week": 8, "internship_target": "Semester 6", "budget_pref": "free" },
  "template_stages": [{ "order": 1, "title": "Fondasi Linux dan jaringan" }],
  "candidates": {
    "courses": [{ "ref_id": "MK-SO", "name": "Sistem Operasi", "semester": 3, "status": "completed", "grade": "A" }],
    "certifications": [{ "ref_id": "CERT-001", "name": "...", "cost_type": "free", "level": "beginner" }],
    "materials": [{ "ref_id": "MAT-001", "title": "...", "cost_type": "free", "level": "beginner", "format": "video" }]
  },
  "feedback_errors": []
}
```

Output: roadmap JSON sesuai [`roadmap.schema.json`](roadmap.schema.json).

- Hanya boleh memakai `ref_id` dari `candidates`. Matkul `completed` ditandai `completed`, bukan tugas baru.
- `feedback_errors` berisi daftar kesalahan validasi dari percobaan sebelumnya (kosong pada percobaan pertama).

## Perubahan Kontrak

Perubahan input/output mewajibkan: memperbarui dokumen ini, kedua varian flow, model Pydantic di `backend/app/ai/schemas/`, dan menjalankan evaluasi persona.
