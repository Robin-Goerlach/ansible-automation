#!/usr/bin/env python3
"""Collect bounded Linux resource diagnostics and print one JSON document."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


def env_int(name: str, default: int) -> int:
    return int(os.environ.get(name, str(default)))


def env_float(name: str, default: float) -> float:
    return float(os.environ.get(name, str(default)))


def read_meminfo() -> dict[str, int]:
    values: dict[str, int] = {}
    for line in Path('/proc/meminfo').read_text(encoding='utf-8').splitlines():
        key, raw = line.split(':', 1)
        number = raw.strip().split()[0]
        values[key] = int(number) * 1024
    return values


def percentage(used: int, total: int) -> float:
    return round((used / total * 100.0), 2) if total > 0 else 0.0


def run_lines(argv: list[str]) -> list[str]:
    result = subprocess.run(argv, check=False, capture_output=True, text=True, timeout=15)
    return result.stdout.splitlines() if result.returncode == 0 else []


def filesystem_rows(excluded_types: set[str]) -> list[dict[str, object]]:
    capacity: dict[str, dict[str, object]] = {}
    lines = run_lines(['df', '-PT'])
    for line in lines[1:]:
        fields = line.split(maxsplit=6)
        if len(fields) != 7:
            continue
        device, fs_type, total, used, available, percent, mount = fields
        if fs_type in excluded_types:
            continue
        capacity[mount] = {
            'device': device,
            'type': fs_type,
            'mount': mount,
            'total_kib': int(total),
            'used_kib': int(used),
            'available_kib': int(available),
            'used_percent': int(percent.rstrip('%')),
        }
    inode_lines = run_lines(['df', '-Pi'])
    for line in inode_lines[1:]:
        fields = line.split(maxsplit=5)
        if len(fields) != 6:
            continue
        _, total, used, available, percent, mount = fields
        if mount in capacity:
            capacity[mount].update({
                'inode_total': int(total),
                'inode_used': int(used),
                'inode_available': int(available),
                'inode_used_percent': int(percent.rstrip('%')),
            })
    return [capacity[key] for key in sorted(capacity)]


def top_processes(limit: int) -> dict[str, list[dict[str, object]]]:
    fields = ['pid', 'ppid', 'user', 'stat', 'cpu_percent', 'memory_percent', 'elapsed_seconds', 'command']

    def collect(sort_key: str) -> list[dict[str, object]]:
        argv = [
            'ps', '-eo', 'pid=,ppid=,user=,stat=,pcpu=,pmem=,etimes=,comm=',
            f'--sort=-{sort_key}',
        ]
        rows: list[dict[str, object]] = []
        for line in run_lines(argv)[:limit]:
            parts = line.split(maxsplit=7)
            if len(parts) != 8:
                continue
            row = dict(zip(fields, parts))
            row['pid'] = int(row['pid'])
            row['ppid'] = int(row['ppid'])
            row['cpu_percent'] = float(row['cpu_percent'])
            row['memory_percent'] = float(row['memory_percent'])
            row['elapsed_seconds'] = int(row['elapsed_seconds'])
            rows.append(row)
        return rows

    return {'by_cpu': collect('pcpu'), 'by_memory': collect('pmem')}


def main() -> None:
    load_warning = env_float('SASD_RESOURCE_LOAD_WARNING_PER_CPU', 1.0)
    memory_warning = env_int('SASD_RESOURCE_MEMORY_AVAILABLE_WARNING_PERCENT', 15)
    swap_warning = env_int('SASD_RESOURCE_SWAP_USED_WARNING_PERCENT', 50)
    fs_warning = env_int('SASD_RESOURCE_FILESYSTEM_USED_WARNING_PERCENT', 85)
    inode_warning = env_int('SASD_RESOURCE_INODE_USED_WARNING_PERCENT', 85)
    process_count = env_int('SASD_RESOURCE_TOP_PROCESS_COUNT', 10)
    excluded = set(json.loads(os.environ.get('SASD_RESOURCE_EXCLUDED_FILESYSTEM_TYPES', '[]')))

    cpu_count = os.cpu_count() or 1
    load_1, load_5, load_15 = os.getloadavg()
    mem = read_meminfo()
    total = mem.get('MemTotal', 0)
    available = mem.get('MemAvailable', mem.get('MemFree', 0))
    swap_total = mem.get('SwapTotal', 0)
    swap_free = mem.get('SwapFree', 0)
    fs_rows = filesystem_rows(excluded)
    issues: list[dict[str, str]] = []

    if load_1 / cpu_count >= load_warning:
        issues.append({
            'severity': 'warning', 'component': 'cpu', 'code': 'load-high',
            'message': f'1-minute load per CPU is {load_1 / cpu_count:.2f}',
        })
    memory_available_percent = percentage(available, total)
    if memory_available_percent <= memory_warning:
        issues.append({
            'severity': 'warning', 'component': 'memory', 'code': 'available-low',
            'message': f'Available memory is {memory_available_percent:.2f} percent',
        })
    swap_used = max(swap_total - swap_free, 0)
    swap_used_percent = percentage(swap_used, swap_total)
    if swap_total > 0 and swap_used_percent >= swap_warning:
        issues.append({
            'severity': 'warning', 'component': 'swap', 'code': 'usage-high',
            'message': f'Swap usage is {swap_used_percent:.2f} percent',
        })
    for row in fs_rows:
        if int(row['used_percent']) >= fs_warning:
            issues.append({
                'severity': 'critical', 'component': 'filesystem', 'code': 'capacity-high',
                'message': f"{row['mount']} is {row['used_percent']} percent used",
            })
        if int(row.get('inode_used_percent', 0)) >= inode_warning:
            issues.append({
                'severity': 'critical', 'component': 'filesystem', 'code': 'inodes-high',
                'message': f"{row['mount']} inode usage is {row['inode_used_percent']} percent",
            })

    status = 'critical' if any(item['severity'] == 'critical' for item in issues) else ('warning' if issues else 'ok')
    payload = {
        'status': status,
        'issues': issues,
        'cpu': {
            'logical_cpu_count': cpu_count,
            'load_1': load_1,
            'load_5': load_5,
            'load_15': load_15,
            'load_1_per_cpu': round(load_1 / cpu_count, 3),
        },
        'memory': {
            'total_bytes': total,
            'available_bytes': available,
            'available_percent': memory_available_percent,
            'used_percent': round(100.0 - memory_available_percent, 2),
        },
        'swap': {
            'total_bytes': swap_total,
            'used_bytes': swap_used,
            'free_bytes': swap_free,
            'used_percent': swap_used_percent,
        },
        'filesystems': fs_rows,
        'top_processes': top_processes(process_count),
    }
    print(json.dumps(payload, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
