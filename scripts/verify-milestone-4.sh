#!/usr/bin/env bash
set -Eeuo pipefail

readonly repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly ansible_step_timeout="${SASD_ANSIBLE_STEP_TIMEOUT:-420}"
readonly run_id="milestone4-localhost"
readonly log_root="${repository_root}/.cache/milestone-4-verification"
cd "${repository_root}"

required_commands=(ansible-playbook python3 tar)
for command_name in "${required_commands[@]}"; do
  command -v "${command_name}" >/dev/null 2>&1 || {
    printf 'ERROR: required command unavailable: %s\n' "${command_name}" >&2
    exit 1
  }
done

run_playbook() {
  local log_name="$1"
  shift
  python3 tests/diagnostics/run_ansible_playbook.py \
    --timeout "${ansible_step_timeout}" \
    --log "${log_root}/${log_name}.log" \
    -- ansible-playbook "$@"
}

rm -rf \
  "${log_root}" \
  "reports/diagnostics/${run_id}" \
  "reports/diagnostics/bundles/${run_id}.json" \
  "diagnostic-bundles/sasd-diagnostic-bundle-${run_id}.tar.gz" \
  "diagnostic-bundles/sasd-diagnostic-bundle-${run_id}.manifest.json"
mkdir -p "${log_root}"

printf '== Milestone 4 isolated localhost diagnostics ==\n'
run_playbook resources \
  -i inventories/example/hosts.yml \
  playbooks/diagnostics/resources.yml \
  -e "sasd_diagnostics_run_id=${run_id}"
run_playbook services \
  -i inventories/example/hosts.yml \
  playbooks/diagnostics/services.yml \
  -e "sasd_diagnostics_run_id=${run_id}"
run_playbook packages \
  -i inventories/example/hosts.yml \
  playbooks/diagnostics/packages.yml \
  -e "sasd_diagnostics_run_id=${run_id}"
run_playbook network \
  -i inventories/example/hosts.yml \
  playbooks/diagnostics/network.yml \
  -e "sasd_diagnostics_run_id=${run_id}"
run_playbook certificates \
  -i inventories/example/hosts.yml \
  playbooks/diagnostics/certificates.yml \
  -e "sasd_diagnostics_run_id=${run_id}" \
  -e '{"sasd_certificate_diagnostics_files":[{"name":"fixture","path":"'"${repository_root}"'/tests/fixtures/diagnostics/test-certificate.pem"}]}'
run_playbook aggregate \
  -i inventories/example/hosts.yml \
  playbooks/diagnostics/aggregate-reports.yml \
  -e "sasd_diagnostics_run_id=${run_id}"

printf '\n== Inject bundle redaction canary ==\n'
python3 tests/diagnostics/verify_milestone4.py prepare

printf '\n== Milestone 4 standardized bundle ==\n'
run_playbook bundle \
  -i inventories/example/hosts.yml \
  playbooks/diagnostics/build-bundle.yml \
  -e "sasd_diagnostics_run_id=${run_id}"

python3 tests/diagnostics/verify_milestone4.py verify

printf '\nMilestone 4 safe localhost runtime verification passed.\n'
