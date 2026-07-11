# Role: sasd_php

Audit-first PHP CLI, PHP-FPM, extension-package, and INI drop-in management.

## Safety

```yaml
sasd_php_mode: apply
sasd_php_apply_confirmation: SASD_APPLY_WEB_SERVICES
sasd_php_manage: true
```

The role never guesses production INI paths. Declare each managed drop-in explicitly. After a change, PHP CLI startup and, where available, PHP-FPM configuration are validated. Failed validation restores the previous file.

```yaml
sasd_php_ini_files:
  - path: /etc/php/8.3/fpm/conf.d/99-sasd.ini
    settings:
      expose_php: 'Off'
      memory_limit: 256M
      upload_max_filesize: 32M
```

Package names and FPM service names can be overridden for distribution repositories or third-party PHP streams.
