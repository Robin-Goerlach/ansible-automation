#!/usr/bin/env bash
set -Eeuo pipefail

readonly repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly ansible_step_timeout="${SASD_ANSIBLE_STEP_TIMEOUT:-420}"
cd "${repository_root}"

required_commands=(ansible ansible-inventory ansible-lint ansible-playbook timeout yamllint python3)
for command_name in "${required_commands[@]}"; do
  command -v "${command_name}" >/dev/null 2>&1 || {
    printf 'ERROR: required command unavailable: %s\n' "${command_name}" >&2
    exit 1
  }
done

run_playbook() {
  local temporary_directory exit_code
  temporary_directory="$(mktemp -d "${TMPDIR:-/tmp}/sasd-ansible-m2.XXXXXX")"

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

rm -rf reports/linux-baseline reports/linux-updates

printf '== Milestone 2 safe localhost acceptance scenario ==\n'
run_playbook -i inventories/example/hosts.yml playbooks/validation/milestone-2-localhost.yml

python3 - <<'PY'
from pathlib import Path
import json

root = Path("reports")
required = [
    "linux-baseline/localhost.json",
    "linux-baseline/package-management/localhost.json",
    "linux-baseline/user-management/localhost.json",
    "linux-baseline/sudo-configuration/localhost.json",
    "linux-baseline/ssh-server/localhost.json",
    "linux-baseline/time-synchronization/localhost.json",
    "linux-baseline/log-management/localhost.json",
    "linux-baseline/firewall/localhost.json",
    "linux-updates/localhost.json",
]
for relative in required:
    path = root / relative
    if not path.is_file():
        raise SystemExit(f"missing report: {path}")
    json.loads(path.read_text(encoding="utf-8"))

consolidated = json.loads((root / "linux-baseline/localhost.json").read_text(encoding="utf-8"))
if consolidated.get("schema") != "sasd.linux-baseline.v2":
    raise SystemExit("unexpected consolidated schema")

expected_sections = {
    "package_management": "sasd.package-management.v1",
    "user_management": "sasd.user-management.v1",
    "sudo_configuration": "sasd.sudo-configuration.v1",
    "ssh_server": "sasd.ssh-server.v1",
    "time_synchronization": "sasd.time-synchronization.v1",
    "log_management": "sasd.log-management.v1",
    "firewall": "sasd.firewall.v1",
}
for section, schema in expected_sections.items():
    if consolidated.get(section, {}).get("schema") != schema:
        raise SystemExit(f"unexpected or missing schema for section: {section}")

print(f"Validated {len(required)} JSON reports and all consolidated schemas.")
PY

printf '\nMilestone 2 safe localhost runtime verification passed.\n'
