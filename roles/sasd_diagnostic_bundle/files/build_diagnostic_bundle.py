#!/usr/bin/env python3
"""Create a sanitized, checksummed diagnostics archive on the control node."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def sanitize(value: Any, patterns: list[str]) -> Any:
    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        for key, child in value.items():
            lowered = key.lower()
            sanitized[key] = '[REDACTED]' if any(pattern in lowered for pattern in patterns) else sanitize(child, patterns)
        return sanitized
    if isinstance(value, list):
        return [sanitize(item, patterns) for item in value]
    return value


def main() -> None:
    repository = Path(os.environ['SASD_BUNDLE_REPOSITORY_ROOT']).resolve()
    run_id = os.environ['SASD_BUNDLE_RUN_ID']
    source_root = repository / os.environ['SASD_BUNDLE_SOURCE_ROOT'] / run_id
    output_root = repository / os.environ['SASD_BUNDLE_OUTPUT_ROOT']
    maximum = int(os.environ.get('SASD_BUNDLE_MAXIMUM_FILE_BYTES', '5242880'))
    result_root = repository / os.environ.get('SASD_BUNDLE_RESULT_ROOT', 'reports/diagnostics/bundles')
    patterns = [item.lower() for item in json.loads(os.environ.get('SASD_BUNDLE_REDACTED_KEY_PATTERNS', '[]'))]
    if not source_root.is_dir():
        raise SystemExit(f'Diagnostics run directory does not exist: {source_root}')
    output_root.mkdir(parents=True, exist_ok=True, mode=0o750)
    result_root.mkdir(parents=True, exist_ok=True, mode=0o750)
    archive_path = output_root / f'sasd-diagnostic-bundle-{run_id}.tar.gz'
    manifest_path = output_root / f'sasd-diagnostic-bundle-{run_id}.manifest.json'
    warnings: list[str] = []

    with tempfile.TemporaryDirectory(prefix='sasd-diagnostic-bundle-') as temporary:
        stage_root = Path(temporary) / f'sasd-diagnostic-bundle-{run_id}'
        stage_root.mkdir(mode=0o750)
        for source in sorted(source_root.rglob('*')):
            relative = source.relative_to(source_root)
            if source.is_symlink():
                warnings.append(f'Skipped symbolic link: {relative}')
                continue
            if source.is_dir():
                (stage_root / relative).mkdir(parents=True, exist_ok=True, mode=0o750)
                continue
            if not source.is_file():
                warnings.append(f'Skipped non-regular file: {relative}')
                continue
            if source.stat().st_size > maximum:
                warnings.append(f'Skipped oversized file: {relative}')
                continue
            destination = stage_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True, mode=0o750)
            if source.suffix.lower() == '.json':
                try:
                    payload = json.loads(source.read_text(encoding='utf-8'))
                    destination.write_text(
                        json.dumps(sanitize(payload, patterns), indent=2, sort_keys=True) + '\n',
                        encoding='utf-8',
                    )
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    warnings.append(f'Skipped invalid JSON file {relative}: {exc}')
                    continue
            else:
                shutil.copyfile(source, destination)
            destination.chmod(0o640)

        files = []
        for path in sorted(stage_root.rglob('*')):
            if path.is_file():
                files.append({
                    'path': str(path.relative_to(stage_root)),
                    'size_bytes': path.stat().st_size,
                    'sha256': sha256(path),
                })
        manifest = {
            'schema': 'sasd.diagnostics.bundle.v1',
            'run_id': run_id,
            'created_at_utc': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'files': files,
            'warnings': warnings,
            'review_required_before_external_sharing': True,
        }
        internal_manifest = stage_root / 'manifest.json'
        internal_manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        internal_manifest.chmod(0o640)
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        manifest_path.chmod(0o640)
        with tarfile.open(archive_path, 'w:gz') as archive:
            archive.add(stage_root, arcname=stage_root.name, recursive=True)
        archive_path.chmod(0o640)

    result = dict(manifest)
    result.update({
        'archive_path': str(archive_path.relative_to(repository)),
        'manifest_path': str(manifest_path.relative_to(repository)),
        'archive_sha256': sha256(archive_path),
        'result_path': str((result_root / f'{run_id}.json').relative_to(repository)),
    })
    result_path = result_root / f'{run_id}.json'
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    result_path.chmod(0o640)
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
