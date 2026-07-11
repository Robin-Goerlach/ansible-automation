# Creating a role

A role should provide one cohesive capability. Include at least:

- `README.md` with purpose, supported platforms, variables, and examples;
- `defaults/main.yml` for public overridable defaults;
- `tasks/main.yml` with fully qualified module names;
- `handlers/main.yml` when services are notified;
- `meta/main.yml` with role metadata;
- tests appropriate to the behavior.

Defaults should be safe. A role that can remove data, close remote access, or restart critical infrastructure needs stronger safeguards than a normal package role.
