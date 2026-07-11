# Web-services variable reference

## Global orchestration

| Variable | Default | Purpose |
|---|---|---|
| `sasd_web_services_mode` | `audit` | `audit` or `apply` |
| `sasd_web_services_apply_confirmation` | empty | exact apply token |
| `sasd_web_services_server` | `none` | `none`, `apache`, `nginx`, or `both` |
| `sasd_web_services_allow_dual_server` | `false` | explicit dual-server acknowledgement |
| `sasd_web_services_report_root` | `reports/web-services` | control-node report directory |

## Apache

- `sasd_apache_manage`: component write opt-in;
- `sasd_apache_packages`: override distribution package mapping;
- `sasd_apache_modules`: Debian-family modules passed to `a2enmod`;
- `sasd_apache_virtual_hosts`: declarative virtual hosts;
- `sasd_apache_manage_service`: enable/start/reload service;
- `sasd_apache_service_name`: optional service-name override.

Virtual-host keys include `name`, `state`, `server_name`, `server_aliases`, `address`, `port`, `document_root`, `directory_options`, `allow_override`, `tls`, certificate paths, log paths, and `extra_directives`.

## Nginx

- `sasd_nginx_manage`;
- `sasd_nginx_packages`;
- `sasd_nginx_virtual_hosts`;
- `sasd_nginx_manage_service`;
- `sasd_nginx_service_name`.

Virtual-host keys include `name`, `state`, `server_name`, aliases, address, port, `default_server`, `ipv6`, `document_root`, `index`, `fallback`, TLS paths, `php_fpm_socket`, logs, and `extra_directives`.

## PHP

- `sasd_php_manage`;
- `sasd_php_packages`;
- `sasd_php_extension_packages`;
- `sasd_php_ini_files`;
- `sasd_php_manage_fpm_service`;
- `sasd_php_fpm_service_name`.

Each INI declaration requires an approved `/etc/php.../*.ini` path and a `settings` mapping. The role intentionally does not infer production version directories.

## Certificates

- `sasd_certificate_management_manage`;
- `sasd_certificate_management_certificates`;
- `sasd_certificate_management_minimum_remaining_days`.

Certificate entries use `name`, `state`, `source`, `certificate_path`, `private_key_path`, and optional modes. `source: provided` requires certificate and key content from a protected secret source. `source: self_signed` supports `subject`, `key_bits`, and `validity_days` and is intended for labs.

## Endpoints

`sasd_web_validation_endpoints` entries use `name`, `url`, `status_codes`, `headers`, `validate_certs`, `timeout`, `return_content`, and optional `no_log`. Any declaration containing request headers is automatically protected with `no_log`; the generated report stores only sanitized status data.
