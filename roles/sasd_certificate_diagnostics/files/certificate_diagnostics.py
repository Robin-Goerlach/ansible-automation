#!/usr/bin/env python3
"""Inspect public certificate metadata without reading private keys."""
from __future__ import annotations

import hashlib
import json
import os
import socket
import ssl
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_openssl_time(value: str) -> datetime:
    return datetime.strptime(value, '%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)


def decode_certificate(path: Path) -> dict[str, Any]:
    result = subprocess.run(
        [
            'openssl', 'x509', '-in', str(path), '-noout', '-subject', '-issuer',
            '-serial', '-fingerprint', '-sha256', '-startdate', '-enddate',
        ],
        check=False, capture_output=True, text=True, timeout=15,
    )
    if result.returncode != 0:
        raise ValueError(result.stderr.strip() or 'openssl could not decode certificate')
    values: dict[str, str] = {}
    for line in result.stdout.splitlines():
        key, separator, raw = line.partition('=')
        if separator:
            values[key.strip().lower()] = raw.strip()
    not_before = parse_openssl_time(values['notbefore'])
    not_after = parse_openssl_time(values['notafter'])
    remaining = int((not_after - datetime.now(timezone.utc)).total_seconds() // 86400)
    return {
        'subject': values.get('subject', ''),
        'issuer': values.get('issuer', ''),
        'serial': values.get('serial', ''),
        'sha256_fingerprint': values.get('sha256 fingerprint', '').replace(':', '').lower(),
        'not_before_utc': not_before.isoformat().replace('+00:00', 'Z'),
        'not_after_utc': not_after.isoformat().replace('+00:00', 'Z'),
        'remaining_days': remaining,
    }


def inspect_files(entries: list[dict[str, Any]], minimum_days: int) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    results: list[dict[str, Any]] = []
    issues: list[dict[str, str]] = []
    for entry in entries:
        path = Path(entry['path'])
        item: dict[str, Any] = {'name': entry['name'], 'path': str(path), 'exists': path.is_file()}
        if not path.is_file():
            item.update({'ok': False, 'error': 'certificate file does not exist'})
            issues.append({
                'severity': 'critical', 'component': 'certificates', 'code': 'file-missing',
                'message': f"Certificate file is missing: {entry['name']}",
            })
        else:
            try:
                item.update(decode_certificate(path))
                item.update({'ok': item['remaining_days'] >= minimum_days, 'error': ''})
                if item['remaining_days'] < minimum_days:
                    issues.append({
                        'severity': 'warning', 'component': 'certificates', 'code': 'expiry-near',
                        'message': f"Certificate {entry['name']} has {item['remaining_days']} days remaining",
                    })
            except (OSError, ValueError, KeyError) as exc:
                item.update({'ok': False, 'error': str(exc)})
                issues.append({
                    'severity': 'critical', 'component': 'certificates', 'code': 'decode-failed',
                    'message': f"Certificate could not be decoded: {entry['name']}",
                })
        results.append(item)
    return results, issues


def endpoint_certificate(entry: dict[str, Any], timeout: int) -> dict[str, Any]:
    host = str(entry['host'])
    port = int(entry.get('port', 443))
    server_name = str(entry.get('server_name', host))
    validate = bool(entry.get('validate_certs', True))
    context = ssl.create_default_context() if validate else ssl._create_unverified_context()
    with socket.create_connection((host, port), timeout=timeout) as raw_socket:
        with context.wrap_socket(raw_socket, server_hostname=server_name) as tls_socket:
            der = tls_socket.getpeercert(binary_form=True)
            pem = ssl.DER_cert_to_PEM_cert(der)
            with tempfile.NamedTemporaryFile('w', encoding='utf-8', suffix='.pem') as handle:
                handle.write(pem)
                handle.flush()
                metadata = decode_certificate(Path(handle.name))
            metadata.update({
                'name': entry['name'],
                'host': host,
                'port': port,
                'server_name': server_name,
                'validate_certs': validate,
                'tls_version': tls_socket.version() or '',
                'cipher': (tls_socket.cipher() or ('', '', 0))[0],
                'certificate_sha256': hashlib.sha256(der).hexdigest(),
            })
            return metadata


def inspect_endpoints(entries: list[dict[str, Any]], timeout: int, minimum_days: int) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    results: list[dict[str, Any]] = []
    issues: list[dict[str, str]] = []
    for entry in entries:
        try:
            item = endpoint_certificate(entry, timeout)
            item.update({'ok': item['remaining_days'] >= minimum_days, 'error': ''})
            if item['remaining_days'] < minimum_days:
                issues.append({
                    'severity': 'warning', 'component': 'certificates', 'code': 'endpoint-expiry-near',
                    'message': f"TLS endpoint {entry['name']} has {item['remaining_days']} days remaining",
                })
        except (OSError, ssl.SSLError, ValueError, KeyError) as exc:
            item = {
                'name': entry['name'], 'host': entry['host'],
                'port': int(entry.get('port', 443)), 'ok': False, 'error': str(exc),
            }
            issues.append({
                'severity': 'critical', 'component': 'certificates', 'code': 'endpoint-failed',
                'message': f"TLS endpoint check failed: {entry['name']}",
            })
        results.append(item)
    return results, issues


def main() -> None:
    files = json.loads(os.environ.get('SASD_CERTIFICATE_FILES', '[]'))
    endpoints = json.loads(os.environ.get('SASD_CERTIFICATE_ENDPOINTS', '[]'))
    minimum_days = int(os.environ.get('SASD_CERTIFICATE_MINIMUM_REMAINING_DAYS', '30'))
    timeout = int(os.environ.get('SASD_CERTIFICATE_TIMEOUT_SECONDS', '5'))
    file_results, file_issues = inspect_files(files, minimum_days)
    endpoint_results, endpoint_issues = inspect_endpoints(endpoints, timeout, minimum_days)
    issues = file_issues + endpoint_issues
    status = 'critical' if any(item['severity'] == 'critical' for item in issues) else ('warning' if issues else 'ok')
    print(json.dumps({
        'status': status, 'files': file_results, 'endpoints': endpoint_results, 'issues': issues,
    }, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
