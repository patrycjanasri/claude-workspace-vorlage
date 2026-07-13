#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut den Leader-Reader ("Dein Leader-Code") aus dem Business-Reader.
Gleiches Design + gleiche Astro-Engine (Placidus), nur das Reading-Gehirn
wird getauscht:

Network-Marketing-Reading fuer Patrycjas MONAT-Team (ShineUp).
Elf Punkte in drei Bloecken:
  Block 1 (Wirkung + Verkauf):  AC/1. Haus, Merkur/3. Haus, Venus
  Block 2 (Geld + Arbeit):      2. Haus, 6. Haus, 8. Haus
  Block 3 (Vom Partner zum Leader): Sonne, 7. Haus, Jupiter/9. Haus,
                                    MC/10. Haus, 11. Haus
Mars, Saturn und Mond werden von der KI dort eingewoben, wo sie stehen.

Der Reader rechnet zusaetzlich die Network-Haeuser aus (Zeichen auf der
Placidus-Haeuserspitze + Planeten im Haus, Accessor wie im Womancode-Reader
verifiziert) und legt sie in window.__leader.

WERBEFREI: kein E-Mail-Gate, kein Abschluss-CTA, keine Upsell-Box.
Nur Impressum/Datenschutz im Footer bleiben.

Quelle:  astro-business-reader.html
Ziel:    astro-leader-reader.html (+ astro-leader-reader-netlify/index.html)
Bei Design-Updates am Business-Reader dieses Skript erneut laufen lassen.
"""
import os, re, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-leader-reader.html")
NETLIFY = os.path.join(HERE, "astro-leader-reader-netlify")

with open(SRC, "r", encoding="utf-8") as f:
    s = f.read()

def repl(old, new, label):
    global s
    if old not in s:
        sys.exit("FEHLT (" + label + "): " + old[:80])
    s = s.replace(old, new, 1)

# --- 1. Branding / sichtbare Texte ---------------------------------------
repl("<title>Dein Business-Code</title>",
     "<title>Dein Leader-Code</title>", "title")

repl('<p class="header-eyebrow">Dein kosmischer Business-Blueprint</p>',
     '<p class="header-eyebrow">Dein Network-Marketing-Blueprint</p>', "eyebrow")

repl("<h1>Dein Business-Code</h1>",
     "<h1>Dein Leader-Code</h1>", "h1")

repl('<p class="subtitle">Gib deine Geburtsdaten ein. Auf der nächsten Seite bekommst du dein Geburtshoroskop angezeigt und einen fertigen KI-Prompt, der dir sagt, wie du dein Business führst, dich positionierst, skalierst und Geld verdienst.</p>',
     '<p class="subtitle">Gib deine Geburtsdaten ein. Auf der nächsten Seite bekommst du dein Geburtshoroskop angezeigt und einen fertigen KI-Prompt, der dir zeigt, wie du wirkst, wie du verkaufst, wie du mit Geld umgehst und was für eine Leaderin in dir steckt.</p>',
     "subtitle")

repl('onclick="runCheck()">Meinen Business-Code aufdecken</button>',
     'onclick="runCheck()">Meinen Leader-Code aufdecken</button>', "submit-btn")

# --- E-Mail komplett entfernen (kein Opt-in, wie beim Chiron-Reader) -------
repl('''    <div class="name-group">
      <label class="field-label" for="userEmail">Deine E-Mail</label>
      <input type="email" id="userEmail" placeholder="Wohin schicken wir deinen Business-Code?" autocomplete="email" inputmode="email">
    </div>

''', '', "email-field-remove")

repl("    const email = ($('userEmail').value || '').trim();", "    const email = '';", "email-var")

repl('''    const emailOk = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email);
    if(!emailOk){ return fail('Bitte gib eine gültige E-Mail-Adresse ein. Dorthin kommt dein Business-Code.'); }
''', '', "email-validation")

repl("      subscribeLead(name, email);\n", "", "subscribe-call")

repl('''  // Trägt die Lead über die Netlify-Funktion in die GetResponse-Liste ein.
  // Bewusst nicht-blockierend: scheitert der Eintrag (Netzwerk/Server), bekommt
  // die Nutzerin trotzdem ihr Reading. Doppelte Einträge fängt GetResponse selbst ab.
  function subscribeLead(name, email){
    try{
      fetch('/.netlify/functions/subscribe', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ name: name || '', email: email || '' })
      }).catch(function(){});
    }catch(e){}
  }
''', '', "subscribe-fn-remove")

# --- 1b. Minireading-Texte (5 Punkte x 12 Zeichen) einhaengen ---------------
# Wird VOR generateReading definiert, damit die Funktion darauf zugreifen kann.
mini_texts = r"""window.LEADER_MINI = {
  ac: {
    "Widder": "Du wirkst direkt und voller Energie. Wer deine Story öffnet, spürt sofort: Diese Frau wartet nicht, die geht los. Das zieht Menschen an, die selbst starten wollen. Achte im Erstgespräch auf dein Tempo, sonst überfährst du Frauen, die noch Anlauf brauchen.",
    "Stier": "Du wirkst ruhig, geerdet und verlässlich. Menschen spüren in deiner Story, dass du bleibst und keinem Trend hinterherläufst. Genau das schafft Vertrauen bei Kundinnen, die schon oft enttäuscht wurden. Trau dich, öfter sichtbar zu werden, deine Ruhe verkauft besser als jeder Hype.",
    "Zwillinge": "Du wirkst leicht, wach und gesprächig. In deiner Story wechselst du mühelos zwischen Themen und machst Fremden den Einstieg leicht. Menschen schreiben dir schneller zurück als anderen. Bleib bei einem Thema pro Story, damit man dich mit etwas Konkretem verbindet.",
    "Krebs": "Du wirkst warm und nahbar. Fremde haben in deiner Story das Gefühl, dich schon zu kennen. Diese Nähe öffnet dir Türen, die für andere verschlossen bleiben. Zeig dich auch an den Tagen, an denen du dich lieber zurückziehen würdest.",
    "Löwe": "Du wirkst präsent. Wenn du in der Story sprichst, schauen Menschen bis zum Ende. Diese natürliche Bühne ist im Network dein größtes Kapital. Zeig neben deinem Glanz auch deine Zwischentöne, sie machen dich nahbar.",
    "Jungfrau": "Du wirkst klar, sortiert und kompetent. Menschen kaufen bei dir, weil sie merken: Die weiß, wovon sie redet. Deine Story darf trotzdem unperfekt sein. Der ungeschminkte Moment bringt dir mehr Anfragen als die durchgeplante Kachel.",
    "Waage": "Du wirkst charmant und verbindend. Menschen fühlen sich in deiner Gegenwart gesehen, auch durch den Bildschirm. Das macht dich zur geborenen Beziehungsverkäuferin. Bezieh klar Position, Gefallen-Wollen kostet dich den Abschluss.",
    "Skorpion": "Du wirkst intensiv und magnetisch. Menschen spüren deine Tiefe, bevor du ein Wort geschrieben hast. Wer dir folgt, folgt dir ganz. Trau dich, diese Intensität zu zeigen, angepasste Storys nehmen dir deine Kraft.",
    "Schütze": "Du wirkst begeisternd und weit. Deine Story macht Lust auf mehr Leben, mehr Freiheit, mehr Möglichkeiten. Genau diese Vision verkauft im Network. Unterfüttere das große Versprechen mit konkreten Schritten, dann glauben dir auch die Skeptischen.",
    "Steinbock": "Du wirkst seriös und souverän. Menschen trauen dir zu, dass du hältst, was du sagst. Das hebt dich von jedem lauten Hype ab. Zeig neben der Professionalität auch dein Lachen, es macht aus Respekt Nähe.",
    "Wassermann": "Du wirkst anders als der Rest, und genau das bleibt hängen. Menschen folgen dir, weil du keine Kopie bist. Dein Auftritt darf ungewöhnlich sein. Lass trotzdem Nähe zu, Distanz wird im Network schnell zur Wand.",
    "Fische": "Du wirkst weich, feinfühlig und offen. Menschen erzählen dir Dinge, die sie sonst niemandem schreiben. Dieses Vertrauen ist Gold im Verkauf. Setz klare Grenzen, sonst wirst du zur kostenlosen Seelsorgerin statt zur Geschäftspartnerin."
  },
  sonne: {
    "Widder": "Du führst, indem du vorangehst. Dein Team folgt deinem Beispiel, deine Ansagen sind zweitrangig. Wenn du selbst ins Tun kommst, kommt Bewegung in die ganze Struktur. Lern, andere gewinnen zu lassen, auch wenn du selbst schneller wärst.",
    "Stier": "Du führst über Beständigkeit. Dein Team weiß, woran es bei dir ist, und genau das hält es zusammen. Du baust langsam, aber was du baust, bleibt. Lass Veränderungen zu, wenn das Business sie verlangt.",
    "Zwillinge": "Du führst über Kommunikation. Du erklärst, verbindest und hältst dein Team im Gespräch. Deine Calls sind lebendig statt zäh. Zieh Entscheidungen auch durch, wenn das nächste Neue lockt.",
    "Krebs": "Du führst über Fürsorge. Dein Team fühlt sich bei dir gehalten und bleibt deshalb. Menschen gehen für dich durchs Feuer, weil du sie wirklich siehst. Vergiss dabei eines: Auch ein liebevolles Nein ist Führung.",
    "Löwe": "Du führst über Ausstrahlung. Menschen wollen in deiner Nähe sein und Teil von dem, was du aufbaust. Dein Feuer entfacht das Feuer der anderen. Lass dein Team glänzen, geteilte Bühne macht dich größer.",
    "Jungfrau": "Du führst über Struktur und Können. Dein Team lernt bei dir sauberes Handwerk: Follow-ups, Systeme, Abläufe. Das macht deine Partnerinnen schnell selbstständig. Denk daran, dass Menschen Ermutigung brauchen, bevor sie Korrektur vertragen.",
    "Waage": "Du führst über Verbindung. Du spürst, was dein Team braucht, und gleichst aus, bevor es kracht. Menschen arbeiten gern mit dir. Schieb unbequeme Entscheidungen trotzdem an, Klarheit ist die freundlichste Form von Führung.",
    "Skorpion": "Du führst über Tiefe. Du siehst, was in deinen Partnerinnen steckt, oft bevor sie es selbst sehen. Deine Gespräche verändern Menschen. Lass die Kontrolle los: Ein Team wächst nur, wenn du es machen lässt.",
    "Schütze": "Du führst über Vision. Du zeigst deinem Team, wohin die Reise geht, und plötzlich glauben alle daran. Sinn ist dein stärkstes Führungsinstrument. Übersetz die Vision in Wochenschritte, sonst bleibt sie ein schönes Bild.",
    "Steinbock": "Du führst über Verantwortung. Du nimmst dein Business ernst und dein Team richtet sich daran auf. Bei dir lernen Partnerinnen, was Commitment bedeutet. Lass Leichtigkeit zu, Erfolg darf sich auch gut anfühlen.",
    "Wassermann": "Du führst über Freiheit. Du lässt dein Team eigene Wege gehen und genau deshalb bleiben die Starken bei dir. Du denkst Network neu, statt Altes zu kopieren. Bleib präsent, Freiheit ohne Anbindung fühlt sich wie Alleinsein an.",
    "Fische": "Du führst über Gespür. Du merkst, wenn eine Partnerin wackelt, bevor sie es ausspricht. Deine Intuition trifft öfter als jede Statistik. Grenz dich ab: Du darfst führen, ohne jede Stimmung deines Teams mitzutragen."
  },
  merkur: {
    "Widder": "Du schreibst und sprichst direkt auf den Punkt. Deine Nachrichten haben Zug, Menschen wissen sofort, was du willst. Das schließt schneller ab als jedes Drumherum. Frag erst, dann pitch.",
    "Stier": "Du sprichst ruhig, konkret und glaubwürdig. Bei dir klingt nichts nach Masche, und genau das verkauft. Menschen kaufen, weil sie dir glauben. Nimm dir Zeit für deine Antworten, dein Tempo ist deine Stärke.",
    "Zwillinge": "Worte sind dein Werkzeug. Du findest für jede Frau den passenden Ton und drehst ein Gespräch mühelos zum Angebot. Sprachnachrichten und DMs sind dein Spielfeld. Stell am Ende die eine klare Frage statt drei.",
    "Krebs": "Du verkaufst über Gefühl. Deine Nachrichten berühren, weil du erst zuhörst und dann antwortest. Menschen öffnen sich dir schnell. Trau dich, nach dem emotionalen Moment auch die Abschlussfrage zu stellen.",
    "Löwe": "Du erzählst mitreißend. Deine Sprachnachrichten haben Wärme und Größe, Menschen hören sie bis zum Ende. Story-Selling ist deine Sprache. Gib der anderen mindestens so viel Raum wie deiner Geschichte.",
    "Jungfrau": "Du erklärst präzise und beantwortest Einwände, bevor sie kommen. Kompliziertes wird bei dir einfach. Das überzeugt die Skeptischen, an denen andere scheitern. Manchmal reicht ein Satz und die Frage danach.",
    "Waage": "Du formulierst schön und diplomatisch. Menschen fühlen sich von deinen Nachrichten nie überrumpelt. Das öffnet dir Gespräche, die andere gar nicht erst bekommen. Frag am Ende klar: Willst du dabei sein?",
    "Skorpion": "Du sprichst wenig und triffst. Deine Worte gehen unter die Oberfläche, du benennst, was die andere wirklich bewegt. Solche Gespräche vergisst niemand. Lass der anderen Zeit, wenn du eine wunde Stelle berührt hast.",
    "Schütze": "Du sprichst in Möglichkeiten. Deine Worte machen aus einem Produkt eine Zukunft. Menschen kaufen bei dir das größere Leben gleich mit. Bleib ehrlich und versprich nichts, was das Business erst in Jahren hält.",
    "Steinbock": "Du sprichst klar, sachlich und ohne Show. Menschen nehmen dir ab, was du sagst, weil du nichts aufbläst. Gerade kritische Kundinnen schließen bei dir ab. Lass auch Emotion in deine Nachrichten, gekauft wird mit Gefühl.",
    "Wassermann": "Du formulierst überraschend und eigen. Deine Nachrichten klingen nach niemandem sonst, das bleibt im Kopf. Standard-Skripte machen dich schwächer statt stärker. Schreib, wie du denkst, und stell am Ende eine klare Frage.",
    "Fische": "Du spürst beim Schreiben, was die andere gerade braucht. Deine Worte kommen weich an und bauen keinen Druck auf. Deshalb sagen dir Menschen Dinge, die sie sonst verschweigen. Führ das Gespräch trotzdem und lade zum nächsten Schritt ein."
  },
  haus2: {
    "Widder": "Geld kommt bei dir über Mut und Eigeninitiative. Du verdienst, wenn du losgehst, ohne auf Erlaubnis zu warten. Dein Einkommen wächst im Tempo deiner Entscheidungen. Warten ist die einzige Ausgabe, die du dir sparen kannst.",
    "Stier": "Geld will bei dir solide wachsen. Du brauchst Sicherheit, um frei zu verkaufen, und baust dir am besten treue Stammkundinnen auf. Wiederkehrende Bestellungen sind dein Fundament. Verlang mehr, als sich gewohnt anfühlt, dein Wert trägt das.",
    "Zwillinge": "Geld kommt bei dir über Kommunikation. Jedes Gespräch, jede Nachricht, jede Story kann bei dir zu Umsatz werden. Du verdienst am meisten, wenn du im Austausch bist. Verzettel dich nicht in zwanzig halben Gesprächen, führ fünf ganze.",
    "Krebs": "Geld und Gefühl hängen bei dir zusammen. Du verkaufst stark, wenn du dich sicher fühlst, und hältst zurück, wenn du dich schutzlos fühlst. Sorg gut für dich, dann fließt auch dein Umsatz. Dein Einkommen darf dich nähren, ohne dass du dich vorher erschöpfst.",
    "Löwe": "Geld folgt bei dir der Sichtbarkeit. Je mehr du dich zeigst, desto mehr verdienst du, diese Linie ist bei dir fast eine Gerade. Du darfst stolz verkaufen, dein Angebot ist eine Einladung in deine Welt. Verstecken ist bei dir die teuerste Gewohnheit.",
    "Jungfrau": "Geld kommt bei dir über Qualität und Verlässlichkeit. Kundinnen bleiben, weil du lieferst, nachfasst und an alles denkst. Dein Umsatz wächst über Systeme statt über Zufall. Hör auf, deinen Preis kleinzurechnen, gute Arbeit darf kosten.",
    "Waage": "Geld kommt bei dir über Beziehungen. Empfehlungen, Kooperationen und treue Kundinnen tragen dein Einkommen. Menschen kaufen, weil sie sich bei dir wohlfühlen. Bleib bei deinem Preis, Rabatte kaufen keine Liebe.",
    "Skorpion": "Geld ist bei dir ein Kraftthema. Alles oder nichts liegt dir mehr als ein bisschen. Wenn du dich ganz committest, entsteht bei dir Umsatz, der andere staunen lässt. Schau dir deine alten Geldgeschichten an, sonst steuern sie unsichtbar deine Preise.",
    "Schütze": "Geld wächst bei dir mit deinem Horizont. Kleine Ziele langweilen dein Konto. Du verdienst, wenn du groß denkst und dein Warum spürbar ist. Setz dir Ziele, die dich leicht nervös machen, genau dort beginnt dein Umsatz.",
    "Steinbock": "Geld ist bei dir das Ergebnis von Ausdauer und Struktur. Du baust Einkommen wie ein Haus: Fundament zuerst, dann die Stockwerke. In fünf Jahren stehst du dort, wo Schnellstarterinnen längst aufgegeben haben. Erlaub dir, schon unterwegs zu ernten.",
    "Wassermann": "Geld kommt bei dir über neue Wege. Du verdienst mit Methoden, die andere noch belächeln. Online-Systeme, Automatisierung und ungewöhnliche Ideen sind deine Einkommensquellen. Bau dein eigenes Modell, das kopierte macht dich müde und arm.",
    "Fische": "Geld fließt bei dir, wenn Sinn dahinter liegt. Für etwas, an das du glaubst, verkaufst du stärker als jede Strategin. Verbinde jeden Umsatz mit dem, was er möglich macht. Und schreib deine Zahlen auf, Nebel ist der Feind deines Kontos."
  },
  haus11: {
    "Widder": "Dein Netzwerk wächst über deine Initiative. Du bist die, die Menschen zusammenbringt und den ersten Schritt macht. Dein Team braucht deinen Zündfunken. Bau Partnerinnen auf, die selbst zünden, dann wächst es auch ohne dich.",
    "Stier": "Dein Netzwerk wächst langsam und hält dafür Jahre. Du baust lieber zehn treue Partnerinnen auf als hundert flüchtige Kontakte. Genau diese Treue macht dein Team wertvoll. Gib neuen Menschen trotzdem eine Chance, auch wenn Vertrauen bei dir Zeit braucht.",
    "Zwillinge": "Dein Netzwerk ist lebendig und weit verzweigt. Du kennst immer jemanden, der jemanden kennt. Verbindungen entstehen bei dir im Vorbeigehen. Führ sie zusammen, aus deinen Kontakten darf ein Team werden.",
    "Krebs": "Dein Team ist deine zweite Familie. Menschen bleiben bei dir, weil sie sich zugehörig fühlen. Diese Bindung ist deine Superkraft im Network. Pass auf, dass Zugehörigkeit kein goldener Käfig wird, deine Partnerinnen dürfen eigene Wege gehen.",
    "Löwe": "Du stehst natürlich im Zentrum deiner Community. Menschen versammeln sich um dich und deine Energie. Dein Team trägt deine Handschrift, und das ist gut so. Feiere die Erfolge deiner Partnerinnen lauter als deine eigenen, dann wächst dein Reich von allein.",
    "Jungfrau": "Dein Netzwerk lebt von deiner Zuverlässigkeit. Du bist die, bei der Onboarding, Systeme und Antworten funktionieren. Dein Team duplizierst du über saubere Abläufe. Denk daran, Menschen wollen neben der Organisation auch gefeiert werden.",
    "Waage": "Netzwerken ist deine Natur. Du verbindest Menschen, die einander sonst nie getroffen hätten, und alle fühlen sich wohl dabei. Kooperationen öffnen dir jede Tür. Wähle bewusst, wen du hineinlässt, dein Team braucht deine Klarheit mehr als deine Nettigkeit.",
    "Skorpion": "Dein Netzwerk ist klein, tief und loyal. Oberflächliche Kontakte halten sich bei dir nicht, dafür gehen die richtigen mit dir durch alles. Ein Kern aus wenigen entschlossenen Partnerinnen trägt dein ganzes Business. Vertrau ihnen Verantwortung an, Kontrolle bremst dein Wachstum.",
    "Schütze": "Dein Netzwerk kennt keine Grenzen. Du verbindest dich über Städte und Länder hinweg, und dein Team wächst dort, wo andere gar nicht suchen. Deine Vision hält die vielen zusammen. Gib ihr Struktur, damit aus Begeisterung Duplikation wird.",
    "Steinbock": "Dein Netzwerk baust du wie ein Unternehmen. Klare Rollen, klare Erwartungen, langfristige Bindungen. Menschen respektieren dich und richten sich an dir auf. Zeig deinem Team neben dem Leader auch den Menschen, Nähe macht deine Führung rund.",
    "Wassermann": "Dein Netzwerk ist eine Bewegung. Du sammelst Menschen um eine Idee, die größer ist als ein Produkt. Gleichgesinnte finden dich wie von selbst. Gib deiner Community ein gemeinsames Ziel, dann organisiert sie sich fast allein.",
    "Fische": "Dein Netzwerk entsteht über unsichtbare Fäden. Menschen kommen zu dir, wenn sie es am meisten brauchen, und bleiben, weil sie sich verstanden fühlen. Dein Team eint ein gemeinsames Gefühl statt einer Struktur. Hol dir für Systeme und Zahlen Unterstützung, dein Beitrag ist die Seele."
  }
};

function generateReading() {"""
repl("function generateReading() {", mini_texts, "mini-texts-injection")

# --- 1c. Ergebnis-Seite radikal vereinfachen --------------------------------
# Platzierungen, Aspekte und dominantes Element fliegen raus (Zielgruppe hat
# keinen Astro-Hintergrund). Stattdessen: Minireading aus 5 Punkten.
old_blocks = """  // Dominantes Element aus den Hauptpunkten zählen
  const elementCounts = { "Feuer": 0, "Erde": 0, "Luft": 0, "Wasser": 0 };
  planets.forEach(p => { const s = (CHART[p.key] || {}).sign; if (s && elementMap[s]) elementCounts[elementMap[s]]++; });

  const FULL = window.__fullChart || [];
  if (FULL.length) {
    const rows = FULL.map(e => `<div class="data-row"><span class="data-planet">${e.label}</span><span class="data-values"><span class="badge sign-badge">${e.sign}</span>${e.house ? `<span class="badge house-badge">${e.house}. Haus</span>` : ''}</span></div>`).join('');
    html += `
    <div class="data-block">
      <h3>Deine Platzierungen</h3>
      <div class="data-grid">${rows}</div>
      <button class="copy-btn" id="copyBtn" onclick="copyChartData()">Alle Daten kopieren</button>
    </div>`;
  }

  const ASP = window.__aspects || [];
  if (ASP.length) {
    const arows = ASP.map(a => `<div class="data-row"><span class="data-planet">${a.p1}${a.s1 ? ` <span class="asp-sign">${a.s1}</span>` : ''} <span class="asp-sym">·</span> ${a.p2}${a.s2 ? ` <span class="asp-sign">${a.s2}</span>` : ''}</span><span class="data-values"><span class="badge sign-badge">${a.type}</span></span></div>`).join('');
    html += `
    <div class="data-block">
      <h3>Deine wichtigsten Aspekte</h3>
      <div class="data-grid aspect-grid">${arows}</div>
      <button class="copy-btn" id="copyAspBtn" onclick="copyAspects()">Aspekte kopieren</button>
    </div>`;
  }

  const maxEl = Object.entries(elementCounts).sort((a,b)=>b[1]-a[1]).filter(e=>e[1]>0);
  if (maxEl.length > 0) {
    const dominantEl = maxEl[0][0];
    html += `
    <div class="summary-block">
      <h3>Dein dominantes Element: ${dominantEl}</h3>
      <p>${elementDescriptions[dominantEl]}</p>
    </div>`;
  }
"""
new_blocks = """  // Minireading: 5 Punkte, kurz und konkret, ohne Astro-Fachsprache
  const FULL = window.__fullChart || [];
  const LX = window.__leader || {};
  const MINI = window.LEADER_MINI || {};
  function fSign(label){ const e = FULL.find(function(x){ return x.label === label; }); return e ? e.sign : ''; }
  function cuspSign(n){ const h = (LX.houses || []).find(function(x){ return x.num === n; }); return h ? h.sign : ''; }
  const miniParts = [
    { title: 'Dein Außenauftritt', sub: 'Aszendent', sign: fSign('Aszendent'), texts: MINI.ac },
    { title: 'Dein Leadership-Kern', sub: 'Sonne', sign: fSign('Sonne'), texts: MINI.sonne },
    { title: 'Deine Verkaufssprache', sub: 'Merkur', sign: fSign('Merkur'), texts: MINI.merkur },
    { title: 'Dein Geld-Selbstwert', sub: '2. Haus', sign: cuspSign(2), texts: MINI.haus2 },
    { title: 'Dein Netzwerk und dein Team', sub: '11. Haus', sign: cuspSign(11), texts: MINI.haus11 }
  ];
  miniParts.forEach(function(p){
    if(!p.sign || !p.texts || !p.texts[p.sign]) return;
    html += `
    <div class="summary-block">
      <h3>${p.title}</h3>
      <p style="color:var(--gold);font-size:0.95rem;letter-spacing:0.06em;margin:0 0 12px;">${p.sub}: ${p.sign}</p>
      <p>${p.texts[p.sign]}</p>
    </div>`;
  });
"""
repl(old_blocks, new_blocks, "mini-reading-blocks")

# --- 2. Ergebnis-Kopf + Zurueck-Button ------------------------------------
repl("<h2>Dein Business-Code${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Dein Chart als Business-Blueprint'}</p>",
     "<h2>Dein Leader-Code${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Dein Weg vom Partner zum Leader'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Neuen Leader-Code erstellen", "back-btn")

# --- 3. Network-Haeuser in runCheck berechnen ------------------------------
# Anker NACH window.__chart, damit __fullChart bereits gesetzt ist.
# Haeuserspitzen-Accessor 1:1 aus dem Womancode-Reader (dort gegen die Engine
# verifiziert): horo.Houses[h].ChartPosition.StartPosition.Ecliptic.DecimalDegrees
calc_anchor = "      window.__chart = chart;\n      generateReading();"
leader_calc = """      window.__chart = chart;

      // Network-Haeuser: Zeichen auf der Placidus-Haeuserspitze + Punkte im Haus.
      (function(){
        try{
          const SIGNS_DE = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische'];
          const THEMES = { 1:'Außenauftritt', 2:'Geld und Selbstwert', 3:'Kommunikation und Verkauf', 6:'Routinen und Arbeit', 7:'Kundinnen und Partnerinnen', 8:'Geld durch andere', 9:'Duplikation und Lehren', 10:'Ruf und Sichtbarkeit', 11:'Netzwerk und Team' };
          const FULL = window.__fullChart || [];
          const houses = [];
          [1,2,3,6,7,8,9,10,11].forEach(function(n){
            let deg = null;
            try{
              const H = horo.Houses[n-1];
              deg = (H && H.ChartPosition && H.ChartPosition.StartPosition && H.ChartPosition.StartPosition.Ecliptic)
                ? H.ChartPosition.StartPosition.Ecliptic.DecimalDegrees : null;
            }catch(e){}
            if(deg == null) return;
            const sign = SIGNS_DE[Math.floor((((deg % 360) + 360) % 360) / 30)] || '';
            const points = FULL.filter(function(e){ return Number(e.house) === n; }).map(function(e){ return e.label; });
            houses.push({ num: n, theme: THEMES[n] || '', sign: sign, points: points });
          });
          window.__leader = (houses.length === 9) ? { houses: houses } : null;
        }catch(e){ window.__leader = null; }
      })();

      generateReading();"""
repl(calc_anchor, leader_calc, "leader-calc-injection")

# --- 4. Reading-Block: sichtbare Network-Haeuser + Prompt-CTA ---------------
old_cta = """  html += `
  <div class="cta-block">
    <h3>Dein Business-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, wie du dein Business führst, wie du dich positionierst, wo deine Zone of Genius liegt und wie du am natürlichsten Geld verdienst.</p>
    <button class="copy-btn" id="copyBizBtn" onclick="copyBusinessReading()">Business-Prompt + Daten kopieren</button>
  </div>`;"""

new_cta = """  html += `
  <div class="cta-block">
    <h3>Dein volles Leader-Reading mit KI</h3>
    <p>Das Minireading oben ist der erste Blick. Kopiere jetzt den Prompt und füg ihn in ChatGPT oder Claude ein. Dein volles Reading geht durch elf Punkte deiner Chart: von deinem Außenauftritt über deine Verkaufssprache und dein Geld bis zu deinem Weg vom Partner zum Leader. Alle Daten dafür sind schon drin, du musst nichts ausfüllen.</p>
    <button class="copy-btn" id="copyLeaderBtn" onclick="copyLeaderReading()">Leader-Prompt + Daten kopieren</button>
  </div>`;"""
repl(old_cta, new_cta, "cta-block")

# --- 5. Abschluss-CTA (AstroCode-Werbung) ersatzlos entfernen ---------------
repl('''  html += `
  <div class="cta-block">
    <p class="cta-kicker">Möchtest du noch tiefer in deine Chart eintauchen?</p>
    <h3>Lerne dich tiefer kennen, als Jahre der Selbstreflexion es je konnten.</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Hier erfährst du mehr: Dein AstroCode &rarr;</a>
  </div>`;

''', '', "upsell-remove")

# --- 6. Prompt-Gehirn + Copy-Funktion austauschen --------------------------
new_region = r"""  const LEADER_PROMPT = `Du bist eine erfahrene Bewusstseinsastrologin und Mentorin für Network Marketing. Du liest ein Geburtshoroskop als Entwicklungsweg: Es zeigt, wie ich wirke, wie ich verkaufe, wie ich mit Geld umgehe und was für eine Leaderin in mir angelegt ist. Du schreibst wie eine Mentorin, die an mich glaubt: klar, warm, motivierend und mit Tiefe. Deine Sätze dürfen fließen und mich mitnehmen, solange jeder Satz etwas Konkretes sagt. Keine Astro-Fachbegriffe ohne Erklärung. Ich soll dein Reading in einem Zug durchlesen und danach Lust haben loszulegen. Keine Floskeln, keine allgemeinen Astro-Sätze, kein Lehrbuchton.

Ich baue ein Network-Marketing-Business auf. Mein Alltag: Ich zeige mich in Storys, schreibe Nachrichten, führe Erstgespräche, mache Follow-ups, gewinne Kundinnen und Partnerinnen und baue ein Team auf, das ohne mich weiterwächst.

Unten bekommst du:
- meine Network-Häuser: das Zeichen auf der Häuserspitze und die Punkte im Haus
- mein vollständiges Chart (alle Punkte mit Zeichen und Haus)

Gehe die elf Punkte unten durch. Für jeden Punkt schreibe vier Dinge:
- Meine Stärke: was Zeichen, Haus und Planeten an diesem Punkt über mich sagen und warum das in meinem Business wertvoll ist. Beginn immer mit dem, was ich gut kann. Steht kein Planet im Haus, dann deute das Zeichen auf der Häuserspitze.
- So nutze ich sie: konkret in Storys, Nachrichten, Gesprächen, Follow-ups und Team-Calls. Nenne reale Situationen, die ich morgen umsetzen kann.
- Mein Wachstumsfeld: was mich an diesem Punkt noch bremst und wie ich es drehe. Formuliere es so, dass ich Lust bekomme, es anzugehen. Kein Urteil, kein erhobener Zeigefinger.
- Eine Frage, die mich motiviert, heute den nächsten Schritt zu gehen.

BLOCK 1: WIE ICH WIRKE UND VERKAUFE
1. Aszendent und 1. Haus: mein Außenauftritt. So erleben mich Fremde in der Story und in der ersten Nachricht.
2. Merkur und 3. Haus: meine Verkaufssprache. Wie ich schreibe, spreche und überzeuge.
3. Venus: meine Anziehungskraft. Wie ich Menschen für mich gewinne und wie ich das, was ich verkaufe, selbst ausstrahle.

BLOCK 2: MEIN GELD UND MEINE ARBEIT
4. 2. Haus: mein Geld-Selbstwert. Was ich mir zu verlangen traue und wie ich über Einkommen denke.
5. 6. Haus: meine Routinen. Wie meine tägliche Arbeit aussehen darf, damit ich über Monate dranbleibe.
6. 8. Haus: Geld durch andere. Provisionen, Teamumsatz und mein Magnetismus.

BLOCK 3: VOM PARTNER ZUM LEADER
7. Sonne: mein Leadership-Kern. Wie ich von Natur aus führe.
8. 7. Haus: meine Partnerschaften. Wie ich Kundinnen und Partnerinnen gewinne und halte.
9. Jupiter und 9. Haus: meine Duplikation. Wie ich lehre, wie ich Wissen weitergebe und wo mein Team am leichtesten wächst.
10. MC und 10. Haus: mein Ruf. Wofür man mich kennt und wie ich als Leaderin sichtbar werde.
11. 11. Haus: mein Netzwerk. Wie ich Community aufbaue und wie mein Team skaliert.

Webe außerdem drei Punkte dort ein, wo sie in meiner Chart stehen, statt sie separat zu behandeln: Mars (wie ich ins Handeln komme und was ein Nein mit mir macht), Saturn (wo ich dranbleibe und wo ich mich selbst ausbremse) und Mond (was ich brauche, um bei Ablehnung stabil zu bleiben).

Am Ende: mein Weg vom Partner zum Leader. Welches eine Kernthema zieht sich durch meine Chart? Welche Art Leaderin ist in mir angelegt und was davon lebe ich noch nicht? Schließe mit einem einzigen konkreten Schritt, den ich diese Woche gehe, und einem Satz, der mir zeigt, was möglich wird, wenn ich dranbleibe.

Schreib auf Deutsch, in der Du-Form. Schreib mit Tiefe: Deine Sätze dürfen fließen, leicht zu lesen und trotzdem voller Substanz. Dein Reading soll mich tragen: Ich lese es zu Ende und will danach sofort die erste Nachricht schreiben. Jeder Satz konkret. Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker.

Hier sind meine Daten:`;

  window.copyLeaderReading = function(){
    const FULL = window.__fullChart || [];
    const L = window.__leader || {};
    const m = window.__meta || {};
    const data = [];
    if(m.name) data.push('Name: ' + m.name);
    if(m.date){ const dp = m.date.split('-'); data.push('Geburtsdatum: ' + dp[2]+'.'+dp[1]+'.'+dp[0] + (m.time ? (' um ' + m.time + ' Uhr') : '')); }
    if(m.place) data.push('Geburtsort: ' + m.place);
    data.push('');
    if(L.houses && L.houses.length){
      data.push('MEINE NETWORK-HÄUSER (Placidus, Zeichen auf der Häuserspitze + Punkte im Haus):');
      L.houses.forEach(function(h){
        data.push(h.num + '. Haus (' + h.theme + '): ' + h.sign + ' / Punkte im Haus: ' + (h.points.length ? h.points.join(', ') : 'keine'));
      });
      data.push('');
    }
    data.push('MEIN VOLLSTÄNDIGES CHART:');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });
    const full = LEADER_PROMPT + '\n\n' + data.join('\n');
    const btn = document.getElementById('copyLeaderBtn');
    const done = function(){ if(btn){ const o = btn.getAttribute('data-label') || btn.textContent; btn.setAttribute('data-label', o); btn.textContent = '✓ Kopiert! Jetzt in ChatGPT einfügen'; setTimeout(function(){ btn.textContent = o; }, 2800); } };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(full).then(done).catch(function(){ fallbackCopy(full, done); });
    } else { fallbackCopy(full, done); }
  };"""

pat = re.compile(r"  const BUSINESS_PROMPT = `.*?\n  window\.copyBusinessReading = function\(\)\{.*?\n  \};", re.DOTALL)
if not pat.search(s):
    sys.exit("FEHLT: BUSINESS_PROMPT / copyBusinessReading Region")
s = pat.sub(lambda _: new_region, s, count=1)

# Sicherheitscheck: keine Business-Reste und keine Werbung mehr
for leftover in ["copyBusinessReading", "copyBizBtn", "BUSINESS_PROMPT", "subscribeLead", "userEmail", "dein-astrocode", "cta-kicker\">"]:
    if leftover in s:
        sys.exit("REST gefunden: " + leftover)

with open(DST, "w", encoding="utf-8") as f:
    f.write(s)

os.makedirs(NETLIFY, exist_ok=True)
shutil.copyfile(DST, os.path.join(NETLIFY, "index.html"))

print("OK ->", DST)
print("OK ->", os.path.join(NETLIFY, "index.html"))
print("Groesse:", len(s), "Zeichen")
