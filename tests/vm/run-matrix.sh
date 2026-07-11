#!/usr/bin/env bash
set -Eeuo pipefail
readonly scenario_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly repository_root="$(cd "${scenario_root}/../.." && pwd)"
cd "${scenario_root}"

for command_name in vagrant ansible-playbook python3; do
  command -v "${command_name}" >/dev/null 2>&1 || {
    printf 'ERROR: required command unavailable: %s
' "${command_name}" >&2
    exit 1
  }
done

cleanup() {
  vagrant destroy -f || true
  rm -f inventory.generated.yml
}
trap cleanup EXIT

vagrant up --provider=libvirt

python3 - <<'PY2'
from pathlib import Path
import subprocess, yaml
nodes=['debian12','ubuntu2404','rocky9','opensuse15']
hosts={}
for node in nodes:
    out=subprocess.check_output(['vagrant','ssh-config',node], text=True)
    values={}
    for line in out.splitlines():
        parts=line.strip().split(None,1)
        if len(parts)==2:
            values[parts[0]]=parts[1]
    hosts[node]={
      'ansible_host': values['HostName'],
      'ansible_port': int(values['Port']),
      'ansible_user': values['User'],
      'ansible_private_key_file': values['IdentityFile'].strip('"'),
      'ansible_ssh_common_args': '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null',
    }
inv={'all':{'children':{'linux_managed':{'hosts':hosts}}}}
Path('inventory.generated.yml').write_text(yaml.safe_dump(inv, sort_keys=False), encoding='utf-8')
PY2

cd "${repository_root}"
ansible-playbook -i tests/vm/inventory.generated.yml playbooks/validation/managed-node-readiness.yml
ansible-playbook -i tests/vm/inventory.generated.yml playbooks/validation/linux-baseline.yml
ansible-playbook -i tests/vm/inventory.generated.yml playbooks/provisioning/linux-baseline.yml
