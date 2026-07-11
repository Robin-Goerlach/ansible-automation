# Remediation: Short descriptive title

## Metadata

| Field | Value |
|---|---|
| Remediation ID | `SASD-AREA-000` |
| Status | Draft |
| Risk level | 0, 1, 2, or 3 |
| Supported platforms | Define explicitly |
| Related playbook | `playbooks/remediation/...` |
| Check mode | Supported, partial, or unsupported |
| Backup required | Yes or no |
| Rollback available | Yes, partial, or no |

## Symptoms

Describe the observable failure without assuming a cause.

## Detection criteria

List the evidence required before the remediation is considered applicable.

## Possible causes

Document known causes and how they are distinguished.

## Preconditions

State required access, maintenance window, backups, free space, dependencies, and approvals.

## Risk assessment

Describe possible service interruption, data loss, access lockout, or collateral changes.

## Automated procedure

Provide the exact command and required variables. Higher-risk operations should require an explicit confirmation variable.

```bash
ansible-playbook -i INVENTORY playbooks/remediation/EXAMPLE.yml --check --diff
```

## Manual procedure

Document manual alternatives and steps that cannot be automated safely.

## Validation

Define objective success criteria and commands or monitoring checks.

## Rollback

Document how to restore the previous state and the limits of rollback.

## Evidence and reporting

State where diagnostic and result artifacts are written and how sensitive content is sanitized.

## Escalation

Define when automation must stop and the issue should be escalated.
