# Evaluasi dan Uji AI

| Berkas | Isi |
|---|---|
| `test_dialog.py` | Transisi dialog manager (logika murni, tanpa LLM) |
| `test_circuit.py` | Circuit breaker |
| `test_langflow_client.py` | Klien Langflow dengan `httpx.MockTransport` (fallback, circuit) |
| `personas/*.json` | Persona uji untuk evaluasi (target 20) |

Evaluasi persona memeriksa validitas skema, grounding terhadap katalog, aturan graf, dan ketahanan guardrails. Lihat [ai-design.md](../../../docs/architecture/ai-design.md) bagian 9.

Jalankan: `pytest tests/ai -q` (klien dan flow palsu). `RUN_LIVE_LLM=1 pytest tests/ai -q` memanggil Langflow sungguhan (berbiaya).
