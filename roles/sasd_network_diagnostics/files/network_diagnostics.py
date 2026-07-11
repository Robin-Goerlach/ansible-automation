#!/usr/bin/env python3
"""Collect Linux network state and perform explicitly declared safe checks."""
from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
from pathlib import Path
from typing import Any


def run_json(argv: list[str]) -> tuple[list[Any], str | None]:
    if not shutil.which(argv[0]):
        return [], f'{argv[0]} is unavailable'
    result = subprocess.run(argv, check=False, capture_output=True, text=True, timeout=15)
    if result.returncode != 0:
        return [], result.stderr.strip() or f'{argv[0]} returned {result.returncode}'
    try:
        return json.loads(result.stdout), None
    except json.JSONDecodeError as exc:
        return [], f'Invalid JSON from {argv[0]}: {exc}'


def resolver_config() -> dict[str, list[str]]:
    result = {'nameservers': [], 'search': [], 'options': []}
    path = Path('/etc/resolv.conf')
    if not path.is_file():
        return result
    for raw in path.read_text(encoding='utf-8', errors='replace').splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        key, *values = line.split()
        if key == 'nameserver' and values:
            result['nameservers'].append(values[0])
        elif key in {'search', 'domain'}:
            result['search'].extend(values)
        elif key == 'options':
            result['options'].extend(values)
    return result


def listening_sockets() -> tuple[list[dict[str, str]], str | None]:
    if not shutil.which('ss'):
        return [], 'ss is unavailable'
    result = subprocess.run(
        ['ss', '-H', '-lntu'], check=False, capture_output=True, text=True, timeout=15,
    )
    if result.returncode != 0:
        return [], result.stderr.strip() or f'ss returned {result.returncode}'
    rows: list[dict[str, str]] = []
    for line in result.stdout.splitlines():
        fields = line.split()
        if len(fields) < 5:
            continue
        rows.append({
            'protocol': fields[0],
            'state': fields[1],
            'local_address': fields[4],
            'peer_address': fields[5] if len(fields) > 5 else '',
        })
    return rows, None


def dns_checks(names: list[str]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for name in names:
        try:
            addresses = sorted({entry[4][0] for entry in socket.getaddrinfo(name, None)})
            results.append({'name': name, 'ok': True, 'addresses': addresses, 'error': ''})
        except (OSError, socket.gaierror) as exc:
            results.append({'name': name, 'ok': False, 'addresses': [], 'error': str(exc)})
    return results


def tcp_checks(targets: list[dict[str, Any]], timeout: int) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for target in targets:
        host = str(target['host'])
        port = int(target['port'])
        try:
            with socket.create_connection((host, port), timeout=timeout):
                results.append({
                    'name': target['name'], 'host': host, 'port': port,
                    'ok': True, 'error': '',
                })
        except OSError as exc:
            results.append({
                'name': target['name'], 'host': host, 'port': port,
                'ok': False, 'error': str(exc),
            })
    return results


def main() -> None:
    names = json.loads(os.environ.get('SASD_NETWORK_DNS_NAMES', '[]'))
    targets = json.loads(os.environ.get('SASD_NETWORK_TCP_TARGETS', '[]'))
    timeout = int(os.environ.get('SASD_NETWORK_TIMEOUT_SECONDS', '3'))
    include_loopback = os.environ.get('SASD_NETWORK_INCLUDE_LOOPBACK', 'true').lower() == 'true'

    interfaces, interface_error = run_json(['ip', '-j', 'address', 'show'])
    routes, route_error = run_json(['ip', '-j', 'route', 'show', 'table', 'main'])
    if not include_loopback:
        interfaces = [item for item in interfaces if item.get('ifname') != 'lo']
    sockets, socket_error = listening_sockets()
    dns = dns_checks(names)
    tcp = tcp_checks(targets, timeout)
    issues: list[dict[str, str]] = []
    for result in dns:
        if not result['ok']:
            issues.append({
                'severity': 'warning', 'component': 'dns', 'code': 'resolution-failed',
                'message': f"DNS resolution failed for {result['name']}",
            })
    for result in tcp:
        if not result['ok']:
            issues.append({
                'severity': 'warning', 'component': 'network', 'code': 'tcp-connect-failed',
                'message': f"TCP connection failed for {result['name']}",
            })
    for tool, error in [('ip-address', interface_error), ('ip-route', route_error), ('ss', socket_error)]:
        if error:
            issues.append({
                'severity': 'warning', 'component': 'network', 'code': 'tool-unavailable',
                'message': f'{tool}: {error}',
            })

    payload = {
        'status': 'warning' if issues else 'ok',
        'interfaces': interfaces,
        'routes': routes,
        'resolver': resolver_config(),
        'listening_sockets': sockets,
        'dns_queries': dns,
        'tcp_checks': tcp,
        'tools': {
            'ip_address_error': interface_error or '',
            'ip_route_error': route_error or '',
            'ss_error': socket_error or '',
        },
        'issues': issues,
    }
    print(json.dumps(payload, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
