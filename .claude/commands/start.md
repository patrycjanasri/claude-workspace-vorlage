# Start

> Session initialisieren: Kontext laden und kompakten Status ausgeben.

## Ausführen

```
ls context/
ls plans/
ls outputs/
ls inbox/ 2>/dev/null || echo "(inbox/ leer oder nicht vorhanden)"
git status --short
git log --oneline -5
```

## Lesen

CLAUDE.md
./context

## Status-Ausgabe

Nach dem Lesen gib eine kompakte Übersicht aus — maximal eine Bildschirmseite:

### Wer bin ich / Workspace-Zweck
Ein Satz: wer der User ist und wofür dieser Workspace dient (aus context/).

### Offene Pläne
Liste aller Dateien in `plans/` mit Status (Draft / In Arbeit / Abgeschlossen) — erkennbar am Dateinamen oder Inhalt.

### Letzte Outputs
Die drei neuesten Dateien in `outputs/` mit kurzem Betreff.

### Inbox
Anzahl unerledigter Notizen in `inbox/` (falls vorhanden).

### Git-Status
Uncommitted changes in einer Zeile zusammengefasst.

### Bereit
Schließe mit: "Bereit. Was möchtest du heute angehen?"
