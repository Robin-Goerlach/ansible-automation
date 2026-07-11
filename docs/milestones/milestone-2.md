# Milestone 2: Linux baseline

Version: `0.2.0`
Status: complete
Default behavior: audit-only

## Objective

Milestone 2 turns the repository foundation into a reusable Linux operating-system baseline. The implementation covers package sources and packages, access administration, SSH, time, logging, firewall state, updates, reboot policy, reports, and optional disposable-VM verification.

## Role boundaries

| Role | Responsibility | Default write behavior |
|---|---|---|
| `sasd_package_management` | packages, repository files, metadata | audit |
| `sasd_user_management` | declared groups/users/authorized keys | audit |
| `sasd_sudo_configuration` | validated sudo drop-ins | audit |
| `sasd_ssh_server` | guarded OpenSSH drop-in | disabled |
| `sasd_time_synchronization` | timesyncd/chrony | audit |
| `sasd_log_management` | journald/logrotate | audit |
| `sasd_firewall` | UFW/firewalld | disabled |

## Safety contract

Apply mode is accepted only when both variables are supplied:

```yaml
sasd_linux_baseline_mode: apply
sasd_linux_baseline_apply_confirmation: SASD_APPLY_LINUX_BASELINE
```

SSH and firewall require additional `manage: true` switches. The example inventory never supplies these. Reboot is not part of baseline or update execution and has an independent playbook and token.

## Supported platform families

The role mappings cover current Debian/Ubuntu, Red Hat-compatible/Fedora, and openSUSE systems. Distribution-specific package names, service names, and syntax should always be verified in a disposable VM before production rollout.

## Acceptance criteria

- all YAML and shell files pass static validation;
- `ansible-lint` passes the production profile;
- every playbook passes syntax-check;
- the safe localhost suite executes all seven roles in audit mode;
- every role emits a versioned result schema and valid JSON report;
- the consolidated report contains all role results;
- no public inventory target exists except localhost;
- no apply or reboot action can run without its exact confirmation token;
- optional Vagrant/libvirt scenarios are documented and scriptable.

See [Milestone 2 verification](../testing/milestone-2-verification.md).
