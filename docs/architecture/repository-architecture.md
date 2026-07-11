# Repository architecture

## Design goals

The repository should remain understandable as it grows from a few playbooks into a broad operations library. It therefore separates reusable desired-state components from orchestration and incident-oriented procedures.

## Boundaries

### Roles

Roles express reusable system capabilities and desired state. They should be idempotent and should not assume a particular inventory layout beyond documented variables.

### Playbooks

Playbooks select hosts, compose roles, and implement operational workflows. They are grouped by intent so that a diagnostic action cannot be confused with a modifying remediation.

### Runbooks

Runbooks describe the human operational context. They define when automation is appropriate, what evidence is required, risk, rollback, and escalation.

### Inventories

Inventories describe environments and provide environment-specific variables. Public examples are stored here; confidential production data is not.

### Collections

The collection workspace is reserved for interfaces that have become stable enough to package and version independently as `sasd.operations`.

## Remediation architecture

A mature remediation should use the following conceptual stages:

```text
preflight -> diagnose -> backup -> remediate -> restart/reload -> validate -> report
```

A failure in a later stage must not silently erase diagnostic evidence. Where a `block` and `rescue` structure is used, the runbook must explain exactly which states are recoverable.

## Risk levels

| Level | Meaning | Typical action |
|---|---|---|
| 0 | Read-only | Collect status and logs |
| 1 | Low-risk correction | Start a known service or refresh safe metadata |
| 2 | Controlled change | Replace configuration with backup and validation |
| 3 | Potentially destructive | Filesystem cleanup, restore, or database recovery |

Levels 2 and 3 normally require an explicit confirmation variable. Level 3 also normally requires a maintenance window and independently verified backup.
