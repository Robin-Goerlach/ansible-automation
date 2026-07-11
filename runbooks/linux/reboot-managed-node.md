# Runbook: Reboot a managed Linux node

Risk: 3

Confirm service redundancy, maintenance window, console access, and successful pre-reboot health checks. Use `playbooks/maintenance/linux-reboot.yml` with `--limit` and the exact token `SASD_REBOOT_MANAGED_NODES`. The default serial value is one host.
