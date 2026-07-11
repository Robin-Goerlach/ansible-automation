# Milestone 1: Repository foundation

**Version:** 0.1.0
**Status:** Complete
**Completion date:** 9 July 2026

Milestone 1 turns the initial directory skeleton into an executable, testable, and documented Ansible project foundation. It intentionally does not claim to provide the complete Linux configuration baseline planned for Milestone 2.

## Delivered capabilities

1. A Linux/WSL control-node bootstrap with an isolated Python environment.
2. A managed-Linux bootstrap for hosts without Python 3.
3. A safe public inventory targeting only localhost.
4. Control-node, connectivity, and managed-node readiness validation.
5. Read-only system overview collection with local JSON reports.
6. An audit-first `sasd_system_baseline` role.
7. Explicit double opt-in before baseline packages may be installed.
8. Machine-readable milestone, playbook, and role manifests.
9. Local checks and GitHub Actions quality gates.
10. English technical documentation and German orientation documentation.

## Safety contract

- SSH host-key checking remains enabled.
- The public inventory contains no external hosts.
- The baseline role starts in `audit` mode.
- `apply` mode alone does not install packages.
- Package installation additionally requires `sasd_system_baseline_manage_packages=true`.
- Diagnostic and baseline reports are written on the control node and excluded from Git.
- Managed-node Python bootstrap is isolated as an explicit change playbook.

## Acceptance

```bash
scripts/test.sh
scripts/verify-milestone-1.sh
```

The two-part acceptance validates manifests, documentation links, inventory, YAML, Ansible lint rules, shell syntax, playbook syntax, safe localhost connectivity, managed-node readiness, and baseline check mode.

## Deferred work

Full package policy, users, groups, sudo, SSH, time synchronization, logging, firewall management, patching, reboot policy, service roles, remediation, and recovery belong to later milestones.
