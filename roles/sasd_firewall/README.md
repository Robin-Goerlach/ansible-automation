# Role: `sasd_firewall`

Audits UFW and firewalld availability/status. Apply mode is intentionally high-risk and requires the global confirmation token, `sasd_firewall_manage: true`, and an explicit provider.

The UFW adapter supports allow/deny/reject port rules. The Milestone 2 firewalld adapter intentionally supports allow-port rules only; it fails rather than silently translating unsupported deny/reject semantics.

Always permit the active management path before enabling a firewall and test first on a disposable VM.
