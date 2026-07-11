#!/usr/bin/env bash
set -Eeuo pipefail

readonly repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly inventory="${INVENTORY:-${repository_root}/inventories/example/hosts.yml}"

cd "${repository_root}"
ansible-inventory -i "${inventory}" --graph
ansible-inventory -i "${inventory}" --list >/dev/null
