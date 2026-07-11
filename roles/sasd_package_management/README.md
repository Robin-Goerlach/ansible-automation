# Role: `sasd_package_management`

Audits installed packages and approved repository files. Apply mode can write only repository files below the native APT, DNF/YUM, or Zypper repository directories, refresh metadata, and install explicitly listed packages.

## Safety

- audit mode is read-only;
- apply mode requires `SASD_APPLY_LINUX_BASELINE`;
- repository paths are restricted by a strict regular expression;
- repository files are backed up before replacement;
- packages are never upgraded implicitly by this role.

See [Linux baseline variables](../../docs/reference/linux-baseline-variables.md).
