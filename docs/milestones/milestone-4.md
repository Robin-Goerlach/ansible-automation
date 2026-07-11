# Milestone 4: Diagnostics

Version: `0.4.0`
Status: complete
Managed-node behavior: read-only

## Objective

Milestone 4 turns the repository into a practical incident data collection tool.
It collects related evidence under one run identifier so that CPU pressure, memory,
filesystems, services, packages, network state, and certificates can be compared from
the same operational point in time.

## Role boundaries

| Role | Responsibility | Persistent write location |
|---|---|---|
| `sasd_resource_diagnostics` | CPU, load, memory, swap, filesystems, inodes, processes | controller report |
| `sasd_service_diagnostics` | service facts, failed units, monitored services | controller report |
| `sasd_package_diagnostics` | package facts, update simulation, locks, reboot marker | controller report |
| `sasd_network_diagnostics` | interfaces, routes, resolver, sockets, DNS, TCP checks | controller report |
| `sasd_certificate_diagnostics` | certificate files and explicit TLS endpoints | controller report |
| `sasd_diagnostic_bundle` | sanitization, manifest, checksums, archive | controller bundle |

## Collection entry points

`incident-snapshot.yml` collects all domains in one invocation. The five component
playbooks can also use one shared run ID. `aggregate-reports.yml` validates their
schemas and reconstructs `summary.json` entirely from controller-side reports, which
supports interrupted-run recovery and independently scheduled collectors.

## Correlated run layout

```text
reports/diagnostics/<run-id>/<host>/
├── resources.json
├── services.json
├── packages.json
├── network.json
├── certificates.json
└── summary.json
```

Every file has a versioned schema. `summary.json` aggregates issues and component
status without duplicating all raw detail.

## Diagnostic scope and limits

The collectors are deliberately bounded:

- process command lines and environment variables are not collected;
- package update output is capped;
- filesystem pseudo-types are excluded by default;
- no external network target is contacted unless declared;
- TLS private keys are not opened;
- bundle files exceeding the configured size are skipped;
- symbolic links are excluded from bundles.

A read-only command can still have operational cost. Update simulation and package facts
may take longer on large systems, while DNS and TCP checks wait for their configured
timeout. Operators should use `--limit`, review defaults, and start with one laboratory host.

## Bundle contract

The bundle builder copies one run into a temporary staging directory, parses JSON,
replaces values of keys matching sensitive patterns with `[REDACTED]`, calculates a
SHA-256 for every included report, writes `manifest.json`, and creates a `tar.gz` archive.

Key-name redaction cannot recognize arbitrary secrets hidden in ordinary text fields.
Therefore every manifest sets `review_required_before_external_sharing: true`.

## Acceptance criteria

- all role variables have argument specifications and documented defaults;
- all diagnostics playbooks pass syntax and production-profile linting;
- managed-node tasks are read-only and run without privilege escalation;
- all six component/summary reports are valid JSON with expected schemas;
- a real public certificate fixture is decoded during localhost acceptance;
- bundle redaction removes canary values while preserving ordinary values;
- archives contain no symbolic or hard links;
- the archive SHA-256 matches the bundle result contract;
- the public inventory contacts only localhost and declares no external TCP/TLS target.

See [Milestone 4 verification](../testing/milestone-4-verification.md).
