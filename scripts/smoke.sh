#!/usr/bin/env bash
# Smoke test untuk staging lokal atau cloud.
# Contoh lokal : bash scripts/smoke.sh
# Contoh cloud : BACKEND_URL=https://... FRONTEND_URL=https://... SKIP_LANGFLOW=1 bash scripts/smoke.sh
set -euo pipefail

BACKEND_URL="${BACKEND_URL:-http://localhost:8080}"
FRONTEND_URL="${FRONTEND_URL:-http://localhost:3000}"
LANGFLOW_URL="${LANGFLOW_URL:-http://localhost:7860}"

check() {
  local name="$1" url="$2"
  for _ in $(seq 1 20); do
    if curl -fsS "$url" > /dev/null; then echo "ok    $name"; return 0; fi
    sleep 3
  done
  echo "FAIL  $name ($url)"
  return 1
}

check backend  "$BACKEND_URL/healthz"
check frontend "$FRONTEND_URL/api/health"
if [ "${SKIP_LANGFLOW:-0}" != "1" ]; then
  check langflow "$LANGFLOW_URL/health_check"
fi
echo "--- status jalur LLM ---"
curl -fsS "$BACKEND_URL/healthz/llm" || echo "(healthz/llm belum tersedia)"
echo
echo "smoke test selesai"
