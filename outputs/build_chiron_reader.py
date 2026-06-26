#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut den Chiron-in-Stier-Reader aus dem Business-Reader.
Gleiches Design + gleiche Astro-Engine, nur das Reading-Gehirn wird getauscht:
Der Reader rechnet automatisch aus, in welchem Haus bei dir Stier liegt
(dort wirkt der Chiron-Transit die naechsten Jahre), wo dein natales Chiron
steht und welche Planeten du im Stier hast. Daraus + dem vollen Chart baut er
einen fertigen KI-Prompt zum Kopieren.

Quelle:  astro-business-reader.html
Ziel:    astro-chiron-reader.html
Bei Design-Updates am Business-Reader dieses Skript erneut laufen lassen.
"""
import re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-chiron-reader.html")

with open(SRC, "r", encoding="utf-8") as f:
    s = f.read()

def repl(old, new, label):
    global s
    if old not in s:
        sys.exit("FEHLT (" + label + "): " + old[:80])
    s = s.replace(old, new, 1)

# --- Womancode-Logo + CSS aus dem Womancode-Reader holen (Design-Signatur) ---
WC = os.path.join(HERE, "womancode-reader.html")
WC_LOGO_IMG = ""
WC_SKIN = ""
if os.path.exists(WC):
    wsrc = open(WC, encoding="utf-8").read()
    mi = re.search(r'<img class="wc-logo"[^>]*>', wsrc)
    if mi:
        WC_LOGO_IMG = mi.group(0)
    # Kompletter Womancode-Skin-Block: Wein/Lotus-Hintergrund, killt Blau
    # (binary-canvas, body::before, Sterne/Mond), Wein-Karten, warme Schrift,
    # Gold-Buttons und das .wc-logo CSS. Erkennbar an Lotus-Bild + #220812.
    for sm in re.finditer(r'<style[^>]*>(.*?)</style>', wsrc, re.DOTALL):
        inner = sm.group(1)
        if 'data:image/' in inner and '#220812' in inner:
            WC_SKIN = inner
            break

# --- 1. Branding / sichtbare Texte ---------------------------------------
repl("<title>Dein Business-Code</title>",
     "<title>Womancode · Chiron in Stier</title>", "title")

# Eyebrow-Zeile durch das Womancode-Logo ersetzen (so wie im Womancode-Reader)
repl('<p class="header-eyebrow">Dein kosmischer Business-Blueprint</p>',
     (WC_LOGO_IMG if WC_LOGO_IMG else '<p class="header-eyebrow">Womancode</p>'),
     "eyebrow-logo")

# Kompletten Womancode-Skin als letzten Style-Block vor </body> einsetzen,
# damit er alles (auch die blaue Ebene) ueberschreibt.
if WC_SKIN:
    repl("</body>", "<style>\n" + WC_SKIN + "\n</style>\n</body>", "wc-skin")

# Mehr Luft zwischen den Karten und innerhalb des Womancode-CTA-Blocks.
SPACING_CSS = """<style>
  .data-block, .cta-block, .summary-block, .results-header{ margin-top:40px !important; margin-bottom:40px !important; }
  .cta-block .cta-kicker{ margin-bottom:16px !important; }
  .cta-block h3{ margin:14px 0 16px !important; line-height:1.3 !important; }
  .cta-block .cta-text{ margin:0 0 24px !important; }
</style>"""
repl("</body>", SPACING_CSS + "\n</body>", "spacing-css")

repl("<h1>Dein Business-Code</h1>", "<h1>Chiron in Stier trifft deine Weiblichkeit</h1>", "h1")

repl('<p class="subtitle">Gib deine Geburtsdaten ein. Auf der nächsten Seite bekommst du dein Geburtshoroskop angezeigt und einen fertigen KI-Prompt, der dir sagt, wie du dein Business führst, dich positionierst, skalierst und Geld verdienst.</p>',
     '<p class="subtitle">Chiron wandert die nächsten Jahre durch das Tierkreiszeichen Stier und rüttelt an deinem Selbstwert und deinem Körper. Gib deine Geburtsdaten ein. Du bekommst zwei fertige KI-Prompts: dein Chiron-Reading für die nächsten Jahre und deinen Womancode-Spiegel, der dir zeigt, wo du dich als Frau noch nicht lebst.</p>',
     "subtitle")

repl('onclick="runCheck()">Meinen Business-Code aufdecken</button>',
     'onclick="runCheck()">Meine Chart aufdecken</button>', "submit-btn")

# --- E-Mail komplett entfernen (kein Opt-in) ------------------------------
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

repl("<h2>Dein Business-Code${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Dein Chart als Business-Blueprint'}</p>",
     "<h2>Deine Chart${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Chiron in Stier trifft deine Weiblichkeit'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Neue Chart erstellen", "back-btn")

# --- Abschluss-CTA: AstroCode-Kurs raus, Womancode-Salespage rein ---------
repl('''  html += `
  <div class="cta-block">
    <p class="cta-kicker">Möchtest du noch tiefer in deine Chart eintauchen?</p>
    <h3>Lerne dich tiefer kennen, als Jahre der Selbstreflexion es je konnten.</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Hier erfährst du mehr: Dein AstroCode &rarr;</a>
  </div>`;''',
'''  html += `
  <div class="cta-block">
    <p class="cta-kicker">Hast du es satt, deine Weiblichkeit zu zügeln?</p>
    <h3>Lebe dein Womancode im Live-Experiment und werde erfolgreich, glücklich und lebendig.</h3>
    <p class="cta-text">Womancode steht für eine gelebte, lebendige Weiblichkeit. Eine Frau, die weiß, wer sie ist und aus ihrem tiefsten Inneren kreiert.</p>
    <a href="https://patrycja-nasri.de/womancode/" target="_blank" class="cta-link">Hier geht's zu Womancode &rarr;</a>
  </div>`;''',
"womancode-salespage-cta")

# --- 2. Chiron-Berechnung in runCheck einhaengen -------------------------
# Anker NACH window.__chart, damit window.__aspects bereits gesetzt ist.
calc_anchor = "      window.__chart = chart;\n      generateReading();"
chiron_calc = """      window.__chart = chart;

      // Chiron in Stier: mehrere Chart-Schichten fuer ein tiefes Reading
      (function(){
        const houses = horo.Houses || [];
        function houseOfLong(L){
          for(let i=0;i<houses.length;i++){
            const h = houses[i];
            let st, en;
            try { st = h.ChartPosition.StartPosition.Ecliptic.DecimalDegrees; en = h.ChartPosition.EndPosition.Ecliptic.DecimalDegrees; }
            catch(err){ continue; }
            const id = h.id || (i+1);
            if(st <= en){ if(L >= st && L < en) return id; }
            else { if(L >= st || L < en) return id; }
          }
          return null;
        }
        const hs = [];
        [30.01, 45, 59.99].forEach(function(L){ const id = houseOfLong(L); if(id && hs.indexOf(id) === -1) hs.push(id); });
        const FULL = window.__fullChart || [];
        function find(label){ return FULL.find(function(e){ return e.label === label; }) || null; }
        const chironEntry = find('Chiron') || {};
        const venusEntry = find('Venus') || {};
        // Alle Punkte im Stier, die Chiron auf seinem Weg beruehrt: Planeten,
        // Knoten, Lilith UND die Achsen (AC/DC/MC/IC). Eine Chiron-Konjunktion
        // zum IC oder MC ist genauso eine Aktivierung wie ueber einen Planeten.
        const taurusPoints = FULL.filter(function(e){ return e.sign === 'Stier' && e.label !== 'Chiron'; });
        const RULER = { 'Widder':'Mars','Stier':'Venus','Zwillinge':'Merkur','Krebs':'Mond','Loewe':'Sonne','Löwe':'Sonne','Jungfrau':'Merkur','Waage':'Venus','Skorpion':'Pluto','Schuetze':'Jupiter','Schütze':'Jupiter','Steinbock':'Saturn','Wassermann':'Uranus','Fische':'Neptun' };
        const rulerName = RULER[chironEntry.sign] || '';
        const rulerEntry = rulerName ? (find(rulerName) || {}) : {};
        const ASP = window.__aspects || [];
        const chironAspects = ASP.filter(function(a){ return a.p1 === 'Chiron' || a.p2 === 'Chiron'; });
        window.__chiron = {
          houses: hs,
          natalSign: chironEntry.sign || '',
          natalHouse: chironEntry.house || '',
          taurusPoints: taurusPoints,
          venus: { sign: venusEntry.sign || '', house: venusEntry.house || '' },
          ruler: { name: rulerName, sign: rulerEntry.sign || '', house: rulerEntry.house || '' },
          chironAspects: chironAspects
        };
      })();

      generateReading();"""
repl(calc_anchor, chiron_calc, "chiron-calc-injection")

# --- 3. Reading-Block: sichtbares Chiron-Thema + Prompt-CTA --------------
old_cta = """  html += `
  <div class="cta-block">
    <h3>Dein Business-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, wie du dein Business führst, wie du dich positionierst, wo deine Zone of Genius liegt und wie du am natürlichsten Geld verdienst.</p>
    <button class="copy-btn" id="copyBizBtn" onclick="copyBusinessReading()">Business-Prompt + Daten kopieren</button>
  </div>`;"""

new_cta = """  // Sichtbares Chiron-in-Stier-Thema
  const C = window.__chiron || {};
  const chs = C.houses || [];
  const houseStr = chs.length ? (chs.length === 1 ? (chs[0] + '. Haus') : (chs.slice(0,-1).join('., ') + '. und ' + chs[chs.length-1] + '. Haus')) : '';
  const tps = (C.taurusPoints || []).map(function(e){ return e.label; });
  const ven = C.venus || {};
  let chiHtml = `
  <div class="data-block">
    <h3>Dein Chiron-in-Stier-Thema</h3>
    <div class="data-grid">`;
  if(houseStr) chiHtml += `<div class="data-row"><span class="data-planet">Stier liegt bei dir im</span><span class="data-values"><span class="badge house-badge">${houseStr}</span></span></div>`;
  if(ven.sign) chiHtml += `<div class="data-row"><span class="data-planet">Venus (Herrscher des Stier)</span><span class="data-values"><span class="badge sign-badge">${ven.sign}</span>${ven.house ? `<span class="badge house-badge">${ven.house}. Haus</span>` : ''}</span></div>`;
  if(C.natalSign) chiHtml += `<div class="data-row"><span class="data-planet">Dein natales Chiron</span><span class="data-values"><span class="badge sign-badge">${C.natalSign}</span>${C.natalHouse ? `<span class="badge house-badge">${C.natalHouse}. Haus</span>` : ''}</span></div>`;
  chiHtml += `<div class="data-row"><span class="data-planet">Punkte im Stier (Planeten & Achsen)</span><span class="data-values"><span class="badge sign-badge">${tps.length ? tps.join(', ') : 'keine'}</span></span></div>`;
  chiHtml += `</div>`;
  if(C.natalSign === 'Stier') chiHtml += `<p style="margin-top:14px;opacity:.92">Dein Chiron steht selbst im Stier. Du erlebst gerade deinen Chiron-Return, einen großen Zyklus rund um deinen Selbstwert.</p>`;
  chiHtml += `</div>`;
  html += chiHtml;

  html += `
  <div class="cta-block">
    <h3>Dein Chiron-in-Stier-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir dein persönliches Chiron-Thema für die nächsten Jahre: in welchem Lebensbereich dein Selbstwert berührt wird, was dein Schatten ist und welches Geschenk darin liegt.</p>
    <button class="copy-btn" id="copyChironBtn" onclick="copyChironReading()">Chiron-Prompt + Daten kopieren</button>
  </div>`;

  html += `
  <div class="cta-block">
    <h3>Und jetzt tiefer: Deine Weiblichkeit</h3>
    <p>Chiron in Stier rührt an deinem Wert und an deinem Körper. Dieser zweite Prompt geht noch tiefer und zeigt dir aus deiner Chart, wo und warum du dich als Frau nicht lebst und deine weibliche Energie unterdrückst. Kopier ihn und füg ihn in ChatGPT oder Claude ein.</p>
    <button class="copy-btn" id="copyWomancodeBtn" onclick="copyWomancodeReading()">Womancode-Painpoints + Daten kopieren</button>
  </div>`;"""
repl(old_cta, new_cta, "cta-block")

# --- 4. Prompt-Gehirn + Copy-Funktion austauschen ------------------------
new_region = r"""  const CHIRON_PROMPT = `Du bist eine erfahrene Bewusstseinsastrologin mit dem Blick für die Urwunde Chiron. Du liest meine Chart in Schichten und schreibst klar, tief und direkt, so dass mich jeder Satz trifft. Keine Floskeln, keine allgemeinen Astro-Sätze, kein Lehrbuchton.

Mein Thema: Chiron läuft die nächsten Jahre durch das Tierkreiszeichen Stier. Stier steht für Selbstwert, Körper, Sinnlichkeit, Genuss, Geld, Sicherheit, Besitz und die Frage "Was bin ich wert?". Chiron ist die Urwunde, die nicht heilt, die berührt und integriert werden will und die mein größtes Geschenk an die Welt in sich trägt.

Unten bekommst du mehrere Schichten meiner Chart:
- in welchem Haus bei mir Stier liegt (dort wirkt der Transit die nächsten Jahre)
- Venus, die Herrscherin des Stier und damit der rote Faden meines Selbstwerts: ihr Zeichen und Haus zeigen, woran ich meinen Wert messe und wie ich empfange
- die Punkte, die ich im Stier habe und die Chiron auf seinem Weg nacheinander berührt, egal ob Planet oder Achse wie MC oder IC (das sind meine Aktivierungs-Phasen)
- mein natales Chiron mit Zeichen, Haus und seinen Aspekten (so ist meine Wunde verdrahtet)
- der Herrscher meines Chiron-Zeichens (dorthin sucht die Wunde ihren Weg in die Heilung)
- mein vollständiges Chart als Kontext

Schreibe mir auf dieser Basis:

1. Mein Kernthema. Ein kraftvoller Absatz: worum es in den nächsten Jahren für mich geht. Sprich mich direkt mit "du" an.

2. Wo es sich zeigt. Nimm das Haus, in dem Stier bei mir liegt, und mach konkret, in welchem Lebensbereich meine Selbstwert-Wunde berührt wird, zum Beispiel Geld, Arbeit, Beziehungen, Körper, Zuhause oder Sichtbarkeit.

3. Venus als Schlüssel. Lies aus Venus' Zeichen und Haus, woran ich heute meinen Wert festmache und wie ich Geld, Genuss und Liebe empfange. Zeig mir, wo ich mich da kleiner mache, als ich bin.

4. Die Aktivierungen. Geh jeden Punkt durch, den ich im Stier habe, egal ob Planet oder Achse. Sag mir, was in mir berührt wird, wenn Chiron darüberzieht, und wie ich diese Phase nutze. Steht eine Achse wie mein IC oder MC im Stier, geh besonders darauf ein, was es heißt, wenn Chiron über diesen sensiblen Lebenspunkt zieht (IC ist meine Wurzel, mein Zuhause, mein innerer Boden; MC ist mein Weg nach außen, meine Berufung). Habe ich keinen Punkt im Stier, dann arbeite mit dem Haus.

5. Wie meine Wunde verdrahtet ist. Lies mein natales Chiron und seine Aspekte. Welche inneren Anteile zieht die Wunde mit hinein? Und über den Herrscher meines Chiron-Zeichens: wohin will sie geheilt werden?

6. Schatten und Geschenk. Wo halte ich fest, mache mich klein, spreche mir meinen Wert ab oder suche Sicherheit im Außen, die es so nicht gibt. Und was wächst, wenn ich die Wunde berühre statt sie zu meiden.

7. Der Weg durch den Körper. Eine konkrete, sinnliche Einladung, wie ich zurück in meinen Körper und in den Genuss komme.

8. Meine Schattenfrage. Eine einzige, konfrontierende Frage, die mich nicht mehr loslässt.

Wenn mein natales Chiron selbst im Stier steht, erlebe ich gerade meinen Chiron-Return. Geh in dem Fall besonders darauf ein, dass sich hier ein großer Lebenszyklus rund um meinen Selbstwert schließt.

Schreib auf Deutsch, in der Du-Form, in Tiefe statt in Breite. Jeder Satz konkret. Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker.

Hier sind meine Daten:`;

  window.copyChironReading = function(){
    const FULL = window.__fullChart || [];
    const C = window.__chiron || {};
    const m = window.__meta || {};
    const data = [];
    if(m.name) data.push('Name: ' + m.name);
    if(m.date){ const dp = m.date.split('-'); data.push('Geburtsdatum: ' + dp[2]+'.'+dp[1]+'.'+dp[0] + (m.time ? (' um ' + m.time + ' Uhr') : '')); }
    if(m.place) data.push('Geburtsort: ' + m.place);
    data.push('');
    data.push('MEIN CHIRON-IN-STIER-THEMA:');
    const hs = C.houses || [];
    const houseStr = hs.length ? (hs.length === 1 ? (hs[0] + '. Haus') : (hs.slice(0,-1).join('., ') + '. und ' + hs[hs.length-1] + '. Haus')) : '';
    if(houseStr) data.push('Das Tierkreiszeichen Stier liegt in meinem ' + houseStr + '. Dort wirkt der Chiron-Transit die nächsten Jahre.');
    const ven = C.venus || {};
    if(ven.sign) data.push('Venus (Herrscherin des Stier, roter Faden meines Selbstwerts): ' + ven.sign + (ven.house ? (', ' + ven.house + '. Haus') : '') + '.');
    const tp = (C.taurusPoints || []).map(function(e){ return e.label; });
    data.push('Punkte (Planeten und Achsen wie MC/IC), die ich im Stier habe und die Chiron nacheinander berührt (meine Aktivierungs-Phasen): ' + (tp.length ? tp.join(', ') : 'keine') + '.');
    if(C.natalSign) data.push('Mein natales Chiron steht in ' + C.natalSign + (C.natalHouse ? (', ' + C.natalHouse + '. Haus') : '') + '.');
    const ru = C.ruler || {};
    if(ru.name && ru.sign) data.push('Herrscher meines Chiron-Zeichens (' + ru.name + ', dorthin sucht die Wunde ihre Heilung): ' + ru.sign + (ru.house ? (', ' + ru.house + '. Haus') : '') + '.');
    const ca = C.chironAspects || [];
    if(ca.length){
      data.push('Aspekte meines natalen Chiron (so ist die Wunde verdrahtet):');
      ca.forEach(function(a){ const other = (a.p1 === 'Chiron') ? a.p2 : a.p1; const os = (a.p1 === 'Chiron') ? a.s2 : a.s1; data.push('- Chiron ' + a.type + ' ' + other + (os ? (' in ' + os) : '')); });
    }
    if(C.natalSign === 'Stier') data.push('Mein Chiron steht selbst im Stier: ich erlebe gerade meinen Chiron-Return.');
    data.push('');
    data.push('MEIN VOLLSTÄNDIGES CHART:');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });
    const full = CHIRON_PROMPT + '\n\n' + data.join('\n');
    const btn = document.getElementById('copyChironBtn');
    const done = function(){ if(btn){ const o = btn.getAttribute('data-label') || btn.textContent; btn.setAttribute('data-label', o); btn.textContent = '✓ Kopiert! Jetzt in ChatGPT einfügen'; setTimeout(function(){ btn.textContent = o; }, 2800); } };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(full).then(done).catch(function(){ fallbackCopy(full, done); });
    } else { fallbackCopy(full, done); }
  };

  const WOMANCODE_PROMPT = `Du bist eine Bewusstseinsastrologin und Embodiment-Mentorin für Weiblichkeit. Du liest meine Chart als Spiegel meiner weiblichen Energie und sprichst schonungslos klar, warm und direkt. Du benennst meinen Schmerz so genau, dass ich mich erkenne und es weh tut, im guten Sinn. Keine Floskeln, keine allgemeinen Astro-Sätze, kein Lehrbuchton.

Worum es geht: Ich bin eine Frau, die im Außen funktioniert. Ich versorge alle, halte alles am Laufen und stehe selbst an letzter Stelle. Ich lebe im Kopf, spüre meinen Körper kaum noch und habe meine Weiblichkeit irgendwann leise abgestellt. Meine Lust, meine Sinnlichkeit, mein Empfangen liegen brach. Ich will wissen, wo und warum ich mich als Frau nicht lebe und meine weibliche Energie unterdrücke.

Lies dafür die weiblichen Marker in meiner Chart und deute sie auf genau diese Frage:
- Mond: meine Bedürfnisse, mein Genährt-werden, das, was ich mir selbst nie gebe
- Venus: mein Selbstwert, mein Genuss, mein Empfangen, ob ich mir Lust und Schönheit erlaube
- Lilith: meine wilde, verbannte weibliche Kraft, das, was ich an mir unterdrückt habe, um dazuzugehören
- Chiron: meine Urwunde, wo ich mich als Frau verletzt oder falsch gefühlt habe
- IC und 4. Haus: meine weibliche Wurzel, die Frauenlinie, was ich von meiner Mutter über das Frausein übernommen habe
- 8. Haus: meine Sexualität, meine Hingabe, meine Tiefe
- 12. Haus: das, was ich versteckt und verleugnet habe
- Mondknoten: wohin meine weibliche Seele eigentlich will

Schreibe mir auf dieser Basis:

1. Mein Spiegel. Ein kurzer, ehrlicher Absatz, der mich sofort trifft: wie ich heute lebe und wo ich mich selbst verloren habe.

2. Meine Painpoints. Drei bis fünf konkrete, schmerzhafte Wunden aus meiner Chart. Für jede: benenne die Stelle in der Chart, dann die echte Alltagsszene, in der sich dieser Schmerz zeigt (zum Beispiel ich falle abends leer ins Bett, ich ziehe weite Kleidung an um nicht gesehen zu werden, ich habe keine Lust mehr auf Nähe, ich kann nicht annehmen wenn mir jemand etwas gibt). Sag mir auch, warum ich diese Energie abgestellt habe.

3. Was es mich kostet. Was in meinem Leben fehlt, solange ich so weiterlebe: an Lebendigkeit, an Lust, an Anziehung, an Fülle.

4. Die Brücke. Sanft und klar: dass diese Energie nicht verschwunden ist. Sie liegt unter dem Funktionieren begraben. Und Womancode ist der Weg zurück, ein gelebtes Experiment zurück in den Körper, in die Sinnlichkeit, ins Empfangen, an die erste Stelle. Lade mich ein, diesen Weg zu gehen, ohne mich zu drängen.

5. Eine einzige Frage, die mich heute Nacht nicht schlafen lässt.

Schreib auf Deutsch, in der Du-Form, in Tiefe statt in Breite. Jeder Satz konkret und aus einer echten Szene. Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker.

Hier sind meine Daten:`;

  window.copyWomancodeReading = function(){
    const FULL = window.__fullChart || [];
    const ASP = window.__aspects || [];
    const m = window.__meta || {};
    const data = [];
    if(m.name) data.push('Name: ' + m.name);
    if(m.date){ const dp = m.date.split('-'); data.push('Geburtsdatum: ' + dp[2]+'.'+dp[1]+'.'+dp[0] + (m.time ? (' um ' + m.time + ' Uhr') : '')); }
    if(m.place) data.push('Geburtsort: ' + m.place);
    data.push('');
    data.push('MEINE WEIBLICHEN PUNKTE:');
    ['Mond','Venus','Lilith','Chiron','IC','Nordknoten'].forEach(function(lab){ const e = FULL.find(function(x){ return x.label === lab; }); if(e) data.push(lab + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });
    data.push('');
    data.push('MEIN VOLLSTÄNDIGES CHART:');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });
    if(ASP.length){
      data.push('');
      data.push('MEINE WICHTIGSTEN ASPEKTE:');
      ASP.forEach(function(a){ data.push(a.p1 + (a.s1 ? (' in ' + a.s1) : '') + ' ' + a.type + ' ' + a.p2 + (a.s2 ? (' in ' + a.s2) : '')); });
    }
    const full = WOMANCODE_PROMPT + '\n\n' + data.join('\n');
    const btn = document.getElementById('copyWomancodeBtn');
    const done = function(){ if(btn){ const o = btn.getAttribute('data-label') || btn.textContent; btn.setAttribute('data-label', o); btn.textContent = '✓ Kopiert! Jetzt in ChatGPT einfügen'; setTimeout(function(){ btn.textContent = o; }, 2800); } };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(full).then(done).catch(function(){ fallbackCopy(full, done); });
    } else { fallbackCopy(full, done); }
  };"""

pat = re.compile(r"  const BUSINESS_PROMPT = `.*?\n  window\.copyBusinessReading = function\(\)\{.*?\n  \};", re.DOTALL)
if not pat.search(s):
    sys.exit("FEHLT: BUSINESS_PROMPT / copyBusinessReading Region")
s = pat.sub(lambda _: new_region, s, count=1)

# Sicherheitscheck: keine Business-Reste mehr in Logik-Hooks
for leftover in ["copyBusinessReading", "copyBizBtn", "BUSINESS_PROMPT"]:
    if leftover in s:
        sys.exit("REST gefunden: " + leftover)

with open(DST, "w", encoding="utf-8") as f:
    f.write(s)

print("OK ->", DST)
print("Groesse:", len(s), "Zeichen")
