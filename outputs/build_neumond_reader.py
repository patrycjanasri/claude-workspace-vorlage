#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut den Neumond-Reader aus dem Business-Reader.
Muster: build_venus_chiron_reader.py (Zwei-Punkte-Transit, Placidus,
Womancode Wein/Gold). Gleiches Design + gleiche Astro-Engine, nur das
Reading-Gehirn wird getauscht.

Der Reader rechnet ZWEI Charts mit derselben Engine:
  1. das Geburtshoroskop der Nutzerin (PLACIDUS)
  2. den Neumond-Moment: 14.07.2026, 11:45 Uhr MESZ (Sonne und Mond beide
     21°59' Krebs, engine-verifiziert; Merkur rueckläufig 19°51' Krebs,
     2°08' vom Neumond; Berlin als Ort, nur fuer die Zeitzone)

Der Reader zieht automatisch:
  - den exakten Grad des Neumonds (= Transit-Sonne) und des rueckl. Merkur
  - das Placidus-Haus, in das der Neumond faellt (DORT wird gesaet —
    Patrycjas Kernfrage "welches Haus beruehrt der Neumond bei dir")
  - das Placidus-Haus des rueckl. Merkur (von dort kehrt ein Thema zurueck)
  - eigene Punkte im Krebs (der Neumond aktiviert sie direkt)
  - Aspekte von Neumond UND Merkur zu den natalen Punkten (Orb 3 Grad)
  - natalen Mond (wie ich naehre/genaehrt werde) + natalen Merkur (Denken)
und baut einen fertigen KI-Prompt zum Kopieren.

Geburtsdatum als Tippfeld TT.MM.JJJJ (Muster build_reise_reader.py,
Patrycjas Feedback 13.07.: Date-Picker ist muehsam).

Kein E-Mail-Gate. Abschluss-CTA -> Womancode (Start 22.07.).

Quelle:  astro-business-reader.html
Ziel:    astro-neumond-reader.html (+ astro-neumond-reader-netlify/index.html)
"""
import os, re, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-neumond-reader.html")
NETLIFY = os.path.join(HERE, "astro-neumond-reader-netlify")
READER = os.path.join(HERE, "womancode-reader.html")

# Gold-"Woman CODE"-Logo + Wein/Lotus-Hintergrund direkt aus dem Womancode-Reader
with open(READER, encoding="utf-8") as f:
    _reader = f.read()
LOGO = re.search(r'class="wc-logo"\s+src="(data:image/png;base64,[^"]+)"', _reader).group(1)
HERO = re.search(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', _reader).group(0)

# --- Neumond-Moment (lokale Zeit, Engine loest Zeitzone ueber Koordinaten) --
T_YEAR, T_MONTH, T_DATE = 2026, 7, 14     # 14.07.2026
T_HOUR, T_MINUTE = 11, 45                  # 11:45 Uhr MESZ (exakt, engine-verifiziert)
T_LAT, T_LON = 52.52, 13.405               # Berlin (nur fuer die Zeitzone)

with open(SRC, "r", encoding="utf-8") as f:
    s = f.read()

def repl(old, new, label):
    global s
    if old not in s:
        sys.exit("FEHLT (" + label + "): " + old[:80])
    s = s.replace(old, new, 1)

# --- 1. Branding / sichtbare Texte ---------------------------------------
repl("<title>Dein Business-Code</title>",
     "<title>Neumond im Krebs · Dein Neumond-Reader</title>", "title")

repl('<p class="header-eyebrow">Dein kosmischer Business-Blueprint</p>',
     '<img class="wc-logo" src="' + LOGO + '" alt="Womancode">\n    <p class="header-eyebrow">Neumond vom 14. Juli 2026</p>', "eyebrow")

repl("<h1>Dein Business-Code</h1>",
     "<h1>Neumond im Krebs</h1>", "h1")

repl('<p class="subtitle">Gib deine Geburtsdaten ein. Auf der nächsten Seite bekommst du dein Geburtshoroskop angezeigt und einen fertigen KI-Prompt, der dir sagt, wie du dein Business führst, dich positionierst, skalierst und Geld verdienst.</p>',
     '<p class="subtitle">Ein neuer Zyklus beginnt, doch sein Ursprung liegt in einem Thema, das zu dir zurückkehrt. Gib deine Geburtsdaten ein. Die Seite berechnet dein Geburtshoroskop, zeigt dir, in welches Haus der Neumond fällt, und erstellt einen fertigen KI-Prompt für dein persönliches Neumond-Reading.</p>',
     "subtitle")

repl('onclick="runCheck()">Meinen Business-Code aufdecken</button>',
     'onclick="runCheck()">Meinen Neumond aufdecken</button>', "submit-btn")

# --- E-Mail komplett entfernen (kein Opt-in, wie beim Venus-Chiron-Reader) --
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
     "<h2>Dein Neumond im Krebs${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Neumond im Krebs beim rückläufigen Merkur'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Neue Chart erstellen", "back-btn")

# --- 4. Neumond-Berechnung in runCheck einhaengen --------------------------
# Anker NACH window.__chart, damit __fullChart und __aspects bereits gesetzt sind.
calc_anchor = "      window.__chart = chart;\n      generateReading();"
transit_calc = """      window.__chart = chart;

      // Neumond-Transit: zweites Chart fuer den exakten Moment rechnen.
      // Ort Berlin, weil die Planeten-Laengen ortsunabhaengig sind, die Engine
      // braucht die Koordinaten nur fuer die Zeitzone (11:45 Uhr Sommerzeit).
      (function(){
        try{
          const tOrigin = new Origin({ year: __T_YEAR__, month: __T_MONTH0__, date: __T_DATE__, hour: __T_HOUR__, minute: __T_MINUTE__, latitude: __T_LAT__, longitude: __T_LON__ });
          const tHoro = new Horoscope({ origin: tOrigin, houseSystem: 'placidus', zodiac: 'tropical', language: 'en', aspectTypes: ['major'] });
          const lonOf = function(b){ try{ return b.ChartPosition.Ecliptic.DecimalDegrees; }catch(e){ return null; } };
          const tSun = lonOf(tHoro.CelestialBodies.sun);
          const tMercury = lonOf(tHoro.CelestialBodies.mercury);
          if(tSun == null || tMercury == null) return;
          const SIGNS_DE = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische'];
          const fmtDeg = function(L){
            const inSign = L % 30;
            let d = Math.floor(inSign);
            let m = Math.round((inSign - d) * 60);
            if(m === 60){ m = 0; d += 1; }
            return d + '°' + (m < 10 ? '0' : '') + m + "' " + (SIGNS_DE[Math.floor(L / 30)] || '');
          };

          // Placidus-Haus des exakten Neumond-Grads: ueber die natalen Haeuserspitzen
          // (Muster: build_chiron_reader.py, houseOfLong)
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
          const newmoonHouse = houseOfLong(tSun);
          const mercuryHouse = houseOfLong(tMercury);

          // Eigene Punkte im Krebs (der Neumond aktiviert sie direkt)
          const cancerPoints = FULL.filter(function(e){ return e.sign === 'Krebs'; });

          // Aspekte von Neumond UND Merkur zu den natalen Punkten (Transit-Orb: 3 Grad)
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
          const hits = [];
          const collect = function(T, who){
            NATAL.forEach(function(pair){
              const L = lonOf(pair[1]);
              if(L == null) return;
              const d = Math.abs(((T - L + 540) % 360) - 180); // Winkelabstand 0..180
              TYPES.forEach(function(t){
                const orb = Math.abs(d - t[0]);
                if(orb <= 3) hits.push({ who: who, point: pair[0], sign: SIGNOF[pair[0]] || '', house: HOUSEOF[pair[0]] || '', type: t[1], orb: Math.round(orb * 10) / 10 });
              });
            });
          };
          collect(tSun, 'Neumond');
          collect(tMercury, 'Merkur');
          hits.sort(function(a, b){ return a.orb - b.orb; });

          const moonEntry = FULL.find(function(e){ return e.label === 'Mond'; }) || {};
          const mercuryEntry = FULL.find(function(e){ return e.label === 'Merkur'; }) || {};
          window.__transit = {
            moonText: fmtDeg(tSun),
            mercuryText: fmtDeg(tMercury),
            newmoonHouse: newmoonHouse,
            mercuryHouse: mercuryHouse,
            cancerPoints: cancerPoints,
            hits: hits,
            natalMoon: { sign: moonEntry.sign || '', house: moonEntry.house || '' },
            natalMercury: { sign: mercuryEntry.sign || '', house: mercuryEntry.house || '' }
          };
        }catch(e){ window.__transit = null; }
      })();

      generateReading();"""
transit_calc = (transit_calc
    .replace("__T_YEAR__", str(T_YEAR))
    .replace("__T_MONTH0__", str(T_MONTH - 1))
    .replace("__T_DATE__", str(T_DATE))
    .replace("__T_HOUR__", str(T_HOUR))
    .replace("__T_MINUTE__", str(T_MINUTE))
    .replace("__T_LAT__", str(T_LAT))
    .replace("__T_LON__", str(T_LON)))
repl(calc_anchor, transit_calc, "transit-calc-injection")

# --- 4b. Ergebnis-Seite verschlanken (Patrycja 14.07.): Platzierungen, ------
# Aspekte und Element-Block raus. Nur Neumond-Thema + Prompt bleiben sichtbar.
# Chart + Aspekte stecken weiter unsichtbar im kopierten Neumond-Prompt.
# REGEL AB JETZT: Reader-Ergebnisseiten immer schlank bauen, volle Bloecke
# nur wenn Patrycja es explizit will.
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

# --- 5. Reading-Block: sichtbares Neumond-Thema + Prompt-CTA ---------------
old_cta = """  html += `
  <div class="cta-block">
    <h3>Dein Business-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, wie du dein Business führst, wie du dich positionierst, wo deine Zone of Genius liegt und wie du am natürlichsten Geld verdienst.</p>
    <button class="copy-btn" id="copyBizBtn" onclick="copyBusinessReading()">Business-Prompt + Daten kopieren</button>
  </div>`;"""

new_cta = """  // Sichtbares Neumond-Thema
  const T = window.__transit || null;
  if(T){
    let tHtml = `
    <div class="data-block">
      <h3>Dein Neumond-Thema</h3>
      <div class="data-grid">`;
    if(T.moonText) tHtml += `<div class="data-row"><span class="data-planet">Der Neumond steht bei</span><span class="data-values"><span class="badge sign-badge">${T.moonText}</span></span></div>`;
    if(T.mercuryText) tHtml += `<div class="data-row"><span class="data-planet">Der rückläufige Merkur steht bei</span><span class="data-values"><span class="badge sign-badge">${T.mercuryText}</span></span></div>`;
    if(T.newmoonHouse) tHtml += `<div class="data-row"><span class="data-planet">Der Neumond fällt in dein</span><span class="data-values"><span class="badge house-badge">${T.newmoonHouse}. Haus</span></span></div>`;
    if(T.mercuryHouse) tHtml += `<div class="data-row"><span class="data-planet">Merkur läuft durch dein</span><span class="data-values"><span class="badge house-badge">${T.mercuryHouse}. Haus</span></span></div>`;
    const canP = (T.cancerPoints || []).map(function(e){ return e.label; });
    tHtml += `<div class="data-row"><span class="data-planet">Deine Punkte im Krebs</span><span class="data-values"><span class="badge sign-badge">${canP.length ? canP.join(', ') : 'keine'}</span></span></div>`;
    const hitStr = (T.hits || []).map(function(h){ return h.who + ' ' + h.type + ' ' + h.point; }).join(', ');
    tHtml += `<div class="data-row"><span class="data-planet">Der Neumond trifft</span><span class="data-values"><span class="badge sign-badge">${hitStr || 'keine engen Aspekte'}</span></span></div>`;
    if(T.natalMoon.sign) tHtml += `<div class="data-row"><span class="data-planet">Dein nataler Mond</span><span class="data-values"><span class="badge sign-badge">${T.natalMoon.sign}</span>${T.natalMoon.house ? `<span class="badge house-badge">${T.natalMoon.house}. Haus</span>` : ''}</span></div>`;
    if(T.natalMercury.sign) tHtml += `<div class="data-row"><span class="data-planet">Dein nataler Merkur</span><span class="data-values"><span class="badge sign-badge">${T.natalMercury.sign}</span>${T.natalMercury.house ? `<span class="badge house-badge">${T.natalMercury.house}. Haus</span>` : ''}</span></div>`;
    tHtml += `</div></div>`;
    html += tHtml;
  }

  html += `
  <div class="cta-block">
    <h3>Dein Neumond-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, welches Thema dieser Neumond bei dir neu beginnt, in welchem Lebensbereich er wirkt und welche Intention jetzt Kraft hat.</p>
    <button class="copy-btn" id="copyMoonBtn" onclick="copyNewmoonReading()">Neumond-Prompt + Daten kopieren</button>
  </div>`;"""
repl(old_cta, new_cta, "cta-block")

# --- 6. Abschluss-CTA: AstroCode raus, Womancode rein ----------------------
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
    <a href="https://patrycja-nasri.de/womancode/" target="_blank" class="cta-link">Hier geht's zu Womancode &rarr;</a>
  </div>`;''',
"womancode-cta")

# --- 7. Prompt-Gehirn + Copy-Funktion austauschen --------------------------
new_region = r"""  const NEWMOON_PROMPT = `Du bist eine erfahrene Bewusstseinsastrologin mit Fokus auf Transite und Mondzyklen. Du liest meine Chart in Schichten und schreibst klar, tief und direkt, so dass mich jeder Satz trifft. Keine Floskeln, keine allgemeinen Astro-Sätze, kein Lehrbuchton.

Das Ereignis: Am 14. Juli 2026 treffen sich Sonne und Mond bei 21°59' im Krebs: Neumond. Ein Neumond ist der Beginn eines neuen Mondzyklus, der Moment der Aussaat. Was hier gesät wird, wächst mit dem zunehmenden Licht und entfaltet sich über die kommenden Wochen. Der Krebs ist das Zeichen des Mondes selbst. Hier geht es um Ursprung, Familie, Zuhause, Nähe und die Frage, was mich wirklich nährt. Gut zwei Grad neben dem Neumond steht Merkur im Krebs, und er läuft rückläufig. Ein rückläufiger Merkur wendet das Denken nach innen, Gedanken kehren zu Themen zurück, die ich für abgeschlossen gehalten habe. Dieser Neumond beginnt deshalb nichts Fremdes: er pflanzt etwas neu ein, das zu mir zurückkehrt. Die Energie wirkt über den ganzen Mondzyklus, am stärksten in den ersten Tagen.

Wichtig: Ich arbeite mit Placidus-Häusern. Alle Häuser in meinen Daten unten sind Placidus-Häuser.

Unten bekommst du:
- den genauen Grad des Neumonds und des rückläufigen Merkur
- das Haus, in das der Neumond bei mir fällt (dort wird gesät)
- das Haus, durch das der rückläufige Merkur läuft (von dort kehrt ein Thema zurück)
- die Punkte, die ich selbst im Krebs habe (der Neumond aktiviert sie direkt)
- die Aspekte, die der Neumond und Merkur zu meinen natalen Punkten bilden (mit Orb, je enger, desto stärker)
- meinen natalen Mond (wie ich nähre und genährt werden will) und meinen natalen Merkur (wie ich denke und spreche)
- mein vollständiges Chart als Kontext

Schreibe mir auf dieser Basis:

1. Das Thema. Ein kraftvoller Absatz: was dieser Neumond bei mir neu beginnen will und welches Thema der rückläufige Merkur dafür noch einmal zu mir zurückbringt. Sprich mich direkt mit du an.

2. Wo es beginnt. Nimm das Haus, in das der Neumond bei mir fällt: in diesem Lebensbereich wird jetzt gesät. Mach konkret, wie sich dieser Bereich in meinem Alltag zeigt und was dort ein neues Kapitel bekommen darf. Läuft Merkur durch ein anderes Haus, nimm es dazu: von dort kommt das Thema zurück.

3. Direkte Treffer. Geh jeden Punkt durch, den ich selbst im Krebs habe. Der Neumond aktiviert diese Punkte direkt. Sag mir für jeden, was er in mir trägt und was der Neumond dort neu beginnen will. Habe ich keine Punkte im Krebs, vertiefe stattdessen das Neumond-Haus.

4. Die Aspekte. Geh jeden Aspekt durch, den der Neumond oder der rückläufige Merkur zu meinen natalen Punkten bildet. Erkläre für jeden, was der Aspekt bedeutet und was er in genau diesem Punkt meiner Chart auslöst. Beginne mit dem engsten Orb, der wirkt am stärksten.

5. Meine Verdrahtung. Lies meinen natalen Mond nach Zeichen und Haus: so wurde ich genährt, so nähre ich, das braucht mein Gefühlskörper wirklich. Lies dann meinen natalen Merkur: so denke und spreche ich. Verbinde beides: Welches Bedürfnis kenne ich seit meiner Kindheit, und was davon habe ich bis heute nicht ausgesprochen?

6. Schatten und Geschenk. Der Schatten dieses Neumonds: Ich kümmere mich um alle und vergesse mein eigenes Bedürfnis, ich ziehe mich zurück, statt zu sagen, was ich brauche, und ich rühre in alten Geschichten, statt neu zu säen. Das Geschenk: Ich erkenne, was mich wirklich nährt, ich richte mir ein Zuhause in mir selbst ein, und meine Intention kommt aus der Tiefe statt aus dem Kopf. Sag mir, woran ich bei mir erkenne, ob ich im Schatten oder im Geschenk unterwegs bin.

7. Meine Neumond-Intention. Formuliere aus allem eine Intention für diesen Zyklus: ein einziger Satz in der Ich-Form, den ich mir aufschreiben kann. Dazu eine kleine, konkrete Handlung für die ersten Tage nach dem Neumond, etwas, das mich nährt und zu meiner Chart passt.

8. Meine Neumond-Frage. Eine einzige, konfrontierende Frage zu dem, was in mir ein Zuhause braucht, damit es wachsen kann.

Schreib auf Deutsch, in der Du-Form, in Tiefe statt in Breite. Jeder Satz konkret. Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker.

Hier sind meine Daten:`;

  window.copyNewmoonReading = function(){
    const FULL = window.__fullChart || [];
    const ASP = window.__aspects || [];
    const T = window.__transit || {};
    const m = window.__meta || {};
    const data = [];
    if(m.name) data.push('Name: ' + m.name);
    if(m.date){ const dp = m.date.split('-'); data.push('Geburtsdatum: ' + dp[2]+'.'+dp[1]+'.'+dp[0] + (m.time ? (' um ' + m.time + ' Uhr') : '')); }
    if(m.place) data.push('Geburtsort: ' + m.place);
    data.push('');
    data.push('MEIN NEUMOND IM KREBS (exakt am 14. Juli 2026):');
    if(T.moonText) data.push('Der Neumond steht bei ' + T.moonText + ' (Sonne und Mond auf demselben Grad).');
    if(T.mercuryText) data.push('Der rückläufige Merkur steht bei ' + T.mercuryText + '.');
    if(T.newmoonHouse) data.push('Der Neumond fällt in mein ' + T.newmoonHouse + '. Haus. Dort wird gesät.');
    if(T.mercuryHouse) data.push('Der rückläufige Merkur läuft durch mein ' + T.mercuryHouse + '. Haus. Von dort kehrt ein Thema zurück.');
    const canP = (T.cancerPoints || []).map(function(e){ return e.label + (e.house ? (' (' + e.house + '. Haus)') : ''); });
    data.push('Punkte, die ich selbst im Krebs habe (der Neumond aktiviert sie direkt): ' + (canP.length ? canP.join(', ') : 'keine') + '.');
    const hits = T.hits || [];
    if(hits.length){
      data.push('Aspekte von Neumond und Merkur zu meinen natalen Punkten (engster Orb wirkt am stärksten):');
      hits.forEach(function(h){ data.push('- ' + (h.who === 'Neumond' ? 'Neumond' : 'Transit-Merkur') + ' ' + h.type + ' zu ' + h.point + (h.sign ? (' in ' + h.sign) : '') + (h.house ? (', ' + h.house + '. Haus') : '') + ' (Orb ' + String(h.orb).replace('.', ',') + '°)'); });
    } else {
      data.push('Der Neumond und Merkur bilden keine engen Aspekte (Orb bis 3°) zu meinen natalen Punkten. Arbeite mit dem Neumond-Haus und meiner Verdrahtung.');
    }
    if(T.natalMoon && T.natalMoon.sign) data.push('Mein nataler Mond: ' + T.natalMoon.sign + (T.natalMoon.house ? (', ' + T.natalMoon.house + '. Haus') : '') + '.');
    if(T.natalMercury && T.natalMercury.sign) data.push('Mein nataler Merkur: ' + T.natalMercury.sign + (T.natalMercury.house ? (', ' + T.natalMercury.house + '. Haus') : '') + '.');
    data.push('');
    data.push('MEIN VOLLSTÄNDIGES CHART (Placidus-Häuser):');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });
    if(ASP.length){
      data.push('');
      data.push('MEINE WICHTIGSTEN NATALEN ASPEKTE:');
      ASP.forEach(function(a){ data.push(a.p1 + (a.s1 ? (' in ' + a.s1) : '') + ' ' + a.type + ' ' + a.p2 + (a.s2 ? (' in ' + a.s2) : '')); });
    }
    const full = NEWMOON_PROMPT + '\n\n' + data.join('\n');
    const btn = document.getElementById('copyMoonBtn');
    const done = function(){ if(btn){ const o = btn.getAttribute('data-label') || btn.textContent; btn.setAttribute('data-label', o); btn.textContent = '✓ Kopiert! Jetzt in ChatGPT einfügen'; setTimeout(function(){ btn.textContent = o; }, 2800); } };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(full).then(done).catch(function(){ fallbackCopy(full, done); });
    } else { fallbackCopy(full, done); }
  };"""

pat = re.compile(r"  const BUSINESS_PROMPT = `.*?\n  window\.copyBusinessReading = function\(\)\{.*?\n  \};", re.DOTALL)
if not pat.search(s):
    sys.exit("FEHLT: BUSINESS_PROMPT / copyBusinessReading Region")
s = pat.sub(lambda _: new_region, s, count=1)

# --- 8. Womancode Wein/Gold-Design als Override-Layer (gewinnt, weil zuletzt im Head)
extra_css = '''<style>
:root{ --gold:#E1BE7E; --gold-light:#F6E6C2; --rose:#B4884A; --bg:#1A060C;
  --burgundy:#3A0D1A; --deep-purple:#2A0710; --mid-purple:#3A0D1A;
  --text:#F0E4D6; --text-muted:#C6A896; --accent-purple:#7A1230; }
body{ background-color:#1A060C !important; }
#binary-canvas{ display:none !important; }
body::after{ content:"" !important; position:fixed; inset:0; z-index:0; pointer-events:none;
  background:
    radial-gradient(circle at 18% 12%, rgba(92,10,40,0.55), transparent 44%),
    radial-gradient(circle at 82% 80%, rgba(58,13,26,0.7), transparent 48%),
    radial-gradient(circle at 50% 118%, rgba(225,190,126,0.10), transparent 55%); }
.moon-scene{ background:url("__HERO__") center top / cover no-repeat !important; opacity:0.92; }
header h1{ text-shadow:0 0 42px rgba(92,10,40,0.85), 0 0 90px rgba(225,190,126,0.25) !important; }
/* Kopf beruhigen (Patrycja 14.07.: wirkt zu groß, zu viel). Eyebrow klein
   in Lesschrift statt fetter Display-Schrift, Intro-Text in normaler
   Lesschrift mit dezenter Groesse — REGEL fuer alle Reader. */
.header-eyebrow{
  font-family:'Inter','Helvetica Neue',sans-serif !important;
  font-size:0.72rem !important;
  font-weight:600 !important;
  letter-spacing:0.3em !important;
  color:var(--gold) !important;
}
/* Die H1 darf auffaellig sein (Patrycja 14.07.) — sie traegt allein die Buehne. */
header h1{
  font-size:clamp(1.9rem, 7vw, 3rem) !important;
  line-height:1.15 !important;
}
.subtitle{
  font-family:'Inter','Helvetica Neue',sans-serif !important;
  font-style:normal !important;
  font-size:1rem !important;
  line-height:1.75 !important;
  letter-spacing:0.01em !important;
  color:#EFD9C2 !important;
  max-width:520px !important; margin:0 auto !important;
}
.results-header h2{ text-shadow:0 0 42px rgba(92,10,40,0.85), 0 0 90px rgba(225,190,126,0.2) !important; }
.results-header p{ color:#EFD9C2 !important; }
.tip-box, .form-section, .reading-block, .summary-block, .data-block, .cta-block{
  background:rgba(42,7,16,0.55) !important;
  border:1px solid rgba(225,190,126,0.22) !important;
  box-shadow:0 18px 70px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.05) !important; }
.tip-box{ border-left:3px solid var(--gold) !important; }
input[type="text"], input[type="date"], input[type="time"]{
  background:rgba(255,255,255,0.04) !important; border:1px solid rgba(225,190,126,0.22) !important; }
input[type="text"]:focus, input[type="date"]:focus, input[type="time"]:focus{
  border-color:rgba(225,190,126,0.6) !important; box-shadow:0 0 28px rgba(225,190,126,0.18) !important; }
.place-results{ background:#2A0710 !important; border:1px solid rgba(225,190,126,0.3) !important; }
.place-item:hover, .place-item.active{ background:rgba(225,190,126,0.15) !important; }
select option{ background:#2A0710 !important; color:#F0E4D6 !important; }
.sign-badge{ background:rgba(92,10,40,0.55) !important; border:1px solid rgba(225,190,126,0.3) !important; color:#F6E6C2 !important; }
.house-badge{ background:rgba(225,190,126,0.14) !important; border:1px solid rgba(225,190,126,0.3) !important; color:#F6E6C2 !important; }
.submit-btn, .cta-link{
  background:linear-gradient(135deg, #E1BE7E 0%, #F6E6C2 50%, #E1BE7E 100%) !important;
  color:#2A0710 !important;
  box-shadow:0 10px 42px rgba(225,190,126,0.4), inset 0 0 0 1px rgba(255,255,255,0.12) !important; }
.submit-btn:hover, .cta-link:hover{ box-shadow:0 16px 60px rgba(225,190,126,0.6) !important; }
.copy-btn{ background:linear-gradient(135deg, #E1BE7E 0%, #F6E6C2 50%, #E1BE7E 100%) !important;
  color:#2A0710 !important; box-shadow:0 10px 42px rgba(225,190,126,0.35) !important; border:none !important; }
.wc-logo{ display:block; margin:0 auto 20px; width:min(300px, 68vw); height:auto; }
</style>
</head>'''.replace("__HERO__", HERO)
repl('</head>', extra_css, "womancode-css")

# Sicherheitscheck: keine Business-Reste mehr in Logik-Hooks
for leftover in ["copyBusinessReading", "copyBizBtn", "BUSINESS_PROMPT", "subscribeLead", "userEmail", "Business-Code", "Business-Blueprint"]:
    if leftover in s:
        sys.exit("REST gefunden: " + leftover)

with open(DST, "w", encoding="utf-8") as f:
    f.write(s)

os.makedirs(NETLIFY, exist_ok=True)
shutil.copyfile(DST, os.path.join(NETLIFY, "index.html"))

print("OK ->", DST)
print("OK ->", os.path.join(NETLIFY, "index.html"))
print("Groesse:", len(s), "Zeichen")
