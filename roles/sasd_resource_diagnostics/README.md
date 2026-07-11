# sasd_resource_diagnostics

Collects CPU load, memory, swap, filesystem capacity, inode pressure,
and bounded top-process samples without changing the managed node.

Threshold breaches are returned as structured issues. The role executes a
portable Python collector through Ansible's temporary script mechanism;
the collector is removed by Ansible after execution.

## Safety

- No privilege escalation is requested.
- No service, package, or configuration state is changed.
- Process command lines are not collected; only the executable name is kept.
- Reports may still contain hostnames, usernames, mount paths, and capacity data.
