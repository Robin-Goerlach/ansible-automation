# sasd_package_diagnostics

Collects installed package facts, selected package versions, known lock
paths, reboot-required state, and a bounded read-only update simulation.

The role never refreshes metadata and never installs or removes packages.
Update output is intentionally capped because complete package inventories
can make incident bundles unnecessarily large.
