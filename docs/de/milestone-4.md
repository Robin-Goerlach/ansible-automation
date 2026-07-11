# Milestone 4: Diagnose

Version: `0.4.0`
Status: abgeschlossen
Verhalten auf Zielsystemen: nur lesend

Milestone 4 sammelt zusammengehörige Diagnosedaten unter einer gemeinsamen Lauf-ID.
Erfasst werden CPU-Last, Arbeitsspeicher, Swap, Dateisysteme, Inodes, Prozesse, Dienste,
Pakete, Netzwerk, DNS, lauschende Ports sowie ausdrücklich angegebene Zertifikate und
TLS-Endpunkte.

## Wichtige Eigenschaften

- keine Installation, Konfigurationsänderung oder Dienststeuerung auf Zielsystemen;
- begrenzte Prozess- und Paketlisten;
- keine Prozess-Kommandozeilen und keine Umgebungsvariablen;
- keine privaten Schlüssel;
- keine externen Prüfziele ohne ausdrückliche Deklaration;
- versionierte JSON-Berichte und eine zusammenfassende `summary.json`;
- optionales Diagnosearchiv mit Manifest, SHA-256-Prüfsummen und JSON-Schlüsselredaktion.

## Sicherer Aufruf

```bash
ansible-playbook -i inventories/lab/hosts.yml   playbooks/diagnostics/incident-snapshot.yml   --limit lab-host-01   -e sasd_diagnostics_run_id=INC-2026-0042
```

Das Archiv wird anschließend separat erzeugt:

```bash
scripts/create-diagnostic-bundle.sh INC-2026-0042
```

Diagnoseberichte enthalten häufig interne Hostnamen, Adressen, Benutzernamen, Ports,
Paketstände und Pfade. Die automatische Redaction ist nur eine zusätzliche Sicherung.
Vor jeder Weitergabe muss das vollständige Archiv manuell geprüft werden.

Weitere Einzelheiten stehen in der [englischen Milestone-Dokumentation](../milestones/milestone-4.md),
der [Architektur](../architecture/diagnostics.md), der [Variablenreferenz](../reference/diagnostics-variables.md)
und den [Sicherheitshinweisen](../security/diagnostic-data-handling.md).
