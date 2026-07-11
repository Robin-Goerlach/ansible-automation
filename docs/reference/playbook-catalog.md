# Playbook catalog

| ID | Path | Risk | Default |
|---|---|---:|---|
| SASD-M1-VAL-001 | `playbooks/validation/control-node.yml` | 0 | read-only |
| SASD-M1-VAL-002 | `playbooks/validation/connectivity.yml` | 0 | read-only |
| SASD-M1-VAL-003 | `playbooks/validation/managed-node-readiness.yml` | 0 | read-only |
| SASD-M1-DIA-001 | `playbooks/diagnostics/system-overview.yml` | 0 | read-only |
| SASD-M2-PRV-001 | `playbooks/provisioning/linux-baseline.yml` | 2 | audit |
| SASD-M2-MNT-001 | `playbooks/maintenance/linux-updates.yml` | 2 | audit |
| SASD-M2-MNT-002 | `playbooks/maintenance/linux-reboot.yml` | 3 | refused without token |
| SASD-M3-PRV-001 | `playbooks/provisioning/web-services.yml` | 2 | audit |
| SASD-M3-PRV-002 | `playbooks/provisioning/apache-webserver.yml` | 2 | audit |
| SASD-M3-PRV-003 | `playbooks/provisioning/nginx-webserver.yml` | 2 | audit |
| SASD-M3-PRV-004 | `playbooks/provisioning/php-runtime.yml` | 2 | audit |
| SASD-M3-PRV-005 | `playbooks/provisioning/tls-certificates.yml` | 2 | audit |
| SASD-M3-DIA-001 | `playbooks/diagnostics/web-services-status.yml` | 0 | read-only |
| SASD-M3-VAL-001 | `playbooks/validation/web-services.yml` | 0 | read-only |
| SASD-M3-VAL-002 | `playbooks/validation/web-endpoints.yml` | 0 | read-only |
| SASD-M3-SITE-001 | `playbooks/site-web.yml` | 2 | audit |

Risk levels are defined in [risk classification](../security/risk-classification.md).
