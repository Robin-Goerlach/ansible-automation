# Remediation framework

A remediation playbook is not a generic troubleshooting script. It should act only when its detection criteria identify a known state.

Required design properties:

- stable remediation ID;
- explicit target scope;
- read-only diagnosis before modification;
- safe failure when the cause is ambiguous;
- backup before changing configuration or data;
- validation before and after service operations;
- structured result information;
- documented rollback and escalation.

Destructive tasks should carry clear tags such as `destructive` and `never`, but tags alone are not a sufficient safety mechanism. Use confirmation variables and assertions as well.
