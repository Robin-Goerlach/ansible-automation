# Runbook: Change the firewall baseline

Risk: 3

Declare the active SSH management port before enabling the provider. Test the exact distribution/provider combination in a disposable VM. Apply with `--limit` to one host, verify a new SSH connection and required service ports, and keep console access available. The role never flushes the complete ruleset.
