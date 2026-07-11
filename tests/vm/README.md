# Disposable VM matrix

This optional suite creates disposable Vagrant/libvirt guests, installs Python, writes a temporary inventory, and runs readiness plus the Linux-baseline audit.

Defaults can be overridden:

- `SASD_VM_BOX_DEBIAN`
- `SASD_VM_BOX_UBUNTU`
- `SASD_VM_BOX_ROCKY`
- `SASD_VM_BOX_OPENSUSE`
- `SASD_VM_MEMORY`
- `SASD_VM_CPUS`

Because Vagrant box availability changes independently of this repository, verify or override box names in your environment. The suite is intentionally not part of hosted CI.
