# sasd_service_diagnostics

Collects service facts, failed systemd units where available, and the
state of explicitly monitored service names.

The role does not treat every stopped service as failed. Only explicit
failed states and missing declared services produce issues.

Service names are manager-specific. For systemd, declare the complete
key shown by `service_facts`, commonly such as `sshd.service`.
