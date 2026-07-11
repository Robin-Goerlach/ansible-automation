#!/usr/bin/env python3
"""Check repository-relative Markdown links without network access."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
errors = []
for document in sorted(ROOT.rglob("*.md")):
    if any(part in {".git", ".venv", "artifacts", "reports"} for part in document.parts):
        continue
    text = document.read_text(encoding="utf-8")
    for raw_target in LINK.findall(text):
        target = raw_target.strip().split("#", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        resolved = (document.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{document.relative_to(ROOT)}: link leaves repository: {target}")
            continue
        if not resolved.exists():
            errors.append(f"{document.relative_to(ROOT)}: missing target: {target}")
if errors:
    print("Documentation link validation failed:", file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)
    raise SystemExit(1)
print("Documentation link validation passed.")
