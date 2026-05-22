# Capture

> Schnelle Notiz sofort in inbox/ speichern — ohne Unterbrechung des Workflows.

## Variablen

notiz: $ARGUMENTS

---

## Anweisungen

1. Erstelle eine neue Datei in `inbox/` mit folgendem Dateinamen:
   ```
   inbox/YYYY-MM-DD-HH-MM-{slug}.md
   ```
   - `YYYY-MM-DD-HH-MM` = aktuelles Datum und Uhrzeit (heute ist $TODAY)
   - `{slug}` = die ersten 4–5 Wörter der Notiz als Kebab-Case, Sonderzeichen entfernt

2. Inhalt der Datei:
   ```markdown
   # {erste Zeile der Notiz}

   **Erfasst:** YYYY-MM-DD HH:MM

   {vollständiger Notiztext}
   ```

3. Bestätige kurz mit Dateiname und erstem Satz der Notiz. Keine weiteren Erklärungen.

---

## Hinweis

Falls kein Argument übergeben wurde (`$ARGUMENTS` ist leer), frage einmalig: "Was soll ich erfassen?"
