# Dein Eclipse Navigator — Wissens-Übergabe für Bernadettes Claude

> Stand: 29.07.2026 (Verkaufsstart-Tag), Version v15.6.
> Dieses Dokument enthält alles, was Claude über den Eclipse Navigator wissen muss:
> Produkt-Fakten, fachliche Regeln, Technik-Überblick und die Antworten auf alle
> Nutzerinnen-Probleme, die bisher aufgetreten sind.

---

## 1. Was der Eclipse Navigator ist

Ein browserbasiertes Astro-Tool von Bernadette Hirschfelder (lieblingsastrologin.de).
Die Nutzerin gibt Name, Geburtsdatum, Geburtszeit und Geburtsort ein. Das Tool berechnet
ihr Geburtshoroskop (Placidus) komplett im Browser und erstellt einen fertigen,
individuellen KI-Prompt für ein persönliches Eclipse-Reading zu den beiden
August-Finsternissen 2026:

- **Sonnenfinsternis 12.08.2026** — Eclipsegrad 20°06' Löwe (Mondposition am Finsternis-Maximum)
- **Mondfinsternis 28.08.2026** — Eclipsegrad 4°50' Fische

Den Prompt kopiert die Nutzerin per Button und fügt ihn bei ChatGPT oder Claude ein.
Das Reading kommt in drei Teilen. Fenster-Fokus: August 2026 bis Anfang 2027.

## 2. Zugang, Preis, Kaufkette

- **Live-URL:** https://eclipsenavigator.netlify.app
- **Passwortschutz:** Die ganze Seite ist AES-256-verschlüsselt hinter einem Passwort-Gate.
  **Passwort: Finsternis2026** — muss bei jedem Besuch eingegeben werden (keine Merken-Funktion
  im Tool; wenn der Browser das Passwort speichert, ist das der Browser-Passwort-Manager).
- **Preis:** 37 € zzgl. 19 % MwSt., fester Preis.
- **Kaufkette:** Salespage → Checkout https://angebot.lieblingsastrologin.de/eclipse-navigator/
  → Kauf → Danke-Seite (zeigt das Passwort mit Kopier-Button) → Reader-URL → Passwort eingeben.
- Passwort ändern = beide Generatoren anpassen (Reader + Danke-Seite) und neu hochladen.

## 3. Bernadettes fachliche Regeln (verbindlich, alle im Tool umgesetzt)

1. **Eclipsegrade:** Gerechnet wird immer mit der Mondposition am Finsternis-MAXIMUM,
   nicht mit dem exakten Neu-/Vollmond. (Deshalb 20°06' Löwe und 4°50' Fische.)
2. **Orbs bei Eclipsen: pauschal 10°** für alle Hauptaspekte. Je enger der Orb, desto
   stärker; die engsten Aspekte tragen die Hauptbotschaft.
3. **Häuserherrscher im Zentrum:** Jede Finsternis wird über ihr Haus UND den Herrscher
   dieses Hauses gelesen. Das Haus zeigt, wo es geschieht; der Herrscher zeigt, worüber
   es läuft und wohin es führt.
4. **Herrscher: modern + Mitherrscher.** Skorpion = Pluto (Mitherrscher Mars),
   Wassermann = Uranus (Mitherrscher Saturn), Fische = Neptun (Mitherrscher Jupiter).
   Widder hat nur Mars, kein Zwei-Herrscher-Fall.
5. **Vorrang-Regel (Bernadette, 29.07.):** Wenn sich die Deutung zwischen zwei Herrschern
   entscheiden muss, gilt der moderne Herrscher: Skorpion → Pluto, Wassermann → Uranus,
   Fische → Neptun. Das gilt genauso für die Häuserherrscher.
6. **Wahrer Mondknoten** als Berechnungsgrundlage (nicht der mittlere). Knotenachse zur
   Eclipse Season: 29°47'/29°50' Wassermann.
7. **Minuten werden abgeschnitten,** nicht gerundet (astro.com-Konvention) — alle Anzeigen
   decken sich mit Profi-Software.
8. **Sprache:** Tierkreiszeichen wie Ortsangaben, nie beugen („in Löwe", nie „im Löwen").
   „Horoskopherrscher" statt „Chartruler", „Horoskop/Radix" statt „Chart", Du/Dich/Dein groß,
   größtenteils kein Englisch (Produktname „Dein Eclipse Navigator" bleibt englisch).

## 4. Wie der Prompt aufgebaut ist

Der Prompt wird KOMPONIERT, nicht aus einer festen Vorlage gefüllt: Kapitel erscheinen nur,
wenn die Chart sie hergibt (9–11 Kapitel, dynamisch nummeriert). Schichten: Haus der SoFi ·
MoFi als Haus-Achse (Mond + Sonne gegenüber) · Häuserherrscher der Finsternis-Häuser mit
Position · Aspekte beider Finsternis-Punkte zu allen natalen Punkten (Orb 10°) · Treffer auf
den Horoskopherrscher mit eigenem Kapitel · Knotenachse + natale Knoten (Seelenweg) ·
natale Sonne + nataler Mond. Das volle Horoskop steht als Datenblock unten im Prompt.

**Vermerke im Datenblock:**
- `[HOROSKOPHERRSCHER]` = Aspekt trifft den Herrscher des 1. Hauses.
- `[HOROSKOPHERRSCHER, Mitherrscher]` = Aspekt trifft den Mitherrscher (zählt genauso,
  der Prompt erklärt der KI ausdrücklich, dass das kein Widerspruch ist).

## 5. Support-Wissen: aufgetretene Probleme + Antworten

### „Mein Geburtsort wird nicht gefunden"
Bis v15.2 fand die Ortssuche (Open-Meteo/Geonames) vieles nicht: „Melle Niedersachsen"
(Leerzeichen-Zusatz), „melle, nie" (Teileingabe), „Halle" zeigte Dörfer vor Halle (Saale),
Bad Friedrichshall fehlte in der Datenbank komplett. **Seit v15.3/v15.4 gelöst:**
Fallback-Kette + DACH-Sortierung nach Einwohnerzahl + zweiter Geocoder (Photon/OpenStreetMap)
als Sicherheitsnetz, sogar fehlertolerant bei Tippfehlern. Wenn trotzdem mal ein Ort fehlt:
nächstgrößere Stadt eingeben — für das Horoskop zählen die Koordinaten, wenige Kilometer
Unterschied ändern praktisch nichts an den Häusern.

### „Mein Geburtsort wurde umbenannt" (Beispiel Kievka, Kasachstan)
Viele Orte in Osteuropa und Kasachstan tragen heute einen anderen Namen als zur Geburt.
Die Ortsdatenbanken kennen nur den HEUTIGEN Namen. Fall vom 29.07.: „Kievka, Kasachstan"
heißt heute **Nura**. Für diesen Fall hat der Reader seit dem 29.07. eine **eingebaute
Zusatz-Ortsliste**: Die Eingabe „Kievka" (auch Kiewka/Kijewka/Kiyevka) zeigt direkt
„Kievka (heute Nura), Qaraghandy, Kasachstan" mit den korrekten Koordinaten
(50°16'N / 71°33'E, identisch mit Astro-Seek, verifiziert am Kundinnen-Fall Olga).
Generelle Antwort bei weiteren umbenannten Orten: den heutigen Namen suchen (steht meist
bei Wikipedia unter dem alten Namen) — fürs Horoskop zählen nur die Koordinaten. Und:
Solche Orte können jederzeit in die Zusatz-Ortsliste aufgenommen werden (ein Eintrag im
Generator, neu bauen, neu hochladen).

### „ChatGPT meldet einen Widerspruch beim Horoskopherrscher"
Fall vom 29.07.: AC Skorpion, Vermerk HOROSKOPHERRSCHER stand an einem Mars-Aspekt, die
Daten nannten Pluto als Herrscher → ChatGPT stoppte. Ursache: Mars ist Mitherrscher von
Skorpion, das stand aber nicht deutlich genug im Prompt. **Seit v15.5/v15.6 gelöst**
(eigener Vermerk, Erklärung, Vorrang-Regel). Kundinnen mit einem ALTEN Prompt antworten
der KI einfach: „Mars ist der Mitherrscher meines Aszendenten Skorpion und zählt als
Horoskopherrscher. Der Vermerk ist korrekt." Oder neuen Prompt aus dem Reader holen.

### „Die Eingabe der Geburtszeit funktioniert nicht"
Bis v15.1 wurde „930" (für 9:30 Uhr) beim Tippen zu „93:0" verformt. **Seit v15.2 gelöst:**
Der Doppelpunkt springt erst ab der vierten Ziffer rein. Man tippt nur Ziffern —
„930" oder „1352" — Punkt und Doppelpunkt setzt das Feld selbst. Die Platzhalter zeigen
das jetzt auch so („z.B. 08101986", „z.B. 1352").

### „Der Reader fragt nicht nach dem Passwort"
Das Gate ist immer aktiv. Wer ohne Passwortabfrage reinkommt, hat das Passwort im eigenen
Browser gespeichert (Passwort-Manager füllt es aus) oder der Browser stellt den schon
entsperrten Tab wieder her. Test: privates Fenster öffnen — dort kommt das Gate immer.

### „KI stoppt mitten im Reading / gibt keine Antwort"
Neues Chatfenster öffnen und den Prompt erneut eingeben. Für das beste Ergebnis das
stärkste KI-Modell wählen (nicht das schnelle). Reading kommt in drei Teilen — wenn die
KI stoppt, „weiter" schreiben.

## 6. Technik-Überblick (für Claude, nicht für Kundinnen)

- Berechnung läuft **100 % im Browser** (eingebettete Engine, Public Domain; eingebettete
  Wahrer-Knoten-Ephemeride aus Swiss Ephemeris 1900–2036). Keine Geburtsdaten verlassen
  den Browser, nichts wird gespeichert.
- Einzige externe Aufrufe zur Laufzeit: die **Ortssuche** — Open-Meteo Geocoding (primär)
  + photon.komoot.io (Fallback). Beide kostenlos, ohne Schlüssel, austauschbar.
- Passwortschutz: AES-256-GCM, PBKDF2/SHA-256 mit 310.000 Iterationen, Entschlüsselung
  per WebCrypto im Browser. Ohne Passwort ist der Inhalt wirklich unlesbar.
- Quelle/Build: Generator `build_eklipsen_reader.py` in Patrycjas Workspace. Jede Änderung
  läuft über den Generator; hochgeladen wird immer der Ordner mit der geschützten
  `index.html` (Netlify Drop auf eclipsenavigator.netlify.app).

## 7. Versionshistorie 29.07.2026 (Verkaufsstart-Tag)

| Version | Fix |
| --- | --- |
| v15 | Ortssuche: Fallback-Kette für „Melle Niedersachsen" + DACH zuerst; Regionszeile im Vorschlag schwarz |
| v15.1 | Platzhalter-Beispiele ohne Trennzeichen (08101986 / 1352) |
| v15.2 | Zeit-Tippfeld: Doppelpunkt erst ab 4. Ziffer („930" bleibt tippbar) |
| v15.3 | Ortssuche holt 30 Treffer, sortiert DACH + Einwohnerzahl → Halle (Saale) gefunden, „halle an der saale" geht |
| v15.4 | Photon-Fallback für Datenbank-Lücken → Bad Friedrichshall gefunden, tippfehlertolerant |
| v15.5 | Prompt: Mitherrscher-Vermerk + Erklärung (behebt ChatGPT-„Widerspruch" bei AC Skorpion/Wassermann/Fische) |
| v15.6 | Prompt: Bernadettes Vorrang-Regel (im Zweifel moderner Herrscher, auch bei Häuserherrschern) |
