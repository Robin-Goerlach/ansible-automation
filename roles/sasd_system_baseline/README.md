# Role: `sasd_system_baseline`

Milestone 1 implements an audit-first foundation role. It demonstrates variable validation, safe defaults, local reports, check mode, and explicit opt-in changes without prematurely implementing the complete Linux baseline planned for Milestone 2.

## Default behavior

```yaml
sasd_system_baseline_mode: audit
sasd_system_baseline_manage_packages: false
```

The role gathers package facts, reports whether requested baseline packages are present, and writes a JSON report on the control node. It does not change the managed node.

## Explicit package application

```bash
ansible-playbook -i inventories/lab-local/hosts.yml playbooks/provisioning/linux-baseline.yml   --check --diff   -e sasd_system_baseline_mode=apply   -e sasd_system_baseline_manage_packages=true
```

Remove `--check` only after reviewing the target inventory, limit, and predicted changes.
