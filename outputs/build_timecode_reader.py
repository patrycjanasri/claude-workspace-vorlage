#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut den Timecode-Reader aus dem Business-Reader.
Muster: build_birthcode_reader.py (ASTROCODE-Design, Tippfeld-Datum,
schlanke Ergebnis-Seite, kein E-Mail-Gate, komponierter Prompt).

DAS BESONDERE (Patrycjas Idee 22.07.2026): Der erste Reader ohne festen
Transit-Moment. Er rechnet ab dem Tag der Nutzung drei Monate nach vorn
(evergreen, wiederverwendbar) und legt die laufenden Planeten ueber das
Geburtshoroskop der Anwenderin:

  - Abtastung des Zeitfensters in 2-Tages-Schritten (92 Tage, 47 Charts
    der Engine), Termine per linearer Interpolation auf den Tag genau
  - exakte Aspekt-Termine von Transit-Mars bis Transit-Chiron zu den
    natalen Punkten (Sonne, Mond, Merkur, Venus, Mars, Jupiter, Saturn,
    AC, MC, plus Chartruler, falls der ein aeusserer Planet ist)
  - Dauer-Transite: langsame Planeten, die das ganze Fenster eng im Orb
    stehen, ohne exakt zu werden (die wuerden sonst durchs Raster fallen)
  - Hauswechsel: wann ein Transit-Planet in ein neues Placidus-Haus der
    Anwenderin wechselt (auch rueckwaerts bei Rueckläufigkeit)
  - Merkur-Rueckläufigkeits-Fenster im Zeitraum
  - Neumonde und Vollmonde mit dem natalen Haus, in das sie fallen

Der Prompt wird daraus KOMPONIERT (Muster Birthcode): Kapitel, die das
Zeitfenster nicht hergibt, tauchen gar nicht auf. Business-Fokus:
Haeuser 2, 6, 8, 10, 11, Investitions-Fenster, Launch-Termine.

Name final (Patrycja 22.07.): "Dein Timecode". Monetarisierung offen,
gebaut ohne Gate nach Barbault-Modell (Link = Produkt, falls bezahlt).

Quelle:  astro-business-reader.html
Ziel:    astro-timecode-reader.html (+ astro-timecode-reader-netlify/index.html + ZIP)
"""
import os, re, sys, shutil, io, base64
from PIL import Image, ImageFilter, ImageChops

NAME = "Dein Timecode"             # <- Reader-Name (final, Patrycja 22.07.2026)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-timecode-reader.html")
NETLIFY = os.path.join(HERE, "astro-timecode-reader-netlify")
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

# --- Engine eingebettet + wahrer Mondknoten (Sammel-Update 26.07.2026) ------
# Muster 1:1 aus build_eklipsen_reader.py (Eclipse Navigator): Die Engine kann
# nur den MITTLEREN Knoten rechnen, astro.com zeigt den WAHREN. Die eingebettete
# Swiss-Ephemeris-Reihe (build_true_node_data.py, 1900-2036, taeglich) liefert
# den wahren Knoten. Die Engine liegt lokal vor -> kein CDN mehr, Reader autark.
with open(os.path.join(HERE, "true-node-data.js"), "r", encoding="utf-8") as f:
    TRUE_NODE_DATA_JS = f.read()
with open(os.path.join(HERE, "circular-natal-horoscope-1.1.0.js"), "r", encoding="utf-8") as f:
    ENGINE_JS = f.read()

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
     '<p class="subtitle">Dein Business-Timing für die nächsten drei Monate. Gib deine Geburtsdaten ein. Die Seite legt die laufenden Planeten über dein Geburtshoroskop, berechnet deine Termine auf den Tag genau und komponiert daraus deinen individuellen KI-Prompt: welche Räume sich öffnen, wann du investierst und worauf du achten darfst.</p>',
     "subtitle")

repl('onclick="runCheck()">Meinen Business-Code aufdecken</button>',
     'onclick="runCheck()">Meinen Timecode berechnen</button>', "submit-btn")

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
     "<h2>" + NAME + "${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Dein Business-Timing der nächsten drei Monate'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Neuen Timecode erstellen", "back-btn")

# --- 4. Transit-Scan in runCheck einhaengen --------------------------------
# --- 3b. Engine eingebettet (statt CDN) + Wahrer-Knoten-Ephemeride ----------
# 1:1 das Muster aus build_eklipsen_reader.py (Eclipse Navigator, 25.07.)
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

# Anker NACH window.__chart, damit __fullChart und __aspects bereits gesetzt sind.
calc_anchor = "      window.__chart = chart;\n      generateReading();"
scan_calc = r"""      window.__chart = chart;

      // Timecode: Transit-Scan der naechsten drei Monate ab dem Tag der Nutzung.
      // Die Seite tastet das Zeitfenster in 2-Tages-Schritten ab (47 Charts der
      // Engine, Koordinaten Berlin nur fuer die Zeitzonen-Aufloesung, die
      // Planeten-Laengen sind ortsunabhaengig) und legt alle Termine in
      // window.__timecode ab. Der Prompt wird daraus komponiert.
      (function(){
        try{
          // TIMECODE-SCAN-START
          const lonOf = function(b){ try{ return b.ChartPosition.Ecliptic.DecimalDegrees; }catch(e){ return null; } };
          const SIGNS_DE = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische'];
          const wrap180 = function(x){ return ((x % 360) + 540) % 360 - 180; };
          const norm360 = function(x){ return ((x % 360) + 360) % 360; };
          const pad2 = function(n){ return (n < 10 ? '0' : '') + n; };
          const fmtDate = function(d){ return pad2(d.getDate()) + '.' + pad2(d.getMonth() + 1) + '.' + d.getFullYear(); };
          const fmtDeg = function(L){
            const inSign = L % 30;
            let d = Math.floor(inSign);
            let m = Math.round((inSign - d) * 60);
            if(m === 60){ m = 0; d += 1; }
            return d + '°' + (m < 10 ? '0' : '') + m + "' " + (SIGNS_DE[Math.floor(norm360(L) / 30)] || '');
          };

          // Natale Haeuserspitzen + Placidus-Haus eines Transit-Grads
          // (Muster: build_chiron_reader.py / build_neumond_reader.py, houseOfLong)
          const houses = (horo && horo.Houses) ? horo.Houses : [];
          const cusps = [];
          for(let i = 0; i < houses.length; i++){
            try{
              cusps.push({ id: houses[i].id || (i + 1), st: houses[i].ChartPosition.StartPosition.Ecliptic.DecimalDegrees });
            }catch(err){}
          }
          const houseOfLong = function(L){
            for(let i = 0; i < houses.length; i++){
              const h = houses[i];
              let st, en;
              try { st = h.ChartPosition.StartPosition.Ecliptic.DecimalDegrees; en = h.ChartPosition.EndPosition.Ecliptic.DecimalDegrees; }
              catch(err){ continue; }
              const id = h.id || (i + 1);
              if(st <= en){ if(L >= st && L < en) return id; }
              else { if(L >= st || L < en) return id; }
            }
            return null;
          };

          // Natale Ziel-Punkte fuer die Aspekt-Termine
          const FULL = window.__fullChart || [];

          // WAHRE natale Mondknoten (Sammel-Update 26.07.): Die Engine kann nur
          // den mittleren Knoten, astro.com zeigt den wahren. Zeichen UND Haus
          // koennen dadurch kippen. Faellt die Reihe aus (Jahrgang ausserhalb
          // 1900-2036), bleiben die Engine-Werte stehen.
          try{
            const natalJd = (typeof origin !== 'undefined' && origin && origin.julianDate) ? origin.julianDate
              : ((horo && horo.origin && horo.origin.julianDate) ? horo.origin.julianDate : null);
            const tnNatal = (typeof trueNodeLon === 'function') ? trueNodeLon(natalJd) : null;
            if(tnNatal != null){
              const snNatal = (tnNatal + 180) % 360;
              const signOfL = function(L){ return SIGNS_DE[Math.floor(norm360(L) / 30)] || ''; };
              FULL.forEach(function(e){
                if(e.label === 'Nordknoten'){ e.sign = signOfL(tnNatal); e.house = houseOfLong(tnNatal) || e.house; }
                if(e.label === 'Südknoten'){ e.sign = signOfL(snNatal); e.house = houseOfLong(snNatal) || e.house; }
              });
            }
          }catch(e){}

          const SIGNOF = {}, HOUSEOF = {};
          FULL.forEach(function(e){ SIGNOF[e.label] = e.sign; HOUSEOF[e.label] = e.house; });
          const RULER = { 'Widder':'Mars','Stier':'Venus','Zwillinge':'Merkur','Krebs':'Mond','Löwe':'Sonne','Jungfrau':'Merkur','Waage':'Venus','Skorpion':'Pluto','Schütze':'Jupiter','Steinbock':'Saturn','Wassermann':'Uranus','Fische':'Neptun' };
          const acEntry = FULL.find(function(e){ return e.label === 'Aszendent'; }) || {};
          const rulerName = RULER[acEntry.sign || ''] || '';
          const targets = [
            ['Sonne', lonOf(CB.sun)], ['Mond', lonOf(CB.moon)], ['Merkur', lonOf(CB.mercury)],
            ['Venus', lonOf(CB.venus)], ['Mars', lonOf(CB.mars)], ['Jupiter', lonOf(CB.jupiter)],
            ['Saturn', lonOf(CB.saturn)], ['Aszendent', lonOf(horo.Ascendant)], ['MC', lonOf(horo.Midheaven)]
          ];
          const OUTER = { 'Uranus': CB.uranus, 'Neptun': CB.neptune, 'Pluto': CB.pluto };
          if(rulerName && OUTER[rulerName]) targets.push([rulerName, lonOf(OUTER[rulerName])]);

          // Abtastung: alle 2 Tage um 12:00 Uhr
          const DAYS = 92, STEP = 2;
          const t0 = window.__tcNow || Date.now();
          const samples = [];
          for(let i = 0; i <= DAYS; i += STEP){
            const d = new Date(t0 + i * 86400000);
            const o = new Origin({ year: d.getFullYear(), month: d.getMonth(), date: d.getDate(), hour: 12, minute: 0, latitude: 52.52, longitude: 13.405 });
            const h = new Horoscope({ origin: o, houseSystem: 'placidus', zodiac: 'tropical', language: 'en', aspectTypes: ['major'] });
            const B = h.CelestialBodies;
            samples.push({
              i: i,
              sun: lonOf(B.sun), moon: lonOf(B.moon), mercury: lonOf(B.mercury),
              mars: lonOf(B.mars), jupiter: lonOf(B.jupiter), saturn: lonOf(B.saturn),
              uranus: lonOf(B.uranus), neptune: lonOf(B.neptune), pluto: lonOf(B.pluto),
              chiron: lonOf(B.chiron)
            });
          }
          const dayDate = function(dayF){ return new Date(t0 + dayF * 86400000); };

          const TRANS = [
            ['Mars', 'mars'], ['Jupiter', 'jupiter'], ['Saturn', 'saturn'],
            ['Uranus', 'uranus'], ['Neptun', 'neptune'], ['Pluto', 'pluto'], ['Chiron', 'chiron']
          ];
          const SLOWP = { 'Saturn':1, 'Uranus':1, 'Neptun':1, 'Pluto':1, 'Chiron':1 };
          const TYPES = [[0,'Konjunktion'],[60,'Sextil'],[90,'Quadrat'],[120,'Trigon'],[180,'Opposition']];
          const W_P = { 'Pluto':5, 'Neptun':4.5, 'Uranus':4.5, 'Chiron':4, 'Saturn':4, 'Jupiter':3.5, 'Mars':2 };
          const W_A = { 'Konjunktion':3, 'Opposition':2.5, 'Quadrat':2.5, 'Trigon':2, 'Sextil':1.5 };
          const W_T = { 'Aszendent':3, 'MC':3, 'Sonne':3, 'Mond':2.5 };
          const NOM = { 'Sonne':'deine Sonne','Mond':'dein Mond','Merkur':'dein Merkur','Venus':'deine Venus','Mars':'dein Mars','Jupiter':'dein Jupiter','Saturn':'dein Saturn','Uranus':'dein Uranus','Neptun':'dein Neptun','Pluto':'dein Pluto','Aszendent':'dein Aszendent','MC':'dein MC' };
          const DAT = { 'Sonne':'meiner Sonne','Mond':'meinem Mond','Merkur':'meinem Merkur','Venus':'meiner Venus','Mars':'meinem Mars','Jupiter':'meinem Jupiter','Saturn':'meinem Saturn','Uranus':'meinem Uranus','Neptun':'meinem Neptun','Pluto':'meinem Pluto','Aszendent':'meinem Aszendenten','MC':'meinem MC' };

          // Exakte Aspekt-Termine + Dauer-Transite (eng im Orb, nie exakt)
          const hits = [], standing = [];
          TRANS.forEach(function(tp){
            const pName = tp[0], key = tp[1];
            targets.forEach(function(tg){
              const nName = tg[0], nLon = tg[1];
              if(nLon == null) return;
              TYPES.forEach(function(ty){
                const A = ty[0], aName = ty[1];
                if(pName === 'Mars' && aName === 'Sextil') return;
                const offs = (A === 0 || A === 180) ? [A] : [A, -A];
                let minOrb = 999, found = false;
                offs.forEach(function(off){
                  for(let k = 0; k + 1 < samples.length; k++){
                    const g1 = wrap180(samples[k][key] - nLon - off);
                    const g2 = wrap180(samples[k + 1][key] - nLon - off);
                    if(Math.abs(g1) < minOrb) minOrb = Math.abs(g1);
                    if(Math.abs(g2) < minOrb) minOrb = Math.abs(g2);
                    if((g1 < 0) !== (g2 < 0) || g1 === 0){
                      if(Math.abs(g1) > 45 || Math.abs(g2) > 45) continue;
                      const frac = Math.abs(g1) / ((Math.abs(g1) + Math.abs(g2)) || 1);
                      const dayF = samples[k].i + frac * STEP;
                      const isRuler = (nName === rulerName);
                      hits.push({
                        day: dayF, dateStr: fmtDate(dayDate(dayF)),
                        p: pName, type: aName, target: nName,
                        tSign: SIGNOF[nName] || '', tHouse: HOUSEOF[nName] || '',
                        nom: NOM[nName] || nName, dat: DAT[nName] || nName,
                        ruler: isRuler,
                        score: (W_P[pName] || 2) + (W_A[aName] || 2) + (W_T[nName] || 2) + (isRuler ? 1.5 : 0)
                      });
                      found = true;
                    }
                  }
                });
                if(!found && SLOWP[pName] && minOrb <= 1.2){
                  standing.push({ p: pName, type: aName, target: nName,
                    tSign: SIGNOF[nName] || '', tHouse: HOUSEOF[nName] || '',
                    dat: DAT[nName] || nName,
                    minOrb: Math.round(minOrb * 10) / 10, ruler: (nName === rulerName) });
                }
              });
            });
          });
          hits.sort(function(a, b){ return a.day - b.day; });

          // Hauswechsel der Transit-Planeten (auch rueckwaerts bei Rueckläufigkeit)
          const ingress = [];
          TRANS.forEach(function(tp){
            const pName = tp[0], key = tp[1];
            for(let k = 0; k + 1 < samples.length; k++){
              const L1 = samples[k][key], L2 = samples[k + 1][key];
              if(L1 == null || L2 == null) continue;
              const h1 = houseOfLong(L1), h2 = houseOfLong(L2);
              if(h1 == null || h2 == null || h1 === h2) continue;
              const dL = wrap180(L2 - L1);
              const retro = dL < 0;
              const cuspId = retro ? h1 : h2;
              let c = null;
              for(let ci = 0; ci < cusps.length; ci++){ if(cusps[ci].id === cuspId){ c = cusps[ci].st; break; } }
              let dayF = samples[k].i + STEP / 2;
              if(c != null && dL !== 0){
                const frac = wrap180(c - L1) / dL;
                if(frac >= 0 && frac <= 1) dayF = samples[k].i + frac * STEP;
              }
              ingress.push({ day: dayF, dateStr: fmtDate(dayDate(dayF)), p: pName, from: h1, to: h2, retro: retro });
            }
          });
          ingress.sort(function(a, b){ return a.day - b.day; });

          // Merkur-Rueckläufigkeits-Fenster
          const mercWins = [];
          (function(){
            const v = [];
            for(let k = 0; k + 1 < samples.length; k++){
              v.push(wrap180(samples[k + 1].mercury - samples[k].mercury));
            }
            const stations = [];
            for(let k = 0; k + 1 < v.length; k++){
              if((v[k] < 0) !== (v[k + 1] < 0)){
                const frac = Math.abs(v[k]) / ((Math.abs(v[k]) + Math.abs(v[k + 1])) || 1);
                stations.push({ day: samples[k].i + 1 + frac * STEP, toRetro: v[k] >= 0 });
              }
            }
            let rx = v.length > 0 && v[0] < 0;
            let curStart = rx ? 0 : null;
            let curOpen = rx;
            stations.forEach(function(st){
              if(st.toRetro && !rx){ rx = true; curStart = st.day; curOpen = false; }
              else if(!st.toRetro && rx){
                rx = false;
                mercWins.push({ fromDay: curStart, toDay: st.day, openStart: curOpen, openEnd: false });
                curStart = null; curOpen = false;
              }
            });
            if(rx){ mercWins.push({ fromDay: (curStart == null ? 0 : curStart), toDay: DAYS, openStart: curOpen, openEnd: true }); }
          })();
          const mercLines = mercWins.map(function(w){
            const a = w.openStart ? 'seit Fensterbeginn' : 'ab ' + fmtDate(dayDate(w.fromDay));
            const b = w.openEnd ? 'über das Fenster hinaus' : 'bis ' + fmtDate(dayDate(w.toDay));
            return a + ' ' + b;
          });

          // Neumonde und Vollmonde mit dem natalen Haus, in das sie fallen
          const moons = [];
          for(let k = 0; k + 1 < samples.length; k++){
            const s1 = samples[k].sun, s2 = samples[k + 1].sun;
            const e1 = norm360(samples[k].moon - s1);
            const e2 = norm360(samples[k + 1].moon - s2);
            const de = norm360(e2 - e1);
            const sunAt = function(frac){ return norm360(s1 + wrap180(s2 - s1) * frac); };
            if(e1 + de >= 360){
              const frac = (360 - e1) / (de || 1);
              const L = sunAt(frac);
              const dayF = samples[k].i + frac * STEP;
              moons.push({ day: dayF, dateStr: fmtDate(dayDate(dayF)), kind: 'Neumond', lon: L, sign: SIGNS_DE[Math.floor(L / 30)], house: houseOfLong(L) });
            } else if(e1 < 180 && e1 + de >= 180){
              const frac = (180 - e1) / (de || 1);
              const L = norm360(sunAt(frac) + 180);
              const dayF = samples[k].i + frac * STEP;
              moons.push({ day: dayF, dateStr: fmtDate(dayDate(dayF)), kind: 'Vollmond', lon: L, sign: SIGNS_DE[Math.floor(L / 30)], house: houseOfLong(L) });
            }
          }

          // Startpositionen der Transit-Planeten (Tag 1 des Fensters)
          const transNow = TRANS.map(function(tp){
            const L = samples[0][tp[1]], L2 = samples[1][tp[1]];
            if(L == null) return null;
            return { p: tp[0], deg: fmtDeg(L), rx: (L2 != null && wrap180(L2 - L) < 0), house: houseOfLong(L) };
          }).filter(function(x){ return !!x; });

          const rulerEntry = rulerName ? (FULL.find(function(e){ return e.label === rulerName; }) || {}) : {};
          const top = hits.slice().sort(function(a, b){ return b.score - a.score; }).slice(0, 3);

          window.__timecode = {
            startStr: fmtDate(new Date(t0)),
            endStr: fmtDate(new Date(t0 + DAYS * 86400000)),
            transNow: transNow, ingress: ingress, hits: hits, top: top,
            standing: standing, mercLines: mercLines, moons: moons,
            cusps: cusps.map(function(c){ return { id: c.id, sign: SIGNS_DE[Math.floor(norm360(c.st) / 30)] }; }),
            ruler: { name: rulerName, acSign: acEntry.sign || '', sign: rulerEntry.sign || '', house: rulerEntry.house || '' }
          };
          // TIMECODE-SCAN-END
        }catch(e){ window.__timecode = null; }
      })();

      generateReading();"""
repl(calc_anchor, scan_calc, "timecode-scan-injection")

# --- 4b. Ergebnis-Seite verschlanken (REGEL seit 14.07.): Platzierungen, ----
# Aspekte und Element-Block raus. Nur Timecode-Block + Prompt bleiben sichtbar.
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

# --- 5. Sichtbarer Timecode-Block + Prompt-CTA ------------------------------
old_cta = """  html += `
  <div class="cta-block">
    <h3>Dein Business-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, wie du dein Business führst, wie du dich positionierst, wo deine Zone of Genius liegt und wie du am natürlichsten Geld verdienst.</p>
    <button class="copy-btn" id="copyBizBtn" onclick="copyBusinessReading()">Business-Prompt + Daten kopieren</button>
  </div>`;"""

new_cta = """  // Sichtbar: das Zeitfenster und die staerksten Termine (schlanke Ergebnis-Seite)
  const TC = window.__timecode || null;
  if(TC){
    let tHtml = `
    <div class="data-block">
      <h3>Dein Timecode auf einen Blick</h3>
      <div class="data-grid">`;
    tHtml += `<div class="data-row"><span class="data-planet">Dein Zeitfenster</span><span class="data-values"><span class="badge sign-badge">${TC.startStr} bis ${TC.endStr}</span></span></div>`;
    tHtml += `<div class="data-row"><span class="data-planet">Deine Transit-Termine</span><span class="data-values"><span class="badge house-badge">${TC.hits.length} Termine auf den Tag genau</span></span></div>`;
    TC.top.forEach(function(ev){
      tHtml += `<div class="data-row"><span class="data-planet">${ev.p} ${ev.type} ${ev.nom}${ev.ruler ? ' (dein Chartruler)' : ''}</span><span class="data-values"><span class="badge sign-badge">${ev.dateStr}</span></span></div>`;
    });
    (TC.mercLines || []).forEach(function(ln){
      tHtml += `<div class="data-row"><span class="data-planet">Merkur rückläufig</span><span class="data-values"><span class="badge sign-badge">${ln}</span></span></div>`;
    });
    const nm = (TC.moons || []).find(function(mo){ return mo.kind === 'Neumond'; });
    if(nm){
      tHtml += `<div class="data-row"><span class="data-planet">Dein nächster Neumond</span><span class="data-values"><span class="badge sign-badge">${nm.dateStr} im Zeichen ${nm.sign}</span>${nm.house ? `<span class="badge house-badge">dein ${nm.house}. Haus</span>` : ''}</span></div>`;
    }
    tHtml += `</div></div>`;
    html += tHtml;
  }

  html += `
  <div class="cta-block">
    <h3>Dein Business-Timing mit KI</h3>
    <p>Dein Prompt wurde aus deinen Transiten komponiert: deine Termine, deine Hauswechsel, deine Neumonde und Vollmonde, alles auf den Tag genau berechnet für die nächsten drei Monate. Kopiere ihn und füge ihn bei ChatGPT oder Claude ein. Du bekommst ein Business-Reading wie von einer Astrologin, die deine Chart und den Himmel darüber vor sich liegen hat.</p>
    <button class="copy-btn" id="copyTimeBtn" onclick="copyTimecodeReading()">Timecode-Prompt + Termine kopieren</button>
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
    <p class="cta-kicker">Dir gefallen die Antworten aus meinem Timecode Reader?</p>
    <h3>Weißt du, dass du dank meines Astrocode-Portals dein ganzes Geburtshoroskop analysieren kannst! Tiefer als jedes Astroreading, denn erst die Bewegung bewirkt Veränderung! Wie oft hast du schon was über dich gehört, aber nicht umgesetzt!</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Öffne dein Astrocode-Portal und begib dich auf eine unvergessliche Reise zurück zu dir!</a>
  </div>`;''',
"astrocode-cta")

# --- 7. Prompt-Gehirn + Copy-Funktion austauschen --------------------------
# Der Prompt wird beim Kopieren aus den Transit-Terminen komponiert:
# Kapitel, die das Zeitfenster nicht hergibt, tauchen gar nicht auf.
new_region = r"""  const READING_INTRO = `Du bist eine erfahrene Astrologin und Business-Mentorin, die seit Jahrzehnten mit Transiten arbeitet. Ich sitze dir gegenüber wie in einer persönlichen Sitzung. Du legst heute die laufenden Planeten über mein Geburtshoroskop und liest daraus mein Business-Timing für die nächsten drei Monate. Du schreibst klar, tief und direkt, so dass mich jeder Satz trifft. Keine Floskeln, keine allgemeinen Astro-Sätze, kein Lehrbuchton.

Wichtig: Ich arbeite mit Placidus-Häusern. Alle Häuser in meinen Daten unten sind Placidus-Häuser. Alle Termine unten sind fertig berechnet. Du erfindest keine zusätzlichen Termine und verschiebst keine Daten: die Rechnung ist gemacht, du deutest.

Mein Reading hat diese Kapitel:`;

  const READING_OUTRO = `Schreib auf Deutsch, in der Du-Form, in Tiefe statt in Breite. Jeder Satz konkret. Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker. Nimm dir Raum für jedes Kapitel.

Hier sind meine Daten:`;

  window.copyTimecodeReading = function(){
    const FULL = window.__fullChart || [];
    const TC = window.__timecode || {};
    const m = window.__meta || {};
    const hits = TC.hits || [], ingress = TC.ingress || [], standing = TC.standing || [];
    const moons = TC.moons || [], mercLines = TC.mercLines || [], transNow = TC.transNow || [];
    const ruler = TC.ruler || {};
    const rulerHits = hits.filter(function(h){ return h.ruler; });
    const hardHits = hits.some(function(h){ return h.type === 'Quadrat' || h.type === 'Opposition'; }) || standing.length > 0;

    // --- Kapitel komponieren: nur was dieses Zeitfenster wirklich hat -------
    const steps = [];

    steps.push('Wo ich stehe. Wirf zuerst einen Blick auf mein Geburtshoroskop unten, besonders auf mein MC und auf mein 2., 6., 8., 10. und 11. Haus mit den Planeten darin und den Zeichen auf den Häuserspitzen. Beschreib in wenigen Sätzen, wie ich als Businessfrau aufgestellt bin: womit ich Geld verdiene, wie ich am besten arbeite, wie ich mit Investitionen und fremdem Geld umgehe, wohin meine Karriere zeigt und welche Rolle mein Netzwerk spielt. Das ist die Bühne, auf die meine Transite treffen.');

    if(transNow.length){
      steps.push('Die Räume, die sich öffnen. Unten stehen die laufenden Planeten mit dem Haus, durch das sie bei mir gerade ziehen, dazu meine Hauswechsel mit Datum. Lies daraus, welche Lebensbereiche in diesen drei Monaten Energie bekommen. Jupiter bringt Wachstum und Sichtbarkeit in sein Haus, Saturn verlangt dort Struktur und prüft, was trägt, Uranus bringt Umbrüche und neue Freiheit, Neptun macht durchlässig und verlangt Klarheit, Pluto wandelt den Bereich von Grund auf, Chiron macht eine empfindliche Stelle sichtbar, Mars gibt Antrieb und Tempo. Konzentriere dich auf mein 2., 6., 8., 10. und 11. Haus: Welche Räume öffnen sich für mein Business, und was mache ich in jedem konkret damit?');
    }

    if(hits.length){
      steps.push('Meine Termine. Unten steht meine Transit-Timeline, chronologisch, jeder Eintrag mit dem Tag, an dem der Aspekt exakt ist. Ein Transit wirkt schon Tage bis Wochen vor dem exakten Tag und klingt danach aus, bei den langsamen Planeten länger als bei Mars. Geh die Termine der Reihe nach durch. Für jeden: was er in meinem Business bewegt, welche Entscheidung er reif macht und woran ich in dieser Woche merke, dass er arbeitet.');
    }

    if(rulerHits.length && ruler.name){
      steps.push('Mein Chartruler im Fokus. ' + ruler.name + ' regiert meinen ' + ruler.acSign + '-Aszendenten und führt damit meine gesamte Chart. Termine mit dem Zusatz CHARTRULER treffen genau diesen Planeten. Lies sie als die persönlichsten Termine des Quartals: hier verändert sich, wie ich mich selbst führe, und mein Business zieht nach.');
    }

    if(standing.length){
      steps.push('Was durchgehend wirkt. Einige langsame Transite stehen im ganzen Zeitfenster eng im Orb, ohne exakt zu werden. Sie sind unten eigens aufgeführt. Lies sie als Grundton dieser drei Monate: kein einzelner Termin, eher ein Klima, in dem alle anderen Termine stattfinden.');
    }

    if(hits.length || ingress.length){
      steps.push('Investieren und säen. Lies aus meiner Timeline meine Fenster: Wann darf ich investieren, einkaufen, Verträge schließen, launchen, sichtbar werden? Wann prüfe ich besser, verhandle nach und konsolidiere? Nutze dafür vor allem die Jupiter-Termine, die Termine, die Punkte in meinem 2. oder 8. Haus treffen, und die Saturn-Termine als Gegengewicht. Mach es konkret und nenne Zeiträume mit Datum.');
    }

    if(mercLines.length){
      steps.push('Merkur rückläufig. Unten steht, wann Merkur in meinem Zeitfenster rückläufig läuft. Sag mir, was das für Verträge, Technik, Launches und Kommunikation in meinem Business heißt, wofür so eine Phase gut ist und was ich in ihr bewusst anders mache.');
    }

    if(moons.length){
      steps.push('Meine Neumonde und Vollmonde. Jeder Neumond ist ein Startpunkt, jeder Vollmond eine Ernte oder ein Abschluss. Unten stehen sie mit Datum und dem Haus, in das sie bei mir fallen. Sag mir zu jedem, was ich an diesem Termin in meinem Business am besten beginne oder abschließe.');
    }

    if(hardHits){
      steps.push('Worauf ich achten darf. Fasse die Reibungsfenster zusammen, vor allem die Quadrate und Oppositionen von Saturn und Pluto. Bei jedem: was der Schatten wäre, wenn ich unbewusst hineinlaufe, und was das Geschenk ist, wenn ich die Spannung nutze.');
    }

    steps.push('Der rote Faden. Erzähl mir die eine Geschichte dieser drei Monate: welches Kapitel mein Business gerade schreibt und was am Ende des Zeitfensters anders sein darf. Formuliere daraus einen Satz in der Ich-Form, den ich mir aufschreiben kann. Danach gib mir drei konkrete Schritte, jeder an einen Termin aus meiner Timeline gebunden, mit Datum.');

    steps.push('Meine Frage. Stell mir am Ende eine einzige, konfrontierende Frage zu dem Business-Muster, das mich in diesen drei Monaten am meisten bremsen könnte. Danach biete mir drei Richtungen an, in die wir das Reading vertiefen können, und frag mich, welche ich wählen will.');

    const numbered = steps.map(function(t, i){ return (i + 1) + '. ' + t; }).join('\n\n');

    // --- Datenteil ----------------------------------------------------------
    const data = [];
    if(m.name) data.push('Name: ' + m.name);
    if(m.date){ const dp = m.date.split('-'); data.push('Geburtsdatum: ' + dp[2]+'.'+dp[1]+'.'+dp[0] + (m.time ? (' um ' + m.time + ' Uhr') : '')); }
    if(m.place) data.push('Geburtsort: ' + m.place);
    data.push('');
    data.push('MEIN ZEITFENSTER: ' + (TC.startStr || '') + ' bis ' + (TC.endStr || ''));
    if(transNow.length){
      data.push('');
      data.push('DIE LAUFENDEN PLANETEN AM STARTTAG (mit dem Haus, durch das sie bei mir ziehen):');
      transNow.forEach(function(t){
        data.push('- Transit-' + t.p + ': ' + t.deg + ', läuft ' + (t.rx ? 'rückläufig' : 'direkt') + (t.house ? (', in meinem ' + t.house + '. Haus') : ''));
      });
    }
    if(ingress.length){
      data.push('');
      data.push('MEINE HAUSWECHSEL IM ZEITFENSTER:');
      ingress.forEach(function(g){
        data.push('- ' + g.dateStr + ': ' + g.p + (g.retro ? (' zieht sich rückläufig in mein ' + g.to + '. Haus zurück') : (' wechselt in mein ' + g.to + '. Haus')));
      });
    }
    if(hits.length){
      data.push('');
      data.push('MEINE TRANSIT-TIMELINE (chronologisch, jeweils der Tag, an dem der Aspekt exakt ist):');
      hits.forEach(function(h){
        const ctx = h.target + ' in ' + h.tSign + (h.tHouse ? (', mein ' + h.tHouse + '. Haus') : '');
        data.push('- ' + h.dateStr + ': Transit-' + h.p + ' ' + h.type + ' zu ' + h.dat + ' (' + ctx + ')' + (h.ruler ? ' [CHARTRULER]' : ''));
      });
    }
    if(standing.length){
      data.push('');
      data.push('DAUERHAFT WIRKSAM IM GANZEN ZEITFENSTER (eng im Orb, wird nicht exakt):');
      standing.forEach(function(st){
        data.push('- Transit-' + st.p + ' ' + st.type + ' zu ' + st.dat + ' (' + st.target + ' in ' + st.tSign + (st.tHouse ? (', mein ' + st.tHouse + '. Haus') : '') + '), engster Orb ' + String(st.minOrb).replace('.', ',') + '°' + (st.ruler ? ' [CHARTRULER]' : ''));
      });
    }
    data.push('');
    data.push('MERKUR IN MEINEM ZEITFENSTER:');
    if(mercLines.length){
      mercLines.forEach(function(ln){ data.push('- Merkur rückläufig: ' + ln); });
    } else {
      data.push('- Merkur läuft im gesamten Zeitfenster direkt.');
    }
    if(moons.length){
      data.push('');
      data.push('MEINE NEUMONDE UND VOLLMONDE (mit dem Haus, in das sie bei mir fallen):');
      moons.forEach(function(mo){
        data.push('- ' + mo.dateStr + ': ' + mo.kind + ' im Zeichen ' + mo.sign + (mo.house ? (', in meinem ' + mo.house + '. Haus') : ''));
      });
    }
    if(ruler.name){
      data.push('');
      data.push('MEIN CHARTRULER (Herrscher meines ' + ruler.acSign + '-Aszendenten): ' + ruler.name + (ruler.sign ? (' in ' + ruler.sign) : '') + (ruler.house ? (', ' + ruler.house + '. Haus') : ''));
    }
    if(TC.cusps && TC.cusps.length){
      data.push('');
      data.push('MEINE PLACIDUS-HÄUSERSPITZEN: ' + TC.cusps.map(function(c){ return c.id + '. Haus ' + c.sign; }).join(' · '));
    }
    data.push('');
    data.push('MEIN GEBURTSHOROSKOP (Placidus-Häuser):');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });

    const full = READING_INTRO + '\n\n' + numbered + '\n\n' + READING_OUTRO + '\n\n' + data.join('\n');
    const btn = document.getElementById('copyTimeBtn');
    const done = function(){ if(btn){ const o = btn.getAttribute('data-label') || btn.textContent; btn.setAttribute('data-label', o); btn.textContent = '✓ Kopiert! Jetzt in ChatGPT einfügen'; setTimeout(function(){ btn.textContent = o; }, 2800); } };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(full).then(done).catch(function(){ fallbackCopy(full, done); });
    } else { fallbackCopy(full, done); }
  };"""

pat = re.compile(r"  const BUSINESS_PROMPT = `.*?\n  window\.copyBusinessReading = function\(\)\{.*?\n  \};", re.DOTALL)
if not pat.search(s):
    sys.exit("FEHLT: BUSINESS_PROMPT / copyBusinessReading Region")
s = pat.sub(lambda _: new_region, s, count=1)

# --- 8. ASTROCODE-Design als Override-Layer (1:1 aus build_birthcode_reader.py)
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
