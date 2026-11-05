# Sidecar Tailscale

Tempat konfigurasi sidecar Tailscale (userspace networking) untuk layanan backend di Cloud Run.

Status: **belum diimplementasikan**. Dikerjakan pada spike Minggu 1 (lihat [SPEC-001](../../docs/specs/SPEC-001-platform-skeleton-dan-cicd.md) T-6 dan [ADR-0005](../../docs/adr/0005-llm-gateway-9router-dengan-fallback-vertex.md)).

Hal yang perlu dibuktikan:
- sidecar tetap hidup dengan CPU always allocated,
- auth key ephemeral bertag dari Secret Manager berfungsi,
- panggilan ke 9router lewat proxy lokal stabil dan latensinya dapat diterima,
- node ephemeral tidak menumpuk di tailnet.
Bila gagal, Vertex AI menjadi jalur LLM utama.
