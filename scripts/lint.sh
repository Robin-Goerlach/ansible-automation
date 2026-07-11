#!/usr/bin/env bash
set -Eeuo pipefail
readonly repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repository_root}"
yamllint .
ANSIBLE_FORKS="${ANSIBLE_FORKS:-1}" ansible-lint -v playbooks tests/web
if command -v shellcheck >/dev/null 2>&1; then
  mapfile -t shell_files < <(find bootstrap scripts -type f -name '*.sh' -print | sort)
  shellcheck "${shell_files[@]}"
else
  printf 'NOTICE: shellcheck unavailable; bash -n remains active.\n'
fi
while IFS= read -r script; do
  bash -n "${script}"
done < <(find bootstrap scripts -type f -name '*.sh' -print | sort)
