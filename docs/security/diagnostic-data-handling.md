# Diagnostic data handling

Diagnostic output is operationally sensitive even when it contains no password.
Hostnames, IP addresses, usernames, package versions, mounted paths, listening ports,
certificate subjects, and failure details can help an attacker understand an environment.

## Repository rules

- `reports/`, `diagnostic-bundles/`, and `artifacts/` are ignored by Git.
- Collectors do not request process command lines, environment variables, private keys,
  HTTP headers, cookies, or application response bodies.
- External checks must be explicitly declared in private inventory.
- Bundle staging rejects links and oversized files.
- JSON key redaction protects common secret fields before archiving.

## Operator responsibilities

1. Use a dedicated incident identifier without customer secrets in its name.
2. Limit collection to relevant hosts.
3. Review generated JSON before bundle creation.
4. Extract and review the final bundle in a private directory.
5. Transfer only through an approved encrypted channel.
6. Record recipient, purpose, retention period, and deletion confirmation.
7. Delete local copies when the incident retention requirement expires.

## Redaction limits

The builder redacts values based on JSON key names. It cannot reliably identify a token
embedded in a free-form error string or an organization-specific field with an innocent
name. A successfully built bundle is therefore not automatically safe to publish.
