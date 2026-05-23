# Shutdown

> Session zusammenfassen, Workspace aufräumen, alle Änderungen speichern und committen.

## Instructions

Führe die folgenden Schritte der Reihe nach aus. Überspringe keinen.

---

### Schritt 1: Session-Zusammenfassung

Fasse die Session in 3–5 Punkten zusammen:
- Was wurde besprochen oder bearbeitet?
- Welche Entscheidungen wurden getroffen?
- Was wurde erstellt oder geändert?
- Was ist offen geblieben?

---

### Schritt 2: Workspace scannen

```
git status --short
ls context/
ls plans/
ls outputs/
ls inbox/ 2>/dev/null
```

Prüfe:
- `context/` — Gibt es neue Erkenntnisse aus dieser Session, die festgehalten werden sollten?
- `plans/` — Haben sich Plan-Status geändert? (Entwurf → In Arbeit → Abgeschlossen)
- `outputs/` — Gibt es temporäre oder verwaiste Dateien?
- `inbox/` — Gibt es erledigte Notizen, die archiviert oder gelöscht werden sollten?

---

### Schritt 3: Dateien aktualisieren

1. **CLAUDE.md** — Prüfe ob Struktur, Commands oder Workflows dokumentiert werden müssen
2. **context/** — Aktualisiere relevante Kontext-Dateien mit neuen Erkenntnissen
3. **Plans** — Aktualisiere Status-Zeilen in Plänen, die sich geändert haben

Für Dateien, bei denen unklar ist ob sie gebraucht werden: **NICHT löschen**, sondern im Abschluss-Report auflisten.

---

### Schritt 4: Aufräumen

Lösche offensichtlich unnötige Dateien:
- `.DS_Store`
- `__pycache__/` und `.pyc`-Dateien
- Temporäre Dateien (`*.tmp`, `*.bak`, `*.log`)

---

### Schritt 5: Git — Committen

1. `git status` — Was hat sich geändert?
2. Stage alle relevanten Änderungen (KEINE Secrets, KEINE .env)
3. Commit-Message: `"shutdown: {kurze Beschreibung der Session-Ergebnisse}"`
4. Push auf Remote

---

### Schritt 6: Abschluss-Report

Liefere einen kurzen Report:

| Bereich | Was passiert ist |
| ------- | ---------------- |
| **Erstellt** | Neue Dateien / Outputs dieser Session |
| **Aktualisiert** | Geänderte Dateien |
| **Offen** | Was nicht erledigt wurde — mit nächstem Schritt |
| **Nächste Session** | Empfehlung, womit man anfangen sollte |

---

### Schritt 7: Verabschiedung

Verabschiede dich persönlich und fasse in einem Satz zusammen, was heute erreicht wurde. Warm aber knapp — wie ein guter Kollege, der Feierabend macht.
