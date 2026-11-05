# ADR-0003: PostgreSQL + pgvector pada Cloud SQL

> **Status:** Diterima
> **Tanggal:** 2026-10-31 | **Pengambil keputusan:** Anaya

## Konteks

Sistem membutuhkan data relasional (pengguna, transkrip, katalog) dan pencarian kemiripan untuk RAG atas katalog kecil (ratusan baris). Database yang sama juga menyimpan state percakapan.

## Opsi yang Dipertimbangkan

### Opsi A: PostgreSQL + pgvector (Cloud SQL)
- Kelebihan: satu penyimpanan untuk relasional, vektor, dan state percakapan; filter metadata via SQL; mudah diakses dari FastAPI dan Langflow.
- Kekurangan: Cloud SQL berjalan terus (biaya tetap kecil).

### Opsi B: Vector DB terpisah (Qdrant, Chroma, Pinecone)
- Kelebihan: fitur vektor lebih kaya.
- Kekurangan: layanan tambahan untuk dikelola dan dibiayai; berlebihan untuk data sekecil ini.

### Opsi C: Firestore dengan vector search
- Kelebihan: serverless penuh.
- Kekurangan: model dokumen kurang cocok untuk relasi katalog dan transkrip.

## Keputusan

**PostgreSQL 16 dengan ekstensi pgvector pada Cloud SQL.** Pencarian eksak cukup untuk data kecil; indeks HNSW ditambahkan hanya bila terbukti perlu.

## Konsekuensi

- Positif: arsitektur sederhana, transaksi konsisten.
- Negatif: pool koneksi harus kecil dan `max-instances` dibatasi.
