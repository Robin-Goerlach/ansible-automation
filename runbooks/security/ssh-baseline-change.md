# Runbook: Change the SSH baseline

Risk: 3

Keep an existing root-capable session open. Confirm console or hypervisor access. Ensure the new port is permitted by the network and firewall before changing SSH. Run check mode, apply to one disposable VM, then one lab host. The role validates `sshd -t` and restores the previous drop-in on failure, but it cannot protect against every semantically valid lockout.
