# Milestone 3: Webdienste

Version: `0.3.0`
Status: abgeschlossen
Standardverhalten: ausschließlich Audit

Milestone 3 ergänzt Rollen für Apache, Nginx, PHP und TLS-Zertifikate. Keine Rolle verändert standardmäßig ein Zielsystem. Für Änderungen sind der globale Modus `apply`, der exakte Bestätigungstoken `SASD_APPLY_WEB_SERVICES` und der jeweilige komponentenspezifische `manage`-Schalter erforderlich.

## Schutzmaßnahmen

- Apache- und Nginx-Konfigurationen werden vor Änderungen gesichert.
- Nach jeder Virtual-Host-Änderung wird die vollständige Konfiguration geprüft.
- Bei einem Fehler werden Datei und Aktivierungslink wiederhergestellt.
- PHP-INI-Änderungen werden durch CLI-Start und, sofern vorhanden, FPM-Konfigurationstest geprüft.
- Zertifikat und privater Schlüssel werden auf Zusammengehörigkeit geprüft.
- Private Schlüssel und HTTP-Anforderungsheader werden nicht in Berichte geschrieben und bei der Verarbeitung automatisch mit `no_log` geschützt.
- Apache und Nginx gleichzeitig erfordern eine zusätzliche ausdrückliche Freigabe.

## Sicherer Test

```bash
scripts/test.sh
scripts/verify-milestone-3.sh
```

Die lokale Abnahme schreibt nur in das vom Git ausgeschlossene Verzeichnis `reports/`. Vor einem produktiven Einsatz muss jede Distribution und jede Kombination in einer kurzlebigen VM getestet werden.

Weitere Einzelheiten stehen in der [englischen Milestone-Dokumentation](../milestones/milestone-3.md), der [Architektur](../architecture/web-services.md) und der [Variablenreferenz](../reference/web-services-variables.md).
