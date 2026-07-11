# Diagnostics architecture

## Design goals

Milestone 4 separates evidence collection from remediation. A warning or critical issue
is data, not permission to modify the node. Milestone 5 may later consume these contracts,
but it must add its own confirmation, backup, validation, and rollback controls.

## Collection layers

1. Ansible gathers normal facts and validates variables.
2. Built-in modules collect services, packages, file markers, and command results.
3. Small standard-library Python collectors normalize Linux data that otherwise requires
   fragile shell parsing.
4. Each role publishes a fact and optionally writes one JSON report on the controller.
5. The incident-snapshot playbook builds one summary across all role results.
6. The bundle role sanitizes and archives one completed run.

Python collectors are transferred through `ansible.builtin.script`, run from Ansible's
temporary directory, and removed by Ansible. They do not install dependencies.

## Result severity

- `ok`: no configured threshold or explicit check failed;
- `warning`: investigation is recommended;
- `critical`: a declared file/endpoint is unavailable or a critical capacity threshold is exceeded.

Severity does not cause automatic remediation and does not fail the playbook. Invalid
configuration, malformed declarations, or collector execution errors do fail the run.

## Portability

The core contracts are Linux-oriented. Resource data uses `/proc`, `df`, and `ps`.
Network enrichment uses `ip` and `ss` when present and records a tool warning otherwise.
Package update simulation supports APT, DNF, YUM, and Zypper without refreshing metadata.

## Data location

Managed nodes retain no report files. Controller output is ignored by Git because it may
contain sensitive infrastructure information. CI acceptance deletes its generated run
before execution and validates artifacts in place.
