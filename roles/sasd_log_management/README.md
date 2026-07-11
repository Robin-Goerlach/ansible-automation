# Role: `sasd_log_management`

Audits journald storage and disk usage. Apply mode installs logrotate, writes a journald drop-in, optionally creates persistent journal storage, and creates explicitly declared logrotate policies.

No application log path is managed unless it is declared in `sasd_log_management_logrotate_entries`.
