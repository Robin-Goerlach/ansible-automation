# Naming conventions

## Files and directories

Use lowercase kebab-free or underscore-separated names consistently within a category. Playbooks use descriptive lowercase names such as:

```text
linux-baseline.yml
system-overview.yml
apache-service-failed.yml
```

## Plays and tasks

Names should describe the observable action and object:

```yaml
- name: Validate the Apache configuration
```

Avoid names such as `Run command`, `Do setup`, or `Fix problem`.

## Variables

Project and role variables should use the `sasd_` prefix. Role public variables should include the role name when ambiguity is possible:

```text
sasd_system_baseline_manage_packages
sasd_system_baseline_packages
```

## Remediation IDs

Use a stable pattern:

```text
SASD-LINUX-001
SASD-WEB-001
SASD-DB-001
```
