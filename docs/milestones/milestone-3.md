# Milestone 3: Web services

Version: `0.3.0`
Status: complete
Default behavior: audit-only

## Objective

Milestone 3 adds production-oriented web-service automation without weakening the repository safety model. Apache, Nginx, PHP, and TLS certificates are independent roles and can be audited together or applied selectively.

## Role boundaries

| Role | Responsibility | Default write behavior |
|---|---|---|
| `sasd_apache` | packages, service, Debian modules, virtual hosts | disabled |
| `sasd_nginx` | packages, service, virtual hosts | disabled |
| `sasd_php` | CLI/FPM packages, extensions, explicit INI drop-ins | disabled |
| `sasd_certificate_management` | certificate/key audit, deployment, self-signed lab pairs | disabled |

## Safety contract

Apply mode requires:

```yaml
sasd_web_services_mode: apply
sasd_web_services_apply_confirmation: SASD_APPLY_WEB_SERVICES
```

Each component additionally requires its own `manage: true` variable. Selecting both Apache and Nginx is refused unless `sasd_web_services_allow_dual_server: true`; the operator remains responsible for non-conflicting addresses and ports.

Configuration files are captured before change. Apache and Nginx execute full native configuration tests before reload. PHP validates CLI startup and FPM configuration where available. Certificate deployment validates syntax and certificate/private-key correspondence. A failed validation restores the prior file state and stops the play.

## Supported platform families

Mappings cover Debian/Ubuntu, Red Hat-compatible/Fedora, and openSUSE package and service conventions. Exact package streams, PHP versions, FPM service names, TLS module availability, and repository-specific paths must be verified in disposable VMs before production rollout.

## Acceptance criteria

- all YAML and shell files pass static validation;
- `ansible-lint` passes the production profile;
- every playbook passes syntax-check;
- the safe localhost suite executes all four roles in audit mode;
- every role emits a versioned valid JSON report;
- the consolidated report contains all four role contracts;
- Apache, Nginx, TLS, and PHP templates render in an isolated directory;
- public inventory remains localhost-only and audit-only;
- no web-service write occurs without the exact token and component opt-in;
- rollback behavior and operational procedures are documented.

See [Milestone 3 verification](../testing/milestone-3-verification.md).
