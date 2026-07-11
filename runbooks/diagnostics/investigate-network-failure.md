# Investigate a network failure

Review interfaces, routes, resolver configuration, listening sockets, DNS results, and
explicit TCP checks in `network.json`. A successful TCP handshake proves only that a port
accepted a connection; it does not validate application protocol, authorization, or data.
