# Role: `sasd_ssh_server`

Audits OpenSSH and optionally manages one drop-in file. SSH is a high-risk area and therefore requires all three conditions:

1. `sasd_ssh_server_mode: apply`
2. `sasd_ssh_server_apply_confirmation: SASD_APPLY_LINUX_BASELINE`
3. `sasd_ssh_server_manage: true`

Before reload, the role validates the complete configuration with `sshd -t`. A failed validation restores the previous drop-in or removes a newly created invalid file. Always keep a second administrative session open during the first real-host test.
