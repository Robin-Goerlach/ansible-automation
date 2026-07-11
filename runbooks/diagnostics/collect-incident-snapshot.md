# Collect an incident snapshot

## Purpose

Capture correlated evidence before a troubleshooting or remediation attempt changes state.

## Procedure

1. Assign a non-sensitive incident ID.
2. Confirm the inventory and `--limit` expression.
3. Review configured DNS, TCP, certificate, and TLS targets.
4. Run `playbooks/diagnostics/incident-snapshot.yml`.
5. Open `summary.json` first, then inspect component reports.
6. Record collection time, host scope, and any unavailable diagnostic tools.

## Stop conditions

Stop if the inventory scope is broader than intended, a declared target is external without
approval, or package-query cost is unacceptable for the incident window.
