"""Fallback: import exported flows into a running Langflow through its API.

Use only if loading flows from LANGFLOW_LOAD_FLOWS_PATH is not available in the pinned version.
Usage: LANGFLOW_BASE_URL=http://localhost:7860 LANGFLOW_API_KEY=... python import_flows.py
Endpoint and payload are taken from the Langflow API docs (create flow); verify against the pinned version.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

FLOWS_DIR = Path(__file__).resolve().parents[1] / "flows"


def main() -> int:
    base = os.environ.get("LANGFLOW_BASE_URL", "http://localhost:7860").rstrip("/")
    key = os.environ.get("LANGFLOW_API_KEY", "")
    if not key:
        print("LANGFLOW_API_KEY is required")
        return 1
    failures = 0
    for path in sorted(FLOWS_DIR.glob("*.json")):
        flow = json.loads(path.read_text(encoding="utf-8"))
        flow["name"] = path.stem  # <flow>__<variant>
        req = urllib.request.Request(
            f"{base}/api/v1/flows/",
            data=json.dumps(flow).encode("utf-8"),
            headers={"Content-Type": "application/json", "x-api-key": key},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                print(f"imported {path.name}: HTTP {resp.status}")
        except Exception as exc:  # noqa: BLE001 - report and continue
            failures += 1
            print(f"FAILED   {path.name}: {exc}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
