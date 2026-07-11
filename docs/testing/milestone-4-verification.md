# Milestone 4 verification

## Static suite

```bash
scripts/test.sh
```

The static suite validates manifests, links, inventory, YAML, shell syntax, Python syntax,
Ansible syntax, and the `ansible-lint` production profile.

## Safe runtime suite

```bash
scripts/verify-milestone-4.sh
```

The runtime suite:

1. removes only the fixed `milestone4-localhost` test artifacts;
2. runs all five managed-node collector roles against localhost;
3. rebuilds the correlated summary from the component reports;
4. parses a committed public certificate fixture;
5. validates six JSON schemas;
6. injects secret canaries into a JSON fixture;
7. creates a sanitized diagnostic bundle;
8. confirms canaries are absent and ordinary values remain;
9. rejects links in the archive;
10. verifies the archive SHA-256 from the bundle result contract.

The suite does not change packages, services, network configuration, firewall state,
or certificate material on localhost.

## Disposable VM review

Before broad production use, run the snapshot against Debian/Ubuntu, EL-compatible,
and openSUSE VMs. Verify package-query behavior, service-manager output, filesystem
exclusions, network tool availability, runtime cost, and organization-specific redaction.
