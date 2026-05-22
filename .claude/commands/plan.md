# Plan

> Ausführlichen Projektplan erstellen und in plans/ ablegen.

## Variablen

projekt: $ARGUMENTS

---

## Anweisungen

**Wichtig:** Du erstellst einen PLAN, keine Implementierung. Denke gründlich nach, dann schreibe ein vollständiges Plan-Dokument.

### Schritt 1: Recherche

Lies vor dem Schreiben:
- `CLAUDE.md` — Workspace-Überblick und Konventionen
- `context/` — Wer der User ist, seine Ziele und Prioritäten
- `plans/` — Bestehende Pläne als Stil-Referenz
- `outputs/` — Was bereits geliefert wurde

### Schritt 2: Plan-Datei erstellen

Dateiname: `plans/YYYY-MM-DD-{projektname-kebab}.md`
- Heutiges Datum verwenden
- `{projektname-kebab}` = kurzer beschreibender Name (z.B. `newsletter-workflow`, `recherche-datenbank`, `onboarding-redesign`)

### Schritt 3: Plan-Inhalt

Fülle alle Abschnitte vollständig aus:

```markdown
# Plan: {Projekttitel}

**Erstellt:** YYYY-MM-DD
**Status:** Entwurf
**Ziel:** {Ein-Satz-Zusammenfassung}

---

## Überblick

### Was erreicht wird
{2–3 Sätze: Endergebnis und Nutzen}

### Warum das wichtig ist
{Verbindung zu den Zielen des Users / Projekts}

---

## Ausgangslage

### Was bereits existiert
{Relevante Dateien, Strukturen, Vorarbeiten}

### Was fehlt oder gelöst werden muss
{Lücken, Probleme, Anforderungen}

---

## Liefergegenstände

| Nr. | Deliverable | Speicherort | Format |
| --- | ----------- | ----------- | ------ |
| 1   | {Name}      | outputs/... | .md / .pdf / etc. |

---

## Phasen & Aufgaben

### Phase 1: {Phasenname}

**Ziel dieser Phase:** {ein Satz}

- [ ] {Aufgabe 1}
- [ ] {Aufgabe 2}
- [ ] {Aufgabe 3}

### Phase 2: {Phasenname}

**Ziel dieser Phase:** {ein Satz}

- [ ] {Aufgabe 1}
- [ ] {Aufgabe 2}

---

## Ressourcen & Abhängigkeiten

### Benötigte Inputs
{Was der User liefern muss: Daten, Zugänge, Entscheidungen}

### Externe Abhängigkeiten
{Tools, APIs, Personen, Deadlines}

---

## Zeitrahmen

| Phase | Aufwand (geschätzt) | Priorität |
| ----- | ------------------- | --------- |
| Phase 1 | {z.B. 2h} | Hoch |
| Phase 2 | {z.B. 1h} | Mittel |

---

## Erfolgskriterien

Die Arbeit ist abgeschlossen, wenn:

1. {Messbares Kriterium}
2. {Messbares Kriterium}
3. {Messbares Kriterium}

---

## Offene Fragen

{Liste von Entscheidungen, die der User treffen muss, bevor es losgeht}

---

## Notizen

{Zusätzlicher Kontext, Ideen, Risiken}
```

---

## Bericht

Nach dem Erstellen:
1. Kurze Zusammenfassung des Plans (3–5 Sätze)
2. Liste offener Fragen, die User-Input brauchen
3. Pfad zur Plan-Datei: `plans/YYYY-MM-DD-{name}.md`
4. Nächster Schritt: "Soll ich direkt mit Phase 1 loslegen?"
