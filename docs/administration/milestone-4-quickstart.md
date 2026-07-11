# Milestone 4 quick start

## 1. Validate the repository

```bash
scripts/test.sh
scripts/verify-milestone-4.sh
```

## 2. Define private diagnostic targets

Example private group variables:

```yaml
sasd_service_diagnostics_monitored_services:
  - ssh.service
  - apache2.service

sasd_network_diagnostics_dns_names:
  - internal.example

sasd_network_diagnostics_tcp_targets:
  - name: database
    host: db01.internal.example
    port: 5432

sasd_certificate_diagnostics_files:
  - name: web-certificate
    path: /etc/ssl/certs/web.example.pem

sasd_certificate_diagnostics_endpoints:
  - name: public-web
    host: web.example
    port: 443
    server_name: web.example
    validate_certs: true
```

Do not place confidential production inventory in the public example directories.

## 3. Start with one host

```bash
ansible-playbook -i inventories/lab/hosts.yml   playbooks/diagnostics/incident-snapshot.yml   --limit lab-host-01   -e sasd_diagnostics_run_id=INC-2026-0042
```

## 4. Review reports

```bash
find reports/diagnostics/INC-2026-0042 -type f -maxdepth 3 -print
python -m json.tool reports/diagnostics/INC-2026-0042/lab-host-01/summary.json
```

## Rebuild a summary after separate component runs

Every diagnostic area can be run independently with the same run ID. Rebuild the
correlated summary afterward without contacting the managed host for those component
checks again:

```bash
ansible-playbook -i inventories/lab/hosts.yml \
  playbooks/diagnostics/aggregate-reports.yml \
  --limit lab-host-01 \
  -e sasd_diagnostics_run_id=INC-2026-0042
```

This is useful after an interrupted combined collection or when the five component
playbooks are deliberately scheduled separately.

## 5. Build and review a bundle

```bash
scripts/create-diagnostic-bundle.sh INC-2026-0042

tar -tzf diagnostic-bundles/sasd-diagnostic-bundle-INC-2026-0042.tar.gz
sha256sum diagnostic-bundles/sasd-diagnostic-bundle-INC-2026-0042.tar.gz
```

Extract into a private temporary directory, inspect every file, and remove the extracted
copy after use. The automatic JSON redaction is not a substitute for human review.
