#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut den Geburtscode-Reader aus dem Business-Reader.
Muster: build_barbault_reader.py (ASTROCODE-Design, Tippfeld-Datum,
schlanke Ergebnis-Seite, kein E-Mail-Gate).

DAS BESONDERE (Patrycjas Idee 20.07.2026): Dieser Reader hat keinen
festen Prompt. Er liest die Chart zuerst selbst, wie eine Astrologin,
und KOMPONIERT daraus einen individuellen Prompt fuer ein komplettes
Geburtshoroskop-Reading:

  - Big Three (Sonne, Mond, Aszendent) als Eroeffnung
  - Chartruler (Herrscher des AC, Logik aus build_chartruler_reader.py)
    + Mitherrscher + eigenes Zeichen
  - Dominanzen: dominantes Element, fehlende Elemente, dominante
    Qualitaet (kardinal/fix/veraenderlich), Hemisphaeren-Betonung
    (ueber/unter dem Horizont, oestlich/westlich)
  - Stellium-Erkennung (3+ Planeten in einem Zeichen oder Haus)
  - staerkste Haeuser (Lebensschwerpunkte) mit den Planeten darin
  - engste Aspekte (bereits nach Orb sortiert, Aspekt fuer Aspekt,
    das Format, das Patrycja beim Business-Reader besser fand)
  - Mondknoten als Seelenweg

Schritte, die auf eine Chart nicht zutreffen (kein Stellium, keine
fehlenden Elemente, keine Hemisphaeren-Betonung), erscheinen im Prompt
gar nicht. Zwei Frauen bekommen zwei verschieden aufgebaute Prompts.

ERSTER Reader-Zweck: BEZAHLTES Produkt (Patrycja 20.07.: "Ich geb
nichts mehr einfach so kostenlos raus"), Verkauf nach dem
Barbault-Modell (Tentary, Netlify-URL nicht erratbar).

Name final (Patrycja 20.07.): "Dein Birthcode".

Quelle:  astro-business-reader.html
Ziel:    astro-birthcode-reader.html (+ astro-birthcode-reader-netlify/index.html + ZIP)
"""
import os, re, sys, shutil, io, base64
from PIL import Image, ImageFilter, ImageChops

NAME = "Dein Birthcode"            # <- Reader-Name (final, Patrycja 20.07.2026)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-birthcode-reader.html")
NETLIFY = os.path.join(HERE, "astro-birthcode-reader-netlify")
TPL = os.path.join(HERE, "..", "reference", "email-astrocode-design", "vorlage-astrocode-original.webp")

# --- ASTROCODE-Slices aus Patrycjas Original-Vorlage (1080x1920) -------------
def jpg64(img, q):
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=q)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

_tpl = Image.open(TPL).convert("RGB")
HERO = jpg64(_tpl.crop((0, 0, 1080, 560)).resize((1300, 674), Image.LANCZOS), 85)
FOOT = jpg64(_tpl.crop((0, 1560, 1080, 1920)).resize((1200, 400), Image.LANCZOS), 85)
_strip = _tpl.crop((0, 700, 1080, 1560)).resize((600, 478), Image.LANCZOS)
_diff = ImageChops.subtract(_strip, _strip.filter(ImageFilter.GaussianBlur(14)))
TILE = jpg64(ImageChops.add(Image.new("RGB", _diff.size, (128, 128, 128)), _diff), 80)

with open(SRC, "r", encoding="utf-8") as f:
    s = f.read()

def repl(old, new, label):
    global s
    if old not in s:
        sys.exit("FEHLT (" + label + "): " + old[:80])
    s = s.replace(old, new, 1)

# --- 1. Branding / sichtbare Texte ---------------------------------------
repl("<title>Dein Business-Code</title>",
     "<title>" + NAME + "</title>", "title")

repl('<p class="header-eyebrow">Dein kosmischer Business-Blueprint</p>',
     '', "eyebrow-remove")

repl("<h1>Dein Business-Code</h1>",
     "<h1>" + NAME + "</h1>", "h1")

repl('<p class="subtitle">Gib deine Geburtsdaten ein. Auf der nächsten Seite bekommst du dein Geburtshoroskop angezeigt und einen fertigen KI-Prompt, der dir sagt, wie du dein Business führst, dich positionierst, skalierst und Geld verdienst.</p>',
     '<p class="subtitle">Ein komplettes Geburtshoroskop-Reading, wie bei einer Astrologin. Gib deine Geburtsdaten ein. Die Seite berechnet dein Chart, erkennt, was dich prägt, und komponiert daraus deinen individuellen KI-Prompt.</p>',
     "subtitle")

repl('onclick="runCheck()">Meinen Business-Code aufdecken</button>',
     'onclick="runCheck()">Meinen individuellen Reading-Prompt kreieren</button>', "submit-btn")

repl('''<div class="tip-box">
    <p><strong>Gib deine Geburtsdaten ein.</strong></p>
  </div>''', '', "tip-box-remove")

# --- E-Mail komplett entfernen (kein Opt-in) -------------------------------
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

# --- 2. Geburtsdatum als Tippfeld TT.MM.JJJJ (Muster build_reise_reader.py) -
repl('<input type="date" id="birthDate" autocomplete="off" min="1900-01-01" max="2035-12-31">',
     '<input type="text" id="birthDate" placeholder="TT.MM.JJJJ, z.B. 08.10.1986" inputmode="numeric" autocomplete="off">',
     "date-field-text")

repl("    const date = $('birthDate').value;",
     '''    const dateRaw = ($('birthDate').value || '').trim();
    let date = '';
    (function(){
      let v = dateRaw;
      if(/^\\d{8}$/.test(v)) v = v.slice(0,2) + '.' + v.slice(2,4) + '.' + v.slice(4);
      const dm = v.match(/^(\\d{1,2})\\.(\\d{1,2})\\.(\\d{4})$/);
      if(!dm) return;
      const d = parseInt(dm[1], 10), mo = parseInt(dm[2], 10), y = parseInt(dm[3], 10);
      if(d < 1 || d > 31 || mo < 1 || mo > 12 || y < 1900 || y > 2035) return;
      date = y + '-' + (mo < 10 ? '0' : '') + mo + '-' + (d < 10 ? '0' : '') + d;
    })();''',
     "date-parse")

repl("if(!date){ return fail('Bitte gib dein Geburtsdatum ein.'); }",
     "if(!date){ return fail('Bitte gib dein Geburtsdatum als TT.MM.JJJJ ein, zum Beispiel 08.10.1986.'); }",
     "date-error-msg")

date_autodots = '''<script>
document.addEventListener('DOMContentLoaded', function(){
  const bd = document.getElementById('birthDate');
  if(bd){
    bd.addEventListener('input', function(){
      let v = bd.value.replace(/[^\\d.]/g, '');
      if(v.indexOf('.') === -1 && v.length > 4){
        v = v.slice(0,2) + '.' + v.slice(2,4) + '.' + v.slice(4,8);
      }
      bd.value = v.slice(0, 10);
    });
  }
});
</script>
</body>'''
repl('</body>', date_autodots, "date-autodots")

# --- 3. Ergebnis-Kopf + Zurueck-Button ------------------------------------
repl("<h2>Dein Business-Code${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Dein Chart als Business-Blueprint'}</p>",
     "<h2>" + NAME + "${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Dein komplettes Geburtshoroskop'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Neue Chart erstellen", "back-btn")

# --- 4. Analyse-Schicht in runCheck einhaengen ------------------------------
# Anker NACH window.__chart, damit __fullChart und __aspects bereits gesetzt sind.
calc_anchor = "      window.__chart = chart;\n      generateReading();"
natal_calc = r"""      window.__chart = chart;

      // Geburtscode: die Chart selbst lesen, wie eine Astrologin, bevor
      // der Prompt entsteht. Alles Weitere baut auf dieser Analyse auf.
      (function(){
        try{
          const FULL = window.__fullChart || [];
          const ASP = window.__aspects || [];
          const find = function(label){
            for(let i = 0; i < FULL.length; i++){ if(FULL[i].label === label) return FULL[i]; }
            return null;
          };

          // Big Three
          const sun = find('Sonne') || {}, moon = find('Mond') || {}, asc = find('Aszendent') || {};

          // Chartruler: Herrscher des Aszendenten (Logik aus dem Chartruler-Reader)
          const RULER = { 'Widder':'Mars','Stier':'Venus','Zwillinge':'Merkur','Krebs':'Mond','Löwe':'Sonne','Jungfrau':'Merkur','Waage':'Venus','Skorpion':'Pluto','Schütze':'Jupiter','Steinbock':'Saturn','Wassermann':'Uranus','Fische':'Neptun' };
          const CORULER = { 'Skorpion':'Mars','Wassermann':'Saturn','Fische':'Jupiter' };
          const HOME = { 'Sonne':['Löwe'],'Mond':['Krebs'],'Merkur':['Zwillinge','Jungfrau'],'Venus':['Stier','Waage'],'Mars':['Widder','Skorpion'],'Jupiter':['Schütze','Fische'],'Saturn':['Steinbock','Wassermann'],'Uranus':['Wassermann'],'Neptun':['Fische'],'Pluto':['Skorpion'] };
          const acSign = asc.sign || '';
          const rulerName = RULER[acSign] || '';
          const rulerEntry = rulerName ? (find(rulerName) || {}) : {};
          const coName = CORULER[acSign] || '';
          const coEntry = coName ? (find(coName) || {}) : {};
          const inOwnSign = rulerName ? ((HOME[rulerName] || []).indexOf(rulerEntry.sign || '') !== -1) : false;

          // Dominanzen ueber die 10 Planeten
          const PLANETS = ['Sonne','Mond','Merkur','Venus','Mars','Jupiter','Saturn','Uranus','Neptun','Pluto'];
          const ELEM = { 'Widder':'Feuer','Löwe':'Feuer','Schütze':'Feuer','Stier':'Erde','Jungfrau':'Erde','Steinbock':'Erde','Zwillinge':'Luft','Waage':'Luft','Wassermann':'Luft','Krebs':'Wasser','Skorpion':'Wasser','Fische':'Wasser' };
          const MODAL = { 'Widder':'kardinal','Krebs':'kardinal','Waage':'kardinal','Steinbock':'kardinal','Stier':'fix','Löwe':'fix','Skorpion':'fix','Wassermann':'fix','Zwillinge':'veränderlich','Jungfrau':'veränderlich','Schütze':'veränderlich','Fische':'veränderlich' };
          const eCount = { 'Feuer':0, 'Erde':0, 'Luft':0, 'Wasser':0 };
          const mCount = { 'kardinal':0, 'fix':0, 'veränderlich':0 };
          const houseWho = {}, signWho = {};
          let above = 0, below = 0, east = 0, west = 0, houseKnown = 0;
          PLANETS.forEach(function(p){
            const e = find(p);
            if(!e) return;
            if(eCount[ELEM[e.sign]] != null) eCount[ELEM[e.sign]]++;
            if(mCount[MODAL[e.sign]] != null) mCount[MODAL[e.sign]]++;
            if(e.sign){ (signWho[e.sign] = signWho[e.sign] || []).push(p); }
            const h = parseInt(e.house, 10);
            if(h >= 1 && h <= 12){
              houseKnown++;
              (houseWho[h] = houseWho[h] || []).push(p);
              if(h >= 7){ above++; } else { below++; }
              if(h >= 10 || h <= 3){ east++; } else { west++; }
            }
          });
          const eSorted = Object.keys(eCount).sort(function(a, b){ return eCount[b] - eCount[a]; });
          const missing = Object.keys(eCount).filter(function(k){ return eCount[k] === 0; });
          const mSorted = Object.keys(mCount).sort(function(a, b){ return mCount[b] - mCount[a]; });

          // Hemisphaeren-Betonung nur, wenn sie deutlich ist (7+ von 10)
          let hemiV = '', hemiH = '';
          if(houseKnown >= 8){
            if(above >= 7) hemiV = 'oben';
            else if(below >= 7) hemiV = 'unten';
            if(east >= 7) hemiH = 'ost';
            else if(west >= 7) hemiH = 'west';
          }

          // Staerkste Haeuser (Lebensschwerpunkte): mind. 2 Planeten, max. 3 Haeuser
          const focus = Object.keys(houseWho).map(Number)
            .sort(function(a, b){ return houseWho[b].length - houseWho[a].length || a - b; })
            .filter(function(h){ return houseWho[h].length >= 2; })
            .slice(0, 3)
            .map(function(h){ return { house: h, who: houseWho[h] }; });

          // Stellium: 3+ Planeten in einem Zeichen oder Haus
          const stelliumSigns = Object.keys(signWho)
            .filter(function(sg){ return signWho[sg].length >= 3; })
            .map(function(sg){ return { sign: sg, who: signWho[sg] }; });
          const stelliumHouses = Object.keys(houseWho).map(Number)
            .filter(function(h){ return houseWho[h].length >= 3; })
            .map(function(h){ return { house: h, who: houseWho[h] }; });

          const nn = find('Nordknoten') || {}, sn = find('Südknoten') || {};

          window.__natal = {
            sun: sun, moon: moon, acSign: acSign,
            ruler: {
              name: rulerName, sign: rulerEntry.sign || '', house: rulerEntry.house || '',
              inOwnSign: inOwnSign,
              co: { name: coName, sign: coEntry.sign || '', house: coEntry.house || '' }
            },
            eCount: eCount, domElement: eSorted[0], domElementN: eCount[eSorted[0]],
            missing: missing,
            mCount: mCount, domModal: mSorted[0], domModalN: mCount[mSorted[0]],
            hemi: { above: above, below: below, east: east, west: west, known: houseKnown, v: hemiV, h: hemiH },
            focus: focus,
            stelliumSigns: stelliumSigns,
            stelliumHouses: stelliumHouses,
            nn: nn, sn: sn
          };
        }catch(e){ window.__natal = null; }
      })();

      generateReading();"""
repl(calc_anchor, natal_calc, "natal-calc-injection")

# --- 4b. Ergebnis-Seite verschlanken (REGEL seit 14.07.): Platzierungen, ----
# Aspekte und Element-Block raus. Nur Analyse-Block + Prompt bleiben sichtbar.
repl('''  const FULL = window.__fullChart || [];
  if (FULL.length) {
    const rows = FULL.map(e => `<div class="data-row"><span class="data-planet">${e.label}</span><span class="data-values"><span class="badge sign-badge">${e.sign}</span>${e.house ? `<span class="badge house-badge">${e.house}. Haus</span>` : ''}</span></div>`).join('');
    html += `
    <div class="data-block">
      <h3>Deine Platzierungen</h3>
      <div class="data-grid">${rows}</div>
      <button class="copy-btn" id="copyBtn" onclick="copyChartData()">Alle Daten kopieren</button>
    </div>`;
  }

''', '', "platzierungen-block-remove")

repl('''  const ASP = window.__aspects || [];
  if (ASP.length) {
    const arows = ASP.map(a => `<div class="data-row"><span class="data-planet">${a.p1}${a.s1 ? ` <span class="asp-sign">${a.s1}</span>` : ''} <span class="asp-sym">·</span> ${a.p2}${a.s2 ? ` <span class="asp-sign">${a.s2}</span>` : ''}</span><span class="data-values"><span class="badge sign-badge">${a.type}</span></span></div>`).join('');
    html += `
    <div class="data-block">
      <h3>Deine wichtigsten Aspekte</h3>
      <div class="data-grid aspect-grid">${arows}</div>
      <button class="copy-btn" id="copyAspBtn" onclick="copyAspects()">Aspekte kopieren</button>
    </div>`;
  }

''', '', "aspekte-block-remove")

repl('''  const maxEl = Object.entries(elementCounts).sort((a,b)=>b[1]-a[1]).filter(e=>e[1]>0);
  if (maxEl.length > 0) {
    const dominantEl = maxEl[0][0];
    html += `
    <div class="summary-block">
      <h3>Dein dominantes Element: ${dominantEl}</h3>
      <p>${elementDescriptions[dominantEl]}</p>
    </div>`;
  }

''', '', "element-block-remove")

# --- 5. Reading-Block: sichtbare Analyse + Prompt-CTA -----------------------
old_cta = """  html += `
  <div class="cta-block">
    <h3>Dein Business-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, wie du dein Business führst, wie du dich positionierst, wo deine Zone of Genius liegt und wie du am natürlichsten Geld verdienst.</p>
    <button class="copy-btn" id="copyBizBtn" onclick="copyBusinessReading()">Business-Prompt + Daten kopieren</button>
  </div>`;"""

new_cta = """  // Sichtbar: was die Chart praegt (die Analyse, aus der der Prompt komponiert wird)
  const N = window.__natal || null;
  if(N){
    const dj = function(arr){
      if(!arr || !arr.length) return '';
      if(arr.length === 1) return arr[0];
      return arr.slice(0, -1).join(', ') + ' und ' + arr[arr.length - 1];
    };
    let nHtml = `
    <div class="data-block">
      <h3>Was deine Chart prägt</h3>
      <div class="data-grid">`;
    if(N.sun.sign) nHtml += `<div class="data-row"><span class="data-planet">Deine Sonne</span><span class="data-values"><span class="badge sign-badge">${N.sun.sign}</span>${N.sun.house ? `<span class="badge house-badge">${N.sun.house}. Haus</span>` : ''}</span></div>`;
    if(N.moon.sign) nHtml += `<div class="data-row"><span class="data-planet">Dein Mond</span><span class="data-values"><span class="badge sign-badge">${N.moon.sign}</span>${N.moon.house ? `<span class="badge house-badge">${N.moon.house}. Haus</span>` : ''}</span></div>`;
    if(N.acSign) nHtml += `<div class="data-row"><span class="data-planet">Dein Aszendent</span><span class="data-values"><span class="badge sign-badge">${N.acSign}</span></span></div>`;
    if(N.ruler.name) nHtml += `<div class="data-row"><span class="data-planet">Dein Chartruler: ${N.ruler.name}</span><span class="data-values"><span class="badge sign-badge">${N.ruler.sign}</span>${N.ruler.house ? `<span class="badge house-badge">${N.ruler.house}. Haus</span>` : ''}</span></div>`;
    if(N.domElement) nHtml += `<div class="data-row"><span class="data-planet">Dein dominantes Element</span><span class="data-values"><span class="badge sign-badge">${N.domElement} (${N.domElementN} von 10)</span></span></div>`;
    if(N.missing.length) nHtml += `<div class="data-row"><span class="data-planet">Bei dir unbesetzt</span><span class="data-values"><span class="badge sign-badge">${dj(N.missing)}</span></span></div>`;
    N.stelliumSigns.forEach(function(st){
      nHtml += `<div class="data-row"><span class="data-planet">Dein Stellium im Zeichen ${st.sign}</span><span class="data-values"><span class="badge sign-badge">${st.who.join(', ')}</span></span></div>`;
    });
    N.focus.forEach(function(fh){
      nHtml += `<div class="data-row"><span class="data-planet">Stark besetzt: dein ${fh.house}. Haus</span><span class="data-values"><span class="badge house-badge">${fh.who.join(', ')}</span></span></div>`;
    });
    nHtml += `</div></div>`;
    html += nHtml;
  }

  html += `
  <div class="cta-block">
    <h3>Dein Geburtshoroskop-Reading mit KI</h3>
    <p>Dein Prompt wurde aus deiner Chart komponiert: dein Chartruler, deine Dominanzen, deine stärksten Lebensbereiche und deine engsten Aspekte geben ihm die Dramaturgie vor. Kopiere ihn und füge ihn bei ChatGPT oder Claude ein. Du bekommst ein komplettes Reading, wie bei einer Astrologin, die deine Chart vor sich liegen hat.</p>
    <button class="copy-btn" id="copyReadingBtn" onclick="copyBirthReading()">Reading-Prompt + Daten kopieren</button>
  </div>`;"""
repl(old_cta, new_cta, "cta-block")

# --- 6. Abschluss-CTA: AstroCode-Portal (Patrycjas Text vom 15.07., 1:1,
# nur der Reader-Name im Kicker angepasst) ----------------------------------
repl('''  html += `
  <div class="cta-block">
    <p class="cta-kicker">Möchtest du noch tiefer in deine Chart eintauchen?</p>
    <h3>Lerne dich tiefer kennen, als Jahre der Selbstreflexion es je konnten.</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Hier erfährst du mehr: Dein AstroCode &rarr;</a>
  </div>`;''',
'''  html += `
  <div class="cta-block astro-cta">
    <p class="cta-kicker">Dir gefallen die Antworten aus meinem Birthcode Reader?</p>
    <h3>Weißt du, dass du dank meines Astrocode-Portals dein ganzes Geburtshoroskop analysieren kannst! Tiefer als jedes Astroreading, denn erst die Bewegung bewirkt Veränderung! Wie oft hast du schon was über dich gehört, aber nicht umgesetzt!</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Öffne dein Astrocode-Portal und begib dich auf eine unvergessliche Reise zurück zu dir!</a>
  </div>`;''',
"astrocode-cta")

# --- 7. Prompt-Gehirn + Copy-Funktion austauschen --------------------------
# Der Prompt wird NICHT als fester Text abgelegt, sondern beim Kopieren aus
# der Analyse komponiert: Schritte, die auf die Chart nicht zutreffen,
# tauchen gar nicht auf. Zwei Frauen bekommen zwei verschiedene Prompts.
new_region = r"""  const READING_INTRO = `Du bist eine erfahrene Astrologin, die seit Jahrzehnten Geburtshoroskope liest. Ich sitze dir gegenüber wie in einer persönlichen Sitzung, und du liest heute meine Chart. Du schreibst klar, tief und direkt, so dass mich jeder Satz trifft. Keine Floskeln, keine allgemeinen Astro-Sätze, kein Lehrbuchton. Du liest meine Chart in Schichten und beginnst mit dem, was am stärksten wirkt.

Wichtig: Ich arbeite mit Placidus-Häusern. Alle Häuser in meinen Daten unten sind Placidus-Häuser.

Unten findest du zwei Dinge: die vorbereitete Analyse meiner Chart und mein vollständiges Chart mit meinen engsten Aspekten. Die Analyse gibt deinem Reading die Dramaturgie vor. Mein Reading hat diese Kapitel:`;

  const READING_OUTRO = `Schreib auf Deutsch, in der Du-Form, in Tiefe statt in Breite. Jeder Satz konkret. Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker. Nimm dir Raum für jedes Kapitel.

Hier sind meine Daten:`;

  window.copyBirthReading = function(){
    const FULL = window.__fullChart || [];
    const ASP = window.__aspects || [];
    const N = window.__natal || {};
    const m = window.__meta || {};
    const dj = function(arr){
      if(!arr || !arr.length) return '';
      if(arr.length === 1) return arr[0];
      return arr.slice(0, -1).join(', ') + ' und ' + arr[arr.length - 1];
    };
    const ph = function(e){ return (e && e.sign) ? (e.sign + ((e.house) ? (' in meinem ' + e.house + '. Haus') : '')) : ''; };

    // --- Kapitel komponieren: nur was diese Chart wirklich hat --------------
    const steps = [];

    if(N.sun && N.sun.sign && N.moon && N.moon.sign && N.acSign){
      steps.push('Der erste Blick. Beginne wie in einer Sitzung: Meine Sonne steht in ' + ph(N.sun) + ', mein Mond in ' + ph(N.moon) + ', mein Aszendent ist ' + N.acSign + '. Lies die drei zusammen als ein Bild: wie ich auf Menschen wirke (Aszendent), was mich von innen antreibt (Sonne) und was ich brauche, um mich sicher und genährt zu fühlen (Mond). Wo die drei sich widersprechen, liegt eine Spannung, die ich jeden Tag spüre. Benenne sie klar.');
    }

    if(N.ruler && N.ruler.name){
      let r = 'Mein Chartruler. ' + N.ruler.name + ' regiert meinen Aszendenten und führt damit meine gesamte Chart. ' + N.ruler.name + ' steht in ' + ph(N.ruler) + '.';
      if(N.ruler.inOwnSign) r += ' ' + N.ruler.name + ' steht im eigenen Zeichen und wirkt in voller Kraft.';
      r += ' Lies daraus, in welchem Lebensbereich sich mein Leben entscheidet und welche Energie dabei den Ton angibt.';
      if(N.ruler.co && N.ruler.co.name && N.ruler.co.sign){
        r += ' Der klassische Mitherrscher meines Aszendenten ist ' + N.ruler.co.name + ' in ' + ph(N.ruler.co) + '. Lies ihn als zweite Stimme dazu.';
      }
      steps.push(r);
    }

    (function(){
      const facts = [];
      if(N.domElement) facts.push('In meiner Chart stehen ' + N.domElementN + ' von 10 Planeten in ' + N.domElement + '-Zeichen.');
      if(N.missing && N.missing.length){
        facts.push('Kein Planet steht in einem ' + dj(N.missing) + '-Zeichen. Sag mir, was das fehlende Element für mich bedeutet, woran ich im Alltag merke, dass es fehlt, und wie ich es bewusst nähre.');
      }
      if(N.domModal) facts.push('Die dominante Qualität ist ' + N.domModal + ' (' + N.domModalN + ' von 10 Planeten).');
      if(N.hemi && N.hemi.v === 'oben') facts.push(N.hemi.above + ' meiner 10 Planeten stehen über dem Horizont, in den Häusern 7 bis 12. Mein Leben spielt sich stark im Außen ab: in Begegnung, Öffentlichkeit und Wirkung.');
      if(N.hemi && N.hemi.v === 'unten') facts.push(N.hemi.below + ' meiner 10 Planeten stehen unter dem Horizont, in den Häusern 1 bis 6. Meine wichtigsten Prozesse laufen innen und im Nahbereich, bevor sie sichtbar werden.');
      if(N.hemi && N.hemi.h === 'ost') facts.push(N.hemi.east + ' meiner 10 Planeten stehen in der östlichen Hälfte meiner Chart (Häuser 10 bis 3). Ich setze mein Leben selbst in Gang.');
      if(N.hemi && N.hemi.h === 'west') facts.push(N.hemi.west + ' meiner 10 Planeten stehen in der westlichen Hälfte meiner Chart (Häuser 4 bis 9). Mein Leben entwickelt sich in der Begegnung mit anderen.');
      if(N.stelliumSigns && N.stelliumSigns.length){
        const sparts = N.stelliumSigns.map(function(st){ return 'im Zeichen ' + st.sign + ' ' + dj(st.who); });
        facts.push('Bei mir stehen ' + dj(sparts) + '. ' + (N.stelliumSigns.length > 1 ? 'Diese Zeichen prägen mich' : 'Dieses Zeichen prägt mich') + ' weit über die Sonne hinaus.');
      }
      if(facts.length){
        steps.push('Was meine Chart prägt. ' + facts.join(' ') + ' Lies diese Gewichtung, bevor du weitergehst: Was fällt dir an meiner Chart als Erstes auf, und was ist mein Grundton?');
      }
    })();

    if(N.focus && N.focus.length){
      const fparts = N.focus.map(function(fh){ return 'mein ' + fh.house + '. Haus mit ' + dj(fh.who); });
      let f = 'Meine Lebensschwerpunkte. Die am stärksten besetzten Häuser meiner Chart sind ' + dj(fparts) + '.';
      (N.stelliumHouses || []).forEach(function(sh){
        f += ' Mein ' + sh.house + '. Haus ist mit ' + sh.who.length + ' Planeten ein Stellium: ein Lebensschwerpunkt, um den ich nicht herumkomme.';
      });
      f += ' Geh diese Bereiche einzeln durch: Wofür steht das Haus, was bedeutet jeder Planet darin, und wie zeigt sich das konkret in meinem Alltag?';
      steps.push(f);
    } else if(N.sun){
      steps.push('Meine Lebensbühnen. Meine Planeten verteilen sich breit über die Häuser, kein Haus sammelt sie. Sag mir, was diese Streuung bedeutet: viele Bühnen statt einem einzelnen Schwerpunkt. Und sag mir, woran ich erkenne, welche Bühne in einer Lebensphase gerade dran ist.');
    }

    if(ASP.length){
      const a0 = ASP[0];
      steps.push('Meine engsten Aspekte. Unten stehen meine Aspekte, sortiert nach Orb, der engste zuerst. Der engste ist ' + a0.p1 + ' ' + a0.type + ' ' + a0.p2 + ': er wirkt am stärksten, beginne mit ihm. Geh dann alle einzeln durch, Aspekt für Aspekt. Für jeden: worum es geht, wie er sich konkret in meinem Alltag zeigt, was sein Schatten ist, was sein Geschenk, und eine kurze Selbstfrage dazu.');
    }

    if(N.nn && N.nn.sign && N.sn && N.sn.sign){
      steps.push('Mein Seelenweg. Mein Südknoten steht in ' + ph(N.sn) + ', mein Nordknoten in ' + ph(N.nn) + '. Lies daraus, was ich mitbringe und im Schlaf kann, wohin ich mich zurückziehe, wenn es eng wird, und in welche Richtung mein Leben wachsen will. Mach die Wachstumsrichtung konkret: Woran erkenne ich in einer normalen Woche, dass ich dem Nordknoten folge?');
    }

    steps.push('Schatten und Geschenk. Fasse zusammen: die zwei größten Spannungen meiner Chart und die zwei größten Geschenke. Sag mir bei beiden, woran ich im Alltag erkenne, ob ich gerade im Schatten oder im Geschenk unterwegs bin.');

    steps.push('Der rote Faden. Lies aus allem die eine Geschichte, die meine Chart erzählt: wer ich bin, wenn ich ganz bei mir bin, und was mein Leben von mir will. Formuliere daraus einen Satz in der Ich-Form, den ich mir aufschreiben kann, und einen konkreten Schritt für die kommenden sieben Tage, der zu meiner Chart passt.');

    steps.push('Meine Frage. Stelle mir am Ende eine einzige, konfrontierende Frage zu dem Muster, das ich in meinem Leben am längsten übersehe. Danach biete mir drei Richtungen an, in die wir mein Reading vertiefen können, passend zu meiner Chart, und frag mich, welche ich wählen will.');

    const numbered = steps.map(function(t, i){ return (i + 1) + '. ' + t; }).join('\n\n');

    // --- Datenteil ----------------------------------------------------------
    const data = [];
    if(m.name) data.push('Name: ' + m.name);
    if(m.date){ const dp = m.date.split('-'); data.push('Geburtsdatum: ' + dp[2]+'.'+dp[1]+'.'+dp[0] + (m.time ? (' um ' + m.time + ' Uhr') : '')); }
    if(m.place) data.push('Geburtsort: ' + m.place);
    data.push('');
    data.push('DIE VORBEREITETE ANALYSE MEINER CHART:');
    if(N.ruler && N.ruler.name){
      data.push('Chartruler (Herrscher meines ' + N.acSign + '-Aszendenten): ' + N.ruler.name + ' in ' + N.ruler.sign + (N.ruler.house ? (', ' + N.ruler.house + '. Haus') : '') + (N.ruler.inOwnSign ? ' (im eigenen Zeichen)' : ''));
      if(N.ruler.co && N.ruler.co.name && N.ruler.co.sign) data.push('Klassischer Mitherrscher: ' + N.ruler.co.name + ' in ' + N.ruler.co.sign + (N.ruler.co.house ? (', ' + N.ruler.co.house + '. Haus') : ''));
    }
    if(N.eCount) data.push('Elemente (10 Planeten): Feuer ' + N.eCount['Feuer'] + ', Erde ' + N.eCount['Erde'] + ', Luft ' + N.eCount['Luft'] + ', Wasser ' + N.eCount['Wasser'] + (N.missing && N.missing.length ? (' (unbesetzt: ' + dj(N.missing) + ')') : ''));
    if(N.mCount) data.push('Qualitäten (10 Planeten): kardinal ' + N.mCount['kardinal'] + ', fix ' + N.mCount['fix'] + ', veränderlich ' + N.mCount['veränderlich']);
    if(N.hemi){
      const pl = function(n){ return n + ' ' + (n === 1 ? 'Planet' : 'Planeten'); };
      data.push('Hemisphären: ' + pl(N.hemi.above) + ' über dem Horizont (Häuser 7 bis 12), ' + N.hemi.below + ' darunter; ' + N.hemi.east + ' in der östlichen Hälfte (Häuser 10 bis 3), ' + N.hemi.west + ' in der westlichen.');
    }
    (N.stelliumSigns || []).forEach(function(st){ data.push('Stellium im Zeichen ' + st.sign + ': ' + st.who.join(', ')); });
    (N.stelliumHouses || []).forEach(function(sh){ data.push('Stellium im ' + sh.house + '. Haus: ' + sh.who.join(', ')); });
    (N.focus || []).forEach(function(fh){ data.push('Stark besetzt: ' + fh.house + '. Haus (' + fh.who.join(', ') + ')'); });
    data.push('');
    data.push('MEIN VOLLSTÄNDIGES CHART (Placidus-Häuser):');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });
    if(ASP.length){
      data.push('');
      data.push('MEINE ENGSTEN ASPEKTE (nach Orb sortiert, der engste wirkt am stärksten):');
      ASP.forEach(function(a){ data.push('- ' + a.p1 + (a.s1 ? (' in ' + a.s1) : '') + ' ' + a.type + ' ' + a.p2 + (a.s2 ? (' in ' + a.s2) : '') + ' (Orb ' + String(Math.round(a.orb * 10) / 10).replace('.', ',') + '°)'); });
    }

    const full = READING_INTRO + '\n\n' + numbered + '\n\n' + READING_OUTRO + '\n\n' + data.join('\n');
    const btn = document.getElementById('copyReadingBtn');
    const done = function(){ if(btn){ const o = btn.getAttribute('data-label') || btn.textContent; btn.setAttribute('data-label', o); btn.textContent = '✓ Kopiert! Jetzt in ChatGPT einfügen'; setTimeout(function(){ btn.textContent = o; }, 2800); } };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(full).then(done).catch(function(){ fallbackCopy(full, done); });
    } else { fallbackCopy(full, done); }
  };"""

pat = re.compile(r"  const BUSINESS_PROMPT = `.*?\n  window\.copyBusinessReading = function\(\)\{.*?\n  \};", re.DOTALL)
if not pat.search(s):
    sys.exit("FEHLT: BUSINESS_PROMPT / copyBusinessReading Region")
s = pat.sub(lambda _: new_region, s, count=1)

# --- 8. ASTROCODE-Design als Override-Layer (1:1 aus build_barbault_reader.py)
extra_css = '''<style>
html{ background:#8d7fc7 linear-gradient(180deg,#8B8ED9 0%,#A06AB5 18%,#8979C1 37%,#9267A8 58%,#B6697D 79%,#DB705C 100%) !important;
  background-size:100% 100% !important; }
body{ background:transparent !important; color:#111111 !important; }
#binary-canvas{ display:none !important; }
body::after{ content:"" !important; position:fixed; inset:0; z-index:0; pointer-events:none;
  background:url("__TILE__") !important; background-size:620px auto !important; background-repeat:repeat !important;
  mix-blend-mode:overlay; opacity:0.5; }
.moon-scene{ position:relative !important; top:auto !important;
  background:url("__HERO__") center top / cover no-repeat !important;
  height:clamp(220px, 42vw, 540px) !important; opacity:1 !important;
  margin-bottom:clamp(-100px, -6vw, -30px) !important; }
.header-eyebrow{
  font-family:'Inter','Helvetica Neue',sans-serif !important;
  font-size:0.92rem !important;
  font-weight:700 !important;
  letter-spacing:0.3em !important;
  color:#FFFFFF !important;
  text-shadow:1px 2px 8px rgba(40,20,80,0.65) !important;
}
header h1{
  font-size:clamp(1.9rem, 7vw, 3rem) !important;
  line-height:1.15 !important;
  color:#FFFFFF !important;
  text-shadow:2px 4px 14px rgba(40,20,80,0.55), 0 0 40px rgba(255,255,255,0.25) !important;
}
.subtitle{
  font-family:'Inter','Helvetica Neue',sans-serif !important;
  font-style:normal !important;
  font-size:1.28rem !important;
  font-weight:700 !important;
  line-height:1.75 !important;
  letter-spacing:0.01em !important;
  color:#151033 !important;
  max-width:600px !important; margin:0 auto !important;
}
header{ margin-bottom:16px !important; }
.place-chosen{ color:#312782 !important; font-weight:700 !important; }
.results-header h2{ color:#FFFFFF !important; text-shadow:2px 4px 14px rgba(40,20,80,0.55) !important; }
.results-header p{ color:#1c1440 !important; }
h3, .data-planet, .field-label, label, p, li{ color:#111111; }
.reading-block h3, .summary-block h3, .data-block h3, .cta-block h3, .form-section h3{ color:#1c1440 !important; }
.tip-box, .form-section, .reading-block, .summary-block, .data-block, .cta-block{
  background:rgba(255,255,255,0.30) !important;
  border:1px solid rgba(255,255,255,0.35) !important;
  border-radius:26px !important;
  box-shadow:0 12px 44px rgba(49,39,130,0.20) !important;
  color:#111111 !important; }
.tip-box{ border-left:3px solid #312782 !important; }
.tip-box, .tip-box p, .tip-box strong{ color:#1c1440 !important; }
.field-label{ color:#312782 !important; }
.error-msg{ color:#7A1230 !important; }
.data-block, .reading-block, .summary-block, .cta-block{ margin:36px 0 !important; }
.cta-kicker{
  font-size:clamp(1.15rem, 2.4vw, 1.45rem) !important;
  font-weight:800 !important;
  font-style:normal !important;
  color:#312782 !important;
  letter-spacing:0.01em !important;
  margin-bottom:16px !important;
}
.cta-block h3{ font-size:clamp(1.15rem, 2.2vw, 1.4rem) !important; line-height:1.5 !important; }
.cta-block p{ color:#111111 !important; }
.astro-cta h3{
  font-family:'Inter','Helvetica Neue',sans-serif !important;
  text-transform:none !important;
  letter-spacing:0.01em !important;
  color:#111111 !important;
  font-weight:700 !important;
  line-height:1.55 !important;
}
.astro-cta .cta-link{ white-space:normal !important; line-height:1.45 !important; padding-top:16px !important; padding-bottom:16px !important; }
input[type="text"], input[type="date"], input[type="time"]{
  background:rgba(255,255,255,0.55) !important; border:1px solid rgba(49,39,130,0.28) !important;
  color:#111111 !important; }
input::placeholder{ color:rgba(17,17,17,0.45) !important; }
input[type="text"]:focus, input[type="date"]:focus, input[type="time"]:focus{
  border-color:#312782 !important; box-shadow:0 0 24px rgba(49,39,130,0.25) !important; }
.place-results{ background:#FFFFFF !important; border:1px solid rgba(49,39,130,0.25) !important; }
.place-item{ color:#111111 !important; }
.place-item:hover, .place-item.active{ background:rgba(49,39,130,0.10) !important; }
select option{ background:#FFFFFF !important; color:#111111 !important; }
.sign-badge{ background:rgba(49,39,130,0.12) !important; border:1px solid rgba(49,39,130,0.28) !important; color:#1c1440 !important; }
.house-badge{ background:rgba(49,39,130,0.12) !important; border:1px solid rgba(49,39,130,0.28) !important; color:#1c1440 !important; }
.submit-btn, .cta-link, .copy-btn{
  background:#312782 !important;
  color:#FFFFFF !important;
  border-radius:40px !important;
  border:none !important;
  text-transform:none !important;
  letter-spacing:0.04em !important;
  box-shadow:0 10px 32px rgba(49,39,130,0.40) !important; }
.submit-btn:hover, .cta-link:hover, .copy-btn:hover{ background:#3d31a0 !important; box-shadow:0 14px 44px rgba(49,39,130,0.55) !important; }
.back-btn{ color:#312782 !important; }
.legal-footer, .legal-footer a{ color:#1c1440 !important; }
.legal-logo{ display:none !important; }
.astrocode-footer{ display:block; position:relative; z-index:2; width:100%; margin:56px 0 0; }
.astrocode-footer img{ width:100%; height:auto; display:block;
  -webkit-mask-image:linear-gradient(to bottom, transparent 0, #000 22%);
  mask-image:linear-gradient(to bottom, transparent 0, #000 22%); }
</style>
</head>'''.replace("__HERO__", HERO).replace("__TILE__", TILE)
repl('</head>', extra_css, "astrocode-css")

# --- 8b. ASTROCODE-Abschluss (NP-Logo + Schriftzug) vor dem Footer ----------
repl('<footer class="legal-footer">',
     '<a class="astrocode-footer" href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" rel="noopener"><img src="' + FOOT + '" alt="AstroCode von Patrycja Nasri"></a>\n<footer class="legal-footer">',
     "astrocode-footer-img")

# Sicherheitscheck: keine Business- oder Womancode-Reste mehr in Logik-Hooks
for leftover in ["copyBusinessReading", "copyBizBtn", "BUSINESS_PROMPT", "subscribeLead", "userEmail", "Business-Code", "Business-Blueprint", "wc-logo", "Womancode", "womancode"]:
    if leftover in s:
        sys.exit("REST gefunden: " + leftover)

with open(DST, "w", encoding="utf-8") as f:
    f.write(s)

os.makedirs(NETLIFY, exist_ok=True)
shutil.copyfile(DST, os.path.join(NETLIFY, "index.html"))
shutil.make_archive(NETLIFY, "zip", NETLIFY)

print("OK ->", DST)
print("OK ->", os.path.join(NETLIFY, "index.html"))
print("OK ->", NETLIFY + ".zip")
print("Groesse:", len(s), "Zeichen")
