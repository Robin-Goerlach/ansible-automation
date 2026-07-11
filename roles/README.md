# Roles

Roles contain focused reusable desired-state components. Public variables belong in `defaults/main.yml`, are validated through `meta/argument_specs.yml`, and are documented in the role README.

Implemented role groups:

- Milestone 1/2: system baseline, packages, users, sudo, SSH, time, logging, firewall;
- Milestone 3: Apache, Nginx, PHP, and certificate management.

Database, container, virtualization, monitoring, and backup-client placeholders remain reserved for later milestones.
