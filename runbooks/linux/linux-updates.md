# Runbook: Linux updates

Risk: 2

Run update audit, verify backups and free disk space, select `safe` or `full`, preview with check mode where the package manager supports it, and apply in batches. Updates never reboot. Review `/var/run/reboot-required` and schedule the separate reboot playbook when required.
