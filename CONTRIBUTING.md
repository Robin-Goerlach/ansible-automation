# Contributing

Contributions should keep the repository safe, understandable, and operationally conservative.

## Workflow

1. Create a focused branch.
2. Add or update documentation together with code.
3. Run `make test`.
4. Test changes against disposable lab systems.
5. Open a pull request describing risk, test coverage, and rollback.

## Commit messages

Use concise imperative subjects. Examples:

```text
Add managed-node Python bootstrap
Document remediation risk levels
Fix Debian package mapping
```

The repository foundation is intended for the commit:

```text
Initial commit
```

## Pull request expectations

A pull request should state:

- what problem it solves;
- which operating systems were tested;
- whether the change is read-only or modifying;
- whether check mode is supported;
- what data is backed up;
- how to validate success;
- how to roll back.

## Ansible style

- Use fully qualified collection names.
- Prefer modules over `command`, `shell`, and `raw`.
- Use `raw` only when normal modules cannot run, such as initial Python bootstrap.
- Use `changed_when: false` for diagnostic commands.
- Avoid broad `ignore_errors: true`.
- Use `block`, `rescue`, and `always` only with a documented recovery purpose.
- Keep defaults safe and non-destructive.
- Do not make an irreversible change without explicit documentation and confirmation.

## Empty directories

Git does not track empty directories. `.gitkeep` files are used only where the planned structure must remain visible before implementation.
