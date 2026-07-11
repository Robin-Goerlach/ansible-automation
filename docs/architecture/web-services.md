# Web-services architecture

## Composition

`playbooks/provisioning/web-services.yml` orchestrates certificates, PHP, Apache, and Nginx in that order. Certificates are prepared before web-server configurations reference them. PHP is independent because static-only hosts do not need it.

## Audit-first execution

All roles collect package, binary, service, configuration, and declaration state without changing managed nodes. Reports are delegated to the control node under `reports/web-services/`.

## Transaction boundary

Ansible cannot make an operating-system configuration change globally atomic. Milestone 3 therefore uses a file-level safety boundary:

1. inspect and capture the existing file;
2. render or remove the declared file;
3. run the service's complete native configuration test;
4. restore the previous state on failure;
5. reload only through a handler after validation.

Multiple virtual hosts in one run are validated one by one. A later failure restores that declaration but does not roll back earlier successfully validated declarations. Use small batches and `--limit` for production changes.

## Secret boundary

Private keys are never embedded in public examples. Provided key content must come from Ansible Vault or another secret source. Tasks handling private key content use `no_log: true`, while reports include paths and validation state only.

## Dual-server protection

The orchestration playbook rejects an Apache-plus-Nginx apply unless explicitly allowed. This is a guardrail, not a port planner. A reviewed design must assign distinct addresses/ports or a reverse-proxy topology.
