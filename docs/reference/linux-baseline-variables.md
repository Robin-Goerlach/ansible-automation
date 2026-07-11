# Linux baseline variable reference

## Global

| Variable | Default | Purpose |
|---|---|---|
| `sasd_linux_baseline_mode` | `audit` | `audit` or `apply` |
| `sasd_linux_baseline_apply_confirmation` | empty | must equal `SASD_APPLY_LINUX_BASELINE` in apply mode |
| `sasd_linux_baseline_report_enabled` | `true` | write consolidated JSON |
| `sasd_linux_baseline_report_root` | `reports/linux-baseline` | local report directory |

## Packages

- `sasd_package_management_manage`
- `sasd_package_management_packages`
- `sasd_package_management_repository_files`
- `sasd_package_management_update_cache`

Repository entries use `path`, `state`, and, for present files, `content`. Paths are restricted to native repository directories.

## Users and sudo

- `sasd_user_management_groups`
- `sasd_user_management_users`
- `sasd_sudo_configuration_entries`

User entries may contain `name`, `state`, `uid`, `group`, `groups`, `shell`, `home`, and `authorized_keys`. Sudo entries contain `name`, `state`, and complete validated `content`.

## SSH

- `sasd_ssh_server_manage` defaults to `false`;
- `sasd_ssh_server_port`;
- `sasd_ssh_server_password_authentication`;
- `sasd_ssh_server_permit_root_login`;
- `sasd_ssh_server_allow_groups`.

## Time and logging

- `sasd_time_synchronization_provider`: `auto`, `systemd-timesyncd`, or `chrony`;
- `sasd_time_synchronization_servers`;
- `sasd_log_management_journal_storage`;
- `sasd_log_management_system_max_use`;
- `sasd_log_management_logrotate_entries`.

## Firewall

- `sasd_firewall_manage` defaults to `false`;
- `sasd_firewall_provider`: `none`, `ufw`, or `firewalld`;
- `sasd_firewall_rules`: list of `port`, `protocol`, `source`, and `action`.

The firewalld adapter currently accepts allow-port rules only and fails on unsupported deny/reject declarations.
