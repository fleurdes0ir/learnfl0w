# ADR-0007: Embedding melalui Vertex AI

> **Status:** Diusulkan
> **Tanggal:** 2026-10-31 | **Pengambil keputusan:** Anaya

## Konteks

RAG membutuhkan embedding multibahasa (Indonesia dan Inggris). Layanan berjalan di Cloud Run sehingga ukuran image dan *cold start* penting. Endpoint embedding di 9router tidak dijamin tersedia.

## Opsi yang Dipertimbangkan

### Opsi A: Vertex AI Embeddings
- Kelebihan: tanpa menambah ukuran image, serverless, memakai kredit GCP.
- Kekurangan: butuh jaringan ke API; ketersediaan model per region perlu diperiksa.

### Opsi B: Model lokal (sentence-transformers)
- Kelebihan: tanpa panggilan eksternal.
- Kekurangan: image besar (PyTorch), cold start lambat.

### Opsi C: Model ONNX ringan di dalam container
- Kelebihan: lebih ringan dari Opsi B.
- Kekurangan: tetap menambah ukuran image dan perawatan.

## Keputusan

**Vertex AI** sebagai default (`EMBEDDING_PROVIDER=vertex`); ONNX di dalam container sebagai alternatif bila Vertex tidak tersedia. Embedding katalog dihitung sekali per perubahan dan disimpan; hanya query yang dihitung saat runtime.

## Konsekuensi

- Positif: image ramping, cold start cepat.
- Negatif: model dan dimensi harus dicatat per baris (`embedding_model`) untuk reindex.
