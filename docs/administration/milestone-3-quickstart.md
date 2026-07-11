# Milestone 3 quick start

## 1. Run the safe acceptance suite

```bash
scripts/test.sh
scripts/verify-milestone-3.sh
```

## 2. Audit a private web-server group

```bash
ansible-playbook -i inventories/lab/hosts.yml \
  playbooks/diagnostics/web-services-status.yml \
  --limit lab-web-01
```

## 3. Preview an Apache deployment

```bash
ansible-playbook -i inventories/lab/hosts.yml \
  playbooks/provisioning/web-services.yml \
  --limit lab-web-01 --check --diff \
  -e sasd_web_services_mode=apply \
  -e sasd_web_services_apply_confirmation=SASD_APPLY_WEB_SERVICES
```

The private inventory must set `sasd_web_services_server: apache` and `sasd_apache_manage: true`. Check mode previews file and package actions but cannot prove a post-change service configuration test. Perform the first real apply only in a disposable VM.

## 4. Apply to one laboratory host

```bash
ansible-playbook -i inventories/lab/hosts.yml \
  playbooks/provisioning/web-services.yml \
  --limit lab-web-01 --diff \
  -e sasd_web_services_mode=apply \
  -e sasd_web_services_apply_confirmation=SASD_APPLY_WEB_SERVICES
```

## 5. Validate endpoints

```bash
ansible-playbook -i inventories/lab/hosts.yml \
  playbooks/validation/web-endpoints.yml \
  --limit lab-web-01
```

Declare endpoints in private group or host variables. Keep credentials out of URLs. Checks containing request headers automatically use `no_log`; `no_log: true` can additionally protect other sensitive declarations.
