#!/usr/bin/env python3
"""Validate milestone manifests and every referenced repository path."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "manifests/milestone-1.yml": ["status: complete", "version: 0.1.0"],
    "manifests/milestone-2.yml": ["status: complete", "version: 0.2.0"],
    "manifests/milestone-3.yml": ["status: complete", "version: 0.3.0"],
    "manifests/milestone-4.yml": ["status: complete", "version: 0.4.0"],
    "manifests/playbooks.yml": [
        "playbooks:", "SASD-M2-PRV-001", "SASD-M3-PRV-001", "SASD-M4-DIA-001"
    ],
    "manifests/roles.yml": [
        "roles:", "package_management", "firewall", "certificate_management",
        "resource_diagnostics", "diagnostic_bundle"
    ],
}
errors = []
for relative, markers in REQUIRED.items():
    path = ROOT / relative
    if not path.is_file():
        errors.append(f"missing manifest: {relative}")
        continue
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"{relative}: missing marker {marker!r}")
    for match in re.finditer(r"^\s*- path:\s*(\S+)\s*$", text, re.MULTILINE):
        target = ROOT / match.group(1)
        if not target.exists():
            errors.append(f"{relative}: referenced path does not exist: {match.group(1)}")
if errors:
    print("Manifest validation failed:", file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)
    raise SystemExit(1)
print("Manifest validation passed.")
