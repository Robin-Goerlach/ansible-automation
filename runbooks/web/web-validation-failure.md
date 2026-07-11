# Runbook: Web validation failure

1. Stop rollout expansion.
2. Preserve Ansible output and generated JSON reports.
3. Run native configuration tests directly with privilege escalation.
4. Inspect service status, journal, error logs, sockets, firewall, DNS, and certificate paths.
5. Confirm whether Ansible restored the previous managed file.
6. Revert the desired-state declaration when the new configuration is unsafe.
7. Never bypass native validation merely to complete automation.
