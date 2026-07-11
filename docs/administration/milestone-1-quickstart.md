# Milestone 1 quick start

## Install the toolchain

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-dev.txt
```

External collections are optional for Milestone 1:

```bash
ansible-galaxy collection install -r requirements.yml
```

## Run safe acceptance

```bash
scripts/test.sh
scripts/verify-milestone-1.sh
```

The public inventory resolves to localhost only.

## Create a private lab inventory

```bash
cp -a inventories/example inventories/lab-local
$EDITOR inventories/lab-local/hosts.yml
ansible-inventory -i inventories/lab-local/hosts.yml --graph
```

Do not commit confidential inventory data.

## Bootstrap Python on a target

```bash
ansible-playbook   -i inventories/lab-local/hosts.yml   playbooks/bootstrap/managed-linux.yml   --limit new-host   --ask-become-pass
```

## Audit the baseline

```bash
ansible-playbook   -i inventories/lab-local/hosts.yml   playbooks/provisioning/linux-baseline.yml   --limit new-host   --check --diff
```
