#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut den Saturn-Reader aus dem Business-Reader.
Muster: build_timecode_reader.py (ASTROCODE-Design, Tippfeld-Datum,
schlanke Ergebnis-Seite, kein E-Mail-Gate, komponierter Prompt).

DIE IDEE (Patrycja 24.07.2026): Saturn laeuft vom 26.07.2026 bis zum
11.12.2026 rueckläufig durch den Widder. Der Reader beantwortet die zwei
Fragen, die kein Kollektiv-Content beantworten kann: WO findet das in
meiner Chart statt und WANN genau.

Engine-verifizierte Fixpunkte (JSC-Scan 24.07.2026):
  - Station rueckläufig: 26.07.2026 bei 14°45' Widder
  - Station direkt:      11.12.2026 bei  7°56' Widder
  - Schatten-Ende:       15.03.2027 (Saturn wieder auf 14°45' Widder)
  - Korridor der Rueckläufigkeit: 7°56' bis 14°45' Widder (nur Widder,
    kein Rueckfall in die Fische)

DAS BESONDERE: die Drei-Passagen-Logik. Jeder natale Punkt, dessen
Aspekt-Grad im Korridor liegt, wird DREIMAL exakt getroffen: direkt
(das Thema zeigt sich), rueckläufig (die Nachpruefung), wieder direkt
(die Abnahme, bis Maerz 2027). Der Reader tastet Saturns Lauf vom
01.03.2026 bis 25.03.2027 in 3-Tages-Schritten ab (~130 Engine-Charts)
und interpoliert jede Passage auf den Tag genau.

Schichten in window.__saturnrx:
  - Korridor-Haeuser: durch welche natalen Placidus-Haeuser die Zone
    7°56'-14°45' Widder laeuft (houseOfLong, Segmente mit Grad-Grenzen)
  - Haus-Passagen: wann Saturn eine Hausspitze ueberquert (auch die
    rueckläufige Rueckkehr ins vorige Haus, mit Datum)
  - Drei-Passagen-Termine: Konjunktion/Sextil/Quadrat/Trigon/Opposition
    zu Sonne, Mond, Merkur, Venus, Mars, Jupiter, Saturn, AC, MC,
    Nordknoten + Chartruler (falls aeusserer Planet), mit Flags
    [CHARTRULER], [STATION] (Punkt nahe einem Stationsgrad, Saturn
    dreht praktisch auf ihm um), [SATURN-RETURN] (Konjunktion zum
    natalen Saturn)
  - Dauerhaft nah: Punkte knapp ausserhalb des Korridors (Orb <= 1,2°),
    die nie exakt werden, aber monatelang unter Druck stehen
  - nataler Saturn (Zeichen, Haus) + alle natalen Saturn-Aspekte

Der Prompt wird daraus KOMPONIERT (Muster Birthcode): Kapitel, die die
Chart nicht hergibt, tauchen gar nicht auf; ehrlicher Fallback, wenn
keine exakten Treffer da sind (dann traegt das Korridor-Haus).

Name: Arbeitstitel "Dein Saturn-Code" (NAME-Konstante unten).

Quelle:  astro-business-reader.html
Ziel:    astro-saturn-reader.html (+ astro-saturn-reader-netlify/index.html + ZIP)
"""
import os, re, sys, shutil, io, base64
from PIL import Image, ImageFilter, ImageChops

NAME = "Dein Saturn-Code"          # <- Reader-Name (Arbeitstitel, Patrycja entscheidet)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-saturn-reader.html")
NETLIFY = os.path.join(HERE, "astro-saturn-reader-netlify")
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
     '<p class="subtitle">Saturn läuft vom 26. Juli bis zum 11. Dezember 2026 rückläufig. Gib deine Geburtsdaten ein. Die Seite berechnet, in welchem Haus deiner Chart das stattfindet, welche deiner Punkte Saturn dabei trifft und wann jede seiner drei Passagen exakt ist, auf den Tag genau. Dazu alle Transite, die in diesen Monaten relevant werden und dein Saturn-Thema vertiefen. Daraus komponiert sie deinen individuellen KI-Prompt.</p>',
     "subtitle")

repl('onclick="runCheck()">Meinen Business-Code aufdecken</button>',
     'onclick="runCheck()">Meinen Saturn-Code berechnen</button>', "submit-btn")

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
     "<h2>" + NAME + "${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Saturn rückläufig: 26.07. bis 11.12.2026'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Neuen Saturn-Code erstellen", "back-btn")

# --- 4. Saturn-Rx-Scan in runCheck einhaengen -------------------------------
# Anker NACH window.__chart, damit __fullChart und __aspects bereits gesetzt sind.
calc_anchor = "      window.__chart = chart;\n      generateReading();"
scan_calc = r"""      window.__chart = chart;

      // Saturn-Code: Drei-Passagen-Scan der Rueckläufigkeit 2026.
      // Fixpunkte (engine-verifiziert): Station rx 26.07.2026 bei 14°45' Widder,
      // Station direkt 11.12.2026 bei 7°56' Widder, Schatten-Ende 15.03.2027.
      // Die Seite tastet Saturns Lauf vom 01.03.2026 bis 25.03.2027 in
      // 3-Tages-Schritten ab (Koordinaten Berlin nur fuer die Zeitzonen-
      // Aufloesung, die Planeten-Laengen sind ortsunabhaengig) und legt alle
      // Ergebnisse in window.__saturnrx ab. Der Prompt wird daraus komponiert.
      (function(){
        try{
          // SATURNRX-SCAN-START
          const lonOf = function(b){ try{ return b.ChartPosition.Ecliptic.DecimalDegrees; }catch(e){ return null; } };
          const SIGNS_DE = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische'];
          const wrap180 = function(x){ return ((x % 360) + 540) % 360 - 180; };
          const norm360 = function(x){ return ((x % 360) + 360) % 360; };
          const pad2 = function(n){ return (n < 10 ? '0' : '') + n; };
          const fmtDate = function(d){ return pad2(d.getDate()) + '.' + pad2(d.getMonth() + 1) + '.' + d.getFullYear(); };
          const fmtDeg = function(L){
            const Ln = norm360(L);
            const inSign = Ln % 30;
            let d = Math.floor(inSign);
            let m = Math.round((inSign - d) * 60);
            if(m === 60){ m = 0; d += 1; }
            return d + '°' + (m < 10 ? '0' : '') + m + "' " + (SIGNS_DE[Math.floor(Ln / 30)] || '');
          };

          // Korridor der Rueckläufigkeit (absolute ekliptikale Laengen im Widder)
          const RX_LO = 7 + 56/60;      // 7°56' Widder, Station direkt 11.12.2026
          const RX_HI = 14 + 45/60;     // 14°45' Widder, Station rx 26.07.2026
          const STATION_ORB = 1.0;      // Punkt so nah am Stationsgrad: Saturn dreht auf ihm um

          // Natale Haeuserspitzen + Placidus-Haus eines Grads
          // (houseOfLong-Muster der Reader-Familie)
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

          // Korridor-Segmente: durch welche natalen Haeuser laeuft die Zone
          const segments = [];
          (function(){
            let cur = null;
            for(let L = RX_LO; L <= RX_HI + 0.0001; L += 0.2){
              const Lc = Math.min(L, RX_HI);
              const hId = houseOfLong(Lc);
              if(!cur || cur.house !== hId){
                if(cur) segments.push(cur);
                cur = { house: hId, from: Lc, to: Lc };
              } else { cur.to = Lc; }
              if(Lc >= RX_HI) break;
            }
            if(cur) segments.push(cur);
          })();
          const segList = segments.map(function(sg){
            return { house: sg.house, fromStr: fmtDeg(sg.from), toStr: fmtDeg(sg.to) };
          });

          // Natale Ziel-Punkte fuer die Drei-Passagen-Termine
          const FULL = window.__fullChart || [];
          const SIGNOF = {}, HOUSEOF = {};
          FULL.forEach(function(e){ SIGNOF[e.label] = e.sign; HOUSEOF[e.label] = e.house; });
          const RULER = { 'Widder':'Mars','Stier':'Venus','Zwillinge':'Merkur','Krebs':'Mond','Löwe':'Sonne','Jungfrau':'Merkur','Waage':'Venus','Skorpion':'Pluto','Schütze':'Jupiter','Steinbock':'Saturn','Wassermann':'Uranus','Fische':'Neptun' };
          const CO_RULER = { 'Skorpion':'Mars', 'Wassermann':'Saturn', 'Fische':'Jupiter' };
          const acEntry = FULL.find(function(e){ return e.label === 'Aszendent'; }) || {};
          const rulerName = RULER[acEntry.sign || ''] || '';
          const saturnIsRuler = (rulerName === 'Saturn') || (acEntry.sign === 'Wassermann');

          // Herrscher der Korridor-Haeuser (modern + Mitherrscher): sie tragen
          // das Thema des Pruefungs-Hauses durch die Chart und werden eigene
          // Aspekt-Ziele fuer Saturn UND die Begleit-Transite.
          const HR_OF = {};       // Planet -> Liste der Korridor-Haeuser, die er regiert
          const houseRulers = []; // fuer Datenteil: {house, sign, ruler, coRuler}
          (function(){
            const seenH = {};
            segments.forEach(function(sg){
              if(!sg.house || seenH[sg.house]) return;
              seenH[sg.house] = 1;
              let cuspSign = '';
              for(let ci = 0; ci < cusps.length; ci++){
                if(cusps[ci].id === sg.house){ cuspSign = SIGNS_DE[Math.floor(norm360(cusps[ci].st) / 30)] || ''; break; }
              }
              const r = RULER[cuspSign] || '', co = CO_RULER[cuspSign] || '';
              if(r){ (HR_OF[r] = HR_OF[r] || []).push(sg.house); }
              if(co){ (HR_OF[co] = HR_OF[co] || []).push(sg.house); }
              houseRulers.push({ house: sg.house, sign: cuspSign, ruler: r, coRuler: co });
            });
          })();

          const targets = [
            ['Sonne', lonOf(CB.sun)], ['Mond', lonOf(CB.moon)], ['Merkur', lonOf(CB.mercury)],
            ['Venus', lonOf(CB.venus)], ['Mars', lonOf(CB.mars)], ['Jupiter', lonOf(CB.jupiter)],
            ['Saturn', lonOf(CB.saturn)], ['Aszendent', lonOf(horo.Ascendant)], ['MC', lonOf(horo.Midheaven)],
            ['Nordknoten', lonOf(CP.northnode)]
          ];
          const OUTER = { 'Uranus': CB.uranus, 'Neptun': CB.neptune, 'Pluto': CB.pluto };
          const hasTarget = function(n){ return targets.some(function(t){ return t[0] === n; }); };
          if(rulerName && OUTER[rulerName] && !hasTarget(rulerName)) targets.push([rulerName, lonOf(OUTER[rulerName])]);
          Object.keys(HR_OF).forEach(function(n){
            if(OUTER[n] && !hasTarget(n)) targets.push([n, lonOf(OUTER[n])]);
          });

          // Abtastung: Saturns Lauf 01.03.2026 bis 25.03.2027, alle 3 Tage, 12:00 Uhr
          const T0 = Date.UTC(2026, 2, 1, 12, 0);
          const DAYS = 389, STEP = 3;
          const samples = [];
          for(let i = 0; i <= DAYS; i += STEP){
            const d = new Date(T0 + i * 86400000);
            const o = new Origin({ year: d.getUTCFullYear(), month: d.getUTCMonth(), date: d.getUTCDate(), hour: 12, minute: 0, latitude: 52.52, longitude: 13.405 });
            const h = new Horoscope({ origin: o, houseSystem: 'placidus', zodiac: 'tropical', language: 'en', aspectTypes: ['major'] });
            const B = h.CelestialBodies;
            samples.push({ i: i, sat: lonOf(B.saturn),
              sun: lonOf(B.sun), moon: lonOf(B.moon), mercury: lonOf(B.mercury),
              mars: lonOf(B.mars), jupiter: lonOf(B.jupiter), uranus: lonOf(B.uranus),
              neptune: lonOf(B.neptune), pluto: lonOf(B.pluto), chiron: lonOf(B.chiron) });
          }
          const dayDate = function(dayF){ return new Date(T0 + dayF * 86400000); };
          const RX_START_DAY = (Date.UTC(2026, 6, 26, 12, 0) - T0) / 86400000;
          const RX_END_DAY = (Date.UTC(2026, 11, 11, 12, 0) - T0) / 86400000;

          // Alle Ueberquerungen eines Grads durch Saturn (bis zu 3 Passagen)
          const crossingsOf = function(deg){
            const out = [];
            for(let k = 0; k + 1 < samples.length; k++){
              const L1 = samples[k].sat, L2 = samples[k + 1].sat;
              if(L1 == null || L2 == null) continue;
              const g1 = wrap180(L1 - deg), g2 = wrap180(L2 - deg);
              if(Math.abs(g1) > 45 || Math.abs(g2) > 45) continue;
              if((g1 < 0) !== (g2 < 0)){
                const frac = Math.abs(g1) / ((Math.abs(g1) + Math.abs(g2)) || 1);
                const dayF = samples[k].i + frac * STEP;
                out.push({ day: dayF, dateStr: fmtDate(dayDate(dayF)), retro: (g2 - g1) < 0 });
              }
            }
            return out;
          };
          // Engster Abstand Saturns zu einem Grad (fuer Dauerhaft-nah-Punkte)
          const minOrbOf = function(deg){
            let mo = 999;
            for(let k = 0; k < samples.length; k++){
              if(samples[k].sat == null) continue;
              const g = Math.abs(wrap180(samples[k].sat - deg));
              if(g < mo) mo = g;
            }
            return mo;
          };

          const TYPES = [[0,'Konjunktion'],[60,'Sextil'],[90,'Quadrat'],[120,'Trigon'],[180,'Opposition']];
          const W_A = { 'Konjunktion':3, 'Opposition':2.5, 'Quadrat':2.5, 'Trigon':2, 'Sextil':1.5 };
          const W_T = { 'Aszendent':3, 'MC':3, 'Sonne':3, 'Mond':2.5, 'Nordknoten':3 };
          const NOM = { 'Sonne':'deine Sonne','Mond':'dein Mond','Merkur':'dein Merkur','Venus':'deine Venus','Mars':'dein Mars','Jupiter':'dein Jupiter','Saturn':'dein Saturn','Uranus':'dein Uranus','Neptun':'dein Neptun','Pluto':'dein Pluto','Aszendent':'dein Aszendent','MC':'dein MC','Nordknoten':'dein Nordknoten' };
          const DAT = { 'Sonne':'meiner Sonne','Mond':'meinem Mond','Merkur':'meinem Merkur','Venus':'meiner Venus','Mars':'meinem Mars','Jupiter':'meinem Jupiter','Saturn':'meinem Saturn','Uranus':'meinem Uranus','Neptun':'meinem Neptun','Pluto':'meinem Pluto','Aszendent':'meinem Aszendenten','MC':'meinem MC','Nordknoten':'meinem Nordknoten' };

          // Drei-Passagen-Termine + Dauerhaft-nah-Punkte
          const events = [], nearmiss = [];
          targets.forEach(function(tg){
            const nName = tg[0], nLon = tg[1];
            if(nLon == null) return;
            TYPES.forEach(function(ty){
              const A = ty[0], aName = ty[1];
              const offs = (A === 0 || A === 180) ? [A] : [A, -A];
              offs.forEach(function(off){
                const hitDeg = norm360(nLon + off);
                // Nur Grade im Widder interessieren (Korridor + naechste Umgebung)
                if(hitDeg > 40) return;
                const inCorridor = (hitDeg >= RX_LO && hitDeg <= RX_HI);
                if(inCorridor){
                  const cr = crossingsOf(hitDeg);
                  if(!cr.length) return;
                  const isRuler = (nName === rulerName);
                  const isHR = HR_OF[nName] || null;
                  const isReturn = (nName === 'Saturn' && aName === 'Konjunktion');
                  const stationRx = Math.abs(hitDeg - RX_HI) <= STATION_ORB;
                  const stationDir = Math.abs(hitDeg - RX_LO) <= STATION_ORB;
                  events.push({
                    target: nName, type: aName, hitDeg: hitDeg, degStr: fmtDeg(hitDeg),
                    tSign: SIGNOF[nName] || '', tHouse: HOUSEOF[nName] || '',
                    nom: NOM[nName] || nName, dat: DAT[nName] || nName,
                    passes: cr, ruler: isRuler, houseR: isHR, ret: isReturn,
                    station: stationRx ? 'rx' : (stationDir ? 'dir' : ''),
                    score: (W_A[aName] || 2) + (W_T[nName] || 2)
                         + ((stationRx || stationDir) ? 2.5 : 0)
                         + (isRuler ? 1.5 : 0) + (isHR ? 1.5 : 0) + (isReturn ? 2 : 0)
                  });
                } else if(hitDeg > RX_HI && hitDeg <= RX_HI + 1.2){
                  // Saturn kommt bis kurz vor den Punkt, dreht um, kommt wieder:
                  // monatelang nah, nie exakt
                  nearmiss.push({ target: nName, type: aName, dat: DAT[nName] || nName,
                    tSign: SIGNOF[nName] || '', tHouse: HOUSEOF[nName] || '',
                    minOrb: Math.round(minOrbOf(hitDeg) * 10) / 10 });
                }
              });
            });
          });
          // Chronologisch nach der Nachpruefungs-Passage (erste rueckläufige)
          const rxDayOf = function(ev){
            for(let i = 0; i < ev.passes.length; i++){ if(ev.passes[i].retro) return ev.passes[i].day; }
            return ev.passes.length ? ev.passes[0].day : 9999;
          };
          events.sort(function(a, b){ return rxDayOf(a) - rxDayOf(b); });
          const totalDates = events.reduce(function(n, ev){ return n + ev.passes.length; }, 0);
          const top = events.slice().sort(function(a, b){ return b.score - a.score; }).slice(0, 3);

          // Haus-Passagen Saturns im Scan-Fenster (auch die rueckläufige Rueckkehr)
          const ingress = [];
          for(let k = 0; k + 1 < samples.length; k++){
            const L1 = samples[k].sat, L2 = samples[k + 1].sat;
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
            ingress.push({ day: dayF, dateStr: fmtDate(dayDate(dayF)), from: h1, to: h2, retro: retro,
              inRx: (dayF >= RX_START_DAY && dayF <= RX_END_DAY) });
          }
          ingress.sort(function(a, b){ return a.day - b.day; });

          // --- Begleit-Transite im Rx-Fenster: exakte Termine
          // der anderen laufenden Planeten zu den natalen Punkten, 26.07.-11.12.
          const inWin = function(dayF){ return dayF >= RX_START_DAY && dayF <= RX_END_DAY; };
          const satTargets = {};
          events.forEach(function(ev){ satTargets[ev.target] = 1; });
          const TRANS2 = [['Mars','mars'],['Jupiter','jupiter'],['Uranus','uranus'],['Neptun','neptune'],['Pluto','pluto'],['Chiron','chiron']];
          const SLOWP = { 'Jupiter':1, 'Uranus':1, 'Neptun':1, 'Pluto':1, 'Chiron':1 };
          const W_P = { 'Pluto':5, 'Neptun':4.5, 'Uranus':4.5, 'Chiron':4, 'Jupiter':3.5, 'Mars':2 };
          const coHits = [], coStanding = [];
          TRANS2.forEach(function(tp){
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
                    if(!inWin(samples[k].i) && !inWin(samples[k + 1].i)) continue;
                    const g1 = wrap180(samples[k][key] - nLon - off);
                    const g2 = wrap180(samples[k + 1][key] - nLon - off);
                    if(Math.abs(g1) > 45 || Math.abs(g2) > 45) continue;
                    if(Math.abs(g1) < minOrb) minOrb = Math.abs(g1);
                    if(Math.abs(g2) < minOrb) minOrb = Math.abs(g2);
                    if((g1 < 0) !== (g2 < 0)){
                      const frac = Math.abs(g1) / ((Math.abs(g1) + Math.abs(g2)) || 1);
                      const dayF = samples[k].i + frac * STEP;
                      if(!inWin(dayF)) continue;
                      const isRuler = (nName === rulerName);
                      const isHR = HR_OF[nName] || null;
                      coHits.push({
                        day: dayF, dateStr: fmtDate(dayDate(dayF)),
                        p: pName, type: aName, target: nName,
                        tSign: SIGNOF[nName] || '', tHouse: HOUSEOF[nName] || '',
                        nom: NOM[nName] || nName, dat: DAT[nName] || nName,
                        ruler: isRuler, houseR: isHR, satTheme: !!satTargets[nName],
                        score: (W_P[pName] || 2) + (W_A[aName] || 2) + (W_T[nName] || 2) + (isRuler ? 1.5 : 0) + (isHR ? 1.5 : 0)
                      });
                      found = true;
                    }
                  }
                });
                if(!found && SLOWP[pName] && minOrb <= 1.2){
                  coStanding.push({ p: pName, type: aName, target: nName,
                    tSign: SIGNOF[nName] || '', tHouse: HOUSEOF[nName] || '',
                    dat: DAT[nName] || nName,
                    minOrb: Math.round(minOrb * 10) / 10, ruler: (nName === rulerName),
                    houseR: HR_OF[nName] || null, satTheme: !!satTargets[nName] });
                }
              });
            });
          });
          coHits.sort(function(a, b){ return a.day - b.day; });
          const coTop = coHits.slice().sort(function(a, b){ return b.score - a.score; }).slice(0, 2);

          // --- Zuendtage: Sonne und Mars aktivieren den laufenden Saturn ------
          const TRIG = [['Sonne','sun'],['Mars','mars']];
          const TRIG_TYPES = [[0,'Konjunktion'],[90,'Quadrat'],[120,'Trigon'],[180,'Opposition']];
          const triggers = [];
          TRIG.forEach(function(tp){
            const pName = tp[0], key = tp[1];
            TRIG_TYPES.forEach(function(ty){
              const A = ty[0], aName = ty[1];
              const offs = (A === 0 || A === 180) ? [A] : [A, -A];
              offs.forEach(function(off){
                for(let k = 0; k + 1 < samples.length; k++){
                  if(!inWin(samples[k].i) && !inWin(samples[k + 1].i)) continue;
                  const g1 = wrap180(samples[k][key] - samples[k].sat - off);
                  const g2 = wrap180(samples[k + 1][key] - samples[k + 1].sat - off);
                  if(Math.abs(g1) > 45 || Math.abs(g2) > 45) continue;
                  if((g1 < 0) !== (g2 < 0)){
                    const frac = Math.abs(g1) / ((Math.abs(g1) + Math.abs(g2)) || 1);
                    const dayF = samples[k].i + frac * STEP;
                    if(!inWin(dayF)) continue;
                    triggers.push({ day: dayF, dateStr: fmtDate(dayDate(dayF)), p: pName, type: aName });
                  }
                }
              });
            });
          });
          triggers.sort(function(a, b){ return a.day - b.day; });

          // --- Neumonde und Vollmonde im Rx-Fenster mit natalem Haus ----------
          const corridorHouses = {};
          segList.forEach(function(sg){ if(sg.house) corridorHouses[sg.house] = 1; });
          const moons = [];
          for(let k = 0; k + 1 < samples.length; k++){
            if(!inWin(samples[k].i) && !inWin(samples[k + 1].i)) continue;
            const s1 = samples[k].sun, s2 = samples[k + 1].sun;
            const e1 = norm360(samples[k].moon - s1);
            const e2 = norm360(samples[k + 1].moon - s2);
            const de = norm360(e2 - e1);
            const sunAt = function(frac){ return norm360(s1 + wrap180(s2 - s1) * frac); };
            if(e1 + de >= 360){
              const frac = (360 - e1) / (de || 1);
              const dayF = samples[k].i + frac * STEP;
              if(inWin(dayF)){
                const L = sunAt(frac);
                moons.push({ day: dayF, dateStr: fmtDate(dayDate(dayF)), kind: 'Neumond', lon: L, sign: SIGNS_DE[Math.floor(L / 30)], house: houseOfLong(L), satHouse: !!corridorHouses[houseOfLong(L)] });
              }
            } else if(e1 < 180 && e1 + de >= 180){
              const frac = (180 - e1) / (de || 1);
              const dayF = samples[k].i + frac * STEP;
              if(inWin(dayF)){
                const L = norm360(sunAt(frac) + 180);
                moons.push({ day: dayF, dateStr: fmtDate(dayDate(dayF)), kind: 'Vollmond', lon: L, sign: SIGNS_DE[Math.floor(L / 30)], house: houseOfLong(L), satHouse: !!corridorHouses[houseOfLong(L)] });
              }
            }
          }

          // --- Merkur-Rueckläufigkeits-Fenster im Rx-Zeitraum -----------------
          const mercLines = [];
          (function(){
            const v = [];
            for(let k = 0; k + 1 < samples.length; k++){
              v.push(wrap180(samples[k + 1].mercury - samples[k].mercury));
            }
            const stations = [];
            for(let k = 0; k + 1 < v.length; k++){
              if((v[k] < 0) !== (v[k + 1] < 0)){
                const frac = Math.abs(v[k]) / ((Math.abs(v[k]) + Math.abs(v[k + 1])) || 1);
                stations.push({ day: samples[k].i + STEP / 2 + frac * STEP, toRetro: v[k] >= 0 });
              }
            }
            let rx = v.length > 0 && v[0] < 0;
            let curStart = rx ? 0 : null;
            stations.forEach(function(st){
              if(st.toRetro && !rx){ rx = true; curStart = st.day; }
              else if(!st.toRetro && rx){
                rx = false;
                if(curStart != null && curStart <= RX_END_DAY && st.day >= RX_START_DAY){
                  mercLines.push('von ' + fmtDate(dayDate(curStart)) + ' bis ' + fmtDate(dayDate(st.day)));
                }
                curStart = null;
              }
            });
          })();

          // Nataler Saturn + seine Aspekte im Geburtshoroskop
          const satEntry = FULL.find(function(e){ return e.label === 'Saturn'; }) || {};
          const satAspects = (window.__aspects || []).filter(function(a){
            return a.p1 === 'Saturn' || a.p2 === 'Saturn';
          }).map(function(a){
            const other = (a.p1 === 'Saturn') ? a.p2 : a.p1;
            const oSign = (a.p1 === 'Saturn') ? a.s2 : a.s1;
            return { type: a.type, other: other, oSign: oSign || '' };
          });

          const rulerEntry = rulerName ? (FULL.find(function(e){ return e.label === rulerName; }) || {}) : {};

          window.__saturnrx = {
            stationRx: { dateStr: '26.07.2026', degStr: fmtDeg(RX_HI), house: houseOfLong(RX_HI) },
            stationDir: { dateStr: '11.12.2026', degStr: fmtDeg(RX_LO), house: houseOfLong(RX_LO) },
            shadowEndStr: '15.03.2027',
            segments: segList, ingress: ingress,
            events: events, top: top, totalDates: totalDates, nearmiss: nearmiss,
            coHits: coHits, coTop: coTop, coStanding: coStanding,
            triggers: triggers, moons: moons, mercLines: mercLines,
            houseRulers: houseRulers,
            natalSaturn: { sign: satEntry.sign || '', house: satEntry.house || '' },
            satAspects: satAspects,
            cusps: cusps.map(function(c){ return { id: c.id, sign: SIGNS_DE[Math.floor(norm360(c.st) / 30)] }; }),
            ruler: { name: rulerName, acSign: acEntry.sign || '', sign: rulerEntry.sign || '', house: rulerEntry.house || '', saturnRules: saturnIsRuler }
          };
          // SATURNRX-SCAN-END
        }catch(e){ window.__saturnrx = null; }
      })();

      generateReading();"""
repl(calc_anchor, scan_calc, "saturnrx-scan-injection")

# --- 4b. Ergebnis-Seite verschlanken (REGEL seit 14.07.): Platzierungen, ----
# Aspekte und Element-Block raus. Nur Saturn-Block + Prompt bleiben sichtbar.
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

# --- 5. Sichtbarer Saturn-Block + Prompt-CTA ---------------------------------
old_cta = """  html += `
  <div class="cta-block">
    <h3>Dein Business-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, wie du dein Business führst, wie du dich positionierst, wo deine Zone of Genius liegt und wie du am natürlichsten Geld verdienst.</p>
    <button class="copy-btn" id="copyBizBtn" onclick="copyBusinessReading()">Business-Prompt + Daten kopieren</button>
  </div>`;"""

new_cta = """  // Sichtbar: wo es stattfindet und die staerksten Termine (schlanke Ergebnis-Seite)
  const SR = window.__saturnrx || null;
  if(SR){
    let tHtml = `
    <div class="data-block">
      <h3>Dein Saturn-Code auf einen Blick</h3>
      <div class="data-grid">`;
    tHtml += `<div class="data-row"><span class="data-planet">Saturn rückläufig</span><span class="data-values"><span class="badge sign-badge">26.07. bis 11.12.2026</span></span></div>`;
    const segHouses = (SR.segments || []).map(function(sg){ return sg.house; }).filter(function(h){ return !!h; });
    if(segHouses.length){
      const uniq = segHouses.filter(function(h, i){ return segHouses.indexOf(h) === i; });
      tHtml += `<div class="data-row"><span class="data-planet">Wo es bei dir stattfindet</span><span class="data-values">${uniq.map(function(h){ return `<span class=\\"badge house-badge\\">dein ${h}. Haus</span>`; }).join('')}</span></div>`;
    }
    if(SR.totalDates > 0){
      tHtml += `<div class="data-row"><span class="data-planet">Deine Saturn-Termine</span><span class="data-values"><span class="badge sign-badge">${SR.totalDates} Termine auf den Tag genau</span></span></div>`;
    }
    (SR.top || []).forEach(function(ev){
      let label = 'Saturn ' + ev.type + ' ' + ev.nom;
      if(ev.ret) label += ' (dein Saturn-Return)';
      else if(ev.ruler) label += ' (dein Chartruler)';
      let when = '';
      for(let i = 0; i < ev.passes.length; i++){ if(ev.passes[i].retro){ when = ev.passes[i].dateStr; break; } }
      if(!when && ev.passes.length) when = ev.passes[0].dateStr;
      tHtml += `<div class="data-row"><span class="data-planet">${label}</span><span class="data-values"><span class="badge sign-badge">${ev.passes.length} Passagen</span><span class="badge house-badge">rückläufig exakt ${when}</span></span></div>`;
    });
    const stEv = (SR.events || []).find(function(ev){ return !!ev.station; });
    if(stEv){
      tHtml += `<div class="data-row"><span class="data-planet">Saturn dreht direkt auf einem deiner Punkte um</span><span class="data-values"><span class="badge sign-badge">${stEv.nom}</span></span></div>`;
    }
    if((SR.coHits || []).length){
      tHtml += `<div class="data-row"><span class="data-planet">Transite, die im Fenster dazukommen</span><span class="data-values"><span class="badge sign-badge">${SR.coHits.length} Termine auf den Tag genau</span></span></div>`;
    }
    (SR.coTop || []).forEach(function(ev){
      tHtml += `<div class="data-row"><span class="data-planet">${ev.p} ${ev.type} ${ev.nom}${ev.satTheme ? ' (vertieft dein Saturn-Thema)' : ''}</span><span class="data-values"><span class="badge sign-badge">${ev.dateStr}</span></span></div>`;
    });
    if((SR.triggers || []).length){
      tHtml += `<div class="data-row"><span class="data-planet">Zündtage deines Saturn-Themas</span><span class="data-values"><span class="badge sign-badge">${SR.triggers.length} Tage</span></span></div>`;
    }
    const nm2 = (SR.moons || []).find(function(mo){ return mo.satHouse; });
    if(nm2){
      tHtml += `<div class="data-row"><span class="data-planet">${nm2.kind} in deinem Saturn-Haus</span><span class="data-values"><span class="badge sign-badge">${nm2.dateStr}</span><span class="badge house-badge">dein ${nm2.house}. Haus</span></span></div>`;
    }
    tHtml += `<div class="data-row"><span class="data-planet">Nachprüfung abgeschlossen</span><span class="data-values"><span class="badge sign-badge">${SR.shadowEndStr}</span></span></div>`;
    tHtml += `</div></div>`;
    html += tHtml;
  }

  html += `
  <div class="cta-block">
    <h3>Dein Saturn-Reading mit KI</h3>
    <p>Dein Prompt wurde aus deiner Chart komponiert: das Haus, in dem Saturn bei dir rückläufig wird, deine Punkte mit allen drei Passagen, dazu die Transite, die in diesen Monaten dazukommen, deine Zündtage, deine Neumonde und Vollmonde. Alles auf den Tag genau. Kopiere ihn und füge ihn bei ChatGPT oder Claude ein. Du bekommst ein Reading wie von einer Astrologin, die deine Chart und den kompletten Himmel dieser Monate vor sich liegen hat.</p>
    <button class="copy-btn" id="copySatBtn" onclick="copySaturnReading()">Saturn-Prompt + Termine kopieren</button>
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
    <p class="cta-kicker">Dir gefallen die Antworten aus meinem Saturn-Code Reader?</p>
    <h3>Weißt du, dass du dank meines Astrocode-Portals dein ganzes Geburtshoroskop analysieren kannst! Tiefer als jedes Astroreading, denn erst die Bewegung bewirkt Veränderung! Wie oft hast du schon was über dich gehört, aber nicht umgesetzt!</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Öffne dein Astrocode-Portal und begib dich auf eine unvergessliche Reise zurück zu dir!</a>
  </div>`;''',
"astrocode-cta")

# --- 7. Prompt-Gehirn + Copy-Funktion austauschen --------------------------
# Der Prompt wird beim Kopieren aus dem Saturn-Scan komponiert:
# Kapitel, die die Chart nicht hergibt, tauchen gar nicht auf.
new_region = r"""  const READING_INTRO = `Du bist eine erfahrene Astrologin, die seit Jahrzehnten mit Transiten arbeitet und Saturn besonders liebt. Ich sitze dir gegenüber wie in einer persönlichen Sitzung. Schreib mir mein vollständiges Reading direkt in deiner ersten Antwort: keine Rückfragen, keine Vorrede, keine Wiederholung meiner Daten, kein Plan, was du gleich tun wirst. Du beginnst sofort mit Kapitel 1 und schreibst das Reading in einem Stück durch.

Im Zentrum steht ein Transit: Saturn läuft vom 26.07.2026 bis zum 11.12.2026 rückläufig, von 14 Grad 45 Widder zurück auf 7 Grad 56 Widder. Am 15.03.2027 hat er diese Strecke zum dritten Mal durchlaufen, dann ist die Nachprüfung abgeschlossen. Du liest aus meiner Chart, wo genau diese Rückläufigkeit bei mir stattfindet und was sie von mir will. Und du liest sie nicht isoliert: Unten stehen auch die anderen Transite, die in diesen Monaten bei mir relevant werden, mit exakten Terminen. Sie sind der Resonanzraum, in dem meine Saturn-Geschichte stattfindet. Du schreibst klar, tief und direkt, so dass mich jeder Satz trifft. Keine Floskeln, keine allgemeinen Astro-Sätze, kein Lehrbuchton.

Wichtig: Ich arbeite mit Placidus-Häusern. Alle Häuser in meinen Daten unten sind Placidus-Häuser. Alle Termine unten sind fertig berechnet. Du erfindest keine zusätzlichen Termine und verschiebst keine Daten: die Rechnung ist gemacht, du deutest.

So liest du meine Termine: Jeder Punkt, den Saturn in seiner Rückläufigkeits-Zone trifft, wird bis zu dreimal exakt berührt. Die erste Passage läuft direkt, da zeigt sich das Thema zum ersten Mal. Die zweite Passage läuft rückläufig, das ist die Nachprüfung: Saturn kommt zurück und schaut, ob das, was ich gebaut habe, wirklich trägt. Die dritte Passage läuft wieder direkt, das ist die Abnahme, da wird das Thema fest. Liegt die erste Passage in der Vergangenheit, dann hat sich das Thema schon gezeigt und ich erkenne es an dem, was seitdem passiert ist.

So gehst du mit der Menge um: Nicht jeder Termin unten verdient gleich viel Raum. Die Saturn-Kapitel sind die Tiefe, dort nimmst du dir Raum. In den Timeline-Kapiteln wählst du aus: Termine mit einem Zusatz in eckigen Klammern deutest du ausführlich, die übrigen bündelst du zu Phasen von wenigen Wochen mit je einem klaren Satz. Du musst nichts aufzählen, was keine Geschichte erzählt.

Mein Reading hat diese Kapitel:`;

  const READING_OUTRO = `Schreib auf Deutsch, in der Du-Form, in Tiefe statt in Breite. Jeder Satz konkret. Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker. Tiefe in den Saturn-Kapiteln, Auswahl in den Timeline-Kapiteln. Und noch einmal: Du beginnst deine Antwort direkt mit Kapitel 1 und schreibst das Reading in einem Stück.

Hier sind meine Daten:`;

  window.copySaturnReading = function(){
    const FULL = window.__fullChart || [];
    const SR = window.__saturnrx || {};
    const m = window.__meta || {};
    const events = SR.events || [], nearmiss = SR.nearmiss || [], ingress = SR.ingress || [];
    const segments = SR.segments || [], satAspects = SR.satAspects || [];
    const ruler = SR.ruler || {}, natalSaturn = SR.natalSaturn || {};
    const coHits = SR.coHits || [], coStanding = SR.coStanding || [];
    const triggers = SR.triggers || [], moons = SR.moons || [], mercLines = SR.mercLines || [];
    const houseRulers = SR.houseRulers || [];
    const rulerHit = events.some(function(e){ return e.ruler; }) || coHits.some(function(h){ return h.ruler; }) || coStanding.some(function(h){ return h.ruler; });
    const hrHit = events.some(function(e){ return e.houseR; }) || coHits.some(function(h){ return h.houseR; }) || coStanding.some(function(h){ return h.houseR; });
    const stationEvents = events.filter(function(ev){ return !!ev.station; });
    const returnEvents = events.filter(function(ev){ return ev.ret; });
    const segHouses = segments.map(function(sg){ return sg.house; }).filter(function(h){ return !!h; });
    const uniqHouses = segHouses.filter(function(h, i){ return segHouses.indexOf(h) === i; });

    // --- Kapitel komponieren: nur was diese Chart wirklich hat --------------
    const steps = [];

    steps.push('Mein Saturn-Fundament. Wirf zuerst einen Blick auf meinen natalen Saturn unten: sein Zeichen, sein Haus und seine Aspekte in meinem Geburtshoroskop. Beschreib, wie ich mit Saturn verdrahtet bin: wie ich Verantwortung trage, wo ich Struktur liebe oder fürchte, wie ich mit Grenzen, Pflicht und Reife umgehe. Das ist die Grundlage, auf der diese Rückläufigkeit bei mir arbeitet.');

    if(ruler.saturnRules){
      steps.push('Saturn führt meine Chart. Saturn ist der Herrscher meines ' + (ruler.acSign || '') + '-Aszendenten und damit mein Chartruler. Wenn mein Chartruler rückläufig wird, geht es nie nur um einen Lebensbereich, es geht um meine Selbstführung. Sag mir, was das heißt: was in diesen Monaten an meiner Art, mich selbst zu führen, nachgeprüft wird, und woran ich merke, dass ich es ernst nehme.');
    }

    if(uniqHouses.length){
      steps.push('Der Raum der Nachprüfung. Unten steht, durch welches Haus meiner Chart Saturn rückläufig läuft' + (uniqHouses.length > 1 ? ' und wo er dabei die Hausgrenze überquert' : '') + '. Das ist der Lebensbereich, in dem seit dem Frühjahr 2026 gebaut wird und in dem jetzt geprüft wird, was davon trägt. Beschreib diesen Raum konkret: was dort in meinem Leben verhandelt wird, was Saturn dort seit Monaten aufbaut und welche Frage er mir in der Rückläufigkeit stellt.');
    }

    if(houseRulers.length){
      steps.push('Die Herrscher. Unten stehen mein Chartruler (der Herrscher meines Aszendenten) und der Herrscher meines Saturn-Hauses' + (houseRulers.some(function(hr){ return hr.coRuler; }) ? ' samt Mitherrscher' : '') + ', jeweils mit ihrer Stellung in meiner Chart. Der Herrscher meines Saturn-Hauses trägt das Thema der Prüfung dorthin, wo er bei mir steht: Deute zuerst, was seine natale Stellung darüber erzählt, wie ich diesen Lebensbereich führe und wo seine Prüfung sich noch bemerkbar macht.' + (rulerHit || hrHit ? ' Danach geh die Termine mit dem Zusatz CHARTRULER oder HERRSCHER MEINES SATURN-HAUSES durch: an diesen Tagen wird das Thema über die Herrscher zusätzlich aktiviert, auch wenn Saturn selbst gerade woanders arbeitet.' : ''));
    }

    if(events.length){
      steps.push('Meine Drei-Passagen-Termine. Unten stehen die Punkte meiner Chart, die Saturn in dieser Rückläufigkeit exakt trifft, jeder mit seinen Passagen und Daten. Geh sie einzeln durch. Für jeden Punkt: was die erste Passage schon gezeigt hat, was die Nachprüfung jetzt von mir will und was bei der Abnahme fest wird. Mach es konkret: welche Entscheidung, welches Verhalten, welche Struktur. Termine mit dem Zusatz CHARTRULER oder STATION oder SATURN-RETURN wiegen am schwersten.');
    }

    if(stationEvents.length){
      steps.push('Saturn dreht auf meinem Punkt um. Bei mir liegt ein Punkt so nah an einem Stationsgrad, dass Saturn praktisch auf ihm anhält und umdreht. Ein stehender Saturn wirkt wochenlang mit voller Kraft auf dieselbe Stelle. Sag mir, was dieser Punkt in meinem Leben ist und wie ich diese Wochen bewusst nutze, statt sie auszusitzen.');
    }

    if(returnEvents.length){
      steps.push('Mein Saturn-Return. Saturn läuft in dieser Phase über meinen natalen Saturn. Das ist mein Saturn-Return, die Reifeprüfung, die nur alle 29 Jahre kommt, und durch die Rückläufigkeit besteht sie aus mehreren Passagen. Sag mir, was in meinem Leben damit abgeschlossen und neu unterschrieben wird.');
    }

    if(nearmiss.length){
      steps.push('Was dauerhaft nah bleibt. Einige meiner Punkte erreicht Saturn in dieser Phase fast, ohne je exakt zu werden. Sie stehen unten mit dem engsten Abstand. Lies sie als Dauerton: kein Termin, eher ein Druck, der über Monate anhält und mich an dieser Stelle ehrlich macht.');
    }

    if(!events.length){
      steps.push('Meine Chart bleibt bei den exakten Terminen still. Saturn trifft in dieser Rückläufigkeit keinen meiner Punkte exakt. Sag mir das ehrlich: diese Phase arbeitet bei mir leiser als bei anderen, und ihre Arbeit läuft komplett über den Raum aus dem Kapitel davor. Kein künstliches Drama, dafür umso genauer: was in diesem einen Lebensbereich zwischen dem 26.07. und dem 11.12.2026 reif wird.');
    }

    if(coHits.length || coStanding.length){
      steps.push('Was gleichzeitig läuft. Saturn arbeitet in diesen Monaten nicht allein. Unten steht meine Begleit-Timeline: die anderen laufenden Planeten mit den exakten Terminen, an denen sie meine Punkte treffen, dazu die Dauer-Transite, die das ganze Fenster eng stehen. Wähle daraus die Termine mit dem Zusatz VERTIEFT DEIN SATURN-THEMA und die drei stärksten weiteren und deute sie IM ZUSAMMENSPIEL mit meiner Saturn-Nachprüfung: Jupiter öffnet, wo Saturn prüft, Mars gibt Tempo und Reibung, Uranus bringt Umbrüche, Neptun macht durchlässig, Pluto wandelt, Chiron macht empfindlich. Alle übrigen Termine bündelst du zu Phasen von wenigen Wochen, je ein Satz pro Phase. Die VERTIEFT-Termine sind meine wichtigsten Wochen: dort verdichtet sich meine Geschichte.');
    }

    if(triggers.length){
      steps.push('Meine Zündtage. Unten stehen die Tage, an denen die Sonne oder Mars den rückläufigen Saturn selbst aktivieren. An diesen Tagen feuert mein Saturn-Thema im Alltag: es kommt eine Situation, eine Nachricht, eine Entscheidung, die genau in mein Saturn-Haus fällt. Fasse dieses Kapitel kompakt: je Zündtag zwei bis drei Sätze, woran ich ihn erkenne und wie ich ihn bewusst nutze statt nur zu reagieren.');
    }

    if(mercLines.length){
      steps.push('Merkur rückläufig in dieser Phase. Unten steht, wann Merkur innerhalb meines Saturn-Fensters rückläufig läuft. In diesen Wochen prüft die Kommunikation gleich mit: Verträge, Absprachen, Technik. Sag mir, was das zusammen mit meiner Saturn-Nachprüfung heißt und was ich in diesen Wochen bewusst anders mache.');
    }

    if(moons.length){
      steps.push('Meine Neumonde und Vollmonde im Fenster. Jeder Neumond ist ein Startpunkt, jeder Vollmond eine Ernte oder ein Abschluss. Unten stehen sie mit Datum und dem Haus, in das sie bei mir fallen. Ausführlich deutest du nur die mit dem Zusatz IM SATURN-HAUS: sie setzen ihren Impuls genau in den Raum der Nachprüfung. Die übrigen Monde bekommen je einen Satz: was ich an diesem Termin am besten beginne oder abschließe.');
    }

    steps.push('Schatten und Geschenk. Saturn rückläufig hat einen Schatten: Härte gegen mich selbst, Aufschieben aus Angst vor der Prüfung, Festhalten an Strukturen, die längst nicht mehr tragen. Und er hat ein Geschenk: Fundamente, die nach dieser Phase wirklich halten. Sag mir, wie beides bei mir konkret aussieht, bezogen auf mein Haus und meine Termine.');

    steps.push('Der rote Faden. Erzähl mir die eine Geschichte dieser Rückläufigkeit: welches Fundament in meinem Leben bis zum 11.12.2026 nachgeprüft wird und was am 15.03.2027, wenn die dritte Passage durch ist, bei mir stehen darf. Formuliere daraus einen Satz in der Ich-Form, den ich mir aufschreiben kann. Danach gib mir drei konkrete Schritte' + (events.length ? ', jeder an einen Termin aus meinen Daten gebunden, mit Datum.' : ': einen für den Start am 26.07.2026, einen für die Wochen um die Station am 11.12.2026 und einen für den Abschluss bis zum 15.03.2027.'));

    steps.push('Meine Frage. Stell mir am Ende eine einzige, konfrontierende Frage zu dem Muster, mit dem ich mich um Saturns Nachprüfung am liebsten herumdrücken würde. Danach biete mir drei Richtungen an, in die wir das Reading vertiefen können, und frag mich, welche ich wählen will.');

    const numbered = steps.map(function(t, i){ return (i + 1) + '. ' + t; }).join('\n\n');

    // --- Datenteil ----------------------------------------------------------
    const data = [];
    if(m.name) data.push('Name: ' + m.name);
    if(m.date){ const dp = m.date.split('-'); data.push('Geburtsdatum: ' + dp[2]+'.'+dp[1]+'.'+dp[0] + (m.time ? (' um ' + m.time + ' Uhr') : '')); }
    if(m.place) data.push('Geburtsort: ' + m.place);
    data.push('');
    data.push('SATURN RÜCKLÄUFIG 2026 (fertig berechnet):');
    data.push('- Station rückläufig: 26.07.2026 bei ' + ((SR.stationRx || {}).degStr || "14°45' Widder"));
    data.push('- Station direkt: 11.12.2026 bei ' + ((SR.stationDir || {}).degStr || "7°56' Widder"));
    data.push('- Dritte Passage abgeschlossen: 15.03.2027');
    if(segments.length){
      data.push('');
      data.push('WO ES BEI MIR STATTFINDET (Rückläufigkeits-Zone in meinen Placidus-Häusern):');
      segments.forEach(function(sg){
        data.push('- Von ' + sg.fromStr + ' bis ' + sg.toStr + ': mein ' + sg.house + '. Haus');
      });
    }
    if(ingress.length){
      data.push('');
      data.push('SATURN UND MEINE HÄUSER (Übertritte mit Datum):');
      ingress.forEach(function(g){
        data.push('- ' + g.dateStr + ': Saturn ' + (g.retro ? ('zieht sich rückläufig aus meinem ' + g.from + '. Haus in mein ' + g.to + '. Haus zurück') : ('wechselt aus meinem ' + g.from + '. Haus in mein ' + g.to + '. Haus')));
      });
    }
    if(events.length){
      data.push('');
      data.push('MEINE DREI-PASSAGEN-TERMINE (jeder Punkt mit allen exakten Daten):');
      events.forEach(function(ev){
        const flags = (ev.ruler ? ' [CHARTRULER]' : '') + (ev.houseR ? ' [HERRSCHER MEINES SATURN-HAUSES]' : '') + (ev.station ? ' [STATION]' : '') + (ev.ret ? ' [SATURN-RETURN]' : '');
        const ctx = ev.target + ' in ' + ev.tSign + (ev.tHouse ? (', mein ' + ev.tHouse + '. Haus') : '');
        const pass = ev.passes.map(function(p, i){
          return (i + 1) + '. Passage ' + (p.retro ? 'rückläufig' : 'direkt') + ' am ' + p.dateStr;
        }).join(' · ');
        data.push('- Saturn ' + ev.type + ' zu ' + ev.dat + ' (' + ctx + ')' + flags + ': ' + pass);
      });
    }
    if(nearmiss.length){
      data.push('');
      data.push('DAUERHAFT NAH, NIE EXAKT (Dauerton dieser Monate):');
      nearmiss.forEach(function(nm){
        data.push('- Saturn ' + nm.type + ' zu ' + nm.dat + ' (' + nm.target + ' in ' + nm.tSign + (nm.tHouse ? (', mein ' + nm.tHouse + '. Haus') : '') + '), engster Abstand ' + String(nm.minOrb).replace('.', ',') + '°');
      });
    }
    if(coHits.length){
      data.push('');
      data.push('MEINE BEGLEIT-TIMELINE 26.07. BIS 11.12.2026 (chronologisch, jeweils der Tag, an dem der Aspekt exakt ist):');
      coHits.forEach(function(h){
        const ctx = h.target + ' in ' + h.tSign + (h.tHouse ? (', mein ' + h.tHouse + '. Haus') : '');
        data.push('- ' + h.dateStr + ': Transit-' + h.p + ' ' + h.type + ' zu ' + h.dat + ' (' + ctx + ')' + (h.ruler ? ' [CHARTRULER]' : '') + (h.houseR ? ' [HERRSCHER MEINES SATURN-HAUSES]' : '') + (h.satTheme ? ' [VERTIEFT DEIN SATURN-THEMA]' : ''));
      });
    }
    if(coStanding.length){
      data.push('');
      data.push('DAUERHAFT WIRKSAM IM GANZEN FENSTER (eng im Orb, wird nicht exakt):');
      coStanding.forEach(function(st){
        data.push('- Transit-' + st.p + ' ' + st.type + ' zu ' + st.dat + ' (' + st.target + ' in ' + st.tSign + (st.tHouse ? (', mein ' + st.tHouse + '. Haus') : '') + '), engster Orb ' + String(st.minOrb).replace('.', ',') + '°' + (st.ruler ? ' [CHARTRULER]' : '') + (st.houseR ? ' [HERRSCHER MEINES SATURN-HAUSES]' : '') + (st.satTheme ? ' [VERTIEFT DEIN SATURN-THEMA]' : ''));
      });
    }
    if(triggers.length){
      data.push('');
      data.push('MEINE ZÜNDTAGE (Sonne oder Mars aktivieren den rückläufigen Saturn):');
      triggers.forEach(function(t){
        data.push('- ' + t.dateStr + ': ' + t.p + ' ' + t.type + ' zum laufenden Saturn');
      });
    }
    if(mercLines.length){
      data.push('');
      data.push('MERKUR RÜCKLÄUFIG IN MEINEM FENSTER:');
      mercLines.forEach(function(ln){ data.push('- Merkur rückläufig ' + ln); });
    }
    if(moons.length){
      data.push('');
      data.push('MEINE NEUMONDE UND VOLLMONDE IM FENSTER (mit dem Haus, in das sie bei mir fallen):');
      moons.forEach(function(mo){
        data.push('- ' + mo.dateStr + ': ' + mo.kind + ' im Zeichen ' + mo.sign + (mo.house ? (', in meinem ' + mo.house + '. Haus') : '') + (mo.satHouse ? ' [IM SATURN-HAUS]' : ''));
      });
    }
    data.push('');
    data.push('MEIN NATALER SATURN: ' + (natalSaturn.sign ? ('Saturn in ' + natalSaturn.sign) : 'Saturn') + (natalSaturn.house ? (', mein ' + natalSaturn.house + '. Haus') : ''));
    if(satAspects.length){
      data.push('SEINE ASPEKTE IN MEINEM GEBURTSHOROSKOP: ' + satAspects.map(function(a){ return a.type + ' zu ' + a.other + (a.oSign ? (' in ' + a.oSign) : ''); }).join(' · '));
    }
    if(ruler.name){
      data.push('');
      data.push('MEIN CHARTRULER (Herrscher meines ' + ruler.acSign + '-Aszendenten): ' + ruler.name + (ruler.sign ? (' in ' + ruler.sign) : '') + (ruler.house ? (', ' + ruler.house + '. Haus') : '') + (ruler.saturnRules ? ' >> Saturn führt meine Chart, diese Rückläufigkeit ist mein persönlichster Transit des Jahres.' : ''));
    }
    if(houseRulers.length){
      const posOf = function(n){
        const e = FULL.find(function(x){ return x.label === n; }) || {};
        return n + (e.sign ? (' in ' + e.sign) : '') + (e.house ? (', ' + e.house + '. Haus') : '');
      };
      houseRulers.forEach(function(hr){
        if(!hr.ruler) return;
        let line = 'HERRSCHER MEINES SATURN-HAUSES (' + hr.house + '. Haus, Spitze ' + hr.sign + '): ' + posOf(hr.ruler);
        if(hr.coRuler) line += ' · Mitherrscher: ' + posOf(hr.coRuler);
        data.push(line);
      });
    }
    if(SR.cusps && SR.cusps.length){
      data.push('');
      data.push('MEINE PLACIDUS-HÄUSERSPITZEN: ' + SR.cusps.map(function(c){ return c.id + '. Haus ' + c.sign; }).join(' · '));
    }
    data.push('');
    data.push('MEIN GEBURTSHOROSKOP (Placidus-Häuser):');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });

    const full = READING_INTRO + '\n\n' + numbered + '\n\n' + READING_OUTRO + '\n\n' + data.join('\n');
    const btn = document.getElementById('copySatBtn');
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

# Sicherheitscheck: keine Business-, Womancode- oder Timecode-Reste in Logik-Hooks
for leftover in ["copyBusinessReading", "copyBizBtn", "BUSINESS_PROMPT", "subscribeLead", "userEmail", "Business-Code", "Business-Blueprint", "wc-logo", "Womancode", "womancode", "Timecode", "timecode", "__timecode"]:
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
