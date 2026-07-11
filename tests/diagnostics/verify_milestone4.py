#!/usr/bin/env python3
"""Prepare and verify deterministic Milestone 4 diagnostic acceptance fixtures.

This helper deliberately keeps JSON/tar verification out of shell heredocs so the
acceptance script remains reproducible in local shells and CI runners.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tarfile
from pathlib import Path
from typing import Any

RUN_ID = "milestone4-localhost"
EXPECTED_SCHEMAS = {
    "resources.json": "sasd.diagnostics.resources.v1",
    "services.json": "sasd.diagnostics.services.v1",
    "packages.json": "sasd.diagnostics.packages.v1",
    "network.json": "sasd.diagnostics.network.v1",
    "certificates.json": "sasd.diagnostics.certificates.v1",
    "summary.json": "sasd.diagnostics.summary.v1",
}


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AssertionError(f"Required JSON file is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AssertionError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(value, dict):
        raise AssertionError(f"Expected a JSON object in {path}")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare(root: Path) -> None:
    host_dir = root / "reports" / "diagnostics" / RUN_ID / "localhost"
    host_dir.mkdir(parents=True, exist_ok=True)
    fixture = {
        "schema": "sasd.diagnostics.redaction-fixture.v1",
        "authorization": "must-not-be-bundled",
        "nested": {
            "api_token": "must-not-be-bundled",
            "ordinary_value": "preserved",
        },
    }
    fixture_path = host_dir / "redaction-fixture.json"
    fixture_path.write_text(
        json.dumps(fixture, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Prepared redaction fixture: {fixture_path}")


def verify(root: Path) -> None:
    host_dir = root / "reports" / "diagnostics" / RUN_ID / "localhost"

    for filename, expected_schema in EXPECTED_SCHEMAS.items():
        path = host_dir / filename
        payload = load_json(path)
        actual_schema = payload.get("schema")
        if actual_schema != expected_schema:
            raise AssertionError(
                f"Unexpected schema in {path}: {actual_schema!r}; "
                f"expected {expected_schema!r}"
            )

    certificate_report = load_json(host_dir / "certificates.json")
    certificate_files = certificate_report.get("files")
    if not isinstance(certificate_files, list) or not certificate_files:
        raise AssertionError("Certificate report contains no file results")
    first_certificate = certificate_files[0]
    if not isinstance(first_certificate, dict) or first_certificate.get("ok") is not True:
        raise AssertionError("Certificate fixture was not decoded successfully")

    bundle_dir = root / "diagnostic-bundles"
    archive = bundle_dir / f"sasd-diagnostic-bundle-{RUN_ID}.tar.gz"
    external_manifest = bundle_dir / f"sasd-diagnostic-bundle-{RUN_ID}.manifest.json"
    bundle_result_path = (
        root / "reports" / "diagnostics" / "bundles" / f"{RUN_ID}.json"
    )

    for required_path in (archive, external_manifest, bundle_result_path):
        if not required_path.is_file():
            raise AssertionError(f"Required bundle artifact is missing: {required_path}")

    manifest = load_json(external_manifest)
    result = load_json(bundle_result_path)
    if result.get("schema") != "sasd.diagnostics.bundle.v1":
        raise AssertionError("Unexpected diagnostic bundle result schema")

    manifest_files = manifest.get("files")
    if not isinstance(manifest_files, list) or len(manifest_files) < len(EXPECTED_SCHEMAS):
        raise AssertionError("Bundle manifest contains too few files")

    archive_names: set[str] = set()
    canary_text: str | None = None
    with tarfile.open(archive, mode="r:gz") as tar:
        for member in tar.getmembers():
            if member.issym() or member.islnk():
                raise AssertionError(f"Archive contains a link member: {member.name}")
            archive_names.add(member.name)
            if member.name.endswith("/redaction-fixture.json"):
                extracted = tar.extractfile(member)
                if extracted is None:
                    raise AssertionError("Could not read bundled redaction fixture")
                canary_text = extracted.read().decode("utf-8")

    if canary_text is None:
        raise AssertionError("Redaction fixture is missing from the archive")
    if "must-not-be-bundled" in canary_text:
        raise AssertionError("Sensitive canary data was included in the archive")
    if "[REDACTED]" not in canary_text:
        raise AssertionError("Expected redaction marker is missing from the archive")
    if "preserved" not in canary_text:
        raise AssertionError("Ordinary fixture data was not preserved")

    expected_archive_sha = result.get("archive_sha256")
    actual_archive_sha = sha256_file(archive)
    if expected_archive_sha != actual_archive_sha:
        raise AssertionError(
            "Archive checksum does not match the bundle result: "
            f"{expected_archive_sha!r} != {actual_archive_sha!r}"
        )

    manifest_archive_name = manifest.get("archive")
    if manifest_archive_name and Path(str(manifest_archive_name)).name != archive.name:
        raise AssertionError("External manifest references an unexpected archive")

    print(
        "Validated Milestone 4 diagnostics: "
        f"{len(EXPECTED_SCHEMAS)} report schemas, "
        f"{len(manifest_files)} bundled files, "
        f"{len(archive_names)} archive members, checksum {actual_archive_sha}."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "verify"))
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (defaults to the current working directory).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.repository_root.resolve()
    try:
        if args.action == "prepare":
            prepare(root)
        else:
            verify(root)
    except AssertionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
