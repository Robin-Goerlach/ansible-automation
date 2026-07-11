# Bootstrap

Milestone 2 contains two separate bootstrap paths:

- `bootstrap-control-node.sh` prepares a Linux or WSL control node, creates an isolated Python virtual environment, installs the development toolchain, clones the repository, and verifies the public inventory.
- `bootstrap-managed-linux.yml` prepares Linux managed nodes that do not yet provide Python 3. It uses `ansible.builtin.raw` only for this initial step and then switches to normal fact gathering.

## Control node

The pinned Milestone 2 control-node toolchain requires Python 3.12 or newer. If the distribution-provided `python3` is older, install a supported Python runtime before running the bootstrap or point the workflow at a suitable control node.


```bash
./bootstrap/bootstrap-control-node.sh --help
```

The script preserves SSH host-key checking and refuses to update a Git checkout containing local changes. Use `--skip-collections` when Ansible Galaxy is unavailable; Milestone 2 uses only `ansible.builtin` modules.

## Managed nodes

```bash
ansible-playbook -i inventories/lab-local/hosts.yml playbooks/bootstrap/managed-linux.yml --ask-become-pass
```

This is a real change operation. Review the inventory and target limit before execution.
