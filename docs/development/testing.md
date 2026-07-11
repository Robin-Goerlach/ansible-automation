# Testing

## Local checks

```bash
make install
make collections
make test
```

## Test layers

1. YAML and Ansible linting
2. inventory parsing
3. playbook syntax checks
4. role convergence and idempotence
5. verification assertions
6. integration tests on disposable systems
7. controlled acceptance in a representative lab

Container tests are not sufficient for every systems-administration task. Use disposable VMs for kernel, boot, storage, network, systemd, virtualization, and recovery behavior.
