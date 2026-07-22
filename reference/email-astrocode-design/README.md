# Astrocode E-Mail-Design — Standard für alle Astrologie-Mails

**Festgelegt von Patrycja am 14.07.2026:** So sehen ab jetzt alle E-Mails rund um Astrologie aus (Neumonde, Transite, Reader-Launches, Astrocode-Portal). Womancode-Mails behalten ihr eigenes Samt-Design (Wein/Gold).

**Referenz-Mail (erste Mail in diesem Design):** `outputs/email-astrocode-neumond/index.html` — bei neuer Mail diese HTML kopieren, Texte tauschen, neue Slices generieren.

## Aufbau (drei Bild-Slices aus Patrycjas Vorlage)

1. **Hero oben:** Planeten + Hände aus der Vorlage, Headline in Collidge (weiß, weicher Schatten) unter den Planeten — wird pro Mail neu gebaut (`build_astrocode_email_assets.py "Headline" ZIEL`)
2. **Body:** Der gesamte Text läuft auf dem Vorlagen-Verlauf (Hellviolett → Lila → Orange mit Binär-Zahlen). Technisch: `background-size:100% 100%` auf dem Body-td, Bild 600px breit, Höhe ≈ geometrisches Mittel aus Desktop-/Mobil-Höhe (Default 4520 bei normaler Mail-Länge)
3. **Abschluss:** NP-Logo + ASTROCODE-Schriftzug aus der Vorlage, als Bild nach der Signatur, verlinkt auf https://patrycja-nasri.de/dein-astrocode/

## Design-Regeln (alle von Patrycja am 14.07. abgenommen)

- **Schrift: klassisch Schwarz** für allen Lesetext, Überschriften, Zitate, Kasten-Text, Signatur („Dunkelblau war ihr noch zu hell")
- **Schriftart:** Inter/Helvetica (Fließtext), Collidge nur für die Headline im Hero-Bild
- **Zitate:** groß (22px, fett-kursiv), weißes Leuchten (`text-shadow` weiß), Stern ✦ darüber, viel Luft davor/danach
- **Zwischen-Kicker** (z.B. „✦ FUNFACTS ZUM NEUMOND ✦"): groß (18px), WEISS mit Leuchten, zentriert, Sterne links/rechts — sonst geht er im Verlauf unter
- **Kästen:** transparentes Weiß `rgba(255,255,255,0.30)`, weich gerundet (26px), KEIN harter Rand — dünner Rand rgba 0.35 + sanfter Schein (`box-shadow`); Fallback-bgcolor für alte Clients
- **Kasten-Zeilen:** IMMER Patrycjas Sätze 1:1, nie selbst texten (Memory `feedback_kasten_zeilen_von_patrycja.md`)
- **Buttons:** massiv gefüllt in NP-Indigo #312782, weiße Schrift, Pill-Form (40px Radius)
- **Signatur:** „The Woman, who breaks the cycle!" / Patrycja / „Bewusstseinsastrologin · Identitycode · Moneycode · Emotioncode" — vor dem Abschluss-Bild
- **Anführungszeichen-Fix:** Letztes Wort + schließendes „ immer in `<span style="white-space:nowrap">` (sonst bricht das „ allein um)
- **PC-Ansicht:** Außenbereich (Body + Wrapper-Table) bekommt einen passenden CSS-Verlauf aus den Vorlagen-Farben (`linear-gradient(180deg,#8B8ED9,#A06AB5,#8979C1,#9267A8,#B6697D,#DB705C)` + Fallback-bgcolor #8d7fc7) — dann wirken die Mail-Ränder am Desktop nicht abgeschnitten; auf dem Handy füllt die Mail eh die Breite
- **Lieferung:** GetResponse-ZIP mit HTML + Bild-Dateien (kein Base64)

## Dateien hier

- `vorlage-astrocode-original.webp` — Patrycjas Original-Vorlage (1080x1920), Quelle aller Slices
- `build_astrocode_email_assets.py` — generiert hero/bg/footer für eine neue Mail
- `font-Collidge.ttf` / `font-Benzin.ttf` — Brand-Fonts (aus den Readern extrahiert)

## Neue Astro-Mail in 4 Schritten

1. `outputs/email-astrocode-neumond/index.html` in neuen Ordner kopieren, Texte tauschen (Patrycjas Text 1:1, nur Rechtschreibung — Korrektur-Tabelle in die Doku-Datei)
2. `python3 reference/email-astrocode-design/build_astrocode_email_assets.py "Neue Headline" outputs/email-astrocode-NAME/` — bei deutlich längerer/kürzerer Mail Body-Höhe messen und als 3. Argument mitgeben
3. Im Browser prüfen (HTML in Session-Scratchpad kopieren, Static-Server via launch.json — Downloads-Pfad ist für den Server gesperrt): Nähte Hero/Body/Footer, Mobil + Desktop
4. ZIP bauen: `zip -j outputs/email-astrocode-NAME-getresponse.zip index.html astrocode-*.jpg`
