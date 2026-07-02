#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut den Mars-Uranus-Transit-Reader aus dem Business-Reader.
Gleiches Design + gleiche Astro-Engine, nur das Reading-Gehirn wird getauscht:

Der Reader rechnet ZWEI Charts mit derselben Engine:
  1. das Geburtshoroskop der Nutzerin (Ganzzeichenhaeuser!)
  2. den Transit-Moment: 04.07.2026, 6:07 Uhr (Mars Konjunktion Uranus exakt,
     Berlin als Ort, fuer die Planeten-Laengen egal, nur die Zeitzone zaehlt)

Daraus zieht er automatisch:
  - den exakten Grad der Konjunktion in den Zwillingen
  - das Ganzzeichenhaus, in dem Zwillinge bei der Nutzerin liegt (Wirkungsort)
  - ihre eigenen Punkte in den Zwillingen (die Konjunktion laeuft darueber)
  - die Aspekte der Konjunktion zu ihren natalen Punkten (Orb 3 Grad)
  - natalen Mars + natalen Uranus (Verdrahtung)
und baut einen fertigen KI-Prompt zum Kopieren.

Quelle:  astro-business-reader.html
Ziel:    astro-transit-reader.html (+ astro-transit-reader-netlify/index.html)
Bei Design-Updates am Business-Reader dieses Skript erneut laufen lassen.

Fuer den NAECHSTEN Transit: nur die T_*-Konstanten unten und die Texte
(Prompt, Ueberschriften) anpassen, Skript neu laufen lassen.
"""
import os, re, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-transit-reader.html")
NETLIFY = os.path.join(HERE, "astro-transit-reader-netlify")

# --- Transit-Moment (lokale Zeit, Engine loest Zeitzone ueber Koordinaten) --
T_YEAR, T_MONTH, T_DATE = 2026, 7, 4      # 04.07.2026
T_HOUR, T_MINUTE = 6, 7                    # 6:07 Uhr (exakt)
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
     "<title>Mars trifft Uranus · Dein Transit-Code</title>", "title")

repl('<p class="header-eyebrow">Dein kosmischer Business-Blueprint</p>',
     '<p class="header-eyebrow">Transit vom 4. Juli 2026</p>', "eyebrow")

repl("<h1>Dein Business-Code</h1>",
     "<h1>Mars trifft Uranus in den Zwillingen</h1>", "h1")

repl('<p class="subtitle">Gib deine Geburtsdaten ein. Auf der nächsten Seite bekommst du dein Geburtshoroskop angezeigt und einen fertigen KI-Prompt, der dir sagt, wie du dein Business führst, dich positionierst, skalierst und Geld verdienst.</p>',
     '<p class="subtitle">Am Samstag, den 4. Juli 2026 um 6:07 Uhr trifft Mars exakt auf Uranus, beide in den Zwillingen. Gib deine Geburtsdaten ein. Die Seite rechnet dein Geburtshoroskop mit Ganzzeichenhäusern, zeigt dir, wo die Konjunktion bei dir wirkt, und baut dir einen fertigen KI-Prompt für deine persönliche Transitanalyse.</p>',
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

# --- 2. Ganzzeichenhaeuser statt Placidus ---------------------------------
repl("houseSystem: 'placidus'", "houseSystem: 'whole-sign'", "whole-sign")

repl("<h3>Deine Platzierungen</h3>",
     "<h3>Deine Platzierungen · Ganzzeichenhäuser</h3>", "placements-heading")

# --- 3. Ergebnis-Kopf + Zurueck-Button ------------------------------------
repl("<h2>Dein Business-Code${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Dein Chart als Business-Blueprint'}</p>",
     "<h2>Dein Mars-Uranus-Transit${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Mars trifft Uranus in den Zwillingen'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Neue Chart erstellen", "back-btn")

# --- 4. Transit-Berechnung in runCheck einhaengen --------------------------
# Anker NACH window.__chart, damit __fullChart und __aspects bereits gesetzt sind.
calc_anchor = "      window.__chart = chart;\n      generateReading();"
transit_calc = """      window.__chart = chart;

      // Mars-Uranus-Transit: zweites Chart fuer den exakten Moment rechnen.
      // Ort Berlin, weil die Planeten-Laengen ortsunabhaengig sind, die Engine
      // braucht die Koordinaten nur fuer die Zeitzone (6:07 Uhr Sommerzeit).
      (function(){
        try{
          const tOrigin = new Origin({ year: __T_YEAR__, month: __T_MONTH0__, date: __T_DATE__, hour: __T_HOUR__, minute: __T_MINUTE__, latitude: __T_LAT__, longitude: __T_LON__ });
          const tHoro = new Horoscope({ origin: tOrigin, houseSystem: 'whole-sign', zodiac: 'tropical', language: 'en', aspectTypes: ['major'] });
          const lonOf = function(b){ try{ return b.ChartPosition.Ecliptic.DecimalDegrees; }catch(e){ return null; } };
          const tMars = lonOf(tHoro.CelestialBodies.mars);
          const tUranus = lonOf(tHoro.CelestialBodies.uranus);
          if(tMars == null || tUranus == null) return;
          // Konjunktionspunkt = Mitte zwischen Mars und Uranus (liegen praktisch aufeinander)
          let dHalf = ((tUranus - tMars + 540) % 360) - 180;
          const T = (tMars + dHalf / 2 + 360) % 360;
          const inSign = T % 30;
          let tDeg = Math.floor(inSign);
          let tMin = Math.round((inSign - tDeg) * 60);
          if(tMin === 60){ tMin = 0; tDeg += 1; }
          const SIGNS_DE = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische'];
          const tSign = SIGNS_DE[Math.floor(T / 30)] || '';
          const degreeText = tDeg + '°' + (tMin < 10 ? '0' : '') + tMin + "' " + tSign;

          // Ganzzeichenhaus des Konjunktions-Zeichens: Abstand zum AC-Zeichen
          const FULL = window.__fullChart || [];
          const acEntry = FULL.find(function(e){ return e.label === 'Aszendent'; }) || {};
          const acIdx = SIGNS_DE.indexOf(acEntry.sign);
          const tSignIdx = Math.floor(T / 30);
          const house = (acIdx >= 0) ? (((tSignIdx - acIdx + 12) % 12) + 1) : null;

          // Eigene Punkte im Konjunktions-Zeichen (die Konjunktion laeuft darueber)
          const signPoints = FULL.filter(function(e){ return e.sign === tSign; });

          // Aspekte der Konjunktion zu den natalen Punkten (enger Transit-Orb: 3 Grad)
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
          NATAL.forEach(function(pair){
            const L = lonOf(pair[1]);
            if(L == null) return;
            const d = Math.abs(((T - L + 540) % 360) - 180); // Winkelabstand 0..180
            TYPES.forEach(function(t){
              const orb = Math.abs(d - t[0]);
              if(orb <= 3) hits.push({ point: pair[0], sign: SIGNOF[pair[0]] || '', house: HOUSEOF[pair[0]] || '', type: t[1], orb: Math.round(orb * 10) / 10 });
            });
          });
          hits.sort(function(a, b){ return a.orb - b.orb; });

          const marsEntry = FULL.find(function(e){ return e.label === 'Mars'; }) || {};
          const uranusEntry = FULL.find(function(e){ return e.label === 'Uranus'; }) || {};
          window.__transit = {
            degreeText: degreeText,
            sign: tSign,
            house: house,
            signPoints: signPoints,
            hits: hits,
            natalMars: { sign: marsEntry.sign || '', house: marsEntry.house || '' },
            natalUranus: { sign: uranusEntry.sign || '', house: uranusEntry.house || '' }
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

new_cta = """  // Sichtbares Mars-Uranus-Transit-Thema
  const T = window.__transit || null;
  if(T){
    const tps = (T.signPoints || []).map(function(e){ return e.label; });
    let tHtml = `
    <div class="data-block">
      <h3>Dein Mars-Uranus-Thema</h3>
      <div class="data-grid">`;
    tHtml += `<div class="data-row"><span class="data-planet">Die Konjunktion steht bei</span><span class="data-values"><span class="badge sign-badge">${T.degreeText}</span></span></div>`;
    if(T.house) tHtml += `<div class="data-row"><span class="data-planet">Zwillinge liegt bei dir im</span><span class="data-values"><span class="badge house-badge">${T.house}. Haus (Ganzzeichen)</span></span></div>`;
    tHtml += `<div class="data-row"><span class="data-planet">Deine Punkte in den Zwillingen</span><span class="data-values"><span class="badge sign-badge">${tps.length ? tps.join(', ') : 'keine'}</span></span></div>`;
    const hitStr = (T.hits || []).map(function(h){ return h.type + ' ' + h.point; }).join(', ');
    tHtml += `<div class="data-row"><span class="data-planet">Die Konjunktion trifft</span><span class="data-values"><span class="badge sign-badge">${hitStr || 'keine engen Aspekte'}</span></span></div>`;
    if(T.natalMars.sign) tHtml += `<div class="data-row"><span class="data-planet">Dein nataler Mars</span><span class="data-values"><span class="badge sign-badge">${T.natalMars.sign}</span>${T.natalMars.house ? `<span class="badge house-badge">${T.natalMars.house}. Haus</span>` : ''}</span></div>`;
    if(T.natalUranus.sign) tHtml += `<div class="data-row"><span class="data-planet">Dein nataler Uranus</span><span class="data-values"><span class="badge sign-badge">${T.natalUranus.sign}</span>${T.natalUranus.house ? `<span class="badge house-badge">${T.natalUranus.house}. Haus</span>` : ''}</span></div>`;
    tHtml += `</div></div>`;
    html += tHtml;
  }

  html += `
  <div class="cta-block">
    <h3>Deine Transitanalyse mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Deine Analyse zeigt dir, in welchem Lebensbereich die Konjunktion bei dir wirkt, welche Punkte in deiner Chart sie berührt und wie du diese Energie für dich nutzt.</p>
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

Das Ereignis: Am Samstag, den 4. Juli 2026 um 6:07 Uhr trifft Mars exakt auf Uranus, beide im Tierkreiszeichen Zwillinge. Mars steht für Antrieb, Wille, Durchsetzung, Wut und Handlungsenergie. Uranus steht für Freiheit, plötzliche Wendungen, Geistesblitze und das Nervensystem. Zwillinge steht für Denken, Sprechen, Stimme, Information und Austausch. Diese Konjunktion entlädt Energie schlagartig: aufgestaute Wut findet Worte, überfällige Entscheidungen fallen, ein Gedanke bringt plötzlich alles auf den Punkt. Die Energie baut sich in den Tagen davor auf und wirkt noch einige Tage nach.

Wichtig: Ich arbeite bei Transiten mit Ganzzeichenhäusern. Das erste Haus ist das komplette Zeichen meines Aszendenten, jedes weitere Zeichen ist das nächste Haus. Alle Häuser in meinen Daten unten sind Ganzzeichenhäuser.

Unten bekommst du:
- den genauen Grad der Konjunktion
- das Ganzzeichenhaus, in dem Zwillinge bei mir liegt (dort wirkt die Konjunktion)
- die Punkte, die ich selbst in den Zwillingen habe (die Konjunktion läuft direkt über sie)
- die Aspekte, die die Konjunktion zu meinen natalen Punkten bildet (mit Orb, je enger, desto stärker)
- meinen natalen Mars und meinen natalen Uranus (so bin ich mit diesen beiden Energien verdrahtet)
- mein vollständiges Chart als Kontext

Schreibe mir auf dieser Basis:

1. Die Zündung. Ein kraftvoller Absatz: was diese Konjunktion in mir wachrüttelt und warum gerade jetzt. Sprich mich direkt mit du an.

2. Wo es wirkt. Nimm das Ganzzeichenhaus, in dem Zwillinge bei mir liegt, und mach konkret, in welchem Lebensbereich sich die Energie entlädt, zum Beispiel Geld, Arbeit, Beziehung, Körper, Zuhause, Sichtbarkeit oder Kommunikation. Beschreib eine Alltagsszene, in der ich das an diesem Wochenende spüren kann.

3. Direkte Treffer. Geh jeden Punkt durch, den ich selbst in den Zwillingen habe. Die Konjunktion läuft direkt über diese Punkte. Sag mir für jeden, was in mir aufwacht und was ich damit anfange. Habe ich keinen Punkt in den Zwillingen, dann vertiefe stattdessen das Haus.

4. Die Aspekte. Geh jeden Aspekt durch, den die Konjunktion zu meinen natalen Punkten bildet. Erkläre für jeden, was der Aspekt bedeutet und was er in genau diesem Punkt meiner Chart auslöst. Beginne mit dem engsten Orb, der wirkt am stärksten.

5. Meine Verdrahtung. Lies meinen natalen Mars (wie ich handle, kämpfe und will) und meinen natalen Uranus (wo ich frei sein will und ausbreche). Der Transit spricht genau diese beiden Anlagen in mir an. Zeig mir, wie meine Version dieser Energie aussieht.

6. Schatten und Geschenk. Der Schatten dieser Konjunktion: Kurzschlussreaktionen, Streit um Worte, überdrehtes Nervensystem, Unruhe, schlechter Schlaf, hektische Entscheidungen, die ich in einer Woche bereue. Das Geschenk: der mutige Schritt, der lange fällig war, das klare Wort, das alles verändert, die Befreiung aus einer Struktur, die zu eng geworden ist. Sag mir, woran ich bei mir erkenne, ob ich im Schatten oder im Geschenk unterwegs bin.

7. Der Weg durch den Körper. Uranus und Zwillinge machen den Kopf laut und das Nervensystem schnell. Gib mir eine konkrete Erdung für dieses Wochenende, zum Beispiel barfuß im Gras stehen, in den Wald gehen, Bewegung, die die Energie aus dem Kopf in den Körper holt.

8. Meine Transit-Frage. Eine einzige, konfrontierende Frage zu der Entscheidung oder dem Ausbruch, der bei mir gerade ansteht.

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
    data.push('MEIN MARS-URANUS-TRANSIT (exakt am 4. Juli 2026 um 6:07 Uhr):');
    if(T.degreeText) data.push('Die Konjunktion steht bei ' + T.degreeText + '.');
    if(T.house) data.push('Zwillinge liegt in meinem ' + T.house + '. Ganzzeichenhaus. Dort wirkt die Konjunktion.');
    const tp = (T.signPoints || []).map(function(e){ return e.label + (e.house ? (' (' + e.house + '. Haus)') : ''); });
    data.push('Punkte, die ich selbst in den Zwillingen habe (die Konjunktion läuft direkt über sie): ' + (tp.length ? tp.join(', ') : 'keine') + '.');
    const hits = T.hits || [];
    if(hits.length){
      data.push('Aspekte der Konjunktion zu meinen natalen Punkten (engster Orb wirkt am stärksten):');
      hits.forEach(function(h){ data.push('- ' + h.type + ' zu ' + h.point + (h.sign ? (' in ' + h.sign) : '') + (h.house ? (', ' + h.house + '. Haus') : '') + ' (Orb ' + String(h.orb).replace('.', ',') + '°)'); });
    } else {
      data.push('Die Konjunktion bildet keine engen Aspekte (Orb bis 3°) zu meinen natalen Punkten. Arbeite mit dem Haus und meiner Verdrahtung.');
    }
    if(T.natalMars && T.natalMars.sign) data.push('Mein nataler Mars: ' + T.natalMars.sign + (T.natalMars.house ? (', ' + T.natalMars.house + '. Haus') : '') + '.');
    if(T.natalUranus && T.natalUranus.sign) data.push('Mein nataler Uranus: ' + T.natalUranus.sign + (T.natalUranus.house ? (', ' + T.natalUranus.house + '. Haus') : '') + '.');
    data.push('');
    data.push('MEIN VOLLSTÄNDIGES CHART (alle Häuser sind Ganzzeichenhäuser):');
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

# Sicherheitscheck: keine Business-Reste mehr in Logik-Hooks
for leftover in ["copyBusinessReading", "copyBizBtn", "BUSINESS_PROMPT", "subscribeLead", "userEmail"]:
    if leftover in s:
        sys.exit("REST gefunden: " + leftover)

with open(DST, "w", encoding="utf-8") as f:
    f.write(s)

os.makedirs(NETLIFY, exist_ok=True)
shutil.copyfile(DST, os.path.join(NETLIFY, "index.html"))

print("OK ->", DST)
print("OK ->", os.path.join(NETLIFY, "index.html"))
print("Groesse:", len(s), "Zeichen")
