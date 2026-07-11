# Runbook: Deploy TLS certificate material

- Production private keys must originate from Ansible Vault or an approved secret system.
- Never commit decrypted key content.
- Verify subject/SANs, issuer, chain, validity, permissions, and target paths.
- Deploy certificate material before enabling a TLS virtual host.
- Validate externally after service reload.

The role validates certificate syntax and public-key equality. A failed deployment restores both previous files. Self-signed mode is for laboratories and refuses partial existing pairs.
