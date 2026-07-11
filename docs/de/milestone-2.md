# Meilenstein 2: Linux-Baseline

Version: `0.2.0`
Status: vollständig umgesetzt
Standardmodus: ausschließlich Audit

Meilenstein 2 implementiert eine wiederverwendbare Linux-Grundkonfiguration für Pakete, Repository-Dateien, Benutzer und Gruppen, SSH-Schlüssel, sudo, OpenSSH, Zeitsynchronisation, journald, logrotate, UFW/firewalld sowie Update- und Reboot-Abläufe.

## Sicherheitsmodell

Änderungen benötigen gleichzeitig:

```yaml
sasd_linux_baseline_mode: apply
sasd_linux_baseline_apply_confirmation: SASD_APPLY_LINUX_BASELINE
```

SSH und Firewall bleiben zusätzlich deaktiviert, bis `sasd_ssh_server_manage` beziehungsweise `sasd_firewall_manage` ausdrücklich auf `true` gesetzt werden. Ein Neustart benötigt den getrennten Schlüssel `SASD_REBOOT_MANAGED_NODES`.

## Empfohlenes Vorgehen

1. Privates Lab-Inventar erstellen.
2. Readiness- und Audit-Playbooks ausführen.
3. JSON-Berichte prüfen.
4. `--check --diff` mit dem Apply-Schlüssel ausführen.
5. Zuerst auf einer Wegwerf-VM testen.
6. SSH und Firewall separat und mit einer zweiten offenen Administrationssitzung einführen.
7. Produktion nur mit `--limit`, Wartungsfenster und dokumentiertem Rückweg ändern.

Siehe auch die [englische Meilenstein-Dokumentation](../milestones/milestone-2.md) und die [Variablenreferenz](../reference/linux-baseline-variables.md).
