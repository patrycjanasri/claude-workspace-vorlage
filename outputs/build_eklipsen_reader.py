#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut den Eklipsen-Reader "Dein Eklipsen-Code" aus dem Business-Reader.
Muster: build_barbault_reader.py (fester Transit-Moment, ASTROCODE-Design,
schlanke Ergebnis-Seite, Tippfeld-Datum, kein E-Mail-Gate) + Prompt-
Komposition nach Birthcode-Muster (Kapitel nur, wenn die Chart sie hergibt).

Der Reader rechnet DREI Charts mit derselben Engine:
  1. das Geburtshoroskop der Nutzerin (PLACIDUS)
  2. die Sonnenfinsternis: 12.08.2026, 19:38 Uhr MESZ (Neumond exakt,
     engine-verifiziert: Sonne + Mond 20°02' Loewe; real total in Spanien)
  3. die Mondfinsternis: 28.08.2026, 06:20 Uhr MESZ (Vollmond exakt,
     engine-verifiziert: Mond 4°54' Fische, Sonne 4°54' Jungfrau,
     Mond 5,4° von der Knotenachse)

Der Reader zieht automatisch (window.__eclipse):
  - Placidus-Haus der SoFi (wo etwas Neues beginnt)
  - MoFi als ACHSE: Haus des Mondes + Haus der Sonne gegenueber
  - Aspekte beider Finsternis-Punkte zu den natalen Punkten (Orb 3 Grad),
    Treffer auf den Chartruler mit CHARTRULER-Flag (inkl. Mitherrscher)
  - Knotenachse zur Finsternis-Zeit (beide Momente; wechselt dazwischen
    das Zeichen, sagt der Prompt das dazu) + natale Haeuser beider Enden
  - natale Mondknoten (Seelenweg), natale Sonne + nataler Mond (die Lichter)
und KOMPONIERT daraus einen KI-Prompt: Kapitel dynamisch nummeriert,
Treffer-Kapitel nur wenn Treffer da sind, Chartruler-Kapitel nur bei
Chartruler-Treffer. Fenster-Fokus: August 2026 bis Anfang 2027.

Kontext: Reader fuer den Astrologin-Deal (8.888 Euro) — gebaut im
ASTROCODE-Design als Arbeitsstand; ihr Branding kommt spaeter von
Patricia (Tausch ueber diesen Generator).

Quelle:  astro-business-reader.html
Ziel:    astro-eklipsen-reader.html (+ astro-eklipsen-reader-netlify/index.html)
"""
import os, re, sys, shutil, base64

NAME = "Dein Eclipse Navigator"      # Bernadettes Favorit (24.07.); final wenn sie ihn bestaetigt

# Bernadette Hirschfelder — lieblingsastrologin.de (Deal fix 24.07.2026)
IMPRESSUM_URL = "https://lieblingsastrologin.de/impressum/"
DATENSCHUTZ_URL = "https://lieblingsastrologin.de/datenschutzerklaerung/"

# Branding: OFFIZIELLE Hexcodes von Bernadette (24.07.) + Look aus ihrem
# Eclipse Guide PDF (fette schwarze Anton-Headlines, Great-Vibes-Script,
# "ECLIPSE SEASON"-Tape-Baender, Du/Dich GROSS).
C_ROSA = "#FFD1DC"       # Blush Pink (Grundflaeche)
C_CREAM = "#F7F1E6"      # Cream (Kaesten, aus dem PDF)
C_PEACH = "#FEC89A"      # Soft Apricot (Tape, Haus-Badges)
C_FLIEDER = "#E0B0FF"    # Light Lavender (Zeichen-Badges)
C_INK = "#111111"        # Headlines, Buttons, Tape

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-eklipsen-reader.html")
NETLIFY = os.path.join(HERE, "astro-eklipsen-reader-netlify")

def b64file(path):
    with open(path, "rb") as fh:
        return base64.b64encode(fh.read()).decode()

FONT_ANTON = b64file(os.path.join(HERE, "bernadette-anton.woff2"))
FONT_SCRIPT = b64file(os.path.join(HERE, "bernadette-greatvibes.woff2"))

# Bernadettes Foto (outputs/bernadette-hero.jpg) wird NICHT mehr im Kopf
# verbaut (ihre Ansage 25.07.: Schrift hoch, schnell zum Eingabefeld).
# Das Foto bleibt gesichert, falls es spaeter z.B. ans Seitenende soll.

# WAHRER Mondknoten (Bernadettes Vorgabe 25.07.: "er muss den wahren Mond-
# knoten als Berechnungsgrundlage nehmen"): Die Engine kann nur den mittleren
# (meanAscendingNode). Daher eingebettete Ephemeride aus Swiss Ephemeris
# (build_true_node_data.py, 1900-2036, 1-Tages-Schritt, max. Fehler 0,6').
with open(os.path.join(HERE, "true-node-data.js"), "r", encoding="utf-8") as f:
    TRUE_NODE_DATA_JS = f.read()

# --- Finsternis-Momente (lokale Zeit, Engine loest Zeitzone ueber Koordinaten)
# Bernadettes Regel (24.07.): "Wir rechnen immer mit den Eclipsegraden" =
# MONDPOSITION am Finsternis-MAXIMUM (nicht der exakte Neumond/Vollmond).
# Maxima: SoFi 12.08. 17:46 UT = 19:46 MESZ -> Mond 20°06' Loewe (= ihr Guide),
#         MoFi 28.08. 04:13 UT = 06:13 MESZ -> Mond 4°50' Fische (= ihr Guide).
S_YEAR, S_MONTH, S_DATE, S_HOUR, S_MINUTE = 2026, 8, 12, 19, 45   # SoFi-Maximum
M_YEAR, M_MONTH, M_DATE, M_HOUR, M_MINUTE = 2026, 8, 28, 6, 12    # MoFi-Maximum
T_LAT, T_LON = 52.52, 13.405                                       # Berlin (Zeitzone)

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
     '<p class="header-eyebrow">Eclipse Season incoming</p>', "eyebrow-bernadette")

repl("<h1>Dein Business-Code</h1>",
     "<h1>" + NAME + "</h1>", "h1")

repl('<p class="subtitle">Gib deine Geburtsdaten ein. Auf der nächsten Seite bekommst du dein Geburtshoroskop angezeigt und einen fertigen KI-Prompt, der dir sagt, wie du dein Business führst, dich positionierst, skalierst und Geld verdienst.</p>',
     '<p class="subtitle">Im August 2026 ist Eclipse Season: eine totale Sonnenfinsternis in Löwe am 12. August und eine partielle Mondfinsternis in Fische am 28. August. Welche Lebensbereiche die beiden bei Dir aktivieren, verrät Dein Geburtshoroskop. Gib Deine Geburtsdaten ein: Das Tool berechnet Deine Radix, findet Deine Häuser und Häuserherrscher und erstellt Dir einen fertigen KI-Prompt für Dein persönliches Eclipse-Reading.</p>',
     "subtitle")

repl('onclick="runCheck()">Meinen Business-Code aufdecken</button>',
     'onclick="runCheck()">Meinen Eclipse-Prompt erstellen</button>', "submit-btn")

repl('''<div class="tip-box">
    <p><strong>Gib deine Geburtsdaten ein.</strong></p>
  </div>''', '', "tip-box-remove")

# Formular-Anrede in Bernadettes Schreibweise (Du gross)
repl('placeholder="Wie heißt du?"', 'placeholder="Wie heißt Du?"', "name-placeholder-du")

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

# --- 2. Geburtsdatum als Tippfeld TT.MM.JJJJ -------------------------------
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
     "if(!date){ return fail('Bitte gib Dein Geburtsdatum als TT.MM.JJJJ ein, zum Beispiel 08.10.1986.'); }",
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
     "<h2>Deine Eclipse Season${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Sonnenfinsternis und Mondfinsternis im August 2026'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Neues Horoskop berechnen", "back-btn")

# --- 3a. Basis-CSS: Mond-Bild-URL von Patrycjas Page raus (ihr Produkt) -----
repl('background:url("https://patrycja-nasri.de/wp-content/uploads/2026/06/WEB-ASTRO3.png") center top / cover no-repeat;',
     'background:none;', "moon-url-remove")

# --- 3b. Footer: Impressum/Datenschutz der Astrologin (nicht Patrycjas) -----
repl('<a href="https://patrycja-nasri.de/impressum/" target="_blank" rel="noopener">Impressum</a>',
     '<a href="' + IMPRESSUM_URL + '" target="_blank" rel="noopener">Impressum</a>', "impressum-link")
repl('<a href="https://patrycja-nasri.de/datenschutz/" target="_blank" rel="noopener">Datenschutz</a>',
     '<a href="' + DATENSCHUTZ_URL + '" target="_blank" rel="noopener">Datenschutz</a>', "datenschutz-link")

# --- 3c. Wahrer-Knoten-Ephemeride als eigenes Skript nach der Engine --------
repl('<script src="https://cdn.jsdelivr.net/npm/circular-natal-horoscope-js@1.1.0/dist/index.js"></script>',
     '<script src="https://cdn.jsdelivr.net/npm/circular-natal-horoscope-js@1.1.0/dist/index.js"></script>\n<script>\n' + TRUE_NODE_DATA_JS + '''
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

# --- 4. Eklipsen-Berechnung in runCheck einhaengen --------------------------
calc_anchor = "      window.__chart = chart;\n      generateReading();"
transit_calc = """      window.__chart = chart;

      // Eklipsen: zwei Finsternis-Momente als eigene Charts rechnen.
      // Ort Berlin, weil die Planeten-Laengen ortsunabhaengig sind; die
      // Engine braucht die Koordinaten nur fuer die Zeitzone (MESZ).
      (function(){
        try{
          const mkChart = function(y, mo0, d, h, mi){
            const o = new Origin({ year: y, month: mo0, date: d, hour: h, minute: mi, latitude: __T_LAT__, longitude: __T_LON__ });
            return { horo: new Horoscope({ origin: o, houseSystem: 'placidus', zodiac: 'tropical', language: 'en', aspectTypes: [] }), jd: o.julianDate };
          };
          const sofiC = mkChart(__S_YEAR__, __S_MONTH0__, __S_DATE__, __S_HOUR__, __S_MINUTE__);
          const mofiC = mkChart(__M_YEAR__, __M_MONTH0__, __M_DATE__, __M_HOUR__, __M_MINUTE__);
          const sofi = sofiC.horo, mofi = mofiC.horo;
          const lonOf = function(b){ try{ return b.ChartPosition.Ecliptic.DecimalDegrees; }catch(e){ return null; } };

          // Eclipsegrad = MOND am Finsternis-Maximum (Bernadettes Regel)
          const sofiLon = lonOf(sofi.CelestialBodies.moon);
          const mofiMoonLon = lonOf(mofi.CelestialBodies.moon);
          const mofiSunLon = lonOf(mofi.CelestialBodies.sun);
          // WAHRER Knoten (Bernadettes Vorgabe) aus der eingebetteten Swiss-
          // Ephemeris-Reihe; Fallback mittlerer Knoten, falls ausserhalb.
          const nnSofiLon = (typeof trueNodeLon === 'function' ? trueNodeLon(sofiC.jd) : null) != null
            ? trueNodeLon(sofiC.jd) : lonOf(sofi.CelestialPoints.northnode);
          const nnMofiLon = (typeof trueNodeLon === 'function' ? trueNodeLon(mofiC.jd) : null) != null
            ? trueNodeLon(mofiC.jd) : lonOf(mofi.CelestialPoints.northnode);
          if([sofiLon, mofiMoonLon, mofiSunLon, nnSofiLon, nnMofiLon].some(function(v){ return v == null; })) return;

          const SIGNS_DE = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische'];
          const signOfLon = function(L){ return SIGNS_DE[Math.floor((((L % 360) + 360) % 360) / 30)] || ''; };
          // Minuten werden ABGESCHNITTEN, nicht gerundet (astro.com-Konvention,
          // damit die Anzeige mit Astro-Software uebereinstimmt)
          const fmtDeg = function(L){
            const inSign = L % 30;
            const d = Math.floor(inSign);
            const m = Math.floor((inSign - d) * 60 + 0.0001);
            return d + '°' + (m < 10 ? '0' : '') + m + "' " + signOfLon(L);
          };

          // Placidus-Haus eines Transit-Grads: ueber die natalen Haeuserspitzen
          const FULL = window.__fullChart || [];
          const houses = (horo && horo.Houses) ? horo.Houses : [];
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

          // WAHRE natale Mondknoten (Bernadettes Vorgabe): FULL-Eintraege und
          // alle Knoten-Bezuege auf den wahren Knoten umstellen.
          const natalJd = (typeof origin !== 'undefined' && origin && origin.julianDate) ? origin.julianDate
            : ((horo && horo.origin && horo.origin.julianDate) ? horo.origin.julianDate : null);
          const tnNatal = (typeof trueNodeLon === 'function') ? trueNodeLon(natalJd) : null;
          const nnNatalLon2 = tnNatal != null ? tnNatal : lonOf(CP.northnode);
          const snNatalLon2 = nnNatalLon2 == null ? null : ((nnNatalLon2 + 180) % 360);
          if(nnNatalLon2 != null){
            FULL.forEach(function(e){
              if(e.label === 'Nordknoten'){ e.sign = signOfLon(nnNatalLon2); e.house = houseOfLong(nnNatalLon2) || e.house; }
              if(e.label === 'Südknoten'){ e.sign = signOfLon(snNatalLon2); e.house = houseOfLong(snNatalLon2) || e.house; }
            });
            // Natale Aspektliste: Knoten-Aspekte mit dem wahren Knoten neu rechnen
            try{
              const ASPL = window.__aspects || [];
              for(let i = ASPL.length - 1; i >= 0; i--){
                if(ASPL[i].p1 === 'Nordknoten' || ASPL[i].p2 === 'Nordknoten') ASPL.splice(i, 1);
              }
              const PPAIRS = [['Sonne',CB.sun],['Mond',CB.moon],['Merkur',CB.mercury],['Venus',CB.venus],['Mars',CB.mars],['Jupiter',CB.jupiter],['Saturn',CB.saturn],['Uranus',CB.uranus],['Neptun',CB.neptune],['Pluto',CB.pluto],['Chiron',CB.chiron],['Lilith',CP.lilith],['Aszendent',horo.Ascendant],['MC',horo.Midheaven]];
              const AT = [[0,'Konjunktion'],[60,'Sextil'],[90,'Quadrat'],[120,'Trigon'],[180,'Opposition']];
              const SIGNOF0 = {}; FULL.forEach(function(e){ SIGNOF0[e.label] = e.sign; });
              const nodeAsp = [];
              PPAIRS.forEach(function(pr){
                const L = lonOf(pr[1]);
                if(L == null) return;
                const dd = Math.abs(((L - nnNatalLon2 + 540) % 360) - 180);
                AT.forEach(function(t){
                  const orb = Math.abs(dd - t[0]);
                  if(orb <= 5) nodeAsp.push({ p1: pr[0], s1: SIGNOF0[pr[0]] || '', p2: 'Nordknoten', s2: signOfLon(nnNatalLon2), type: t[1], _orb: orb });
                });
              });
              nodeAsp.sort(function(a, b){ return a._orb - b._orb; });
              nodeAsp.forEach(function(a){ ASPL.push(a); });
            }catch(e){}
          }

          // Chartruler: Herrscher des AC-Zeichens (modern) + Mitherrscher
          const RULER = { 'Widder':'Mars','Stier':'Venus','Zwillinge':'Merkur','Krebs':'Mond','Löwe':'Sonne','Jungfrau':'Merkur','Waage':'Venus','Skorpion':'Pluto','Schütze':'Jupiter','Steinbock':'Saturn','Wassermann':'Uranus','Fische':'Neptun' };
          const CORULER = { 'Skorpion':'Mars','Wassermann':'Saturn','Fische':'Jupiter' };
          const acEntry = FULL.find(function(e){ return e.label === 'Aszendent'; }) || {};
          const acSign = acEntry.sign || '';
          const crName = RULER[acSign] || '';
          const crCo = CORULER[acSign] || '';

          // Aspekte eines Finsternis-Grads zu den natalen Punkten (Orb 3 Grad)
          const NATAL = [
            ['Sonne', CB.sun], ['Mond', CB.moon], ['Merkur', CB.mercury], ['Venus', CB.venus],
            ['Mars', CB.mars], ['Jupiter', CB.jupiter], ['Saturn', CB.saturn], ['Uranus', CB.uranus],
            ['Neptun', CB.neptune], ['Pluto', CB.pluto], ['Chiron', CB.chiron],
            ['Lilith', CP.lilith],
            ['Nordknoten', { ChartPosition: { Ecliptic: { DecimalDegrees: nnNatalLon2 } } }],
            ['Aszendent', horo.Ascendant], ['MC', horo.Midheaven]
          ];
          // Orbs: Bernadettes Ansage (24.07.): "Orben bei Eclipsen 10°."
          const TYPES = [[0,'Konjunktion',10],[60,'Sextil',10],[90,'Quadrat',10],[120,'Trigon',10],[180,'Opposition',10]];
          const SIGNOF = {}; FULL.forEach(function(e){ SIGNOF[e.label] = e.sign; });
          const HOUSEOF = {}; FULL.forEach(function(e){ HOUSEOF[e.label] = e.house; });
          const hitsOf = function(T){
            const out = [];
            NATAL.forEach(function(pair){
              const L = lonOf(pair[1]);
              if(L == null) return;
              const d = Math.abs(((T - L + 540) % 360) - 180);
              TYPES.forEach(function(t){
                const orb = Math.abs(d - t[0]);
                if(orb <= t[2]) out.push({ point: pair[0], sign: SIGNOF[pair[0]] || '', house: HOUSEOF[pair[0]] || '', type: t[1], orb: Math.round(orb * 10) / 10, cr: (pair[0] === crName || (crCo && pair[0] === crCo)) });
              });
            });
            out.sort(function(a, b){ return a.orb - b.orb; });
            return out;
          };

          // Natale Mondknoten (wahrer Knoten, oben berechnet)
          const nnNatalLon = nnNatalLon2;
          const snNatalLon = snNatalLon2;
          const natalOf = function(lbl){
            const e = FULL.find(function(x){ return x.label === lbl; }) || {};
            return { sign: e.sign || '', house: e.house || '' };
          };

          // Haeuserherrscher der Finsternis-Haeuser (Kern der Arbeitsweise der
          // Astrologin): Zeichen auf der Placidus-Spitze -> Herrscher (+ Mit-
          // herrscher) -> dessen Position in der Radix. Dedupe ueber das Haus.
          const cuspSignOf = function(houseId){
            for(let i = 0; i < houses.length; i++){
              const h = houses[i];
              const id = h.id || (i + 1);
              if(id !== houseId) continue;
              try { return signOfLon(h.ChartPosition.StartPosition.Ecliptic.DecimalDegrees); }
              catch(err){ return ''; }
            }
            return '';
          };
          const rulerHouses = [];
          [[houseOfLong(sofiLon), 'Sonnenfinsternis'],
           [houseOfLong(mofiMoonLon), 'Mondfinsternis, Mond'],
           [houseOfLong(mofiSunLon), 'Mondfinsternis, Sonne']].forEach(function(pair){
            if(pair[0] == null) return;
            const ex = rulerHouses.find(function(r){ return r.house === pair[0]; });
            if(ex){ ex.roles.push(pair[1]); return; }
            const cs = cuspSignOf(pair[0]);
            if(!cs) return;
            const rn = RULER[cs] || '', rco = CORULER[cs] || '';
            if(!rn) return;
            const rp = natalOf(rn);
            const cp2 = rco ? natalOf(rco) : null;
            rulerHouses.push({ house: pair[0], roles: [pair[1]], cuspSign: cs,
              ruler: rn, sign: rp.sign || '', inHouse: rp.house || '',
              co: rco, coSign: cp2 ? (cp2.sign || '') : '', coHouse: cp2 ? (cp2.house || '') : '' });
          });

          window.__eclipse = {
            rulers: rulerHouses,
            sofi: { text: fmtDeg(sofiLon), lon: sofiLon, house: houseOfLong(sofiLon), hits: hitsOf(sofiLon) },
            mofi: { moonText: fmtDeg(mofiMoonLon), sunText: fmtDeg(mofiSunLon), lon: mofiMoonLon,
                    houseMoon: houseOfLong(mofiMoonLon), houseSun: houseOfLong(mofiSunLon), hits: hitsOf(mofiMoonLon) },
            node: {
              sofiText: fmtDeg(nnSofiLon), mofiText: fmtDeg(nnMofiLon),
              signChange: signOfLon(nnSofiLon) !== signOfLon(nnMofiLon),
              houseNN: houseOfLong(nnSofiLon), houseSN: houseOfLong((nnSofiLon + 180) % 360),
              snText: fmtDeg((nnSofiLon + 180) % 360)
            },
            natalNodes: {
              nn: natalOf('Nordknoten'),
              snSign: snNatalLon == null ? '' : signOfLon(snNatalLon),
              snHouse: snNatalLon == null ? '' : (houseOfLong(snNatalLon) || '')
            },
            chartruler: crName ? { name: crName, co: crCo || '', acSign: acSign,
              sign: (natalOf(crName) || {}).sign || '', house: (natalOf(crName) || {}).house || '' } : null,
            natalSun: natalOf('Sonne'),
            natalMoon: natalOf('Mond')
          };
        }catch(e){ window.__eclipse = null; }
      })();

      generateReading();"""
transit_calc = (transit_calc
    .replace("__S_YEAR__", str(S_YEAR)).replace("__S_MONTH0__", str(S_MONTH - 1))
    .replace("__S_DATE__", str(S_DATE)).replace("__S_HOUR__", str(S_HOUR)).replace("__S_MINUTE__", str(S_MINUTE))
    .replace("__M_YEAR__", str(M_YEAR)).replace("__M_MONTH0__", str(M_MONTH - 1))
    .replace("__M_DATE__", str(M_DATE)).replace("__M_HOUR__", str(M_HOUR)).replace("__M_MINUTE__", str(M_MINUTE))
    .replace("__T_LAT__", str(T_LAT)).replace("__T_LON__", str(T_LON)))
repl(calc_anchor, transit_calc, "transit-calc-injection")

# --- 4b. Ergebnis-Seite verschlanken (REGEL seit 14.07.) --------------------
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

# --- 5. Reading-Block: sichtbares Eklipsen-Thema + Prompt-CTA ---------------
old_cta = """  html += `
  <div class="cta-block">
    <h3>Dein Business-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, wie du dein Business führst, wie du dich positionierst, wo deine Zone of Genius liegt und wie du am natürlichsten Geld verdienst.</p>
    <button class="copy-btn" id="copyBizBtn" onclick="copyBusinessReading()">Business-Prompt + Daten kopieren</button>
  </div>`;"""

new_cta = """  // Sichtbares Eklipsen-Thema
  const E = window.__eclipse || null;
  if(E){
    let tHtml = `
    <div class="data-block">
      <h3>Deine Eclipse Season im August 2026</h3>
      <div class="data-grid">`;
    tHtml += `<div class="data-row"><span class="data-planet">Sonnenfinsternis am 12.08. (${E.sofi.text}) fällt in Dein</span><span class="data-values">${E.sofi.house ? `<span class="badge house-badge">${E.sofi.house}. Haus</span>` : `<span class="badge sign-badge">Haus unbestimmt</span>`}</span></div>`;
    const axStr = (E.mofi.houseMoon && E.mofi.houseSun) ? (E.mofi.houseMoon + '. und ' + E.mofi.houseSun + '. Haus') : 'Haus unbestimmt';
    tHtml += `<div class="data-row"><span class="data-planet">Mondfinsternis am 28.08. (${E.mofi.moonText}) beleuchtet Deine Achse</span><span class="data-values"><span class="badge house-badge">${axStr}</span></span></div>`;
    (E.rulers || []).forEach(function(r){
      tHtml += `<div class="data-row"><span class="data-planet">Herrscher Deines ${r.house}. Hauses (${r.roles.join(' + ')})</span><span class="data-values"><span class="badge sign-badge">${r.ruler}${r.sign ? ' in ' + r.sign : ''}${r.inHouse ? ', ' + r.inHouse + '. Haus' : ''}</span></span></div>`;
    });
    const allHits = (E.sofi.hits || []).map(function(h){ return 'SoFi ' + h.type + ' ' + h.point + (h.cr ? ' (Chartruler)' : ''); })
      .concat((E.mofi.hits || []).map(function(h){ return 'MoFi ' + h.type + ' ' + h.point + (h.cr ? ' (Chartruler)' : ''); }));
    const hitPills = allHits.length
      ? allHits.map(function(t){ return `<span class="badge sign-badge">${t}</span>`; }).join('')
      : `<span class="badge sign-badge">keine engen Aspekte</span>`;
    tHtml += `<div class="data-row hits-row"><span class="data-planet">Die Finsternisse treffen bei Dir</span><span class="data-values">${hitPills}</span></div>`;
    if(E.node.houseNN && E.node.houseSN){
      tHtml += `<div class="data-row"><span class="data-planet">Die Mondknoten-Achse der Finsternisse läuft durch Dein</span><span class="data-values"><span class="badge house-badge">${E.node.houseNN}. und ${E.node.houseSN}. Haus</span></span></div>`;
    }
    tHtml += `</div></div>`;
    html += tHtml;
  }

  html += `
  <div class="cta-block">
    <h3>Dein Eclipse-Reading mit KI</h3>
    <p>Zwei Finsternisse, ein Zeitfenster: Was beginnt bei Dir und was vollendet sich? Kopiere Deinen Prompt und füge ihn bei ChatGPT oder Claude ein. Dein Reading zeigt Dir, welche Lebensbereiche die Eclipse Season bei Dir aktiviert und worauf Du bis Anfang 2027 achten darfst.</p>
    <button class="copy-btn" id="copyEclBtn" onclick="copyEclipseReading()">Eclipse-Prompt + Daten kopieren</button>
  </div>`;"""
repl(old_cta, new_cta, "cta-block")

# --- 6. Abschluss-CTA raus: Das ist das Produkt der ASTROLOGIN, kein Platz
# fuer Patrycjas AstroCode-Werbung. (Optional: spaeter CTA der Astrologin,
# wenn sie einen will — dann hier einsetzen.)
repl('''  html += `
  <div class="cta-block">
    <p class="cta-kicker">Möchtest du noch tiefer in deine Chart eintauchen?</p>
    <h3>Lerne dich tiefer kennen, als Jahre der Selbstreflexion es je konnten.</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Hier erfährst du mehr: Dein AstroCode &rarr;</a>
  </div>`;''',
'', "astrocode-cta-remove")

# --- 7. Prompt-Gehirn + Copy-Funktion austauschen --------------------------
# Der Prompt wird KOMPONIERT (Birthcode-Muster): Kapitel nur, wenn die Chart
# sie hergibt, dynamisch nummeriert.
new_region = r"""  const ECLIPSE_INTRO = `Du bist eine erfahrene Astrologin. Du liest mein Horoskop in Schichten und schreibst klar, warm und direkt, so dass mich jeder Satz trifft. Keine Floskeln, keine Lehrbuch-Erklärungen, keine Astrologie-Theorie: Gib mir direkt die Deutung für mein Leben.

Das Ereignis: Im August 2026 ist Eclipse Season. Am 12. August 2026 steht eine totale Sonnenfinsternis auf 20°06' Löwe. Am 28. August 2026 folgt eine partielle Mondfinsternis auf 4°50' Fische. Beide liegen an der Mondknotenachse. Eine Sonnenfinsternis findet zu einem Neumond statt: Sie steht für neue Chancen, neue Wege, neue Begegnungen und Türen, die sich plötzlich öffnen. Oft beginnt ein neues Kapitel, auch wenn ich es zunächst noch gar nicht erkenne. Eine Mondfinsternis findet zu einem Vollmond statt: Sie steht für Abschlüsse, Erkenntnisse, Entscheidungen und Loslassen. Wahrheit kommt ans Licht, oft zeigt sie genau das, was ich bisher übersehen oder verdrängt habe. Finsternisse wirken selten nur am Tag selbst: Die ersten Hinweise zeigen sich häufig schon etwa vier Wochen vorher, und die Themen entfalten sich manchmal noch Wochen oder Monate danach.

Wichtig: Ich arbeite mit Placidus-Häusern und lese mein Horoskop über die Häuserherrscher. Zu jedem relevanten Haus stehen unten das Zeichen auf der Häuserspitze und der Herrscher mit seiner Position in meiner Radix. Lies jede Finsternis über ihr Haus UND über den Herrscher dieses Hauses: Das Haus zeigt, wo es geschieht, sein Herrscher zeigt, worüber es läuft und wohin es führt. Bei den Aspekten gilt: Ich arbeite bei Finsternissen mit einem weiten Orb von bis zu 10°. Je enger der Orb, desto stärker wirkt der Aspekt, die engsten tragen die Hauptbotschaft. Aspekte mit dem Vermerk CHARTRULER treffen den Herrscher meines 1. Hauses, den Planeten, der mein ganzes Horoskop lenkt. Solche Treffer wiegen doppelt.

Schreibe mir auf dieser Basis:`;

  const ECLIPSE_CLOSING = `Schreib auf Deutsch, in der Du-Form, in Tiefe statt in Breite. Jeder Satz konkret. Schreibe Tierkreiszeichen wie Ortsangaben, ohne Beugung: in Löwe, in Fische, in Waage (niemals "im Löwen" oder "in den Fischen"). Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker.

Hier sind meine Daten:`;

  window.copyEclipseReading = function(){
    const FULL = window.__fullChart || [];
    const ASP = window.__aspects || [];
    const E = window.__eclipse || {};
    const m = window.__meta || {};
    const sofi = E.sofi || {}, mofi = E.mofi || {}, node = E.node || {};
    const cr = E.chartruler || null;
    const crHit = (sofi.hits || []).some(function(h){ return h.cr; }) || (mofi.hits || []).some(function(h){ return h.cr; });

    // --- Kapitel komponieren (nur was das Horoskop hergibt) ---
    // Kern der Arbeitsweise der Astrologin: jede Finsternis wird ueber ihr
    // Haus UND den Herrscher dieses Hauses gelesen.
    const rulers = E.rulers || [];
    const rulerLine = function(r){
      if(!r) return '';
      return 'Der Herrscher meines ' + r.house + '. Hauses ist ' + r.ruler + (r.sign ? (', er steht in ' + r.sign) : '') + (r.inHouse ? (' in meinem ' + r.inHouse + '. Haus') : '') + (r.co ? ('. Mitherrscher ist ' + r.co + (r.coSign ? (' in ' + r.coSign) : '') + (r.coHouse ? (', ' + r.coHouse + '. Haus') : '')) : '') + '.';
    };
    const rulerOfHouse = function(h){ return rulers.find(function(r){ return r.house === h; }) || null; };

    const chap = [];
    chap.push('Das Tor. Ein kraftvoller Absatz: was dieses Finsternis-Fenster im August 2026 bei mir öffnet und welche der beiden Finsternisse mich nach meinem Horoskop stärker berührt. Sprich mich direkt mit du an.');

    const sofiR = rulerOfHouse(sofi.house);
    chap.push('Die Sonnenfinsternis' + (sofi.house ? (' in meinem ' + sofi.house + '. Haus') : '') + '. ' + (sofiR ? (rulerLine(sofiR) + ' Lies die Finsternis über dieses Haus und über seinen Herrscher: Das Haus zeigt, wo es geschieht, der Herrscher zeigt, worüber es läuft und wohin es führt. ') : '') + 'Welche Tür will sich in diesem Lebensbereich rund um den 12. August 2026 öffnen, welches neue Kapitel beginnt, vielleicht ohne dass ich es sofort erkenne? Mach es konkret, keine Kategorien.' + ((sofi.hits || []).length ? '' : ' Die Sonnenfinsternis bildet keine engen Aspekte zu meinen Punkten. Sag mir ehrlich: Sie wirkt bei mir über dieses Haus und seinen Herrscher, leiser, aber über Monate.'));

    if((sofi.hits || []).length){
      chap.push('Direkte Treffer der Sonnenfinsternis. Geh die Aspekte durch, die die Sonnenfinsternis zu meinen natalen Punkten bildet, und sag mir, was jeder in genau diesem Punkt meines Horoskops auslöst. Beginne mit dem engsten Orb und gib ihm den meisten Raum, er trägt die Hauptbotschaft. Aspekte mit weitem Orb fasse kürzer. Keine Theorie, direkt die Deutung.');
    }

    const moonR = rulerOfHouse(mofi.houseMoon), sunR = rulerOfHouse(mofi.houseSun);
    const axTxt = (mofi.houseMoon && mofi.houseSun) ? ('Der Mond steht in meinem ' + mofi.houseMoon + '. Haus, die Sonne gegenüber in meinem ' + mofi.houseSun + '. Haus. ') : '';
    const axRulers = [moonR, (sunR && sunR !== moonR) ? sunR : null].filter(function(x){ return !!x; }).map(rulerLine).join(' ');
    chap.push('Die Mondfinsternis auf meiner Achse. ' + axTxt + (axRulers ? (axRulers + ' Lies die Achse über diese beiden Häuser und ihre Herrscher. ') : '') + 'Was ist in diesem Spannungsfeld reif für einen Abschluss oder eine Entscheidung, welche Wahrheit will um den 28. August ans Licht kommen, was habe ich bisher übersehen oder verdrängt?' + ((mofi.hits || []).length ? '' : ' Die Mondfinsternis bildet keine engen Aspekte zu meinen Punkten. Lies sie über die Achse und ihre Herrscher, dort liegt ihre Botschaft.'));

    if((mofi.hits || []).length){
      chap.push('Direkte Treffer der Mondfinsternis. Geh die Aspekte durch, die die Mondfinsternis zu meinen natalen Punkten bildet, und sag mir, was jeder in genau diesem Punkt meines Horoskops auslöst. Beginne mit dem engsten Orb und gib ihm den meisten Raum. Aspekte mit weitem Orb fasse kürzer. Keine Theorie, direkt die Deutung.');
    }

    if(cr && crHit){
      chap.push('Der Treffer auf meinen Chartruler. Der Herrscher meines 1. Hauses ist ' + cr.name + (cr.sign ? (', er steht in ' + cr.sign) : '') + (cr.house ? (' in meinem ' + cr.house + '. Haus') : '') + ' und lenkt mein ganzes Horoskop. Eine Finsternis berührt ihn direkt, du findest den Aspekt in den Daten mit dem Vermerk CHARTRULER. Widme diesem Treffer einen eigenen Absatz: Wenn der Lenker des Horoskops getroffen wird, verschiebt sich die Richtung des ganzen Lebens spürbarer als bei jedem anderen Punkt.');
    }

    chap.push('Die Richtung. Die Mondknotenachse der Finsternisse läuft bei mir durch' + ((node.houseNN && node.houseSN) ? (' mein ' + node.houseNN + '. und mein ' + node.houseSN + '. Haus') : ' meine Häuser') + '. Lies sie als Richtungsgeber dieses Fensters: wohin das Leben mich zieht und was ich dafür lassen darf. Vergleiche sie mit meinen natalen Mondknoten in den Daten unten: Wo bestätigt das Fenster meinen Weg, wo fordert es einen neuen Schritt?');

    chap.push('Meine Lichter. Lies meine natale Sonne und meinen natalen Mond aus den Daten unten: wie diese beiden Kräfte in meinem Horoskop angelegt sind und was die Finsternisse in ihnen aktivieren.');

    chap.push('Schatten und Geschenk. Der Schatten dieser Wochen: Ich will im Außen erzwingen, was innen reifen will, ich deute jede Unruhe als Zeichen und ich treffe große Entscheidungen aus der Angst, etwas zu verpassen. Das Geschenk: Ich erkenne, welches Kapitel bei mir beginnt und welches sich vollendet, und ich gebe beidem Raum. Sag mir, woran ich bei mir erkenne, ob ich im Schatten oder im Geschenk unterwegs bin.');

    chap.push('Meine Eclipse Season. Formuliere aus allem einen roten Faden für meine Eclipse Season, von Mitte Juli 2026 (die ersten Hinweise zeigen sich oft vier Wochen vorher) bis Anfang 2027: ein einziger Satz in der Ich-Form, den ich mir aufschreiben kann. Dazu zwei Dinge: eine kleine, konkrete Handlung für die Tage zwischen den beiden Finsternissen, vom 12. bis zum 28. August, und die Einladung, wichtige Ereignisse dieser Wochen aufzuschreiben, weil sich der rote Faden oft erst Monate später zeigt.');

    chap.push('Meine Finsternis-Frage. Eine einzige, konfrontierende Frage zu dem, was in meinem Leben reif ist und was ich trotzdem festhalte.');

    const chapters = chap.map(function(c, i){ return (i + 1) + '. ' + c; }).join('\n\n');

    // --- Datenblock ---
    const data = [];
    if(m.name) data.push('Name: ' + m.name);
    if(m.date){ const dp = m.date.split('-'); data.push('Geburtsdatum: ' + dp[2]+'.'+dp[1]+'.'+dp[0] + (m.time ? (' um ' + m.time + ' Uhr') : '')); }
    if(m.place) data.push('Geburtsort: ' + m.place);
    data.push('');
    data.push('MEINE FINSTERNISSE IM AUGUST 2026:');
    data.push('Sonnenfinsternis am 12.08.2026: ' + (sofi.text || '20°02\' Löwe') + (sofi.house ? (', fällt in mein ' + sofi.house + '. Haus.') : '.'));
    const hitLine = function(h, who){ return '- ' + who + ' ' + h.type + ' zu ' + h.point + (h.sign ? (' in ' + h.sign) : '') + (h.house ? (', ' + h.house + '. Haus') : '') + ' (Orb ' + String(h.orb).replace('.', ',') + '°)' + (h.cr ? ' [CHARTRULER]' : ''); };
    if((sofi.hits || []).length){
      data.push('Aspekte der Sonnenfinsternis zu meinen natalen Punkten (engster Orb wirkt am stärksten):');
      sofi.hits.forEach(function(h){ data.push(hitLine(h, 'Sonnenfinsternis')); });
    } else {
      data.push('Die Sonnenfinsternis bildet keine Aspekte (Orb bis 10°) zu meinen natalen Punkten.');
    }
    data.push('Mondfinsternis am 28.08.2026: Mond ' + (mofi.moonText || '4°54\' Fische') + (mofi.houseMoon ? (' in meinem ' + mofi.houseMoon + '. Haus') : '') + ', Sonne gegenüber ' + (mofi.sunText || '4°54\' Jungfrau') + (mofi.houseSun ? (' in meinem ' + mofi.houseSun + '. Haus') : '') + '.');
    if((mofi.hits || []).length){
      data.push('Aspekte der Mondfinsternis (Mondposition) zu meinen natalen Punkten:');
      mofi.hits.forEach(function(h){ data.push(hitLine(h, 'Mondfinsternis')); });
    } else {
      data.push('Die Mondfinsternis bildet keine Aspekte (Orb bis 10°) zu meinen natalen Punkten.');
    }
    if(rulers.length){
      data.push('DIE HÄUSERHERRSCHER DER FINSTERNISSE (so lese ich):');
      rulers.forEach(function(r){
        data.push('- ' + r.house + '. Haus (' + r.roles.join(' + ') + '): Spitze im Zeichen ' + r.cuspSign + ', Herrscher ' + r.ruler + (r.sign ? (' in ' + r.sign) : '') + (r.inHouse ? (', ' + r.inHouse + '. Haus') : '') + (r.co ? (' (Mitherrscher: ' + r.co + (r.coSign ? (' in ' + r.coSign) : '') + (r.coHouse ? (', ' + r.coHouse + '. Haus') : '') + ')') : '') + '.');
      });
    }
    data.push('Mondknotenachse (wahrer Mondknoten) zur Zeit der Sonnenfinsternis: Nordknoten ' + (node.sofiText || '') + (node.houseNN ? (' in meinem ' + node.houseNN + '. Haus') : '') + ', Südknoten ' + (node.snText || '') + (node.houseSN ? (' in meinem ' + node.houseSN + '. Haus') : '') + '.');
    if(node.signChange){
      data.push('Zur Mondfinsternis steht der Nordknoten bei ' + (node.mofiText || '') + ': Die Achse wechselt genau zwischen den beiden Finsternissen das Zeichen.');
    }
    if(E.natalNodes && E.natalNodes.nn && E.natalNodes.nn.sign){
      data.push('Meine natalen Mondknoten (wahrer Mondknoten): Nordknoten in ' + E.natalNodes.nn.sign + (E.natalNodes.nn.house ? (', ' + E.natalNodes.nn.house + '. Haus') : '') + (E.natalNodes.snSign ? (', Südknoten in ' + E.natalNodes.snSign + (E.natalNodes.snHouse ? (', ' + E.natalNodes.snHouse + '. Haus') : '')) : '') + '.');
    }
    if(cr){
      data.push('Mein Chartruler (Herrscher meines 1. Hauses, Aszendent im Zeichen ' + cr.acSign + '): ' + cr.name + (cr.sign ? (' in ' + cr.sign) : '') + (cr.house ? (', ' + cr.house + '. Haus') : '') + (cr.co ? (' (Mitherrscher: ' + cr.co + ')') : '') + '.');
    }
    if(E.natalSun && E.natalSun.sign) data.push('Meine natale Sonne: ' + E.natalSun.sign + (E.natalSun.house ? (', ' + E.natalSun.house + '. Haus') : ''));
    if(E.natalMoon && E.natalMoon.sign) data.push('Mein nataler Mond: ' + E.natalMoon.sign + (E.natalMoon.house ? (', ' + E.natalMoon.house + '. Haus') : ''));
    data.push('');
    data.push('MEINE RADIX (Placidus-Häuser):');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });
    if(ASP.length){
      data.push('');
      data.push('MEINE WICHTIGSTEN NATALEN ASPEKTE:');
      ASP.forEach(function(a){ data.push(a.p1 + (a.s1 ? (' in ' + a.s1) : '') + ' ' + a.type + ' ' + a.p2 + (a.s2 ? (' in ' + a.s2) : '')); });
    }
    const full = ECLIPSE_INTRO + '\n\n' + chapters + '\n\n' + ECLIPSE_CLOSING + '\n\n' + data.join('\n');
    const btn = document.getElementById('copyEclBtn');
    const done = function(){ if(btn){ const o = btn.getAttribute('data-label') || btn.textContent; btn.setAttribute('data-label', o); btn.textContent = '✓ Kopiert! Jetzt bei ChatGPT einfügen'; setTimeout(function(){ btn.textContent = o; }, 2800); } };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(full).then(done).catch(function(){ fallbackCopy(full, done); });
    } else { fallbackCopy(full, done); }
  };"""

pat = re.compile(r"  const BUSINESS_PROMPT = `.*?\n  window\.copyBusinessReading = function\(\)\{.*?\n  \};", re.DOTALL)
if not pat.search(s):
    sys.exit("FEHLT: BUSINESS_PROMPT / copyBusinessReading Region")
s = pat.sub(lambda _: new_region, s, count=1)

# --- 8. Bernadette-Design als Override-Layer (aus ihrem Eclipse Guide PDF) ---
TAPE = ("ECLIPSE SEASON \\2726  " * 16).strip()   # \2726 = ✦ als CSS-Escape
extra_css = '''<style>
@font-face{ font-family:'BAnton'; src:url(data:font/woff2;base64,__ANTON__) format('woff2'); font-weight:400; font-style:normal; font-display:swap; }
@font-face{ font-family:'BScript'; src:url(data:font/woff2;base64,__SCRIPT__) format('woff2'); font-weight:400; font-style:normal; font-display:swap; }
html{ background:__ROSA__ !important; }
body{ background:__ROSA__ !important; color:#111111 !important;
  font-family:'Inter','Helvetica Neue',Arial,sans-serif !important; }
#binary-canvas{ display:none !important; }
/* Tape-Baender statt Planeten-Hero (Signature-Look aus dem Eclipse Guide) */
.moon-scene{ position:relative !important; top:auto !important; background:none !important;
  height:calc(150px + 2.6vw) !important; opacity:1 !important; margin-bottom:0 !important;
  overflow:hidden !important; pointer-events:none !important;
  -webkit-mask-image:none !important; mask-image:none !important; }
.moon-scene::before{ content:"__TAPE__"; position:absolute; left:-6%; right:-6%; top:52px;
  background:__INK__; color:#FFFFFF; font-family:'BAnton',sans-serif; font-size:15px;
  letter-spacing:0.2em; line-height:1; padding:10px 0; white-space:nowrap; overflow:hidden;
  transform:rotate(-3.5deg); }
.moon-scene::after{ content:"__TAPE__"; position:absolute; left:-6%; right:-6%; top:112px;
  background:__PEACH__; color:__INK__; font-family:'BAnton',sans-serif; font-size:15px;
  letter-spacing:0.2em; line-height:1; padding:10px 0; white-space:nowrap; overflow:hidden;
  transform:rotate(2.5deg); }
/* Kein Bild im Kopf: Schrift direkt unter die Tape-Baender (Bernadette 25.07.) */
.container{ padding-top:8px !important; }
.header-eyebrow{
  font-family:'BScript',cursive !important;
  font-size:clamp(1.7rem, 4.5vw, 2.4rem) !important;
  font-weight:400 !important;
  letter-spacing:0.02em !important;
  text-transform:none !important;
  color:#111111 !important;
  text-shadow:none !important;
  margin-bottom:18px !important;
}
header h1{ margin-top:0 !important; margin-bottom:14px !important; }
header h1{
  font-family:'BAnton',sans-serif !important;
  text-transform:uppercase !important;
  font-size:clamp(2.6rem, 9vw, 4.4rem) !important;
  line-height:1.02 !important;
  letter-spacing:0.01em !important;
  color:#111111 !important;
  text-shadow:none !important;
}
.subtitle{
  font-family:'Inter','Helvetica Neue',Arial,sans-serif !important;
  font-style:normal !important;
  font-size:1.05rem !important;
  font-weight:500 !important;
  line-height:1.75 !important;
  letter-spacing:0.01em !important;
  color:#111111 !important;
  max-width:540px !important; margin:10px auto 0 !important;
}
/* Goldstrich (Bernadettes Wunsch 25.07., Loewe-Mond): das Basis-Divider-Element
   als klare goldene Linie */
.divider{ display:block !important; width:110px !important; height:3px !important;
  background:linear-gradient(90deg, rgba(217,169,79,0), #D9A94F 18%, #D9A94F 82%, rgba(217,169,79,0)) !important;
  border:none !important; margin:26px auto !important; opacity:1 !important;
  border-radius:3px !important; box-shadow:none !important; }
/* Treffer-Zeile: jeder Aspekt als eigenes Pill statt einer ueberlangen Zeile */
.data-values{ display:flex !important; flex-wrap:wrap !important; gap:6px !important;
  justify-content:flex-end !important; align-items:center !important; }
.hits-row .data-values{ max-width:62%; }
header{ margin-bottom:16px !important; }
.place-chosen{ color:#111111 !important; font-weight:700 !important; }
.results-header h2{ font-family:'BAnton',sans-serif !important; text-transform:uppercase !important;
  color:#111111 !important; text-shadow:none !important; letter-spacing:0.01em !important; }
.results-header p{ color:#333333 !important;
  font-family:'Inter','Helvetica Neue',Arial,sans-serif !important;
  font-size:1rem !important; font-weight:600 !important; letter-spacing:0.02em !important; }
h3, .data-planet, .field-label, label, p, li{ color:#111111; }
.reading-block h3, .summary-block h3, .data-block h3, .cta-block h3, .form-section h3{
  font-family:'BAnton',sans-serif !important; text-transform:uppercase !important;
  letter-spacing:0.03em !important; color:#111111 !important; font-weight:400 !important; }
.tip-box, .form-section, .reading-block, .summary-block, .data-block, .cta-block{
  background:__CREAM__ !important;
  border:none !important;
  border-radius:18px !important;
  box-shadow:0 10px 30px rgba(17,17,17,0.10) !important;
  color:#111111 !important; }
.field-label{ color:#111111 !important; font-weight:700 !important; }
.error-msg{ color:#B3123E !important; }
.data-block, .reading-block, .summary-block, .cta-block{ margin:36px 0 !important; }
.cta-block h3{ font-size:clamp(1.2rem, 2.4vw, 1.5rem) !important; line-height:1.35 !important; }
.cta-block p{ color:#111111 !important; }
input[type="text"], input[type="date"], input[type="time"]{
  background:#FFFFFF !important; border:2px solid #111111 !important; border-radius:12px !important;
  color:#111111 !important; }
input::placeholder{ color:rgba(17,17,17,0.40) !important; }
input[type="text"]:focus, input[type="date"]:focus, input[type="time"]:focus{
  border-color:#111111 !important; box-shadow:0 0 0 4px __FLIEDER__ !important; }
.place-results{ background:#FFFFFF !important; border:2px solid #111111 !important; }
.place-item{ color:#111111 !important; }
.place-item:hover, .place-item.active{ background:__ROSA__ !important; }
select option{ background:#FFFFFF !important; color:#111111 !important; }
.sign-badge{ background:__FLIEDER__ !important; border:none !important; color:#111111 !important; font-weight:700 !important; }
.house-badge{ background:__PEACH__ !important; border:none !important; color:#111111 !important; font-weight:700 !important; }
.submit-btn, .cta-link, .copy-btn{
  background:#111111 !important;
  color:#FFFFFF !important;
  font-family:'BAnton',sans-serif !important;
  font-weight:400 !important;
  text-transform:uppercase !important;
  letter-spacing:0.12em !important;
  border-radius:999px !important;
  border:none !important;
  box-shadow:0 8px 24px rgba(17,17,17,0.22) !important; }
.submit-btn:hover, .cta-link:hover, .copy-btn:hover{ background:#2c2c2c !important; box-shadow:0 12px 32px rgba(17,17,17,0.30) !important; }
.back-btn{ color:#111111 !important; font-weight:700 !important; }
.legal-footer{ background:__CREAM__ !important; border-radius:0 !important; }
.legal-footer, .legal-footer a{ color:#111111 !important; text-transform:uppercase !important;
  letter-spacing:0.14em !important; font-size:0.72rem !important; }
.legal-logo{ display:none !important; }
</style>
</head>'''
extra_css = (extra_css
    .replace("__ANTON__", FONT_ANTON).replace("__SCRIPT__", FONT_SCRIPT)
    .replace("__TAPE__", TAPE)
    .replace("__ROSA__", C_ROSA).replace("__CREAM__", C_CREAM)
    .replace("__PEACH__", C_PEACH).replace("__FLIEDER__", C_FLIEDER)
    .replace("__INK__", C_INK))
repl('</head>', extra_css, "bernadette-css")

# ASTROCODE-Abschlussbild (NP-Logo + Schriftzug) bewusst NICHT eingebaut —
# das Branding der Astrologin kommt von Patricia und ersetzt diese Stelle.

# Sicherheitscheck: keine Business- oder Womancode-Reste mehr in Logik-Hooks
for leftover in ["copyBusinessReading", "copyBizBtn", "BUSINESS_PROMPT", "subscribeLead", "userEmail", "Business-Code", "Business-Blueprint", "wc-logo", "Womancode", "womancode"]:
    if leftover in s:
        sys.exit("REST gefunden: " + leftover)

with open(DST, "w", encoding="utf-8") as f:
    f.write(s)

os.makedirs(NETLIFY, exist_ok=True)
shutil.copyfile(DST, os.path.join(NETLIFY, "index.html"))

print("OK ->", DST)
print("OK ->", os.path.join(NETLIFY, "index.html"))
print("Groesse:", len(s), "Zeichen")
