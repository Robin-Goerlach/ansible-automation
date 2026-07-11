# Changelog

## [0.4.0] - 2026-07-09

### Added

- Complete Milestone 4 diagnostics platform.
- Resource, service, package, network, certificate, and bundle roles.
- Correlated incident snapshots with versioned JSON contracts and host summaries.
- Controller-side summary reconstruction for separated or interrupted component runs.
- Explicit DNS, TCP, certificate-file, and TLS-endpoint checks.
- Sanitized `tar.gz` bundles with manifests, file-size boundaries, and SHA-256 checksums.
- Milestone 4 runbooks, English documentation, German documentation, CI, and acceptance tests.

### Changed

- Repository status, roadmap, catalogs, and quality workflow now target version `0.4.0`.
- `create-diagnostic-bundle.sh` now requires an existing run ID and uses the guarded bundle role.

## [0.3.0] - 2026-07-09

### Added

- Complete Milestone 3 web-services automation.
- Apache role with package, service, Debian module, virtual-host, native validation, and rollback support.
- Nginx role with package, service, virtual-host, native validation, and rollback support.
- PHP role for CLI/FPM packages, extension packages, explicit INI drop-ins, and runtime validation.
- Certificate role for expiry audits, guarded deployment, key-pair validation, rollback, and self-signed lab pairs.
- Consolidated web-services and component JSON reports.
- HTTP/HTTPS endpoint validation playbook.
- Isolated Apache, Nginx, and PHP template-rendering acceptance tests.
- Milestone 3 manifests, runbooks, English documentation, and German documentation.

### Safety

- Managed-node changes require `sasd_web_services_mode=apply`, the exact token `SASD_APPLY_WEB_SERVICES`, and a component-specific manage opt-in.
- Apache-plus-Nginx apply is refused without an explicit dual-server acknowledgement.
- Native configuration tests execute before reload; failed changes restore previous files and links.
- Private-key content is handled with `no_log: true` and omitted from reports.
- Endpoint declarations containing request headers automatically use `no_log`; reports retain only sanitized status data.

## [0.2.0] - 2026-07-09

### Added

- Complete Milestone 2 Linux baseline.
- Package and native repository-file management with controlled update-cache behavior.
- Declarative local users, groups, home directories, and managed SSH authorized keys.
- Validated sudo drop-ins with `visudo` preflight.
- SSH server drop-in management with pre-change capture, validation, automatic rollback, and reload handlers.
- Time synchronization abstraction for `systemd-timesyncd` and chrony.
- Persistent journald and optional logrotate policy management.
- Audit-first firewall abstraction for UFW and firewalld with explicit high-risk opt-in.
- Safe/full Linux update policy and separately confirmed reboot playbook.
- Consolidated Linux-baseline JSON reports written on the control node.
- Milestone 2 manifests, acceptance suite, runbooks, English documentation, and German documentation.
- Optional Vagrant/libvirt disposable-VM matrix for Debian, Ubuntu, Rocky Linux, and openSUSE.

### Changed

- `playbooks/provisioning/linux-baseline.yml` now orchestrates the complete Milestone 2 role set.
- CI, Make targets, manifests, playbook catalog, role catalog, and repository roadmap now describe version 0.2.0.
- The public example inventory remains localhost-only and audit-only.

### Safety

- Managed-node changes require both `sasd_linux_baseline_mode=apply` and the exact confirmation token `SASD_APPLY_LINUX_BASELINE`.
- SSH and firewall management remain disabled unless separately enabled.
- SSH configuration is validated before reload and restored automatically when validation fails.
- Reboots require the independent token `SASD_REBOOT_MANAGED_NODES`.

## [0.1.0] - 2026-07-09

### Added

- Complete Milestone 1 repository foundation.
- Linux/WSL control-node bootstrap and managed-Linux Python bootstrap.
- Safe localhost-only example inventory.
- Control-node, connectivity, and managed-node readiness playbooks.
- Read-only system overview with local JSON reports.
- Audit-first `sasd_system_baseline` role with argument specifications.
- Double opt-in before package installation.
- Machine-readable milestone, playbook, and role manifests.
- Documentation-link and manifest validators.
- Production-profile Ansible linting and complete syntax discovery.
- Safe localhost acceptance suite and consolidated GitHub Actions workflow.
- English Milestone 1 documentation and German summary.
