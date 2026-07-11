# Remediation playbooks

Remediation playbooks repair known and explicitly documented failure states. Every non-trivial remediation must have a matching runbook and should follow these phases:

1. preflight;
2. diagnose;
3. backup;
4. remediate;
5. reload or restart;
6. validate;
7. report.

Higher-risk remediation must require a confirmation variable and must not be hidden behind an ambiguous command name.
