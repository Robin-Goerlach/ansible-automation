# Role: sasd_nginx

Audit-first Nginx installation and virtual-host management for Debian/Ubuntu, Red Hat-compatible systems, Fedora, and openSUSE.

## Safety

```yaml
sasd_nginx_mode: apply
sasd_nginx_apply_confirmation: SASD_APPLY_WEB_SERVICES
sasd_nginx_manage: true
```

Every changed server block is followed by `nginx -t`. A failed validation restores the previous file and enablement state before aborting. Reload occurs only through a handler after successful validation.

## Virtual host declaration

```yaml
sasd_nginx_virtual_hosts:
  - name: example-http
    server_name: example.test
    server_aliases: [www.example.test]
    port: 80
    document_root: /var/www/example.test
    index: [index.html]
    state: present
```

Optional TLS and PHP-FPM settings are described in [Web-services variables](../../docs/reference/web-services-variables.md).
