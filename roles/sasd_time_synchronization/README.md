# Role: `sasd_time_synchronization`

Selects `systemd-timesyncd` automatically on Debian-family systems and chrony on Red Hat/SUSE families. A provider can be selected explicitly. Audit mode queries service state and `timedatectl` without changing the host.
