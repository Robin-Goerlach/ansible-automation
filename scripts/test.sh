#!/usr/bin/env bash
set -Eeuo pipefail
readonly repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repository_root}"
scripts/check-manifests.py
scripts/check-documentation-links.py
scripts/check-inventory.sh
scripts/lint.sh
scripts/syntax-check.sh
python3 -m py_compile \
  roles/sasd_resource_diagnostics/files/resource_diagnostics.py \
  roles/sasd_network_diagnostics/files/network_diagnostics.py \
  roles/sasd_certificate_diagnostics/files/certificate_diagnostics.py \
  roles/sasd_diagnostic_bundle/files/build_diagnostic_bundle.py \
  tests/diagnostics/verify_milestone4.py \
  tests/diagnostics/run_ansible_playbook.py
bash -n tests/vm/run-matrix.sh
if command -v ruby >/dev/null 2>&1; then
  ruby -c tests/vm/Vagrantfile >/dev/null
fi
bash -n scripts/verify-milestone-2.sh
bash -n scripts/verify-milestone-3.sh
bash -n scripts/verify-milestone-4.sh
