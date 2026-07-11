# Role: sasd_apache

Audit-first Apache installation and virtual-host management for Debian/Ubuntu, Red Hat-compatible systems, Fedora, and openSUSE.

## Safety

The role is read-only by default. Changes require all three conditions:

```yaml
sasd_apache_mode: apply
sasd_apache_apply_confirmation: SASD_APPLY_WEB_SERVICES
sasd_apache_manage: true
```

Every changed virtual host is followed by a complete Apache configuration test. A failed test restores the previous file and enablement link before the play stops. Service reload is handler-driven and only occurs after successful validation.

## Virtual host declaration

```yaml
sasd_apache_virtual_hosts:
  - name: example-http
    server_name: example.test
    server_aliases: [www.example.test]
    address: "*"
    port: 80
    document_root: /var/www/example.test
    allow_override: None
    directory_options: FollowSymLinks
    state: present
```

TLS declarations additionally require `certificate_path` and `private_key_path`. Certificate material is managed by the separate `certificate_management` role.

See [Web-services variables](../../docs/reference/web-services-variables.md) and [Apache deployment runbook](../../runbooks/web/apache-deployment.md).
