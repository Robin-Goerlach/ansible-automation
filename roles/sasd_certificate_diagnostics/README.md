# sasd_certificate_diagnostics

Inspects explicitly declared certificate files and TLS endpoints. Reports
include metadata, SHA-256 fingerprint, validity window, remaining days,
TLS version, and cipher where available.

Private keys are never read. Remote TLS checks send only the TLS handshake.
Certificate verification defaults to true and must be disabled explicitly
for a private laboratory endpoint.
