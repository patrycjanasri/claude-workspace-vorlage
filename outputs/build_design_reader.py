#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut den Designcode-Reader aus dem Business-Reader.
Muster: build_birthcode_reader.py (komponierter Prompt, Tippfeld-Datum,
schlanke Ergebnis-Seite, kein E-Mail-Gate, Engine eingebettet, wahrer
Mondknoten) + build_venus_chiron_reader.py (Womancode Wein/Gold-Design).

DIE IDEE (Patrycja 26.07.2026): Ein Reader, der aus der Chart die
DESIGN-SIGNATUR liest: welche Farben, Formen, Schriften, Bildsprache
und Markenstimme zur eigenen Energie passen. Ihr Spezial fuer die
Branding-Session im Womancode-Raum am 29.07.2026 (Vollmond Wassermann
im 1. Haus). Name final: "Dein Designcode". Astrologie pur (Human
Design bewusst zurueckgestellt, Zeit bis 29.07.).

Analyse-Schichten (window.__design):
  - Aszendent + Horoskopherrscher (inkl. Mitherrscher, eigenes Zeichen)
  - HAEUSERHERRSCHER der Marken-Haeuser 1, 5, 10 (Patrycjas Ansage
    26.07.: "wichtig auch die Haeuserherrscher beruecksichtigen mit den
    wichtigen Aspekten"): Zeichen auf der Placidus-Spitze -> Herrscher
    (modern) + Mitherrscher -> dessen Position, plus Planeten im Haus.
    Muster: Eclipse Navigator v2 (Bernadettes Arbeitsweise).
  - Venus (Aesthetik), Merkur (Markensprache, Lilith-Kontakt-Flag),
    Sonne + Mond (Kern + emotionale Temperatur), MC (oeffentliche Marke)
  - Element- und Qualitaeten-Dominanz (Farbwelt), fehlende Elemente
  - Wichtige Aspekte: je Herrscher/Venus/Merkur aus der Aspektliste

Prompt KOMPONIERT nach Birthcode-Muster, 10 Kapitel, MENTORIN-TON
(Endkundinnen-Regel: Staerke zuerst, Wachstumsfeld statt Schatten).
Abschluss-Kapitel laedt zum Abgleich mit dem bestehenden Design ein
(der Live-Moment im Raum: Ist-Auftritt gegen Chart-Signatur halten).

WERBEFREI wie der Leader-Reader: kein Abschluss-CTA (CTA-Zeilen kommen
nur von Patrycja selbst, Memory feedback_kasten_zeilen_von_patrycja),
nur Impressum/Datenschutz im Footer.

Quelle:  astro-business-reader.html
Ziel:    astro-design-reader.html (+ astro-design-reader-netlify/index.html + ZIP)
"""
import os, re, sys, shutil

NAME = "Dein Designcode"           # <- Reader-Name (Patrycja 26.07.2026)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-design-reader.html")
NETLIFY = os.path.join(HERE, "astro-design-reader-netlify")
# --- Editorial-Texturen (26.07., Patrycjas Design-Wunsch nach Screenshot):
# Petrol-Gewebe-Band + Beton-Grau. Beide Texturen werden als eingebettetes
# SVG-Korn (feTurbulence) erzeugt -> keine externen Bilder, Reader bleibt autark.
from urllib.parse import quote

def svg_uri(svg):
    return "data:image/svg+xml;utf8," + quote(svg, safe="'/:=,()% ")

GRAIN = svg_uri("<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'>"
    "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/>"
    "<feColorMatrix type='saturate' values='0'/>"
    "<feComponentTransfer><feFuncA type='linear' slope='0.16' intercept='0'/></feComponentTransfer></filter>"
    "<rect width='260' height='260' filter='url(%23n)'/></svg>")

WEAVE = svg_uri("<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'>"
    "<filter id='w'><feTurbulence type='turbulence' baseFrequency='0.012 0.09' numOctaves='2' stitchTiles='stitch'/>"
    "<feColorMatrix type='saturate' values='0'/>"
    "<feComponentTransfer><feFuncA type='linear' slope='0.20' intercept='0'/></feComponentTransfer></filter>"
    "<rect width='220' height='220' filter='url(%23w)'/></svg>")

# --- Engine eingebettet + wahrer Mondknoten (Muster Sammel-Update 26.07.) ---
with open(os.path.join(HERE, "true-node-data.js"), "r", encoding="utf-8") as f:
    TRUE_NODE_DATA_JS = f.read()
with open(os.path.join(HERE, "circular-natal-horoscope-1.1.0.js"), "r", encoding="utf-8") as f:
    ENGINE_JS = f.read()

with open(SRC, "r", encoding="utf-8") as f:
    s = f.read()

# NP-Monogramm aus dem Basis-Footer (eingebettetes PNG) als Banner-Wasserzeichen
NP_LOGO = re.search(r'legal-logo"[^>]*src="(data:image/png;base64,[^"]+)"', s).group(1)

def repl(old, new, label):
    global s
    if old not in s:
        sys.exit("FEHLT (" + label + "): " + old[:80])
    s = s.replace(old, new, 1)

# --- 0b. Engine eingebettet (statt CDN) + Wahrer-Knoten-Ephemeride ----------
repl('<script src="https://cdn.jsdelivr.net/npm/circular-natal-horoscope-js@1.1.0/dist/index.js"></script>',
     '<script>\n' + ENGINE_JS + '\n</script>\n<script>\n' + TRUE_NODE_DATA_JS + '''
// Wahrer Mondknoten am Julianischen Datum (UT): quadratische Interpolation
// ueber 3 Stuetzstellen (Base36-Millidegree, 4 Zeichen/Wert), Wrap ueber den
// kuerzesten Bogen. null ausserhalb 1900-2036. Max. Fehler ~0,1 Bogenminuten.
function trueNodeLon(jd){
  if(typeof jd !== 'number' || !isFinite(jd)) return null;
  const idx = (jd - TN_START_JD) / TN_STEP;
  const n = TN_DATA.length / 4;
  if(idx < 0 || idx > n - 1) return null;
  const i = Math.max(1, Math.min(Math.round(idx), n - 2));
  const t = idx - i;
  const v = function(k){ return parseInt(TN_DATA.substr(k * 4, 4), 36) / 1000; };
  const y1 = v(i);
  const y0 = y1 + (((v(i - 1) - y1 + 540) % 360) - 180);
  const y2 = y1 + (((v(i + 1) - y1 + 540) % 360) - 180);
  const val = y1 + t * (y2 - y0) / 2 + t * t * (y2 - 2 * y1 + y0) / 2;
  return ((val % 360) + 360) % 360;
}
</script>''', "true-node-script")

# --- 1. Branding / sichtbare Texte ---------------------------------------
repl("<title>Dein Business-Code</title>",
     "<title>" + NAME + "</title>", "title")

repl('<p class="header-eyebrow">Dein kosmischer Business-Blueprint</p>',
     '', "eyebrow-remove")

repl("<h1>Dein Business-Code</h1>",
     '<h1>Designcode</h1>\n    <p class="dc-brand">Patrycja Nasri</p>', "h1-band")

# --- Autarkie: externes Mond-Bild + Google-Fonts raus (Muster Eclipse v10) --
repl('background:url("https://patrycja-nasri.de/wp-content/uploads/2026/06/WEB-ASTRO3.png") center top / cover no-repeat;',
     'background:none;', "moon-url-remove")
repl('<link rel="preconnect" href="https://fonts.googleapis.com">\n', '', "gfonts-preconnect-remove")
repl('<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">\n', '', "gfonts-link-remove")

repl('<p class="subtitle">Gib deine Geburtsdaten ein. Auf der nächsten Seite bekommst du dein Geburtshoroskop angezeigt und einen fertigen KI-Prompt, der dir sagt, wie du dein Business führst, dich positionierst, skalierst und Geld verdienst.</p>',
     '<p class="subtitle">Farben, Formen, Schrift und Bildsprache: Deine Chart trägt deine Design-Signatur längst in sich. Gib deine Geburtsdaten ein und die Seite komponiert daraus deinen KI-Prompt für dein Branding-Reading.</p>',
     "subtitle")

repl('onclick="runCheck()">Meinen Business-Code aufdecken</button>',
     'onclick="runCheck()">Meinen Designcode aufdecken</button>', "submit-btn")

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

# --- 1b. Optionales Business-Feld (26.07., nach Patrycjas Beispiel-Reading:
# die Antwort wird erst dann richtig konkret, wenn die KI das Business kennt —
# Bildsprache, Kundinnen-Gefuehl und Schritte beziehen sich darauf) ----------
repl('''    <div class="name-group">
      <label class="field-label" for="userName">Dein Name</label>
      <input type="text" id="userName" placeholder="Wie heißt du?" autocomplete="off">
    </div>
''',
'''    <div class="name-group">
      <label class="field-label" for="userName">Dein Name</label>
      <input type="text" id="userName" placeholder="Wie heißt du?" autocomplete="off">
    </div>

    <div class="name-group">
      <label class="field-label" for="userBiz">Dein Business (optional)</label>
      <input type="text" id="userBiz" placeholder="z.B. Coaching, Network Marketing, Massagepraxis" autocomplete="off">
    </div>
''', "biz-field")

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

# --- 2b. Geburtszeit als TIPPFELD statt input[type=time] (Muster Eclipse ----
# Navigator v12: iOS zentriert/versteckt native Zeitfelder, CSS-Fix reichte
# nicht). HH:MM mit Auto-Doppelpunkt (1352 -> 13:52), Validierung 00-23/00-59.
repl('<input type="time" id="birthTime" autocomplete="off">',
     '<input type="text" id="birthTime" placeholder="HH:MM, z.B. 13:52" inputmode="numeric" autocomplete="off">',
     "time-field-text")

repl("    const time = $('birthTime').value;",
     '''    const timeRaw = ($('birthTime').value || '').trim();
    let time = '';
    (function(){
      let v = timeRaw;
      if(/^\\d{3,4}$/.test(v)){ if(v.length === 3) v = '0' + v; v = v.slice(0,2) + ':' + v.slice(2); }
      const tm = v.match(/^(\\d{1,2})[:.](\\d{2})$/);
      if(!tm) return;
      const hh = parseInt(tm[1], 10), mm = parseInt(tm[2], 10);
      if(hh > 23 || mm > 59) return;
      time = (hh < 10 ? '0' : '') + hh + ':' + (mm < 10 ? '0' : '') + mm;
    })();''',
     "time-parse")

repl("if(!time){ return fail('Bitte gib deine genaue Geburtszeit ein. Sie ist für deinen Aszendenten und deine Häuser nötig.'); }",
     "if(!time){ return fail('Bitte gib deine Geburtszeit als HH:MM ein, zum Beispiel 13:52. Sie ist für deinen Aszendenten und deine Häuser nötig.'); }",
     "time-error-msg")

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
  const bt = document.getElementById('birthTime');
  if(bt){
    bt.addEventListener('input', function(){
      let v = bt.value.replace(/[^\\d:.]/g, '').replace('.', ':');
      if(v.indexOf(':') === -1 && v.length > 2){
        v = v.slice(0,2) + ':' + v.slice(2,4);
      }
      bt.value = v.slice(0, 5);
    });
  }
});
</script>
</body>'''
repl('</body>', date_autodots, "date-autodots")

# --- 3. Ergebnis-Kopf + Zurueck-Button ------------------------------------
repl("<h2>Dein Business-Code${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Dein Chart als Business-Blueprint'}</p>",
     "<h2>" + NAME + "${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Deine Design-Signatur aus deiner Chart'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Meine Eingaben korrigieren", "back-btn")

# --- 4. Analyse-Schicht in runCheck einhaengen ------------------------------
# Anker NACH window.__chart, damit __fullChart und __aspects bereits gesetzt sind.
calc_anchor = "      window.__chart = chart;\n      generateReading();"
natal_calc = r"""      window.__chart = chart;

      // Designcode: die Chart als Design-Signatur lesen, bevor der Prompt
      // entsteht. Alles Weitere baut auf dieser Analyse auf.
      (function(){
        try{
          const FULL = window.__fullChart || [];
          const ASP = window.__aspects || [];
          const find = function(label){
            for(let i = 0; i < FULL.length; i++){ if(FULL[i].label === label) return FULL[i]; }
            return null;
          };

          // WAHRE natale Mondknoten (Muster Sammel-Update 26.07.): Die Engine
          // kann nur den mittleren Knoten, astro.com zeigt den wahren. Zeichen
          // UND Haus koennen kippen; die Knoten-Aspekte werden mit dem wahren
          // Knoten neu gerechnet (Orb 5). Faellt die Reihe aus (Jahrgang
          // ausserhalb 1900-2036), bleiben Engine-Werte.
          try{
            const SIGNS_DE = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische'];
            const norm360 = function(x){ return ((x % 360) + 360) % 360; };
            const signOfL = function(L){ return SIGNS_DE[Math.floor(norm360(L) / 30)] || ''; };
            const lonOf = function(b){ try{ return b.ChartPosition.Ecliptic.DecimalDegrees; }catch(e){ return null; } };
            const housesArr = (horo && horo.Houses) ? horo.Houses : [];
            const houseOfLong = function(L){
              for(let i = 0; i < housesArr.length; i++){
                const h = housesArr[i];
                let st, en;
                try { st = h.ChartPosition.StartPosition.Ecliptic.DecimalDegrees; en = h.ChartPosition.EndPosition.Ecliptic.DecimalDegrees; }
                catch(err){ continue; }
                const id = h.id || (i + 1);
                if(st <= en){ if(L >= st && L < en) return id; }
                else { if(L >= st || L < en) return id; }
              }
              return null;
            };
            const natalJd = (typeof origin !== 'undefined' && origin && origin.julianDate) ? origin.julianDate
              : ((horo && horo.origin && horo.origin.julianDate) ? horo.origin.julianDate : null);
            const tnL = (typeof trueNodeLon === 'function') ? trueNodeLon(natalJd) : null;
            if(tnL != null){
              const snL = (tnL + 180) % 360;
              FULL.forEach(function(e){
                if(e.label === 'Nordknoten'){ e.sign = signOfL(tnL); e.house = houseOfLong(tnL) || e.house; }
                if(e.label === 'Südknoten'){ e.sign = signOfL(snL); e.house = houseOfLong(snL) || e.house; }
              });
              for(let i = ASP.length - 1; i >= 0; i--){
                if(ASP[i].p1 === 'Nordknoten' || ASP[i].p2 === 'Nordknoten') ASP.splice(i, 1);
              }
              const PPAIRS = [['Sonne',CB.sun],['Mond',CB.moon],['Merkur',CB.mercury],['Venus',CB.venus],['Mars',CB.mars],['Jupiter',CB.jupiter],['Saturn',CB.saturn],['Uranus',CB.uranus],['Neptun',CB.neptune],['Pluto',CB.pluto],['Chiron',CB.chiron],['Lilith',CP.lilith],['Aszendent',horo.Ascendant],['MC',horo.Midheaven]];
              const AT = [[0,'Konjunktion'],[60,'Sextil'],[90,'Quadrat'],[120,'Trigon'],[180,'Opposition']];
              const SIGNOF0 = {}; FULL.forEach(function(e){ SIGNOF0[e.label] = e.sign; });
              PPAIRS.forEach(function(pr){
                const L = lonOf(pr[1]);
                if(L == null) return;
                const dd = Math.abs(((L - tnL + 540) % 360) - 180);
                AT.forEach(function(t){
                  const orb = Math.abs(dd - t[0]);
                  if(orb <= 5) ASP.push({ p1: pr[0], s1: SIGNOF0[pr[0]] || '', p2: 'Nordknoten', s2: signOfL(tnL), type: t[1], orb: orb });
                });
              });
              ASP.sort(function(a, b){ return (a.orb || 0) - (b.orb || 0); });
            }
          }catch(e){}

          // Horoskopherrscher: Herrscher des Aszendenten (Logik Chartruler-Reader)
          const RULER = { 'Widder':'Mars','Stier':'Venus','Zwillinge':'Merkur','Krebs':'Mond','Löwe':'Sonne','Jungfrau':'Merkur','Waage':'Venus','Skorpion':'Pluto','Schütze':'Jupiter','Steinbock':'Saturn','Wassermann':'Uranus','Fische':'Neptun' };
          const CORULER = { 'Skorpion':'Mars','Wassermann':'Saturn','Fische':'Jupiter' };
          const HOME = { 'Sonne':['Löwe'],'Mond':['Krebs'],'Merkur':['Zwillinge','Jungfrau'],'Venus':['Stier','Waage'],'Mars':['Widder','Skorpion'],'Jupiter':['Schütze','Fische'],'Saturn':['Steinbock','Wassermann'],'Uranus':['Wassermann'],'Neptun':['Fische'],'Pluto':['Skorpion'] };
          const asc = find('Aszendent') || {};
          const acSign = asc.sign || '';
          const rulerName = RULER[acSign] || '';
          const rulerEntry = rulerName ? (find(rulerName) || {}) : {};
          const coName = CORULER[acSign] || '';
          const coEntry = coName ? (find(coName) || {}) : {};
          const inOwnSign = rulerName ? ((HOME[rulerName] || []).indexOf(rulerEntry.sign || '') !== -1) : false;

          // Planeten je Haus + Dominanzen ueber die 10 Planeten
          const PLANETS = ['Sonne','Mond','Merkur','Venus','Mars','Jupiter','Saturn','Uranus','Neptun','Pluto'];
          const ELEM = { 'Widder':'Feuer','Löwe':'Feuer','Schütze':'Feuer','Stier':'Erde','Jungfrau':'Erde','Steinbock':'Erde','Zwillinge':'Luft','Waage':'Luft','Wassermann':'Luft','Krebs':'Wasser','Skorpion':'Wasser','Fische':'Wasser' };
          const MODAL = { 'Widder':'kardinal','Krebs':'kardinal','Waage':'kardinal','Steinbock':'kardinal','Stier':'fix','Löwe':'fix','Skorpion':'fix','Wassermann':'fix','Zwillinge':'veränderlich','Jungfrau':'veränderlich','Schütze':'veränderlich','Fische':'veränderlich' };
          const eCount = { 'Feuer':0, 'Erde':0, 'Luft':0, 'Wasser':0 };
          const mCount = { 'kardinal':0, 'fix':0, 'veränderlich':0 };
          const houseWho = {};
          PLANETS.forEach(function(p){
            const e = find(p);
            if(!e) return;
            if(eCount[ELEM[e.sign]] != null) eCount[ELEM[e.sign]]++;
            if(mCount[MODAL[e.sign]] != null) mCount[MODAL[e.sign]]++;
            const h = parseInt(e.house, 10);
            if(h >= 1 && h <= 12){ (houseWho[h] = houseWho[h] || []).push(p); }
          });
          const eSorted = Object.keys(eCount).sort(function(a, b){ return eCount[b] - eCount[a]; });
          const missing = Object.keys(eCount).filter(function(k){ return eCount[k] === 0; });
          const mSorted = Object.keys(mCount).sort(function(a, b){ return mCount[b] - mCount[a]; });

          // Haeuserherrscher der Marken-Haeuser 1, 5, 10 (Placidus-Spitzen).
          // Das Zeichen der Spitze kommt aus dem Startgrad des Engine-Hauses,
          // der Herrscher (modern + Mitherrscher) aus derselben Tabelle wie
          // der Horoskopherrscher. Muster: Eclipse Navigator v2.
          const SIGNS2 = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische'];
          const housesArr2 = (horo && horo.Houses) ? horo.Houses : [];
          const cuspSign = function(id){
            for(let i = 0; i < housesArr2.length; i++){
              const h = housesArr2[i];
              if((h.id || (i + 1)) !== id) continue;
              try{
                const st = h.ChartPosition.StartPosition.Ecliptic.DecimalDegrees;
                return SIGNS2[Math.floor((((st % 360) + 360) % 360) / 30)] || '';
              }catch(e){ return ''; }
            }
            return '';
          };
          const mkHouse = function(id, role){
            const cs = cuspSign(id);
            const rn = RULER[cs] || '';
            const re = rn ? (find(rn) || {}) : {};
            const cn = CORULER[cs] || '';
            const ce = cn ? (find(cn) || {}) : {};
            return { id: id, role: role, cuspSign: cs,
              ruler: { name: rn, sign: re.sign || '', house: re.house || '' },
              co: { name: cn, sign: ce.sign || '', house: ce.house || '' },
              planets: (houseWho[id] || []).slice() };
          };
          const houses = [
            mkHouse(1, 'mein Auftritt'),
            mkHouse(5, 'mein kreativer Ausdruck'),
            mkHouse(10, 'meine öffentliche Marke')
          ];

          const mc = find('MC') || {};
          window.__design = {
            acSign: acSign,
            ruler: {
              name: rulerName, sign: rulerEntry.sign || '', house: rulerEntry.house || '',
              inOwnSign: inOwnSign,
              co: { name: coName, sign: coEntry.sign || '', house: coEntry.house || '' }
            },
            houses: houses,
            venus: find('Venus') || {}, mercury: find('Merkur') || {},
            sun: find('Sonne') || {}, moon: find('Mond') || {},
            mcSign: mc.sign || '',
            eCount: eCount, domElement: eSorted[0], domElementN: eCount[eSorted[0]],
            missing: missing,
            mCount: mCount, domModal: mSorted[0], domModalN: mCount[mSorted[0]]
          };
        }catch(e){ window.__design = null; }
      })();

      generateReading();"""
repl(calc_anchor, natal_calc, "design-calc-injection")

# --- 4b. Ergebnis-Seite verschlanken (REGEL seit 14.07.): Platzierungen, ----
# Aspekte und Element-Block raus. Nur Signatur-Block + Prompt bleiben sichtbar.
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

# --- 5. Reading-Block: sichtbare Signatur + Prompt-CTA ----------------------
old_cta = """  html += `
  <div class="cta-block">
    <h3>Dein Business-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, wie du dein Business führst, wie du dich positionierst, wo deine Zone of Genius liegt und wie du am natürlichsten Geld verdienst.</p>
    <button class="copy-btn" id="copyBizBtn" onclick="copyBusinessReading()">Business-Prompt + Daten kopieren</button>
  </div>`;"""

new_cta = """  // Sichtbar: die Design-Signatur (die Analyse, aus der der Prompt komponiert wird)
  const D = window.__design || null;
  if(D){
    const badge = function(e){ return `<span class="badge sign-badge">${e.sign}</span>${e.house ? `<span class="badge house-badge">${e.house}. Haus</span>` : ''}`; };
    let dHtml = `
    <div class="data-block">
      <h3>Deine Design-Signatur</h3>
      <div class="data-grid">`;
    if(D.acSign) dHtml += `<div class="data-row"><span class="data-planet">Dein Aszendent</span><span class="data-values"><span class="badge sign-badge">${D.acSign}</span></span></div>`;
    if(D.ruler.name) dHtml += `<div class="data-row"><span class="data-planet">Dein Horoskopherrscher: ${D.ruler.name}</span><span class="data-values">${badge(D.ruler)}</span></div>`;
    D.houses.forEach(function(h){
      if(h.id === 1 || !h.ruler.name) return;
      dHtml += `<div class="data-row"><span class="data-planet">Herrscher deines ${h.id}. Hauses: ${h.ruler.name}</span><span class="data-values">${badge(h.ruler)}</span></div>`;
    });
    if(D.venus.sign) dHtml += `<div class="data-row"><span class="data-planet">Deine Venus</span><span class="data-values">${badge(D.venus)}</span></div>`;
    if(D.mcSign) dHtml += `<div class="data-row"><span class="data-planet">Dein MC</span><span class="data-values"><span class="badge sign-badge">${D.mcSign}</span></span></div>`;
    if(D.domElement) dHtml += `<div class="data-row"><span class="data-planet">Dein dominantes Element</span><span class="data-values"><span class="badge sign-badge">${D.domElement} (${D.domElementN} von 10)</span></span></div>`;
    dHtml += `</div></div>`;
    html += dHtml;
  }

  html += `
  <div class="cta-block">
    <h3>Dein Branding-Reading mit KI</h3>
    <p>Dein Prompt wurde aus deiner Chart komponiert: dein Aszendent, deine Häuserherrscher, deine Venus und dein dominantes Element geben ihm die Dramaturgie vor. Kopiere ihn und füge ihn bei ChatGPT oder Claude ein. Du bekommst dein komplettes Design-Reading: Farben, Schrift, Formen, Bildsprache und deine Markenstimme.</p>
    <button class="copy-btn" id="copyDesignBtn" onclick="copyDesignReading()">Design-Prompt + Daten kopieren</button>
  </div>`;"""
repl(old_cta, new_cta, "cta-block")

# --- 6. Abschluss-CTA raus: WERBEFREI (CTA-Zeilen kommen nur von Patrycja) --
repl('''  html += `
  <div class="cta-block">
    <p class="cta-kicker">Möchtest du noch tiefer in deine Chart eintauchen?</p>
    <h3>Lerne dich tiefer kennen, als Jahre der Selbstreflexion es je konnten.</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Hier erfährst du mehr: Dein AstroCode &rarr;</a>
  </div>`;''', '', "abschluss-cta-remove")

# --- 7. Prompt-Gehirn + Copy-Funktion austauschen --------------------------
# Der Prompt wird beim Kopieren aus der Design-Analyse komponiert.
# MENTORIN-TON (Endkundinnen-Regel): Staerke zuerst, Wachstumsfelder.
new_region = r"""  const READING_INTRO = `Du bist eine erfahrene Astrologin und Markendesignerin in einer Person. Ich sitze dir gegenüber wie in einer persönlichen Branding-Session, und du liest heute meine Chart als Design-Signatur: welche Farben, welche Formen, welche Schrift, welche Bildsprache und welche Markenstimme zu meiner Energie passen. Du schreibst klar, warm und konkret, so dass ich mich in jedem Satz wiedererkenne. Du liest stärkenorientiert: Du beginnst bei dem, was mich ausmacht, und liest herausfordernde Aspekte als Wachstumsfelder. Keine Floskeln, keine allgemeinen Astro-Sätze, kein Lehrbuchton.

Gib jedem Kapitel eine kurze, klare Überschrift, gern mit einem passenden Emoji. Arbeite mit kurzen Absätzen und mit Listen, wo sie helfen. Wenn unten mein Business steht, mach jede Empfehlung konkret dafür: meine Kundinnen, meine Räume, meine Angebote, mein Alltag.

Wichtig: Ich arbeite mit Placidus-Häusern. Alle Häuser in meinen Daten unten sind Placidus-Häuser.

Deine Lesebrille: Ein Haus zeigt die Bühne. Der Herrscher des Hauses zeigt, worüber die Bühne bespielt wird und wohin sie führt. Lies deshalb bei jedem Marken-Haus immer auch seinen Herrscher und dessen Aspekte, sie stehen unten bei meinen Daten.

Mein Design-Reading hat diese Kapitel:`;

  const READING_OUTRO = `Schreib auf Deutsch, in der Du-Form, warm und konkret. Stärke zuerst: Beginne jedes Kapitel bei dem, was mich stark macht, und benenne Wachstumsfelder ohne Härte. Jeder Satz konkret. Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker. Nimm dir Raum für jedes Kapitel.

Hier sind meine Daten:`;

  window.copyDesignReading = function(){
    const FULL = window.__fullChart || [];
    const ASP = window.__aspects || [];
    const D = window.__design || {};
    const m = window.__meta || {};
    const dj = function(arr){
      if(!arr || !arr.length) return '';
      if(arr.length === 1) return arr[0];
      return arr.slice(0, -1).join(', ') + ' und ' + arr[arr.length - 1];
    };
    const ph = function(e){ return (e && e.sign) ? (e.sign + ((e.house) ? (' in meinem ' + e.house + '. Haus') : '')) : ''; };
    const aspStr = function(a){ return a.p1 + (a.s1 ? (' in ' + a.s1) : '') + ' ' + a.type + ' ' + a.p2 + (a.s2 ? (' in ' + a.s2) : '') + ' (Orb ' + String(Math.round(a.orb * 10) / 10).replace('.', ',') + '°)'; };
    const aspOf = function(p){ return ASP.filter(function(a){ return a.p1 === p || a.p2 === p; }); };
    const h5 = (D.houses || []).filter(function(h){ return h.id === 5; })[0] || null;
    const h10 = (D.houses || []).filter(function(h){ return h.id === 10; })[0] || null;
    const lilithMerkur = aspOf('Merkur').some(function(a){ return a.p1 === 'Lilith' || a.p2 === 'Lilith'; });

    // --- Kapitel komponieren: nur was diese Chart wirklich hat --------------
    const steps = [];

    if(D.acSign && D.ruler && D.ruler.name){
      let r = 'Das Tor meiner Marke. Mein Aszendent ist ' + D.acSign + ', mein Auftritt läuft über ' + D.ruler.name + ', den Herrscher meines 1. Hauses und damit meinen Horoskopherrscher. ' + D.ruler.name + ' steht in ' + ph(D.ruler) + '.';
      if(D.ruler.inOwnSign) r += ' ' + D.ruler.name + ' steht im eigenen Zeichen und wirkt in voller Kraft.';
      if(D.ruler.co && D.ruler.co.name && D.ruler.co.sign) r += ' Der klassische Mitherrscher ist ' + D.ruler.co.name + ' in ' + ph(D.ruler.co) + '. Lies ihn als zweite Stimme dazu.';
      r += ' Lies daraus die erste Anmutung meiner Marke: die Energie, die jemand in den ersten drei Sekunden auf meinem Profil oder meiner Website spüren soll, bevor ein einziges Wort gelesen ist.';
      steps.push(r);
    }

    if(h5 && h5.cuspSign){
      let r = 'Mein kreativer Ausdruck. Auf der Spitze meines 5. Hauses steht ' + h5.cuspSign;
      if(h5.ruler.name && h5.ruler.sign) r += ', sein Herrscher ' + h5.ruler.name + ' steht in ' + ph(h5.ruler);
      r += '.';
      if(h5.co && h5.co.name && h5.co.sign) r += ' Mitherrscher ist ' + h5.co.name + ' in ' + ph(h5.co) + '.';
      if(h5.planets.length) r += ' In meinem 5. Haus ' + (h5.planets.length === 1 ? 'steht ' : 'stehen ') + dj(h5.planets) + '.';
      r += ' Das 5. Haus ist meine Spielfreude und meine schöpferische Kraft. Lies daraus, welche Art von Gestaltung und Content mir Freude macht und wie viel Verspieltheit, Kunst oder Ernst mein Design tragen darf.';
      steps.push(r);
    }

    if(h10 && D.mcSign){
      let r = 'Meine öffentliche Marke. Mein MC steht in ' + D.mcSign;
      if(h10.ruler.name && h10.ruler.sign) r += ', der Herrscher meines 10. Hauses ist ' + h10.ruler.name + ' in ' + ph(h10.ruler);
      r += '.';
      if(h10.co && h10.co.name && h10.co.sign) r += ' Mitherrscher ist ' + h10.co.name + ' in ' + ph(h10.co) + '.';
      if(h10.planets.length) r += ' In meinem 10. Haus ' + (h10.planets.length === 1 ? 'steht ' : 'stehen ') + dj(h10.planets) + '.';
      r += ' Lies daraus, welche Autorität mein Auftritt ausstrahlen darf, wofür meine Marke öffentlich stehen will und woran Menschen sie sofort wiedererkennen.';
      steps.push(r);
    }

    if(D.venus && D.venus.sign){
      steps.push('Meine Ästhetik. Meine Venus steht in ' + ph(D.venus) + '. Venus zeigt, was ich schön finde und was an mir anzieht. Lies aus ihr meine Materialität und meine Formensprache: opulent oder reduziert, weich oder kantig, glänzend oder matt. Beziehe die Venus-Aspekte aus meinen Daten ein.');
    }

    if(D.sun && D.sun.sign && D.moon && D.moon.sign){
      steps.push('Mein Kern und meine Temperatur. Meine Sonne steht in ' + ph(D.sun) + ', mein Mond in ' + ph(D.moon) + '. Die Sonne ist der Kern, der durch jedes Design durchscheinen muss, egal welches Produkt ich gerade zeige. Der Mond ist die emotionale Temperatur: wie es sich anfühlen soll, wenn jemand meinen Raum betritt. Benenne beides konkret.');
    }

    if(D.mercury && D.mercury.sign){
      let r = 'Meine Markensprache. Mein Merkur steht in ' + ph(D.mercury) + '. Lies daraus, wie meine Headlines, Captions und Mails klingen dürfen: Tempo, Ton, Satzlänge, wie direkt ich werden darf. Beziehe die Merkur-Aspekte aus meinen Daten ein.';
      if(lilithMerkur) r += ' Mein Merkur hat einen Aspekt zu Lilith: meine Sprache trägt eine wilde, unbequeme Wahrheit. Sag mir, wie ich sie in meiner Marke einsetze.';
      steps.push(r);
    }

    steps.push('Das Gefühl meiner Marke. Formuliere den einen Satz in Anführungszeichen, den eine Kundin innerlich denken soll, wenn sie mein Profil oder meine Website zum ersten Mal öffnet. Dieses Gefühl entscheidet in wenigen Sekunden, ob sie bleibt. Sag mir auch, welche drei Gestaltungs-Entscheidungen dieses Gefühl am stärksten tragen.');

    (function(){
      const facts = [];
      if(D.domElement) facts.push('In meiner Chart stehen ' + D.domElementN + ' von 10 Planeten in ' + D.domElement + '-Zeichen.');
      if(D.domModal) facts.push('Die dominante Qualität ist ' + D.domModal + ' (' + D.domModalN + ' von 10 Planeten).');
      if(facts.length){
        let r = 'Meine Farbwelt und mein Material. ' + facts.join(' ') + ' Übersetze diese Gewichtung in eine Farbwelt: Temperatur (warm oder kühl), Tiefe (hell oder dunkel), Kontrast (laut oder leise) und Material (matt, glänzend, Naturmaterial, Metall). Nenne konkrete Farbnamen, unter denen ich mir sofort etwas vorstellen kann (zum Beispiel Salbeigrün, Cremeweiß, warmes Taupe), und sag mir klar, welche Farben und Kontraste ich vermeide.';
        if(D.missing && D.missing.length) r += ' Kein Planet steht in einem ' + dj(D.missing) + '-Zeichen. Sag mir, was das für mein Design bedeutet: bewusst weglassen oder als kleinen Akzent nachnähren.';
        steps.push(r);
      }
    })();

    steps.push('Mein Design-Steckbrief. Verdichte alles zu konkreten Empfehlungen, mit denen ich sofort arbeiten kann: eine Farbpalette aus 4 bis 6 Farben mit Farbnamen und Hex-Codes und einer kurzen Begründung je Farbe, ein Typografie-Charakter für Headlines und einer für Lesetext (beschreibe den Charakter und nenne 2 bis 3 Beispiel-Schriften), Formen und Layout (Kanten, Rundungen, Weißraum, Ordnung oder Collage), eine Logo-Idee (Schriftzug oder Symbol, welche Formen und Zeichen zu meiner Signatur passen), meine Bildsprache als Liste konkreter Momente und Motive aus meinem Alltag und meinem Business (konkrete Szenen statt Stockfotos) und meine Markenstimme in drei Worten. Dazu drei Do\'s und drei Don\'ts für mein Branding.');

    steps.push('Der rote Faden. Lies aus allem die eine Design-Geschichte, die meine Chart erzählt, und formuliere daraus einen Satz in der Ich-Form über meine Marke, den ich mir aufschreiben kann.');

    steps.push('Meine nächsten Schritte. Gib mir zum Schluss drei konkrete, sofort umsetzbare Schritte für meinen Auftritt, so praktisch wie: Hauptfarben auf drei begrenzen, zwei Schriften festlegen, professionelle Fotos planen. Wähle die drei Schritte, die bei meiner Signatur den größten Unterschied machen.');

    steps.push('Der Abgleich. Stelle mir am Ende eine einzige Frage: An welcher Stelle zeigt mein heutiger Auftritt am wenigsten von dem, was meine Chart über mich weiß? Biete mir danach drei Vertiefungen an und frag mich, welche ich wählen will: erstens, ich beschreibe dir mein aktuelles Design (Farben, Schriften, Logo, Bildwelt) und du gleichst es mit meiner Signatur ab. Zweitens, wir entwerfen meine Farbpalette im Detail. Drittens, wir übersetzen meine Signatur in ein konkretes Instagram-Profil: Profilbild, Bio, Feed-Look, Story-Design.');

    const numbered = steps.map(function(t, i){ return (i + 1) + '. ' + t; }).join('\n\n');

    // --- Datenteil ----------------------------------------------------------
    const data = [];
    if(m.name) data.push('Name: ' + m.name);
    if(m.date){ const dp = m.date.split('-'); data.push('Geburtsdatum: ' + dp[2]+'.'+dp[1]+'.'+dp[0] + (m.time ? (' um ' + m.time + ' Uhr') : '')); }
    if(m.place) data.push('Geburtsort: ' + m.place);
    const biz = (document.getElementById('userBiz') || { value: '' }).value.trim();
    if(biz) data.push('Mein Business: ' + biz);
    data.push('');
    data.push('MEINE DESIGN-SIGNATUR (vorbereitete Analyse):');
    if(D.acSign) data.push('Aszendent: ' + D.acSign);
    if(D.ruler && D.ruler.name){
      data.push('Horoskopherrscher (Herrscher meines 1. Hauses): ' + D.ruler.name + ' in ' + D.ruler.sign + (D.ruler.house ? (', ' + D.ruler.house + '. Haus') : '') + (D.ruler.inOwnSign ? ' (im eigenen Zeichen)' : ''));
      if(D.ruler.co && D.ruler.co.name && D.ruler.co.sign) data.push('Klassischer Mitherrscher: ' + D.ruler.co.name + ' in ' + D.ruler.co.sign + (D.ruler.co.house ? (', ' + D.ruler.co.house + '. Haus') : ''));
    }
    (D.houses || []).forEach(function(h){
      if(h.id === 1 || !h.cuspSign) return;
      let line = 'Spitze meines ' + h.id + '. Hauses (' + h.role + '): ' + h.cuspSign;
      if(h.ruler.name && h.ruler.sign) line += ' / Herrscher: ' + h.ruler.name + ' in ' + h.ruler.sign + (h.ruler.house ? (', ' + h.ruler.house + '. Haus') : '');
      if(h.co && h.co.name && h.co.sign) line += ' / Mitherrscher: ' + h.co.name + ' in ' + h.co.sign + (h.co.house ? (', ' + h.co.house + '. Haus') : '');
      line += ' / Planeten im Haus: ' + (h.planets.length ? h.planets.join(', ') : 'keine');
      data.push(line);
    });
    if(D.mcSign) data.push('MC: ' + D.mcSign);
    if(D.eCount) data.push('Elemente (10 Planeten): Feuer ' + D.eCount['Feuer'] + ', Erde ' + D.eCount['Erde'] + ', Luft ' + D.eCount['Luft'] + ', Wasser ' + D.eCount['Wasser'] + (D.missing && D.missing.length ? (' (unbesetzt: ' + dj(D.missing) + ')') : ''));
    if(D.mCount) data.push('Qualitäten (10 Planeten): kardinal ' + D.mCount['kardinal'] + ', fix ' + D.mCount['fix'] + ', veränderlich ' + D.mCount['veränderlich']);
    data.push('');
    data.push('DIE WICHTIGEN ASPEKTE MEINER SIGNATUR-PUNKTE (Orb bis 5°, der engste wirkt am stärksten):');
    (function(){
      const done = {};
      const keyPlanets = [];
      if(D.ruler && D.ruler.name) keyPlanets.push(['Horoskopherrscher ' + D.ruler.name, D.ruler.name]);
      (D.houses || []).forEach(function(h){
        if(h.id === 1 || !h.ruler.name) return;
        keyPlanets.push(['Herrscher meines ' + h.id + '. Hauses, ' + h.ruler.name, h.ruler.name]);
      });
      keyPlanets.push(['Venus', 'Venus']);
      keyPlanets.push(['Merkur', 'Merkur']);
      keyPlanets.forEach(function(kp){
        if(done[kp[1]]){ data.push('Aspekte von ' + kp[0] + ': siehe ' + done[kp[1]] + '.'); return; }
        done[kp[1]] = kp[0];
        const list = aspOf(kp[1]);
        if(list.length){
          data.push('Aspekte von ' + kp[0] + ':');
          list.forEach(function(a){ data.push('- ' + aspStr(a)); });
        } else {
          data.push('Aspekte von ' + kp[0] + ': keine engen Aspekte (Orb bis 5°). Dieser Punkt wirkt frei und ungebunden.');
        }
      });
    })();
    data.push('');
    data.push('MEIN VOLLSTÄNDIGES CHART (Placidus-Häuser):');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });
    if(ASP.length){
      data.push('');
      data.push('ALLE MEINE ENGSTEN ASPEKTE (nach Orb sortiert):');
      ASP.forEach(function(a){ data.push('- ' + aspStr(a)); });
    }

    const full = READING_INTRO + '\n\n' + numbered + '\n\n' + READING_OUTRO + '\n\n' + data.join('\n');
    const btn = document.getElementById('copyDesignBtn');
    const done = function(){ if(btn){ const o = btn.getAttribute('data-label') || btn.textContent; btn.setAttribute('data-label', o); btn.textContent = '✓ Kopiert! Jetzt in ChatGPT einfügen'; setTimeout(function(){ btn.textContent = o; }, 2800); } };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(full).then(done).catch(function(){ fallbackCopy(full, done); });
    } else { fallbackCopy(full, done); }
  };"""

pat = re.compile(r"  const BUSINESS_PROMPT = `.*?\n  window\.copyBusinessReading = function\(\)\{.*?\n  \};", re.DOTALL)
if not pat.search(s):
    sys.exit("FEHLT: BUSINESS_PROMPT / copyBusinessReading Region")
s = pat.sub(lambda _: new_region, s, count=1)

# --- 8. EDITORIAL-Design als Override-Layer (26.07., Patrycjas Screenshot):
# Petrol-Gewebe-Band mit gesperrter Serifen-Headline, NP-Monogramm als
# Wasserzeichen, Beton-Grau als Fläche, Elfenbein-Buttons (massiv, nie Outline).
# Serifen-Stack Didot/Bodoni/Baskerville = elegant auf Apple-Geräten, faellt
# sauber auf Georgia/serif zurueck. Gewinnt, weil zuletzt im Head.
extra_css = '''<style>
:root{ --petrol:#0B2A28; --petrol-deep:#071E1C; --ink:#101314; --stone:#39393B;
  --ivory:#EDE7DB; --line:rgba(255,255,255,0.16); --text:#E9ECEA; --muted:#B9C2BF; }
html{ background:#39393B !important; }
body{ background:#39393B !important; color:var(--text) !important; }
#binary-canvas{ display:none !important; }
.sparkle{ display:none !important; }
.moon-scene{ display:none !important; }
body::after{ content:"" !important; position:fixed; inset:0; z-index:0; pointer-events:none;
  background-image:url("__GRAIN__"), radial-gradient(130% 100% at 50% 0%, rgba(0,0,0,0) 40%, rgba(0,0,0,0.42) 100%);
  background-repeat:repeat, no-repeat; opacity:0.85; }

/* ---- Petrol-Band (Formular-Kopf) ---- */
.container{ padding-top:0 !important; }
body{ padding-top:0 !important; }
header{ position:relative; width:100vw; margin:0 calc(50% - 50vw) 40px !important;
  padding:clamp(70px, 11vw, 120px) 24px clamp(48px, 7vw, 84px) !important;
  background:linear-gradient(180deg, #0D302D 0%, #082220 100%) !important;
  overflow:hidden; box-shadow:0 30px 70px rgba(0,0,0,0.45); }
header::before{ content:""; position:absolute; inset:0; pointer-events:none;
  background-image:
    radial-gradient(60% 90% at 12% 8%, rgba(72,178,160,0.30), transparent 60%),
    radial-gradient(55% 75% at 86% 78%, rgba(34,104,94,0.38), transparent 65%),
    url("__WEAVE__"), url("__GRAIN__");
  background-repeat:no-repeat, no-repeat, repeat, repeat; }
header::after{ content:""; position:absolute; right:-30px; bottom:-60px;
  width:clamp(180px, 30vw, 320px); height:clamp(180px, 30vw, 320px);
  background:url("__NP__") center / contain no-repeat; opacity:0.11; pointer-events:none; }
header h1{
  font-family:'Didot','Bodoni 72','Playfair Display','Baskerville','Georgia',serif !important;
  font-weight:400 !important; text-transform:uppercase !important;
  letter-spacing:clamp(0.26em, 3.2vw, 0.48em) !important; text-indent:clamp(0.26em, 3.2vw, 0.48em);
  font-size:clamp(1.65rem, 6vw, 3.3rem) !important; line-height:1.2 !important;
  color:#F4F6F4 !important; text-shadow:0 2px 24px rgba(0,0,0,0.35) !important;
  position:relative; z-index:1; margin-bottom:14px !important; }
.dc-brand{
  font-family:'Didot','Bodoni 72','Playfair Display','Baskerville','Georgia',serif;
  text-transform:uppercase; letter-spacing:0.34em; text-indent:0.34em;
  font-size:clamp(0.82rem, 2.4vw, 1.05rem); color:#D9E2DF;
  position:relative; z-index:1; margin:0 0 26px; text-align:center; }
.subtitle{ position:relative; z-index:1;
  font-family:'Inter','Helvetica Neue',sans-serif !important;
  font-style:normal !important; font-size:1.02rem !important; line-height:1.75 !important;
  letter-spacing:0.01em !important; color:#C7D2CE !important;
  max-width:560px !important; margin:0 auto !important; }
header .divider{ position:relative; z-index:1;
  background:linear-gradient(to right, transparent, rgba(237,231,219,0.65), transparent) !important; }

/* ---- Ergebnis-Kopf als schmales Band ---- */
.results-header{ position:relative; width:100vw; margin:0 calc(50% - 50vw) 40px !important;
  padding:clamp(54px, 8vw, 84px) 24px clamp(36px, 5vw, 56px) !important;
  background:linear-gradient(180deg, #0D302D 0%, #082220 100%) !important; overflow:hidden;
  box-shadow:0 30px 70px rgba(0,0,0,0.45); }
.results-header::before{ content:""; position:absolute; inset:0; pointer-events:none;
  background-image:
    radial-gradient(60% 90% at 12% 8%, rgba(72,178,160,0.30), transparent 60%),
    radial-gradient(55% 75% at 86% 78%, rgba(34,104,94,0.38), transparent 65%),
    url("__WEAVE__"), url("__GRAIN__");
  background-repeat:no-repeat, no-repeat, repeat, repeat; }
.results-header h2{
  font-family:'Didot','Bodoni 72','Playfair Display','Baskerville','Georgia',serif !important;
  font-weight:400 !important; text-transform:uppercase !important;
  letter-spacing:clamp(0.14em, 2vw, 0.3em) !important; text-indent:clamp(0.14em, 2vw, 0.3em);
  font-size:clamp(1.3rem, 4.6vw, 2.3rem) !important; color:#F4F6F4 !important;
  text-shadow:0 2px 24px rgba(0,0,0,0.35) !important; position:relative; z-index:1; }
.results-header p{ color:#C7D2CE !important; position:relative; z-index:1;
  font-family:'Inter','Helvetica Neue',sans-serif !important; font-style:normal !important; }

/* ---- Flächen und Kästen ---- */
.tip-box, .form-section, .reading-block, .summary-block, .data-block, .cta-block{
  background:rgba(16,19,20,0.45) !important;
  border:1px solid var(--line) !important;
  border-radius:16px !important;
  box-shadow:0 24px 60px rgba(0,0,0,0.38) !important; }
.reading-block h3, .summary-block h3, .data-block h3, .cta-block h3, .form-section h3{
  font-family:'Didot','Bodoni 72','Playfair Display','Baskerville','Georgia',serif !important;
  font-weight:400 !important; text-transform:uppercase !important;
  letter-spacing:0.16em !important; color:var(--ivory) !important; }
.cta-block p{ color:var(--text) !important; }
.field-label{ color:var(--muted) !important; letter-spacing:0.14em !important; }
.error-msg{ color:#F0A9A0 !important; }
input[type="text"], input[type="date"], input[type="time"]{
  background:rgba(255,255,255,0.05) !important; border:1px solid var(--line) !important;
  color:var(--text) !important; border-radius:10px !important; }
input::placeholder{ color:rgba(233,236,234,0.38) !important; }
input[type="text"]:focus, input[type="date"]:focus, input[type="time"]:focus{
  border-color:rgba(237,231,219,0.65) !important; box-shadow:0 0 26px rgba(237,231,219,0.12) !important; }
.place-results{ background:#1B1E1F !important; border:1px solid var(--line) !important; }
.place-item{ color:var(--text) !important; }
.place-item:hover, .place-item.active{ background:rgba(237,231,219,0.12) !important; }
.place-chosen{ color:#9FD8CC !important; font-weight:600 !important; }
select option{ background:#1B1E1F !important; color:var(--text) !important; }
.sign-badge{ background:rgba(13,48,45,0.65) !important; border:1px solid rgba(159,216,204,0.4) !important; color:#DCEeE9 !important; }
.house-badge{ background:rgba(237,231,219,0.10) !important; border:1px solid rgba(237,231,219,0.35) !important; color:var(--ivory) !important; }

/* ---- Buttons: massiv Elfenbein, editorial ---- */
.submit-btn, .cta-link, .copy-btn{
  background:var(--ivory) !important; color:#101314 !important;
  border:none !important; border-radius:10px !important;
  text-transform:uppercase !important; letter-spacing:0.12em !important; font-weight:700 !important;
  box-shadow:0 14px 40px rgba(0,0,0,0.4) !important; }
.submit-btn:hover, .cta-link:hover, .copy-btn:hover{
  background:#FFFDF7 !important; box-shadow:0 18px 52px rgba(0,0,0,0.5) !important; }
.back-btn{ color:#D9E2DF !important; }
.legal-footer, .legal-footer a{ color:#D9E2DF !important; }
</style>
</head>'''.replace("__GRAIN__", GRAIN).replace("__WEAVE__", WEAVE).replace("__NP__", NP_LOGO)
repl('</head>', extra_css, "editorial-css")

# Sicherheitscheck: keine Business-Reste mehr in Logik-Hooks
for leftover in ["copyBusinessReading", "copyBizBtn", "BUSINESS_PROMPT", "subscribeLead", "userEmail", "Business-Code", "Business-Blueprint", "Zone of Genius"]:
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
