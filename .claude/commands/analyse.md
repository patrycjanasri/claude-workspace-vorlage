# /analyse — Instagram Post-Analyse

Wertet deine besten Posts der letzten Wochen aus. Erkennt Muster in Hooks, Themen und Formaten. Gibt klare Empfehlungen, was öfter gemacht werden sollte.

**Primärer Weg:** Telegram Bot via Make — du schickst `/analyse` im Telegram-Chat, Make zieht die Daten automatisch aus Instagram und Claude schickt den Report zurück. Setup: `reference/make-telegram-analyse-bot.md`

**Fallback (manuell):** Posts in `reference/post-tracking-template.md` eintragen, dann `/analyse` hier ausführen.

---

## Ablauf (manueller Fallback)

**Schritt 1 — Daten laden**

Lies zuerst:
- `reference/post-tracking-template.md` — Struktur und Definitionen verstehen
- Alle Dateien in `posts/` die auf `tracking-*.md` matchen (falls vorhanden)
- Falls keine `posts/`-Dateien existieren: Prüfe `inbox/` auf Post-Daten

Falls keine Tracking-Daten gefunden werden:
> "Ich finde keine Post-Daten. Zwei Optionen:
> 1. Füll `reference/post-tracking-template.md` mit deinen Posts aus — dann `/analyse` nochmal.
> 2. Oder paste deine Posts direkt hier mit Metriken (Reichweite, Saves, Kommentare, DMs)."

**Schritt 2 — Analyse durchführen**

Wenn Daten vorhanden, analysiere entlang dieser vier Dimensionen:

### A) Hook-Performance
Gruppiere Posts nach Hook-Typ. Berechne je Typ:
- Durchschnittliche Saves
- Durchschnittliche DMs
- Durchschnittliche Kommentare
- Durchschnittliche Reichweite

Ergebnis: Ranking der Hook-Typen nach Kaufsignal-Stärke (Saves + DMs zählen doppelt).

### B) Themen-Performance
Gruppiere Posts nach Thema. Gleiche Berechnung.
Ergebnis: Welche Themen ziehen echtes Interesse vs. welche werden weggescrollt.

### C) Format-Performance
Reel vs. Karussell vs. Bild.
Ergebnis: Welches Format bekommt die meiste organische Reichweite UND die stärksten Kaufsignale.

### D) Top-3-Posts
Liste die 3 Posts mit dem stärksten kombinierten Engagement-Score:
Score = Saves×3 + DMs×3 + Kommentare×2 + Likes×1

Für jeden Top-Post: Was hat ihn stark gemacht? Hook, Thema, Format, CTA — was war der entscheidende Faktor?

**Schritt 3 — Muster benennen**

Finde die 2-3 klarsten Muster aus allen vier Dimensionen.
Formuliere sie als Aussagen, keine Fragen:
- "Zahlen-Hooks performen 2,4x besser als Neugier-Hooks bei Saves."
- "Das Thema Geldidentität zieht 3x mehr DMs als MONAT-Content."
- "Reels haben 60% mehr Reichweite, aber Karussells haben 40% mehr Saves."

**Schritt 4 — Empfehlungen ausgeben**

Maximal 5 konkrete Empfehlungen. Jede Empfehlung:
- Basiert direkt auf einem gemessenen Muster
- Ist sofort umsetzbar
- Enthält ein konkretes Beispiel oder Startpunkt

Format:
```
## Empfehlung 1: [Titel]
**Warum:** [Daten-Basis — welches Muster zeigt das]
**Was tun:** [Konkrete Handlung]
**Startpunkt:** [Beispiel-Hook oder Thema oder Format]
```

**Schritt 5 — Nächste Woche planen (optional)**

Falls die Analyse klar genug ist, schlage direkt 3 konkrete Post-Ideen vor, die auf den Top-Mustern aufbauen. Mit Hook-Typ, Thema und erstem Satz.

---

## Ausgabe-Datei

Speichere die Analyse in:
`outputs/analyse-YYYY-MM-DD.md`

Mit diesem Header:
```
---
Zeitraum: [analysierter Zeitraum]
Posts analysiert: [Anzahl]
Stärkster Hook-Typ: [X]
Stärkstes Thema: [X]
---
```

Sag der Nutzerin, wo die Datei liegt.

---

## Kommunikationsprinzip

Direkt. Keine Aufwärm-Sätze. Die Zahlen sprechen — Claude interpretiert sie klar und ohne Weichzeichner.
Wenn ein Muster schwach ist oder ein Format nicht funktioniert: klar sagen. Nicht abschwächen.
