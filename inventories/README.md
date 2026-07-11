# Inventories

The repository separates public examples from real environments.

- `example/` is version-controlled and targets localhost only.
- `lab/` contains policy guidance; create an ignored or private inventory for real lab systems.
- `production/` contains policy guidance only.

```bash
cp -a inventories/example inventories/lab-local
ansible-inventory -i inventories/lab-local/hosts.yml --graph
ansible-inventory -i inventories/lab-local/hosts.yml --list
```

Use `group_vars/` and `host_vars/` for non-secret values. Encrypt secrets with Ansible Vault or retrieve them from an approved secret manager. Never store the Vault password beside encrypted files.
