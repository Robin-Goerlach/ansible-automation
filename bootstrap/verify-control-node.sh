#!/usr/bin/env bash
set -Eeuo pipefail

readonly repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly minimum_python="3.12"
fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

for command_name in python3 git ansible ansible-playbook ansible-lint yamllint; do
  command -v "${command_name}" >/dev/null 2>&1 || fail "${command_name} is unavailable"
done

python3 - "${minimum_python}" <<'PYCODE'
import sys
required = tuple(map(int, sys.argv[1].split('.')))
if sys.version_info[:2] < required:
    raise SystemExit(f"Python {sys.argv[1]}+ required, found {sys.version.split()[0]}")
PYCODE

cd "${repository_root}"
ansible-inventory -i inventories/example/hosts.yml --graph >/dev/null
ansible-playbook -i inventories/example/hosts.yml --syntax-check playbooks/validation/control-node.yml >/dev/null
printf 'Control-node verification passed.\n'
