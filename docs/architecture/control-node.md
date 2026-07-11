# Control node

Ansible executes from a Linux control node. A dedicated management VM or WSL2 environment is preferable to an uncontrolled workstation installation.

The bootstrap script creates a Python virtual environment rather than installing Ansible into the system Python. This reduces conflicts with distribution-managed Python packages and makes the tooling replaceable.

The managed hosts do not normally need Ansible installed. Linux hosts generally require SSH, a suitable account, privilege escalation where needed, and Python for ordinary modules.
