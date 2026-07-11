#!/usr/bin/env bash
set -Eeuo pipefail

readonly repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repository_root}"

python3 -m pip install --upgrade ansible-dev-tools
ansible-galaxy collection install --upgrade -r requirements.yml

printf '%s\n' \
  'Dependencies were updated in the active Python environment.' \
  'Review changelogs and rerun all tests before committing version constraints.'
