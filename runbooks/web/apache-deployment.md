# Runbook: Deploy an Apache virtual host

## Preconditions

- Limit the target explicitly and verify current access.
- Review DNS, firewall, listening port, document root, and certificate paths.
- Pass a disposable-VM apply before production.

## Procedure

1. Run `playbooks/diagnostics/web-services-status.yml`.
2. Add the declaration to private inventory variables.
3. Preview with `--check --diff` and the exact apply token.
4. Apply to one laboratory host.
5. Confirm the native Apache configuration test and handler result.
6. Validate HTTP/HTTPS with the expected Host header.
7. Expand the limit gradually.

## Rollback

A failed configuration test restores the immediately previous managed file and enablement state. For a successful but unwanted change, revert the declaration or repository commit and apply the previous desired state. Maintain independent content and database backups.
