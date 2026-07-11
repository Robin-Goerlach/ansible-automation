# Milestone 2 verification

## Static suite

```bash
scripts/test.sh
```

It validates manifests, Markdown links, inventory, YAML, shell syntax, production-profile `ansible-lint`, and syntax of all playbooks.

## Safe runtime suite

```bash
scripts/verify-milestone-2.sh
```

The suite uses only the localhost example inventory and audit mode. It runs:

- control-node validation;
- connectivity and readiness;
- each Milestone 2 role contract;
- complete Linux-baseline audit;
- update audit;
- JSON parsing and schema assertions.

It never supplies apply or reboot confirmation tokens.

## Optional disposable-VM matrix

```bash
cd tests/vm
./run-matrix.sh
```

Requirements: Vagrant, libvirt/KVM, the vagrant-libvirt plugin, sufficient local resources, and reachable Vagrant boxes. Environment variables can override every box name. This test is not executed on hosted CI because nested virtualization is not assumed.
