#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut den Venus-Chiron-Transit-Reader aus dem Business-Reader.
Muster: build_transit_reader.py (Mars/Uranus). Gleiches Design + gleiche
Astro-Engine, nur das Reading-Gehirn wird getauscht.

Der Reader rechnet ZWEI Charts mit derselben Engine:
  1. das Geburtshoroskop der Nutzerin (PLACIDUS — Patrycjas Wunsch 10.07.,
     anders als der Mars/Uranus-Reader mit Ganzzeichen)
  2. den Transit-Moment: 10.07.2026, 10:45 Uhr (Venus in der Jungfrau
     im exakten Trigon zu Chiron im Stier, engine-verifiziert 120,00 Grad,
     Berlin als Ort, nur fuer die Zeitzone)

Anders als beim Mars/Uranus-Reader (Konjunktion = EIN Punkt) hat dieser
Transit ZWEI Punkte in zwei Zeichen. Der Reader zieht automatisch:
  - die exakten Grade von Transit-Venus und Transit-Chiron
  - das Placidus-Haus, durch das Transit-Chiron laeuft (Wund-Thema) und
    das Placidus-Haus, durch das Transit-Venus laeuft (Fuersorge-Quelle),
    per houseOfLong ueber die Haeuserspitzen (Muster: build_chiron_reader.py)
  - eigene Punkte in Stier und Jungfrau (der Transit laeuft darueber)
  - Aspekte BEIDER Transit-Punkte zu den natalen Punkten (Orb 3 Grad)
  - natale Venus + nataler Chiron (die eigene Wunde! Kern der Frage
    "welches eigene Thema wird beruehrt")
und baut einen fertigen KI-Prompt zum Kopieren.

Design: Womancode Wein/Gold (Patrycjas Wunsch 10.07.) — Logo + Lotus/
Goldschwingen-Hero aus womancode-reader.html, CSS-Override-Layer wie
build_womancode_check.py. Uhrzeit im sichtbaren Text weggelassen.

Quelle:  astro-business-reader.html
Ziel:    astro-venus-chiron-reader.html (+ astro-venus-chiron-reader-netlify/index.html)
"""
import os, re, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-venus-chiron-reader.html")
NETLIFY = os.path.join(HERE, "astro-venus-chiron-reader-netlify")
READER = os.path.join(HERE, "womancode-reader.html")

# Gold-"Woman CODE"-Logo + Wein/Lotus-Hintergrund direkt aus dem Womancode-Reader
with open(READER, encoding="utf-8") as f:
    _reader = f.read()
LOGO = re.search(r'class="wc-logo"\s+src="(data:image/png;base64,[^"]+)"', _reader).group(1)
HERO = re.search(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', _reader).group(0)

# --- Transit-Moment (lokale Zeit, Engine loest Zeitzone ueber Koordinaten) --
T_YEAR, T_MONTH, T_DATE = 2026, 7, 10     # 10.07.2026
T_HOUR, T_MINUTE = 10, 45                  # 10:45 Uhr (exakt, engine-verifiziert)
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
     "<title>Venus im Trigon zu Chiron · Dein Transit-Code</title>", "title")

repl('<p class="header-eyebrow">Dein kosmischer Business-Blueprint</p>',
     '<img class="wc-logo" src="' + LOGO + '" alt="Womancode">\n    <p class="header-eyebrow">Transit vom 10. Juli 2026</p>', "eyebrow")

repl("<h1>Dein Business-Code</h1>",
     "<h1>Venus im Trigon zu Chiron</h1>", "h1")

repl('<p class="subtitle">Gib deine Geburtsdaten ein. Auf der nächsten Seite bekommst du dein Geburtshoroskop angezeigt und einen fertigen KI-Prompt, der dir sagt, wie du dein Business führst, dich positionierst, skalierst und Geld verdienst.</p>',
     '<p class="subtitle">Am Freitag, den 10. Juli 2026 steht Venus in der Jungfrau im exakten Trigon zu Chiron im Stier. Fürsorge erreicht die Wunde um den Wert. Gib deine Geburtsdaten ein. Die Seite rechnet dein Geburtshoroskop, zeigt dir, wo das Trigon bei dir wirkt und wo deine eigene Chiron-Wunde sitzt, und baut dir einen fertigen KI-Prompt für deine persönliche Transitanalyse.</p>',
     "subtitle")

repl('onclick="runCheck()">Meinen Business-Code aufdecken</button>',
     'onclick="runCheck()">Meinen Transit aufdecken</button>', "submit-btn")

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

# --- 2. Haeusersystem: PLACIDUS bleibt (Original des Business-Readers) -----
# Patrycja will fuer diesen Reader Placidus (10.07.), daher KEIN Umbau auf
# whole-sign wie beim Mars/Uranus-Reader.

# --- 3. Ergebnis-Kopf + Zurueck-Button ------------------------------------
repl("<h2>Dein Business-Code${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Dein Chart als Business-Blueprint'}</p>",
     "<h2>Dein Venus-Chiron-Transit${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Venus in der Jungfrau im Trigon zu Chiron im Stier'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Neue Chart erstellen", "back-btn")

# --- 4. Transit-Berechnung in runCheck einhaengen --------------------------
# Anker NACH window.__chart, damit __fullChart und __aspects bereits gesetzt sind.
calc_anchor = "      window.__chart = chart;\n      generateReading();"
transit_calc = """      window.__chart = chart;

      // Venus-Chiron-Transit: zweites Chart fuer den exakten Moment rechnen.
      // Ort Berlin, weil die Planeten-Laengen ortsunabhaengig sind, die Engine
      // braucht die Koordinaten nur fuer die Zeitzone (10:45 Uhr Sommerzeit).
      (function(){
        try{
          const tOrigin = new Origin({ year: __T_YEAR__, month: __T_MONTH0__, date: __T_DATE__, hour: __T_HOUR__, minute: __T_MINUTE__, latitude: __T_LAT__, longitude: __T_LON__ });
          const tHoro = new Horoscope({ origin: tOrigin, houseSystem: 'placidus', zodiac: 'tropical', language: 'en', aspectTypes: ['major'] });
          const lonOf = function(b){ try{ return b.ChartPosition.Ecliptic.DecimalDegrees; }catch(e){ return null; } };
          const tVenus = lonOf(tHoro.CelestialBodies.venus);
          const tChiron = lonOf(tHoro.CelestialBodies.chiron);
          if(tVenus == null || tChiron == null) return;
          const SIGNS_DE = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische'];
          const fmtDeg = function(L){
            const inSign = L % 30;
            let d = Math.floor(inSign);
            let m = Math.round((inSign - d) * 60);
            if(m === 60){ m = 0; d += 1; }
            return d + '°' + (m < 10 ? '0' : '') + m + "' " + (SIGNS_DE[Math.floor(L / 30)] || '');
          };

          // Placidus-Haus des exakten Transit-Grads: ueber die natalen Haeuserspitzen
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
          const chironHouse = houseOfLong(tChiron);
          const venusHouse = houseOfLong(tVenus);

          // Eigene Punkte in Stier und Jungfrau (der Transit laeuft darueber)
          const taurusPoints = FULL.filter(function(e){ return e.sign === 'Stier'; });
          const virgoPoints = FULL.filter(function(e){ return e.sign === 'Jungfrau'; });

          // Aspekte BEIDER Transit-Punkte zu den natalen Punkten (Transit-Orb: 3 Grad)
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
          collect(tVenus, 'Venus');
          collect(tChiron, 'Chiron');
          hits.sort(function(a, b){ return a.orb - b.orb; });

          const venusEntry = FULL.find(function(e){ return e.label === 'Venus'; }) || {};
          const chironEntry = FULL.find(function(e){ return e.label === 'Chiron'; }) || {};
          window.__transit = {
            venusText: fmtDeg(tVenus),
            chironText: fmtDeg(tChiron),
            chironHouse: chironHouse,
            venusHouse: venusHouse,
            taurusPoints: taurusPoints,
            virgoPoints: virgoPoints,
            hits: hits,
            natalVenus: { sign: venusEntry.sign || '', house: venusEntry.house || '' },
            natalChiron: { sign: chironEntry.sign || '', house: chironEntry.house || '' }
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

# --- 5. Reading-Block: sichtbares Transit-Thema + Prompt-CTA ---------------
old_cta = """  html += `
  <div class="cta-block">
    <h3>Dein Business-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, wie du dein Business führst, wie du dich positionierst, wo deine Zone of Genius liegt und wie du am natürlichsten Geld verdienst.</p>
    <button class="copy-btn" id="copyBizBtn" onclick="copyBusinessReading()">Business-Prompt + Daten kopieren</button>
  </div>`;"""

new_cta = """  // Sichtbares Venus-Chiron-Transit-Thema
  const T = window.__transit || null;
  if(T){
    let tHtml = `
    <div class="data-block">
      <h3>Dein Venus-Chiron-Thema</h3>
      <div class="data-grid">`;
    if(T.venusText) tHtml += `<div class="data-row"><span class="data-planet">Venus steht bei</span><span class="data-values"><span class="badge sign-badge">${T.venusText}</span></span></div>`;
    if(T.chironText) tHtml += `<div class="data-row"><span class="data-planet">Chiron steht bei</span><span class="data-values"><span class="badge sign-badge">${T.chironText}</span></span></div>`;
    if(T.chironHouse) tHtml += `<div class="data-row"><span class="data-planet">Chiron läuft durch dein</span><span class="data-values"><span class="badge house-badge">${T.chironHouse}. Haus</span></span></div>`;
    if(T.venusHouse) tHtml += `<div class="data-row"><span class="data-planet">Venus läuft durch dein</span><span class="data-values"><span class="badge house-badge">${T.venusHouse}. Haus</span></span></div>`;
    const tauP = (T.taurusPoints || []).map(function(e){ return e.label; });
    tHtml += `<div class="data-row"><span class="data-planet">Deine Punkte im Stier</span><span class="data-values"><span class="badge sign-badge">${tauP.length ? tauP.join(', ') : 'keine'}</span></span></div>`;
    const virP = (T.virgoPoints || []).map(function(e){ return e.label; });
    tHtml += `<div class="data-row"><span class="data-planet">Deine Punkte in der Jungfrau</span><span class="data-values"><span class="badge sign-badge">${virP.length ? virP.join(', ') : 'keine'}</span></span></div>`;
    const hitStr = (T.hits || []).map(function(h){ return h.who + ' ' + h.type + ' ' + h.point; }).join(', ');
    tHtml += `<div class="data-row"><span class="data-planet">Das Trigon trifft</span><span class="data-values"><span class="badge sign-badge">${hitStr || 'keine engen Aspekte'}</span></span></div>`;
    if(T.natalChiron.sign) tHtml += `<div class="data-row"><span class="data-planet">Dein nataler Chiron (deine Wunde)</span><span class="data-values"><span class="badge sign-badge">${T.natalChiron.sign}</span>${T.natalChiron.house ? `<span class="badge house-badge">${T.natalChiron.house}. Haus</span>` : ''}</span></div>`;
    if(T.natalVenus.sign) tHtml += `<div class="data-row"><span class="data-planet">Deine natale Venus</span><span class="data-values"><span class="badge sign-badge">${T.natalVenus.sign}</span>${T.natalVenus.house ? `<span class="badge house-badge">${T.natalVenus.house}. Haus</span>` : ''}</span></div>`;
    tHtml += `</div></div>`;
    html += tHtml;
  }

  html += `
  <div class="cta-block">
    <h3>Deine Transitanalyse mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Deine Analyse zeigt dir, welche Wunde das Trigon bei dir berührt, in welchem Lebensbereich es wirkt und welche Fürsorge du dir gerade selbst geben darfst.</p>
    <button class="copy-btn" id="copyTransitBtn" onclick="copyTransitReading()">Transit-Prompt + Daten kopieren</button>
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
new_region = r"""  const TRANSIT_PROMPT = `Du bist eine erfahrene Bewusstseinsastrologin mit Fokus auf Transite. Du liest meine Chart in Schichten und schreibst klar, tief und direkt, so dass mich jeder Satz trifft. Keine Floskeln, keine allgemeinen Astro-Sätze, kein Lehrbuchton.

Das Ereignis: Am Freitag, den 10. Juli 2026 steht Venus in der Jungfrau im exakten Trigon zu Chiron im Stier, beide auf demselben Grad ihres Zeichens. Venus steht für die Art zu lieben, für Fürsorge, Genuss, Sinnlichkeit, Werte und Geld. In der Jungfrau liebt sie durch Handeln, durch Fürsorge und den aufmerksamen Blick für das Detail. Chiron zeigt die Stelle der alten Wunde. Im Stier ist es die Wunde um den Wert: ob ich genug bin, auch wenn ich nichts leiste, das Verhältnis zum eigenen Körper, zu Sicherheit und Geld, die Schwierigkeit zu empfangen. Ein Trigon ist ein Winkel von 120 Grad, beide Planeten stehen in Erdzeichen, ihre Energien fließen ineinander: Fürsorge erreicht die Wunde. Die Energie baut sich vor dem exakten Moment auf und wirkt noch einige Tage nach. Chiron bleibt darüber hinaus noch lange am Anfang des Stiers, Venus zieht schneller weiter.

Wichtig: Ich arbeite mit Placidus-Häusern. Alle Häuser in meinen Daten unten sind Placidus-Häuser.

Unten bekommst du:
- die genauen Grade von Transit-Venus und Transit-Chiron
- das Haus, durch das Transit-Chiron bei mir läuft (dort sitzt das Wund-Thema)
- das Haus, durch das Transit-Venus bei mir läuft (von dort kommt die Fürsorge)
- die Punkte, die ich selbst in Stier oder Jungfrau habe (der Transit läuft direkt über sie)
- die Aspekte, die Transit-Venus und Transit-Chiron zu meinen natalen Punkten bilden (mit Orb, je enger, desto stärker)
- meine natale Venus (wie ich liebe und versorge) und meinen natalen Chiron (wo meine eigene Wunde sitzt)
- mein vollständiges Chart als Kontext

Schreibe mir auf dieser Basis:

1. Das Thema. Ein kraftvoller Absatz: welche Wunde dieses Trigon bei mir berührt und welche Fürsorge sie gerade erreichen will. Sprich mich direkt mit du an.

2. Wo es wirkt. Nimm das Haus, durch das Transit-Chiron bei mir läuft: dort lebt das Wund-Thema aus Wert, Körper, Sicherheit und Geld in meinem Alltag. Nimm dann das Haus, durch das Transit-Venus läuft: aus diesem Lebensbereich kommt gerade die Fürsorge. Mach beide konkret und verbinde sie: Was in meinem Leben will gerade versorgt werden, und woher kommt die Kraft dafür?

3. Direkte Treffer. Geh jeden Punkt durch, den ich selbst im Stier oder in der Jungfrau habe. Venus und Chiron laufen direkt über diese Punkte. Sag mir für jeden, was er in mir trägt und was der Transit dort berührt. Habe ich keine Punkte dort, vertiefe stattdessen die beiden Häuser.

4. Die Aspekte. Geh jeden Aspekt durch, den Transit-Venus oder Transit-Chiron zu meinen natalen Punkten bildet. Erkläre für jeden, was der Aspekt bedeutet und was er in genau diesem Punkt meiner Chart auslöst. Beginne mit dem engsten Orb, der wirkt am stärksten.

5. Meine Verdrahtung. Lies meinen natalen Chiron nach Zeichen und Haus: das ist meine eigene Wunde, unabhängig vom Kollektiv. Lies dann meine natale Venus: so liebe und versorge ich. Verbinde beides: Welche Fürsorge braucht meine Wunde wirklich, und gebe ich diese Fürsorge bisher eher anderen als mir selbst?

6. Schatten und Geschenk. Der Schatten dieses Trigons: Ich versorge alle anderen und nenne es Liebe, ich analysiere meine Wunde, statt sie zu fühlen, ich optimiere meinen Körper, statt ihn zu bewohnen, und Zuwendung an mich selbst fühlt sich weiter unverdient an. Das Geschenk: Zuwendung erreicht eine alte Stelle in mir, ich empfange ohne Gegenleistung, mein Wert löst sich von meiner Leistung. Sag mir, woran ich bei mir erkenne, ob ich im Schatten oder im Geschenk unterwegs bin.

7. Der Weg durch den Körper. Der Stier heilt über den Körper, die Jungfrau über das Konkrete. Gib mir eine konkrete Fürsorge-Handlung für die nächsten Tage, die zu meiner Chart passt: etwas, das ich für meinen Körper tue, so aufmerksam, wie ich sonst andere versorge.

8. Meine Transit-Frage. Eine einzige, konfrontierende Frage zu der Fürsorge, die ich mir selbst schulde.

Schreib auf Deutsch, in der Du-Form, in Tiefe statt in Breite. Jeder Satz konkret. Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker.

Hier sind meine Daten:`;

  window.copyTransitReading = function(){
    const FULL = window.__fullChart || [];
    const ASP = window.__aspects || [];
    const T = window.__transit || {};
    const m = window.__meta || {};
    const data = [];
    if(m.name) data.push('Name: ' + m.name);
    if(m.date){ const dp = m.date.split('-'); data.push('Geburtsdatum: ' + dp[2]+'.'+dp[1]+'.'+dp[0] + (m.time ? (' um ' + m.time + ' Uhr') : '')); }
    if(m.place) data.push('Geburtsort: ' + m.place);
    data.push('');
    data.push('MEIN VENUS-CHIRON-TRANSIT (exakt am 10. Juli 2026):');
    if(T.venusText) data.push('Transit-Venus steht bei ' + T.venusText + '.');
    if(T.chironText) data.push('Transit-Chiron steht bei ' + T.chironText + '.');
    if(T.chironHouse) data.push('Transit-Chiron läuft durch mein ' + T.chironHouse + '. Haus. Dort sitzt das Wund-Thema aus Wert, Körper, Sicherheit und Geld.');
    if(T.venusHouse) data.push('Transit-Venus läuft durch mein ' + T.venusHouse + '. Haus. Von dort kommt die Fürsorge.');
    const tauP = (T.taurusPoints || []).map(function(e){ return e.label + (e.house ? (' (' + e.house + '. Haus)') : ''); });
    data.push('Punkte, die ich selbst im Stier habe (Chiron läuft über sie): ' + (tauP.length ? tauP.join(', ') : 'keine') + '.');
    const virP = (T.virgoPoints || []).map(function(e){ return e.label + (e.house ? (' (' + e.house + '. Haus)') : ''); });
    data.push('Punkte, die ich selbst in der Jungfrau habe (Venus läuft über sie): ' + (virP.length ? virP.join(', ') : 'keine') + '.');
    const hits = T.hits || [];
    if(hits.length){
      data.push('Aspekte der Transit-Punkte zu meinen natalen Punkten (engster Orb wirkt am stärksten):');
      hits.forEach(function(h){ data.push('- Transit-' + h.who + ' ' + h.type + ' zu ' + h.point + (h.sign ? (' in ' + h.sign) : '') + (h.house ? (', ' + h.house + '. Haus') : '') + ' (Orb ' + String(h.orb).replace('.', ',') + '°)'); });
    } else {
      data.push('Transit-Venus und Transit-Chiron bilden keine engen Aspekte (Orb bis 3°) zu meinen natalen Punkten. Arbeite mit den Häusern und meiner Verdrahtung.');
    }
    if(T.natalChiron && T.natalChiron.sign) data.push('Mein nataler Chiron (meine eigene Wunde): ' + T.natalChiron.sign + (T.natalChiron.house ? (', ' + T.natalChiron.house + '. Haus') : '') + '.');
    if(T.natalVenus && T.natalVenus.sign) data.push('Meine natale Venus: ' + T.natalVenus.sign + (T.natalVenus.house ? (', ' + T.natalVenus.house + '. Haus') : '') + '.');
    data.push('');
    data.push('MEIN VOLLSTÄNDIGES CHART (Placidus-Häuser):');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });
    if(ASP.length){
      data.push('');
      data.push('MEINE WICHTIGSTEN NATALEN ASPEKTE:');
      ASP.forEach(function(a){ data.push(a.p1 + (a.s1 ? (' in ' + a.s1) : '') + ' ' + a.type + ' ' + a.p2 + (a.s2 ? (' in ' + a.s2) : '')); });
    }
    const full = TRANSIT_PROMPT + '\n\n' + data.join('\n');
    const btn = document.getElementById('copyTransitBtn');
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
.subtitle{ color:#EFD9C2 !important; }
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
for leftover in ["copyBusinessReading", "copyBizBtn", "BUSINESS_PROMPT", "subscribeLead", "userEmail", "Ganzzeichen"]:
    if leftover in s:
        sys.exit("REST gefunden: " + leftover)

with open(DST, "w", encoding="utf-8") as f:
    f.write(s)

os.makedirs(NETLIFY, exist_ok=True)
shutil.copyfile(DST, os.path.join(NETLIFY, "index.html"))

print("OK ->", DST)
print("OK ->", os.path.join(NETLIFY, "index.html"))
print("Groesse:", len(s), "Zeichen")
