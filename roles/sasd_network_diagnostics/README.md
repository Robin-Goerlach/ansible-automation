# sasd_network_diagnostics

Collects addresses, routes, resolver configuration, listening TCP/UDP
sockets, selected DNS resolutions, and optional outbound TCP connection
checks. No payload is sent to tested TCP services.

External DNS names and TCP targets are never implied. The public inventory
resolves only `localhost` and declares no outbound target.
