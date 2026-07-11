# Runbook: Apply the Linux baseline

Risk: 2
Automatic execution: prohibited without explicit approval

## Preconditions

- tested private inventory;
- current backup or recoverable VM snapshot;
- working sudo/become path;
- successful readiness and audit runs;
- reviewed `--check --diff` output;
- SSH and firewall disabled unless their dedicated runbooks are complete.

## Execution

Use a single test host and the exact apply token. Save the Ansible output and generated JSON report.

## Validation

Run `playbooks/validation/linux-baseline.yml`, verify services, reconnect through a fresh SSH session, and compare the consolidated report.

## Rollback

Use module-generated backup files for changed configuration, restore the VM snapshot when appropriate, or apply the documented previous desired state. Do not improvise an account/firewall rollback through the same broken remote path.
