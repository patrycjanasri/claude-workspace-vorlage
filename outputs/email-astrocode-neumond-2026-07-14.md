# E-Mail „Neumond in Krebs" — Astrocode-Style (14.07.2026)

Erste Mail im Astrocode-Design (nicht Womancode-Samt). Patrycjas Text 1:1, nur Rechtschreibung korrigiert. Bewirbt den Neumondreader und am Ende das Astrocode Portal.

## Dateien

- Quellordner: `outputs/email-astrocode-neumond/` (index.html + astrocode-hero.jpg)
- GetResponse-ZIP: `outputs/email-astrocode-neumond-getresponse.zip`
- Textfassung zweite Liste (ohne Formatierung, zum Kopieren): `outputs/email-astrocode-neumond-text.txt`
- Hero-Bild: Patrycjas Astrocode-Vorlage (1080x1920, Hände + Planeten), oben beschnitten auf die Planeten-Zone, Überschrift „Neumond in Krebs" in Collidge (Brand-Font, aus dem Reader extrahiert) unter die Planeten gesetzt, unten weicher Verlauf ins Body-Dunkellila (#140830)

## Design-Entscheidungen (v2, 14.07. nach Patrycjas Feedback)

**v1 (dunkles Kosmos-Lila als Body) verworfen — Patrycja: Der GANZE Hintergrund muss die Vorlage sein.** Die Mail läuft jetzt komplett auf ihrem Vorlagen-Verlauf (Hellviolett → Lila → Orange mit Binär-Zahlen):

- **Drei Bild-Slices aus der Vorlage (1080x1920):** Hero oben (Planeten + Hände, Headline „Neumond in Krebs" in Collidge eingebrannt) · Body-Hintergrund (Verlauf-Streifen, per Blur/Differenz-Trick: Verlauf glatt gestreckt + Zahlen-Textur in Originalgröße gekachelt, Kanten farblich in Hero/Footer eingeblendet) · Footer (NP-Logo + ASTROCODE-Schriftzug, verlinkt aufs Portal)
- Body-Hintergrund 600x4520 mit `background-size:100% 100%` (Kompromiss Desktop/Mobil, Verhältnis = geometrisches Mittel), Fallback-bgcolor #9d8ed4
- Text dunkles Indigo #2A1E5C (NP-Logo-Welt), Überschriften #1D1247, Schrift Inter/Helvetica
- Buttons massiv gefüllt in NP-Indigo #312782, weiße Schrift
- Kästen: transparentes Weiß (rgba 0.30) mit weißem Rand, Fallback-bgcolor
- **Abschluss der Mail = NP-Logo + ASTROCODE aus der Vorlage** (nach der Signatur), klickbar → Portal
- Zwei Kästen: Neumondreader (nach dem Krebs-Absatz, wo ihr Link stand) und Astrocode Portal
- Kein E-Mail-Gate-Thema, keine Feedback-Screenshots

**Learning:** Wenn Patrycja eine Design-Vorlage schickt, ist die Vorlage der komplette Rahmen der Mail (Hintergrund durchgehend, Abschluss-Elemente an ihrem Platz) — nicht nur ein Hero-Ausschnitt plus eigenes Farbschema.

## Links

- Neumondreader: https://neumondreader.netlify.app (LIVE, geprüft 14.07.)
- Astrocode Portal: https://patrycja-nasri.de/dein-astrocode/ (LIVE, geprüft 14.07.)

## Betreff (VORSCHLÄGE — noch nicht bestätigt)

Alle aus ihren eigenen Sätzen der Mail:

1. **„Fahren deine Emotionen gerade Achterbahn?"** · Preheader: „Hallo Neumond in Krebs." — Empfehlung: ihr Eröffnungs-Hook, die Mail löst ihn sofort ein. (Aktuell als Title + Preheader in der HTML eingesetzt.)
2. „Ein Thema aus der Vergangenheit klopft laut an der Tür" · Preheader: „Und der Neumond in Krebs möchte, dass du es anschaust."
3. „Unsere Gedanken erschaffen unsere Realität" · Preheader: „Und dieser Neumond ist dein Startpunkt."

## Korrektur-Tabelle (nur Rechtschreibung/Grammatik, Wortlaut bleibt ihrer)

| Original | Korrigiert | Grund |
| --- | --- | --- |
| „der Rückläufig ist" | „der rückläufig ist" | Kleinschreibung |
| „was ganz interessantes" | „was ganz Interessantes" | Großschreibung |
| „weil es dein gebiet ist" | „weil es dein Gebiet ist" | Großschreibung |
| „mit meinem AC Steinbock auftreten" | „mit meinem AC-Steinbock-Auftreten" | Durchkopplung |
| „das innen" | „das Innen" | Großschreibung |
| „rückläufgkeit bedeutet. Die absolute nachinnenschau!" | „Rückläufigkeit bedeutet: die absolute Nachinnenschau!" | Tippfehler, Doppelpunkt |
| „zum manifestieren" | „zum Manifestieren" | Großschreibung |
| „fürs den Neumondreader" | „für den Neumondreader" | Tippfehler |
| „kraftvollen licht der sonne" | „kraftvollen Licht der Sonne" | Großschreibung |
| „Eklipseseasion" | „Eclipse Season" | Tippfehler |
| „schwingst du den ganzen Tag!" | „schwingst du den ganzen Tag?" | Fragezeichen |
| „ich persönlich Liebe Ekligen" | „ich persönlich liebe Eklipsen" | Tippfehler |
| „davor angst haben" | „davor Angst haben" | Großschreibung |
| „um die Seelen" | „um die Seele" | Tippfehler (Singular) |
| „bevor ich dir jetzt ganz allgemeinen Text" | „bevor ich dir jetzt einen ganz allgemeinen Text" | fehlender Artikel |
| „kostet weitaus weniger wie ein" | „kostet weitaus weniger als ein" | Grammatik |
| „nichtmal ein Bruchteil" | „nicht mal einen Bruchteil" | Getrenntschreibung, Akkusativ |
| „mir so einer Leichtigkeit" (Zitat v2) | „mit so einer Leichtigkeit" | Tippfehler |
| „Lebebsunterhalt" (Absatz v2) | „Lebensunterhalt" | Tippfehler |

**Text-Updates 14.07. (Patrycja):** Zitat neu: „Patrycja, das ist alles so leicht für dich und du sprichst und kreierst mit so einer Leichtigkeit darüber, aber das versteht und kann nicht jeder!" · Absatz danach beginnt jetzt: „Ja, ich beschäftige mich damit auch schon seit 2020 intensiv und habe viel Geld für dieses Wissen investiert. Es hat in mir so viel transformiert! Heute bin ich Unternehmerin und kreiere meinen Lebensunterhalt damit. Mein Ziel ist es, …" („Ja, mag sein. Aber" gestrichen).

**Bewusst gelassen (ihre Stimme):** „Schupser", „Sonne, Mond und Sterne Game", „Kreationskiste", „mega geiles Tool", „Wie genial ist das BITTE!", „ausspuckt", „Jeder Monat (Tierkreiszeichen)".

**Kasten-Zeile Reader (Patrycjas Text 1:1, Korrektur 14.07. nach ihrem Feedback „Nicht dein Chart!!"):** „Du gibst deine Geburtsdaten ein, mein Neumondreader berechnet dein Geburtshoroskop und erstellt dir daraus deinen individuellen Prompt für dein Neumondreading!" (nur „Du gibt" → „Du gibst" korrigiert). Learning: nicht „Chart wird berechnet" schreiben — sie formuliert den Nutzen als Kette bis zum Reading.

**Kasten-Zeile Portal (Patrycjas Text 1:1, Korrektur 14.07.):** „Begib dich in die Tiefen deiner Seelenlandschaft! Entschlüssel dein Geburtshoroskop!" — Claudes Fassungen („In deinem Tempo. So oft du willst." und „mit ChatGPT in der absoluten Tiefe") beide verworfen. Learning: Kasten-Zeilen in den Mail-Boxen IMMER von Patrycja einholen, nicht selbst texten.

**Von Claude ergänzt (bei Bedarf streichen):** Button-Labels „Zum Neumondreader" / „Öffne das Portal".

## Offen

- Betreff bestätigen
- Testversand GMX + Gmail-Gegenprobe (bekanntes GMX-Spam-Thema)
- Signatur-Zeile prüfen: „The Woman, who breaks the cycle!" aus den Womancode-Mails übernommen — passt die auch für die Astrocode-Liste?
