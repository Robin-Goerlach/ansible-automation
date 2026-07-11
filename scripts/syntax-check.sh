#!/usr/bin/env bash
set -Eeuo pipefail

readonly repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly inventory="${INVENTORY:-${repository_root}/inventories/example/hosts.yml}"

cd "${repository_root}"
mapfile -t playbooks < <(find playbooks bootstrap tests/web -type f -name '*.yml' -print | sort)
printf 'Syntax-checking %d playbooks in one Ansible invocation.\n' "${#playbooks[@]}"
ansible-playbook -i "${inventory}" --syntax-check "${playbooks[@]}"
