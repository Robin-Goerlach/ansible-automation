# Milestone 2 quick start

## 1. Prepare the control node

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
scripts/test.sh
scripts/verify-milestone-2.sh
```

## 2. Copy the example inventory into a private lab inventory

Never replace the public localhost-only example with real infrastructure. Create a private or ignored inventory and define one test VM first.

## 3. Run readiness and audit

```bash
ansible-playbook -i inventories/lab/hosts.yml playbooks/validation/managed-node-readiness.yml --limit test-vm
ansible-playbook -i inventories/lab/hosts.yml playbooks/provisioning/linux-baseline.yml --limit test-vm
```

Review `reports/linux-baseline/test-vm.json` and the role reports.

## 4. Preview an approved change

```bash
ansible-playbook -i inventories/lab/hosts.yml playbooks/provisioning/linux-baseline.yml   --limit test-vm --check --diff   -e sasd_linux_baseline_mode=apply   -e sasd_linux_baseline_apply_confirmation=SASD_APPLY_LINUX_BASELINE
```

## 5. Apply in the lab

Remove `--check` only after reviewing the target, variable set, and predicted diff. Keep SSH and firewall disabled until their dedicated runbooks have been followed.
