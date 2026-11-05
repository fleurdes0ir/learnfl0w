# Image Langflow kustom: versi dipin + flow hasil ekspor dimuat dari repositori.
# Verifikasi bahwa tag versi tersedia di Docker Hub (langflowai/langflow) sebelum build.
ARG LANGFLOW_VERSION=1.12.0
FROM langflowai/langflow:${LANGFLOW_VERSION}

COPY flows /app/flows

# Muat flow dari folder ini saat startup. Bila variabel ini tidak berlaku pada versi terpilih,
# gunakan skrip impor: python langflow/scripts/import_flows.py (lihat langflow/README.md).
ENV LANGFLOW_LOAD_FLOWS_PATH=/app/flows
