# Milestone 4 diagnostic acceptance helpers

`verify_milestone4.py` prepares a deterministic redaction canary and verifies
all Milestone 4 JSON reports plus the generated diagnostic archive.

The helper is used by `scripts/verify-milestone-4.sh`; it does not contact
managed hosts and writes only below ignored local artifact directories.
