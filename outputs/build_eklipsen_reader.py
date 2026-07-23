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
import os, re, sys, shutil, io, base64
from PIL import Image, ImageFilter, ImageChops

NAME = "Dein Eklipsen-Code"          # Arbeitstitel — Name entscheidet Patrycja/Astrologin
KICKER_READER = "Eklipsen-Reader"    # fuer den Abschluss-CTA

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-eklipsen-reader.html")
NETLIFY = os.path.join(HERE, "astro-eklipsen-reader-netlify")
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

# --- Finsternis-Momente (lokale Zeit, Engine loest Zeitzone ueber Koordinaten)
S_YEAR, S_MONTH, S_DATE, S_HOUR, S_MINUTE = 2026, 8, 12, 19, 38   # SoFi
M_YEAR, M_MONTH, M_DATE, M_HOUR, M_MINUTE = 2026, 8, 28, 6, 20    # MoFi
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
     '', "eyebrow-remove")

repl("<h1>Dein Business-Code</h1>",
     "<h1>" + NAME + "</h1>", "h1")

repl('<p class="subtitle">Gib deine Geburtsdaten ein. Auf der nächsten Seite bekommst du dein Geburtshoroskop angezeigt und einen fertigen KI-Prompt, der dir sagt, wie du dein Business führst, dich positionierst, skalierst und Geld verdienst.</p>',
     '<p class="subtitle">Im August 2026 öffnen zwei Finsternisse ein gemeinsames Zeitfenster: eine totale Sonnenfinsternis im Löwen am 12. August und eine Mondfinsternis in den Fischen am 28. August. Was sie berühren, trägt etwa ein halbes Jahr. Gib deine Geburtsdaten ein. Die Seite berechnet dein Geburtshoroskop, zeigt dir, in welche Lebensbereiche die Finsternisse bei dir fallen, und erstellt einen fertigen KI-Prompt für dein persönliches Reading.</p>',
     "subtitle")

repl('onclick="runCheck()">Meinen Business-Code aufdecken</button>',
     'onclick="runCheck()">Meinen individuellen KI-Prompt kreieren</button>', "submit-btn")

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
     "<h2>Deine Finsternisse${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Sonnenfinsternis und Mondfinsternis im August 2026'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Neue Chart erstellen", "back-btn")

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
            return new Horoscope({ origin: o, houseSystem: 'placidus', zodiac: 'tropical', language: 'en', aspectTypes: [] });
          };
          const sofi = mkChart(__S_YEAR__, __S_MONTH0__, __S_DATE__, __S_HOUR__, __S_MINUTE__);
          const mofi = mkChart(__M_YEAR__, __M_MONTH0__, __M_DATE__, __M_HOUR__, __M_MINUTE__);
          const lonOf = function(b){ try{ return b.ChartPosition.Ecliptic.DecimalDegrees; }catch(e){ return null; } };

          const sofiLon = lonOf(sofi.CelestialBodies.sun);          // = Mond, Neumond
          const mofiMoonLon = lonOf(mofi.CelestialBodies.moon);
          const mofiSunLon = lonOf(mofi.CelestialBodies.sun);
          const nnSofiLon = lonOf(sofi.CelestialPoints.northnode);
          const nnMofiLon = lonOf(mofi.CelestialPoints.northnode);
          if([sofiLon, mofiMoonLon, mofiSunLon, nnSofiLon, nnMofiLon].some(function(v){ return v == null; })) return;

          const SIGNS_DE = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische'];
          const signOfLon = function(L){ return SIGNS_DE[Math.floor((((L % 360) + 360) % 360) / 30)] || ''; };
          const fmtDeg = function(L){
            const inSign = L % 30;
            let d = Math.floor(inSign);
            let m = Math.round((inSign - d) * 60);
            if(m === 60){ m = 0; d += 1; }
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
            ['Lilith', CP.lilith], ['Nordknoten', CP.northnode],
            ['Aszendent', horo.Ascendant], ['MC', horo.Midheaven]
          ];
          const TYPES = [[0,'Konjunktion'],[60,'Sextil'],[90,'Quadrat'],[120,'Trigon'],[180,'Opposition']];
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
                if(orb <= 3) out.push({ point: pair[0], sign: SIGNOF[pair[0]] || '', house: HOUSEOF[pair[0]] || '', type: t[1], orb: Math.round(orb * 10) / 10, cr: (pair[0] === crName || (crCo && pair[0] === crCo)) });
              });
            });
            out.sort(function(a, b){ return a.orb - b.orb; });
            return out;
          };

          // Natale Mondknoten: Nordknoten aus der Chart, Suedknoten gegenueber
          const nnNatalLon = lonOf(CP.northnode);
          const snNatalLon = nnNatalLon == null ? null : ((nnNatalLon + 180) % 360);
          const natalOf = function(lbl){
            const e = FULL.find(function(x){ return x.label === lbl; }) || {};
            return { sign: e.sign || '', house: e.house || '' };
          };

          window.__eclipse = {
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
      <h3>Deine Finsternisse im August 2026</h3>
      <div class="data-grid">`;
    tHtml += `<div class="data-row"><span class="data-planet">Sonnenfinsternis am 12.08. (${E.sofi.text}) fällt in dein</span><span class="data-values">${E.sofi.house ? `<span class="badge house-badge">${E.sofi.house}. Haus</span>` : `<span class="badge sign-badge">Haus unbestimmt</span>`}</span></div>`;
    const axStr = (E.mofi.houseMoon && E.mofi.houseSun) ? (E.mofi.houseMoon + '. und ' + E.mofi.houseSun + '. Haus') : 'Haus unbestimmt';
    tHtml += `<div class="data-row"><span class="data-planet">Mondfinsternis am 28.08. (${E.mofi.moonText}) beleuchtet deine Achse</span><span class="data-values"><span class="badge house-badge">${axStr}</span></span></div>`;
    const allHits = (E.sofi.hits || []).map(function(h){ return 'SoFi ' + h.type + ' ' + h.point + (h.cr ? ' (Chartruler)' : ''); })
      .concat((E.mofi.hits || []).map(function(h){ return 'MoFi ' + h.type + ' ' + h.point + (h.cr ? ' (Chartruler)' : ''); }));
    tHtml += `<div class="data-row"><span class="data-planet">Die Finsternisse treffen bei dir</span><span class="data-values"><span class="badge sign-badge">${allHits.length ? allHits.join(', ') : 'keine engen Aspekte'}</span></span></div>`;
    if(E.node.houseNN && E.node.houseSN){
      tHtml += `<div class="data-row"><span class="data-planet">Die Mondknoten-Achse der Finsternisse läuft durch dein</span><span class="data-values"><span class="badge house-badge">${E.node.houseNN}. und ${E.node.houseSN}. Haus</span></span></div>`;
    }
    tHtml += `</div></div>`;
    html += tHtml;
  }

  html += `
  <div class="cta-block">
    <h3>Dein Finsternis-Reading mit KI</h3>
    <p>Zwei Finsternisse, ein Zeitfenster: Was beginnt bei dir und was vollendet sich? Kopiere den Prompt und füge ihn bei ChatGPT oder Claude ein. Dein Reading zeigt dir, welche Lebensbereiche die Finsternisse berühren und wohin dein Fokus bis Anfang 2027 gehört.</p>
    <button class="copy-btn" id="copyEclBtn" onclick="copyEclipseReading()">Eklipsen-Prompt + Daten kopieren</button>
  </div>`;"""
repl(old_cta, new_cta, "cta-block")

# --- 6. Abschluss-CTA: AstroCode-Portal (Patrycjas Text 15.07., 1:1) --------
repl('''  html += `
  <div class="cta-block">
    <p class="cta-kicker">Möchtest du noch tiefer in deine Chart eintauchen?</p>
    <h3>Lerne dich tiefer kennen, als Jahre der Selbstreflexion es je konnten.</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Hier erfährst du mehr: Dein AstroCode &rarr;</a>
  </div>`;''',
'''  html += `
  <div class="cta-block astro-cta">
    <p class="cta-kicker">Dir gefallen die Antworten aus meinem ''' + KICKER_READER + '''?</p>
    <h3>Weißt du, dass du dank meines Astrocode-Portals dein ganzes Geburtshoroskop analysieren kannst! Tiefer als jedes Astroreading, denn erst die Bewegung bewirkt Veränderung! Wie oft hast du schon was über dich gehört, aber nicht umgesetzt!</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Öffne dein Astrocode-Portal und begib dich auf eine unvergessliche Reise zurück zu dir!</a>
  </div>`;''',
"astrocode-cta")

# --- 7. Prompt-Gehirn + Copy-Funktion austauschen --------------------------
# Der Prompt wird KOMPONIERT (Birthcode-Muster): Kapitel nur, wenn die Chart
# sie hergibt, dynamisch nummeriert.
new_region = r"""  const ECLIPSE_INTRO = `Du bist eine erfahrene Bewusstseinsastrologin mit Fokus auf Transite, Mondzyklen und Finsternisse. Du liest meine Chart in Schichten und schreibst klar, tief und direkt, so dass mich jeder Satz trifft. Keine Floskeln, keine allgemeinen Astro-Sätze, kein Lehrbuchton.

Das Ereignis: Im August 2026 öffnen zwei Finsternisse ein gemeinsames Zeitfenster. Am 12. August 2026 steht eine totale Sonnenfinsternis auf 20° Löwe, ein Neumond an der Mondknotenachse. In Spanien ist sie total zu sehen, in weiten Teilen Europas als partielle Finsternis am Abendhimmel. Am 28. August 2026 folgt eine partielle Mondfinsternis auf 5° Fische, ein Vollmond an der Knotenachse. Finsternisse sind verdichtete Neu- und Vollmonde: Was sie berühren, entfaltet sich über etwa sechs Monate, bis die nächste Finsternis-Saison Anfang 2027 übernimmt. Eine Sonnenfinsternis setzt einen Anfang, der größer ist als ein gewöhnlicher Neumond. Eine Mondfinsternis bringt etwas zur Reife, macht ein Gefühl sichtbar und löst, was voll ist. Dazu kommt eine Besonderheit: Genau zwischen den beiden Finsternissen wechselt die Mondknotenachse das Zeichen, vom Fische-Jungfrau-Feld in das Wassermann-Löwe-Feld. Die Sonnenfinsternis im Löwen eröffnet damit die neue Finsternis-Serie auf der Löwe-Wassermann-Achse: Selbstausdruck, Sichtbarkeit und Herz auf der einen Seite, Zugehörigkeit und das größere Ganze auf der anderen.

Wichtig: Ich arbeite mit Placidus-Häusern. Alle Häuser in meinen Daten unten sind Placidus-Häuser. Finsternisse sind kollektive Ereignisse. Wie stark und wo sie mich persönlich berühren, zeigen die Häuser, in die sie fallen, und die Aspekte zu meinen natalen Punkten. Aspekte mit dem Vermerk CHARTRULER treffen den Herrscher meines Aszendenten, den Planeten, der meine Chart lenkt. Solche Treffer wiegen doppelt.

Schreibe mir auf dieser Basis:`;

  const ECLIPSE_CLOSING = `Schreib auf Deutsch, in der Du-Form, in Tiefe statt in Breite. Jeder Satz konkret. Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker.

Hier sind meine Daten:`;

  window.copyEclipseReading = function(){
    const FULL = window.__fullChart || [];
    const ASP = window.__aspects || [];
    const E = window.__eclipse || {};
    const m = window.__meta || {};
    const sofi = E.sofi || {}, mofi = E.mofi || {}, node = E.node || {};
    const cr = E.chartruler || null;
    const crHit = (sofi.hits || []).some(function(h){ return h.cr; }) || (mofi.hits || []).some(function(h){ return h.cr; });

    // --- Kapitel komponieren (nur was die Chart hergibt) ---
    const chap = [];
    chap.push('Das Tor. Ein kraftvoller Absatz: was dieses Finsternis-Fenster im August 2026 kollektiv anzeigt und welche der beiden Finsternisse mich nach meiner Chart stärker berührt. Sprich mich direkt mit du an.');

    chap.push('Die Sonnenfinsternis' + (sofi.house ? (' in meinem ' + sofi.house + '. Haus') : '') + '. Beschreibe, wie sich dieser Lebensbereich in meinem Alltag zeigt und was dort ab dem 12. August 2026 neu beginnen will. Mach den Bereich konkret, keine Kategorien. Das Fenster trägt etwa sechs Monate.' + ((sofi.hits || []).length ? '' : ' Die Sonnenfinsternis bildet keine engen Aspekte zu meinen Punkten. Sag mir ehrlich: Sie wirkt bei mir über diesen Lebensbereich, leiser, aber über Monate.'));

    if((sofi.hits || []).length){
      chap.push('Direkte Treffer der Sonnenfinsternis. Geh jeden Aspekt durch, den die Sonnenfinsternis zu meinen natalen Punkten bildet. Erkläre für jeden, was der Aspekt bedeutet und was er in genau diesem Punkt meiner Chart auslöst. Beginne mit dem engsten Orb, der wirkt am stärksten.');
    }

    const axTxt = (mofi.houseMoon && mofi.houseSun) ? ('Der Mond steht in meinem ' + mofi.houseMoon + '. Haus, die Sonne gegenüber in meinem ' + mofi.houseSun + '. Haus.') : '';
    chap.push('Die Mondfinsternis auf meiner Achse. Ein Vollmond spannt immer eine Achse auf. ' + axTxt + ' Beschreibe, was in diesem Spannungsfeld seit Monaten gewachsen ist, jetzt voll ist und sich um den 28. August zeigen oder lösen will.' + ((mofi.hits || []).length ? '' : ' Die Mondfinsternis bildet keine engen Aspekte zu meinen Punkten. Lies sie über die Achse, dort liegt ihre Botschaft.'));

    if((mofi.hits || []).length){
      chap.push('Direkte Treffer der Mondfinsternis. Geh jeden Aspekt durch, den die Mondfinsternis zu meinen natalen Punkten bildet. Erkläre für jeden, was der Aspekt bedeutet und was er in genau diesem Punkt meiner Chart auslöst. Beginne mit dem engsten Orb.');
    }

    if(cr && crHit){
      chap.push('Der Treffer auf meinen Chartruler. Der Herrscher meines Aszendenten ist ' + cr.name + (cr.sign ? (', er steht in ' + cr.sign) : '') + (cr.house ? (' in meinem ' + cr.house + '. Haus') : '') + ' und lenkt meine Chart. Eine Finsternis berührt ihn direkt, du findest den Aspekt oben mit dem Vermerk CHARTRULER. Widme diesem Treffer einen eigenen Absatz: Wenn der Lenker der Chart getroffen wird, verschiebt sich die Richtung des ganzen Lebens spürbarer als bei jedem anderen Punkt.');
    }

    chap.push('Die Richtung. Die Mondknotenachse der Finsternisse läuft bei mir durch' + ((node.houseNN && node.houseSN) ? (' mein ' + node.houseNN + '. und mein ' + node.houseSN + '. Haus') : ' meine Häuser') + '. Lies sie als Richtungsgeber dieses Fensters: wohin das Leben mich zieht und was ich dafür lassen darf. Vergleiche sie mit meinen natalen Mondknoten in den Daten unten, meinem Seelenweg von Geburt an: Wo bestätigt das Finsternis-Fenster meinen Weg, wo fordert es einen neuen Schritt?');

    chap.push('Meine Lichter. Eine Sonnenfinsternis berührt das Sonnen-Prinzip: Identität, Ausdruck, Lebenskraft. Eine Mondfinsternis berührt das Mond-Prinzip: Gefühl, Bedürfnis, Nährung. Lies meine natale Sonne und meinen natalen Mond aus den Daten unten: wie diese beiden Kräfte bei mir angelegt sind und was die Finsternisse in ihnen aktivieren.');

    chap.push('Schatten und Geschenk. Der Schatten dieser Wochen: Ich will im Außen erzwingen, was innen reifen will, ich deute jede Unruhe als Zeichen und ich treffe große Entscheidungen aus der Angst, etwas zu verpassen. Das Geschenk: Ich erkenne, welches Kapitel bei mir beginnt und welches sich vollendet, und ich gebe beidem Raum. Sag mir, woran ich bei mir erkenne, ob ich im Schatten oder im Geschenk unterwegs bin.');

    chap.push('Mein Finsternis-Fenster. Formuliere aus allem einen roten Faden für die Zeit von August 2026 bis Anfang 2027: ein einziger Satz in der Ich-Form, den ich mir aufschreiben kann. Dazu eine kleine, konkrete Handlung für die Tage zwischen den beiden Finsternissen, vom 12. bis zum 28. August, die zu meiner Chart passt.');

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
      data.push('Die Sonnenfinsternis bildet keine engen Aspekte (Orb bis 3°) zu meinen natalen Punkten.');
    }
    data.push('Mondfinsternis am 28.08.2026: Mond ' + (mofi.moonText || '4°54\' Fische') + (mofi.houseMoon ? (' in meinem ' + mofi.houseMoon + '. Haus') : '') + ', Sonne gegenüber ' + (mofi.sunText || '4°54\' Jungfrau') + (mofi.houseSun ? (' in meinem ' + mofi.houseSun + '. Haus') : '') + '.');
    if((mofi.hits || []).length){
      data.push('Aspekte der Mondfinsternis (Mondposition) zu meinen natalen Punkten:');
      mofi.hits.forEach(function(h){ data.push(hitLine(h, 'Mondfinsternis')); });
    } else {
      data.push('Die Mondfinsternis bildet keine engen Aspekte (Orb bis 3°) zu meinen natalen Punkten.');
    }
    data.push('Mondknotenachse zur Zeit der Sonnenfinsternis: Nordknoten ' + (node.sofiText || '') + (node.houseNN ? (' in meinem ' + node.houseNN + '. Haus') : '') + ', Südknoten ' + (node.snText || '') + (node.houseSN ? (' in meinem ' + node.houseSN + '. Haus') : '') + '.');
    if(node.signChange){
      data.push('Zur Mondfinsternis steht der Nordknoten bei ' + (node.mofiText || '') + ': Die Achse wechselt genau zwischen den beiden Finsternissen das Zeichen.');
    }
    if(E.natalNodes && E.natalNodes.nn && E.natalNodes.nn.sign){
      data.push('Meine natalen Mondknoten (mein Seelenweg): Nordknoten in ' + E.natalNodes.nn.sign + (E.natalNodes.nn.house ? (', ' + E.natalNodes.nn.house + '. Haus') : '') + (E.natalNodes.snSign ? (', Südknoten in ' + E.natalNodes.snSign + (E.natalNodes.snHouse ? (', ' + E.natalNodes.snHouse + '. Haus') : '')) : '') + '.');
    }
    if(cr){
      data.push('Mein Chartruler (Herrscher meines Aszendenten im Zeichen ' + cr.acSign + '): ' + cr.name + (cr.sign ? (' in ' + cr.sign) : '') + (cr.house ? (', ' + cr.house + '. Haus') : '') + (cr.co ? (' (Mitherrscher: ' + cr.co + ')') : '') + '.');
    }
    if(E.natalSun && E.natalSun.sign) data.push('Meine natale Sonne: ' + E.natalSun.sign + (E.natalSun.house ? (', ' + E.natalSun.house + '. Haus') : ''));
    if(E.natalMoon && E.natalMoon.sign) data.push('Mein nataler Mond: ' + E.natalMoon.sign + (E.natalMoon.house ? (', ' + E.natalMoon.house + '. Haus') : ''));
    data.push('');
    data.push('MEIN VOLLSTÄNDIGES CHART (Placidus-Häuser):');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });
    if(ASP.length){
      data.push('');
      data.push('MEINE WICHTIGSTEN NATALEN ASPEKTE:');
      ASP.forEach(function(a){ data.push(a.p1 + (a.s1 ? (' in ' + a.s1) : '') + ' ' + a.type + ' ' + a.p2 + (a.s2 ? (' in ' + a.s2) : '')); });
    }
    const full = ECLIPSE_INTRO + '\n\n' + chapters + '\n\n' + ECLIPSE_CLOSING + '\n\n' + data.join('\n');
    const btn = document.getElementById('copyEclBtn');
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

print("OK ->", DST)
print("OK ->", os.path.join(NETLIFY, "index.html"))
print("Groesse:", len(s), "Zeichen")
