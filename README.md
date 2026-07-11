# SASD Ansible Automation

[![Milestone 4 Quality](https://github.com/SASD-Sysadmin/ansible-automation/actions/workflows/quality.yml/badge.svg)](https://github.com/SASD-Sysadmin/ansible-automation/actions/workflows/quality.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.4.0-blue.svg)](VERSION)

A structured Ansible automation repository for provisioning, configuration management,
diagnostics, maintenance, security, recovery, and controlled remediation of Linux infrastructure.

> Repository: `github.com/SASD-Sysadmin/ansible-automation`
> Current status: **Milestone 4 complete — Diagnostics, version 0.4.0**

## Current capabilities

Milestone 4 adds a correlated, read-only diagnostics platform:

- CPU load, memory, swap, filesystem capacity, inode use, and bounded top-process data;
- service inventory, failed systemd units, and explicitly monitored service state;
- installed package facts, selected versions, update simulation, lock paths, and reboot state;
- interfaces, routes, resolver configuration, listening sockets, DNS, and optional TCP checks;
- local certificate and remote TLS endpoint metadata without reading private keys;
- versioned JSON contracts, one host summary, and sanitized checksummed bundles;
- explicit data-handling guidance and runbooks for incident collection and sharing.

Milestones 1–3 remain available: control-node bootstrap, Linux baseline, access,
SSH, time, logging, firewall, updates, Apache, Nginx, PHP, and guarded TLS deployment.

## Safety model

Diagnostics never change managed-node package, service, network, or configuration state.
They may create temporary Ansible transport files that Ansible removes after execution.
Persistent artifacts are written only on the control node under ignored directories:

```text
reports/diagnostics/<run-id>/<host>/
diagnostic-bundles/
```

External DNS names, TCP targets, certificate files, and TLS endpoints are contacted only
when explicitly declared. Diagnostic artifacts can still contain sensitive infrastructure
metadata and must be reviewed before sharing.

## Quick start

The pinned toolchain requires Python 3.12 or newer on the control node.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-dev.txt
scripts/test.sh
scripts/verify-milestone-4.sh
```

## Collect an incident snapshot

Use a private inventory and limit the first run deliberately:

```bash
ansible-playbook -i inventories/lab/hosts.yml   playbooks/diagnostics/incident-snapshot.yml   --limit lab-host-01
```

Collect and bundle in one invocation:

```bash
ansible-playbook -i inventories/lab/hosts.yml   playbooks/diagnostics/full-diagnostic-bundle.yml   --limit lab-host-01
```

The generated run ID is printed in the report path. A fixed incident identifier may be
supplied with `-e sasd_diagnostics_run_id=INC-2026-0042`.

## Repository layout

```text
.
├── bootstrap/                 Control-node and managed-node bootstrap
├── docs/                      Architecture, administration, reference, testing, security
├── inventories/               Safe example plus private lab/production boundaries
├── manifests/                 Machine-readable milestone, playbook, and role catalogs
├── playbooks/                 Validation, diagnostics, provisioning, maintenance
├── roles/                     Reusable desired-state and read-only collector components
├── runbooks/                  Human operational, incident, and rollback procedures
├── scripts/                   Quality, execution, bundle, and acceptance wrappers
└── tests/                     Runtime, fixture, template, and disposable-VM scenarios
```

## Documentation

- [Milestone 4](docs/milestones/milestone-4.md)
- [Milestone 4 quick start](docs/administration/milestone-4-quickstart.md)
- [Diagnostics architecture](docs/architecture/diagnostics.md)
- [Diagnostics variables](docs/reference/diagnostics-variables.md)
- [Diagnostic data handling](docs/security/diagnostic-data-handling.md)
- [Milestone 4 verification](docs/testing/milestone-4-verification.md)
- [German Milestone 4 documentation](docs/de/milestone-4.md)
- [Roadmap](ROADMAP.md)

## License

MIT License. See [LICENSE](LICENSE).
