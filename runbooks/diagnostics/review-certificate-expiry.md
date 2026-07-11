# Review certificate expiry

Use `certificates.json` to compare local files and remote TLS endpoints. Verify subject,
issuer, fingerprint, validity period, SNI name, verification mode, and remaining days.
Never replace certificate material from a diagnostics runbook; use the guarded Milestone 3
certificate role with its apply token and rollback checks.
