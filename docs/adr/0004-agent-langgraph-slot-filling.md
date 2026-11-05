# ADR-0004: Agent LangGraph dengan Alur Slot-Filling

> **Status:** Digantikan oleh [ADR-0010](0010-langflow-dan-fastapi-untuk-lapisan-ai.md)
> **Tanggal:** 2026-10-31 | **Pengambil keputusan:** Anaya

## Konteks

Konsultasi harus hybrid: terarah dan tetap dalam tujuan pemetaan karir, tetapi dengan bahasa natural. Agent memanggil beberapa tool dan state harus bertahan lintas instance serverless.

## Opsi yang Dipertimbangkan

### Opsi A: Graf state LangGraph dengan slot-filling
- Kelebihan: alur eksplisit dan dapat diuji; checkpoint ke PostgreSQL; mudah menambah node.
- Kekurangan: perlu mendesain state dan transisi.

### Opsi B: Agent ReAct bebas
- Kelebihan: cepat dibuat.
- Kekurangan: sulit dikendalikan, rawan keluar topik dan halusinasi, sulit dievaluasi.

## Keputusan

Memakai **LangGraph** dengan node Sapa, KumpulSlot, Ringkas, PilihJalur, BuatRoadmap, Validasi, RoadmapTemplat, Selesai. Checkpoint disimpan dengan `langgraph-checkpoint-postgres`.

## Konsekuensi

- Positif: perilaku dapat diprediksi dan diuji dengan persona sintetis.
- Negatif: perubahan alur percakapan butuh perubahan graf.

## Referensi

- [ai-design.md](../architecture/ai-design.md)
