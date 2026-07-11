# Milestone 3 verification

## Static suite

```bash
scripts/test.sh
```

This validates manifests, Markdown links, public inventory safety, YAML, shell syntax, Ansible production-profile linting, and every discovered playbook.

## Safe runtime suite

```bash
scripts/verify-milestone-3.sh
```

The runtime suite:

1. removes previous generated Milestone 3 reports;
2. runs all four roles against localhost in audit mode;
3. asserts that every write opt-in remains false;
4. validates the consolidated and component JSON schemas;
5. renders Apache HTTP/TLS, Nginx HTTP/TLS/PHP, and PHP INI templates into `reports/`;
6. starts a local HTTP service, validates it with `ansible.builtin.uri`, and checks report redaction;
7. checks expected directives in every rendered template.

It does not install packages, alter `/etc`, or start managed services. The temporary HTTP listener binds only to `127.0.0.1` and is removed when verification ends.

## Optional check-mode exercise

`tests/web/check-mode-apply.yml` exercises managed paths with `--check --diff`. The file is syntax- and lint-checked automatically. Run it role-by-role in a disposable VM because check mode cannot prove service behavior and repeated local filesystem probes can be unreliable in restricted build containers.

## Disposable VM acceptance

Before production use, execute a reviewed apply in disposable VMs for every supported distribution and service combination. Required checks include first apply, second-run idempotence, deliberate invalid configuration rollback, service reload, HTTP/HTTPS endpoint validation, and restoration from repository history or package defaults.
