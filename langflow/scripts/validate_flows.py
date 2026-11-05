"""Validate exported Langflow flows. Standard library only (runs in CI and `make flows-check`).

Checks for every flow with status "exported" in langflow/flows.manifest.json:
  1. both variant files exist (<flow>__router.json, <flow>__vertex.json),
  2. files are valid JSON,
  3. no secrets are embedded (API keys, bearer tokens, private keys),
  4. warns when the two variants differ a lot in structure (parity).
Also fails on files in flows/ that are not listed in the manifest.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLOWS_DIR = ROOT / "flows"
MANIFEST = ROOT / "flows.manifest.json"

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{20,}"),
    re.compile(r"(?i)\"(?:api_key|apikey|password|secret)\"\s*:\s*\"[^\"${][^\"]{6,}\""),
]


def node_types(flow: dict) -> Counter:
    nodes = flow.get("data", {}).get("nodes", [])
    return Counter(n.get("data", {}).get("type", "unknown") for n in nodes)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    variants: list[str] = manifest["variants"]
    errors: list[str] = []
    warnings: list[str] = []
    expected_files: set[str] = set()

    for flow in manifest["flows"]:
        if flow["status"] != "exported":
            continue
        loaded: dict[str, dict] = {}
        for variant in variants:
            filename = f"{flow['name']}__{variant}.json"
            expected_files.add(filename)
            path = FLOWS_DIR / filename
            if not path.exists():
                errors.append(f"missing variant file: {filename}")
                continue
            text = path.read_text(encoding="utf-8")
            try:
                loaded[variant] = json.loads(text)
            except json.JSONDecodeError as exc:
                errors.append(f"{filename}: invalid JSON ({exc})")
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    errors.append(f"{filename}: possible secret matched {pattern.pattern!r}")
        if len(loaded) == len(variants):
            a, b = (node_types(loaded[v]) for v in variants[:2])
            diff = sum(((a - b) + (b - a)).values())
            if diff > 2:
                warnings.append(
                    f"{flow['name']}: variants differ in {diff} node(s); keep them identical except the model component"
                )

    for path in FLOWS_DIR.glob("*.json"):
        if path.name not in expected_files:
            errors.append(f"{path.name}: not listed as exported in flows.manifest.json")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    exported = sum(1 for f in manifest["flows"] if f["status"] == "exported")
    print(f"flows: {exported}/{len(manifest['flows'])} exported, {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
