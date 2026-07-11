# Security Policy

## Reporting a vulnerability

Do not publish sensitive infrastructure information in a public issue. Contact the repository owner through an appropriate private channel and include only the minimum information required to reproduce the problem.

Do not include:

- passwords, tokens, Vault secrets, private keys, or cookies;
- customer or employee data;
- unredacted logs;
- internal hostnames, public exposure details, or complete network diagrams;
- production inventory files;
- diagnostic bundles that have not been reviewed and sanitized.

## Repository security requirements

- Secrets must never be committed in plaintext.
- Production inventory is external to this public repository.
- Sensitive tasks should use `no_log: true` where output can reveal credentials.
- Remediation playbooks must document risk and rollback.
- Third-party collections must be reviewed before use and constrained through `requirements.yml` or a later lock process.
- Bootstrap scripts must be reviewed before they are run with elevated privileges.

## Supported versions

Until the first tagged release, only the current `main` branch receives security fixes.
