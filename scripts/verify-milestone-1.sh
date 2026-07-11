#!/usr/bin/env bash
set -Eeuo pipefail

readonly repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly ansible_step_timeout="${SASD_ANSIBLE_STEP_TIMEOUT:-180}"
cd "${repository_root}"

required_commands=(ansible ansible-inventory ansible-lint ansible-playbook timeout yamllint python3)
for command_name in "${required_commands[@]}"; do
  command -v "${command_name}" >/dev/null 2>&1 || {
    printf 'ERROR: required command unavailable: %s\n' "${command_name}" >&2
    exit 1
  }
done

run_ansible_playbook() {
  local temporary_directory exit_code
  temporary_directory="$(mktemp -d "${TMPDIR:-/tmp}/sasd-ansible-m1.XXXXXX")"

  # A single fork and disabled pipelining keep localhost acceptance predictable
  # in constrained containers. Normal operations still use ansible.cfg.
  set +e
  ANSIBLE_FORKS=1 \
    ANSIBLE_PIPELINING=False \
    ANSIBLE_LOCAL_TEMP="${temporary_directory}/local" \
    timeout "${ansible_step_timeout}" \
    ansible-playbook "$@"
  exit_code=$?
  set -e

  rm -rf "${temporary_directory}"
  return "${exit_code}"
}

rm -rf reports/system-overview reports/baseline

printf '== Safe localhost control-node validation ==\n'
run_ansible_playbook -i inventories/example/hosts.yml \
  playbooks/validation/control-node.yml

printf '\n== Safe localhost connectivity validation ==\n'
run_ansible_playbook -i inventories/example/hosts.yml \
  playbooks/validation/connectivity.yml

printf '\n== Safe localhost managed-node readiness validation ==\n'
run_ansible_playbook -i inventories/example/hosts.yml \
  playbooks/validation/managed-node-readiness.yml

printf '\n== Read-only diagnostics and JSON report validation ==\n'
run_ansible_playbook -i inventories/example/hosts.yml \
  playbooks/diagnostics/system-overview.yml
mapfile -t diagnostic_reports < <(find reports/system-overview -type f -name '*.json' -print | sort)
if ((${#diagnostic_reports[@]} != 1)); then
  printf 'ERROR: expected one diagnostics report, found %d\n' "${#diagnostic_reports[@]}" >&2
  exit 1
fi
python3 -m json.tool "${diagnostic_reports[0]}" >/dev/null
printf 'Validated diagnostics report: %s\n' "${diagnostic_reports[0]}"

printf '\n== Baseline check-mode verification ==\n'
run_ansible_playbook -i inventories/example/hosts.yml \
  playbooks/provisioning/linux-baseline.yml --check --diff

printf '\nMilestone 1 safe localhost runtime verification passed.\n'
