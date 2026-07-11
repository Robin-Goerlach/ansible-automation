# Runbook: Deploy an Nginx virtual host

Audit the host, declare the server block in private inventory, preview with `--check --diff`, apply to one disposable or laboratory host, and validate with `nginx -t` plus HTTP/HTTPS requests. The role restores the previous file and enablement link when native validation fails. Revert a successful but undesired change by restoring the previous declaration and applying it again.
