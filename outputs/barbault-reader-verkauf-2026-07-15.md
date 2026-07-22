# Barbault Basket Reader — Verkaufs-Setup (15.07.2026)

Erster BEZAHLTER Reader (Patrycjas Entscheidung 15.07.). Verkaufsweg: Kommentar-Codewort → DM mit Checkout-Link → Tentary verkauft + liefert automatisch. Zwei Platzhalter werden nach Upload/Anlage ersetzt: **[READER-LINK]** (Netlify) und **https://erfolgsqueen.tentary.com/p/jNjITH** (Tentary).

---

## 1. Preis (Patrycja entscheidet — sie will unter 22€)

**Empfehlung: 11€.** Passt in ihre Zahlenwelt (11 / 22 / 333 / 8888), niedrig genug für den Impulskauf direkt aus der DM, und setzt den Anker für künftige bezahlte Reader nicht zu tief ins Cent-Gefühl. Alternativen: 9€ (maximale Hürdenfreiheit) · 13€ · 17€ (mehr Marge, im viralen Fenster vertretbar).

## 2. Codewort für die Automation

**Vorschlag: BASKET** — passt zu ihrem CTA-Namen „Barbault Basket Reader", unterscheidbar von allen bisherigen Codewörtern (MARSCODE, WOMAN, PORTAL). Alternative: KORB.

## 3. Tentary-Produkt (zum Kopieren beim Anlegen)

**Produktname:** Barbault Basket Reader

**Verkaufstext (v2, 15.07. abends — aus Patrycjas eigenen Sätzen des Tages gebaut: Ergebnis-Share „Während andere Astrologen über das Allgemeine sprechen…", Teaser „langsam laufende Planeten / Persönlichkeitsprozess, der Zeit braucht", ihr CTA-Satz „erst die Bewegung bewirkt Veränderung"):**

Ganz Instagram spricht über den Barbault-Korb: Vier langsam laufende Planeten, Pluto, Neptun, Uranus und Jupiter, stehen gleichzeitig auf dem 4. Grad und bilden die Konstellation, die nach einem Astrologen benannt ist, der schon die Pandemie Jahre vorher kommen sah. Für die Jahre 2026 bis 2030 sprach er von einer Veränderung, für die ihm die Worte Wandel und Umbruch zu schwach waren.

Aber was heißt das für DICH?

Genau das zeigt dir mein Barbault Basket Reader. Während andere Astrologen über das Allgemeine sprechen, gebe ich dir was an die Hand, was exakt auf dich abgestimmt ist.

So funktioniert es:

1. Du gibst deine Geburtsdaten ein. Wichtig: Du brauchst deine exakte Geburtszeit! Mehr brauchst du nicht, keine Vorkenntnisse, keine App.
2. Der Reader berechnet dein Geburtshoroskop und zeigt dir, in welche Lebensbereiche die vier Planeten bei dir fallen, welche deiner Punkte der Korb direkt trifft und ob du mit einem Punkt um 4° Waage oder 4° Schütze die Figur mit deinem eigenen Horoskop komplett machst.
3. Mit einem Klick kreierst du deinen individuellen KI-Prompt. Einfügen bei ChatGPT oder Claude, und du bekommst dein persönliches Reading: welcher Anteil in dir in den Jahren bis 2030 wachsen möchte und wo dein Fokus liegen darf.

Gerade bei langsam laufenden Planeten geht es um einen bedeutenden Persönlichkeitsprozess, der Zeit braucht. Dein Reading begleitet dich deshalb weit über die Korb-Tage im Juli hinaus. Es trägt bis 2030.

Direkt nach dem Kauf bekommst du den Link zu deinem Reader. Er bleibt für dich offen, du kannst ihn jederzeit wieder nutzen.

Erinnere dich: Erst die Bewegung bewirkt Veränderung.

*(v1-Kurzbeschreibung ersetzt; deren Kern steckt in Punkt 2.)*

**Kurzbeschreibung für die Bezahlseite (kompakt, 4 Sätze):**

Der Barbault Basket Reader zeigt dir, was die Konstellation, über die gerade alle sprechen, für DICH bedeutet. Du gibst deine Geburtsdaten ein (wichtig: mit deiner exakten Geburtszeit), der Reader berechnet dein Geburtshoroskop und kreiert deinen individuellen KI-Prompt für ChatGPT oder Claude. Dein Reading zeigt dir, welche Lebensbereiche die vier langsam laufenden Planeten bei dir berühren und welcher Anteil in dir bis 2030 wachsen möchte. Direkt nach dem Kauf bekommst du den Link zu deinem Reader, und er bleibt für dich offen.

**Kaufbestätigung (FINAL 15.07., Patrycjas Fassung 1:1 — nur Rechtschreibung korrigiert: Komma vor „ChatGPT zu nutzen", „tiefer" klein, „bitte" klein, „weiterzuteilen" zusammen):**

Vielen Dank für dein Vertrauen.

Hier ist dein Barbault Basket Reader:
👉 [READER-LINK]

So gehst du vor:

Öffne den Link und gib deine Geburtsdaten ein.

Die Seite berechnet dein Geburtshoroskop und zeigt dir, welche Lebensbereiche diese Konstellationen bei dir berühren.

Kopiere mit einem Klick deinen fertigen KI-Prompt und füge ihn in ChatGPT oder Claude ein. Ich empfehle dir unbedingt, ChatGPT zu nutzen. Die Antworten sind meiner Meinung nach viel tiefer!

Dein Reading zeigt dir, welcher Anteil in dir in den Jahren 2026 bis 2030 wachsen möchte.

Der Reader bleibt für dich offen, du kannst ihn jederzeit wieder nutzen.

Ich bitte dich, den Link zu meinem Reader nicht einfach an jemanden weiterzuteilen! Gerne kann die Person diesen erwerben!

Ich freue mich auf dein Feedback.

Patrycja

## 4. DM-Automation (automatisierter Verkauf)

**Flow:** Kommentar **BASKET** unter Karussell/Reel → DM-Automation (ManyChat/Make, wie bei MARSCODE) schickt den Pitch mit Checkout-Link → Kauf bei Tentary → Tentary liefert Kaufbestätigung mit Reader-Link automatisch. Ab dann null Handarbeit.

**DM-Text (Entwurf, deine Anpassung):**

Hey du! Schön, dass der Barbault-Korb dich ruft.

Mein Barbault Basket Reader berechnet deine Chart und zeigt dir, welche Lebensbereiche diese Konstellation bei dir berührt und welcher Anteil in dir bis 2030 wachsen möchte. Dazu bekommst du deinen fertigen KI-Prompt für dein persönliches Korb-Reading.

Hol dir deinen Barbault Basket Reader hier:
👉 https://erfolgsqueen.tentary.com/p/jNjITH

Direkt nach dem Kauf landet der Link zu deinem Reader in deinem Postfach.

## 5. Reihenfolge zum Livegehen

1. **Netlify:** `outputs/astro-barbault-reader-netlify/` (oder die ZIP daneben) auf app.netlify.com/drop ziehen → URL unauffällig wählen (der Link ist das Produkt), z.B. Zufallsname von Netlify einfach behalten oder etwas Neutrales — NICHT barbaultreader.netlify.app, sonst ist er erratbar.
2. **Tentary:** Produkt mit Name, Preis, Beschreibung anlegen → Reader-Link in die Kaufbestätigung → Testkauf machen (kommt der Link an?).
3. **DM-Automation:** Codewort BASKET mit dem DM-Text + Checkout-Link einrichten.
4. **Content:** Karussell (`instagram-karussell-barbault-korb-2026-07-15.md`) + Reels (`instagram-reels-barbault-korb-2026-07-15.md`) designen und posten, 16.–21.07.
5. Optional Kanal: Reader-Ankündigung als Einlösung des Teasers von heute (ihre Sätze, mit Checkout-Link statt Gratis-Link).

**Wichtig:** Der Kanal-Teaser von heute verspricht nichts Kostenloses („ich sitze am nächsten Reader") — sauber für den Verkaufs-Schwenk.

**Design-Wechsel (15.07., Patrycjas Ansage):** Reader läuft im ASTROCODE-Design (Standard aus `reference/email-astrocode-design/`): heller Vorlagen-Verlauf, Planeten+Hände-Hero, Text schwarz, Kästen transparentes Weiß, Buttons NP-Indigo #312782, Binär-Kachel dezent, Abschluss NP-Logo + ASTROCODE-Bild verlinkt aufs Portal. Abschluss-CTA im Reader → AstroCode-Portal (Patrycjas Reise-Reader-Text 1:1: „DU findest die Antwort von diesem KI-Prompt genial?…"). Der Womancode-CTA ist damit raus.

**Offen:** Codewort bestätigen (BASKET) · Netlify-URL in Doku nachtragen · Testkauf. **Preis: von Patrycja in Tentary gesetzt und bewusst GEHEIM** — wird nirgends genannt (Mail, DM, Kanal), sichtbar erst am Checkout.
