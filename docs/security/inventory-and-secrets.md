# Inventory and secrets

The public repository must not contain real production topology or credentials.

## Acceptable content

- example hostnames such as `web01.example.invalid`;
- variable names without secret values;
- encrypted Vault files only when their metadata is safe to publish;
- documentation and templates.

## Prohibited content

- passwords and tokens;
- Vault password files;
- private keys;
- customer-identifying data;
- unredacted support bundles;
- production host lists and exposure details.

Ansible Vault protects data at rest in a repository, but decrypted values may still appear in process output, temporary files, backups, or logs. Use `no_log: true` where a module invocation could expose a secret and review the operational environment as a whole.
