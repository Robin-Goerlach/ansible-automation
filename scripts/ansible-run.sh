#!/usr/bin/env bash
set -Eeuo pipefail

if (($# < 1)); then
  printf 'Usage: INVENTORY=path/to/hosts.yml %s PLAYBOOK [ansible-playbook options]\n' "$0" >&2
  exit 2
fi

readonly repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly inventory="${INVENTORY:-${repository_root}/inventories/example/hosts.yml}"

cd "${repository_root}"
exec ansible-playbook -i "${inventory}" "$@"
