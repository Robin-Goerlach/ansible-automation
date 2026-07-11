#!/usr/bin/env python3
"""Run ansible-playbook with isolated output and deterministic timeout handling."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=420)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command:
        parser.error("an ansible-playbook command is required after --")
    return args


def main() -> int:
    args = parse_args()
    args.log.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.setdefault("ANSIBLE_FORKS", "1")
    env.setdefault("ANSIBLE_PIPELINING", "False")
    env.setdefault("ANSIBLE_NOCOLOR", "1")

    with args.log.open("wb") as log_handle:
        process = subprocess.Popen(
            args.command,
            env=env,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            close_fds=True,
        )
        try:
            return_code = process.wait(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=10)
            print(
                f"ERROR: command exceeded {args.timeout} seconds; see {args.log}",
                file=sys.stderr,
            )
            return 124

    log_text = args.log.read_text(encoding="utf-8", errors="replace")
    if return_code == 0:
        lines = log_text.rstrip().splitlines()
        recap_index = next(
            (index for index, line in enumerate(lines) if line.startswith("PLAY RECAP")),
            max(0, len(lines) - 12),
        )
        print("\n".join(lines[recap_index:]) + "\n")
    else:
        print(log_text, end="")
        print(f"ERROR: ansible-playbook exited with {return_code}", file=sys.stderr)
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
