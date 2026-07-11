# Milestone 1 verification

Milestone 1 acceptance has two explicit entry points:

```bash
# Static and structural quality gates
scripts/test.sh

# Safe localhost runtime acceptance
scripts/verify-milestone-1.sh
```

## Static checks

- milestone manifest references;
- repository-relative Markdown links;
- inventory graph and serialization;
- YAML style;
- `ansible-lint` production profile;
- shell syntax and optional ShellCheck;
- syntax of every playbook under `playbooks/` and `bootstrap/`.

## Safe execution checks

The public inventory uses local connection only. Runtime acceptance executes control-node validation, connectivity validation, managed-node readiness validation, read-only diagnostics with JSON parsing, and the baseline with `--check --diff`. Static and runtime checks are deliberately separate so CI can report their failures independently.

## Not certified by localhost testing

Disposable virtual machines are still required to test Python installation on a Python-free target, sudo behavior, SSH onboarding, distribution-specific package managers, and package installation in apply mode.
