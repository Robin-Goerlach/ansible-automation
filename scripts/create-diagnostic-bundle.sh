#!/usr/bin/env bash
set -Eeuo pipefail

readonly repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repository_root}"

run_id="${1:-}"
if [[ -z "${run_id}" ]]; then
  printf 'Usage: %s RUN_ID\n' "${0##*/}" >&2
  printf 'Example: %s 20260709T143000Z\n' "${0##*/}" >&2
  exit 2
fi
if [[ ! "${run_id}" =~ ^[A-Za-z0-9._-]+$ ]]; then
  printf 'ERROR: invalid run ID: %s\n' "${run_id}" >&2
  exit 2
fi
if [[ ! -d "reports/diagnostics/${run_id}" ]]; then
  printf 'ERROR: diagnostics run not found: reports/diagnostics/%s\n' "${run_id}" >&2
  exit 1
fi

cat <<'EOF'
WARNING: Diagnostic bundles can contain hostnames, usernames, addresses,
paths, package versions, and operational metadata. JSON key redaction is
only defense in depth. Review every bundle before external sharing.
EOF

ansible-playbook \
  -i inventories/example/hosts.yml \
  playbooks/diagnostics/build-bundle.yml \
  -e "sasd_diagnostics_run_id=${run_id}"
