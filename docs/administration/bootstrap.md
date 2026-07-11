# Bootstrap administration guide

## Control-node bootstrap

The pinned Milestone 2 control-node toolchain requires Python 3.12 or newer. If the distribution-provided `python3` is older, install a supported Python runtime before running the bootstrap or point the workflow at a suitable control node.


Run `bootstrap/bootstrap-control-node.sh --help` to inspect available options. The script uses the operating-system package manager for prerequisites and a dedicated Python virtual environment for Ansible tooling.

Use `--update` only when the existing checkout has no local modifications. The script intentionally refuses to overwrite an unrelated target directory or update a dirty checkout.

## Managed-node bootstrap

Run `playbooks/bootstrap/managed-linux.yml` when a Linux host does not have Python 3. This is one of the limited legitimate uses of the `raw` module.

After bootstrap, use normal Ansible modules and facts rather than continuing to manage the machine through raw commands.
