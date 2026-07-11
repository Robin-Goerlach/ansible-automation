# Meilenstein 1: Repository-Grundlage

**Version:** 0.1.0
**Status:** Abgeschlossen
**Abschlussdatum:** 9. Juli 2026

Meilenstein 1 macht aus dem anfänglichen Verzeichnisgerüst ein ausführbares, prüfbares und dokumentiertes Ansible-Projekt. Die vollständige Linux-Basiskonfiguration folgt erst in Meilenstein 2.

## Enthalten

- Bootstrap-Skript für Linux oder WSL
- isolierte Python-Umgebung
- Python-Bootstrap für verwaltete Linux-Systeme
- sicheres Beispielinventar mit ausschließlich `localhost`
- Validierung von Control Node, Verbindung und Managed-Node-Bereitschaft
- lesender Systembericht als JSON auf dem Control Node
- Audit-first-Rolle `sasd_system_baseline`
- zweistufige Freigabe vor Paketinstallationen
- maschinenlesbare Manifeste
- lokale Tests und GitHub Actions

## Abnahme

```bash
scripts/test.sh
scripts/verify-milestone-1.sh
```

Die Standardabnahme verändert das verwaltete System nicht. Die Baseline wird im Check Mode ausgeführt. Der Python-Bootstrap ist eine separate, ausdrücklich aufzurufende Änderungsoperation.

Siehe auch die [englische Milestone-Dokumentation](../milestones/milestone-1.md).
