# Role: `sasd_sudo_configuration`

Writes only explicitly declared `/etc/sudoers.d/<name>` files. Every present entry is validated with `/usr/sbin/visudo -cf` before replacement and written with mode `0440`.

Example declaration:

```yaml
sasd_sudo_configuration_entries:
  - name: sasd-operators
    content: "%sasd-operators ALL=(ALL:ALL) ALL"
```
