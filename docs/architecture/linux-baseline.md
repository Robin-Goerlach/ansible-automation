# Linux baseline architecture

## Audit-first execution

Each role follows the same lifecycle:

1. validate variables and safety gates;
2. gather read-only state;
3. apply desired state only in confirmed apply mode;
4. normalize a versioned result dictionary;
5. write a JSON report on the control node.

The orchestration playbook combines these dictionaries into `sasd.linux-baseline.v2`.

## Why focused roles

Package management, access, SSH, time, logging, and firewall changes have different rollback and risk characteristics. Independent roles permit targeted execution, role-specific tests, and smaller review scopes.

## Change gates

The global apply token protects against accidental variable changes. SSH and firewall use a second boolean switch because either area can remove remote access. Reboot is deliberately outside all baseline roles.

## Rollback approach

- repository, sudo, SSH, time, and logging configuration files use backups;
- SSH additionally captures the old drop-in, validates `sshd -t`, and restores on failure;
- users and groups are never removed unless a declaration explicitly says `state: absent`;
- undeclared accounts and sudo entries are untouched;
- firewall adapters only act on declared rules and never flush the complete policy;
- package updates do not reboot automatically.
