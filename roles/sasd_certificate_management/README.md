# Role: sasd_certificate_management

Guarded TLS certificate deployment, self-signed laboratory certificate generation, key-pair verification, and expiry auditing.

## Safety

```yaml
sasd_certificate_management_mode: apply
sasd_certificate_management_apply_confirmation: SASD_APPLY_WEB_SERVICES
sasd_certificate_management_manage: true
```

Certificate and private-key destinations are restricted to approved system TLS directories. Provided private-key content is handled with `no_log: true`. After deployment, OpenSSL validates certificate syntax and confirms that the certificate and key expose the same public key. A failure restores both previous files.

Self-signed generation is intended for laboratories. It refuses partial existing state and never silently overwrites an existing pair.

Production secret values belong in Ansible Vault or an external secret system, not plain inventory files.
