#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut den Reise-Code-Reader (Astrokartographie / Relokation) aus dem Business-Reader.
Gleiches Design + gleiche Astro-Engine, nur das Reading-Gehirn wird getauscht:

Die Nutzerin gibt ihre Geburtsdaten UND ein Reiseziel ein. Der Reader rechnet
ZWEI Charts mit derselben Engine:
  1. das Geburtshoroskop (Placidus, wie im Business-Reader)
  2. das Relokationschart: exakt derselbe Geburtsmoment (origin.julianDate),
     gerechnet fuer die Koordinaten des Reiseziels. Die lokale Wanduhrzeit am
     Zielort wird iterativ bestimmt, damit die Engine die Zeitzone des Ziels
     selbst aufloest (inkl. Sommerzeit) und beide Charts denselben Moment treffen.

Daraus zieht er automatisch:
  - die Linien am Reiseziel: Planeten (Sonne bis Pluto, Chiron, Lilith), die
    dort nah an AC, DC, MC oder IC stehen (Orb bis 10 Grad, engste zuerst)
  - Aszendent + MC am Zielort (wie sie dort auftritt, was der Ort sichtbar macht)
  - die Verschiebung der Haeuser: Geburtshaus vs. Haus am Zielort je Planet
und baut einen fertigen Wegweiser-Prompt zum Kopieren: welche Linien durch den
Ort laufen, was sie dort erwartet, was sie erleben kann, wo ihr Fokus liegen darf.

Quelle:  astro-business-reader.html
Ziel:    astro-reise-reader.html (+ astro-reise-reader-netlify/index.html)
Bei Design-Updates am Business-Reader dieses Skript erneut laufen lassen.
"""
import os, re, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-reise-reader.html")
NETLIFY = os.path.join(HERE, "astro-reise-reader-netlify")

with open(SRC, "r", encoding="utf-8") as f:
    s = f.read()

def repl(old, new, label):
    global s
    if old not in s:
        sys.exit("FEHLT (" + label + "): " + old[:80])
    s = s.replace(old, new, 1)

# --- 1. Branding / sichtbare Texte ---------------------------------------
repl("<title>Dein Business-Code</title>",
     "<title>Dein Reise-Code</title>", "title")

repl('<p class="header-eyebrow">Dein kosmischer Business-Blueprint</p>',
     '<p class="header-eyebrow">Dein astrologischer Wegweiser</p>', "eyebrow")

repl("<h1>Dein Business-Code</h1>",
     "<h1>Dein Reise-Code</h1>", "h1")

repl('<p class="subtitle">Gib deine Geburtsdaten ein. Auf der nächsten Seite bekommst du dein Geburtshoroskop angezeigt und einen fertigen KI-Prompt, der dir sagt, wie du dein Business führst, dich positionierst, skalierst und Geld verdienst.</p>',
     '<p class="subtitle">Gib deine Geburtsdaten und dein Reiseziel ein. Die Seite legt dein Geburtshoroskop über die Landkarte und zeigt dir, welche deiner Linien durch dein Reiseziel laufen. Dazu bekommst du einen fertigen KI-Prompt für deinen Wegweiser: was dich an diesem Ort erwartet, was du dort erleben kannst und wo dein Fokus liegen darf.</p>',
     "subtitle")

repl("<p><strong>Gib deine Geburtsdaten ein.</strong></p>",
     "<p><strong>Gib deine Geburtsdaten und dein Reiseziel ein.</strong></p>", "tip-box")

repl('onclick="runCheck()">Meinen Business-Code aufdecken</button>',
     'onclick="runCheck()">Meinen Reise-Code aufdecken</button>', "submit-btn")

# --- E-Mail komplett entfernen (kein Opt-in, wie bei den anderen Readern) ---
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

# --- 2. Reiseziel-Feld unter dem Geburtsort einfuegen -----------------------
repl('''    <div class="name-group place-group">
      <label class="field-label" for="birthPlace">Geburtsort</label>
      <input type="text" id="birthPlace" placeholder="Stadt eingeben und auswählen, z.B. Düsseldorf" autocomplete="off">
      <div id="placeResults" class="place-results"></div>
      <div id="placeChosen" class="place-chosen"></div>
    </div>
''',
'''    <div class="name-group place-group">
      <label class="field-label" for="birthPlace">Geburtsort</label>
      <input type="text" id="birthPlace" placeholder="Stadt eingeben und auswählen, z.B. Düsseldorf" autocomplete="off">
      <div id="placeResults" class="place-results"></div>
      <div id="placeChosen" class="place-chosen"></div>
    </div>

    <div class="name-group place-group">
      <label class="field-label" for="destPlace">Dein Reiseziel</label>
      <input type="text" id="destPlace" placeholder="Wohin zieht es dich? Stadt eingeben und auswählen" autocomplete="off">
      <div id="destResults" class="place-results"></div>
      <div id="destChosen" class="place-chosen"></div>
    </div>
''', "dest-field")

# --- 2b. Geburtsdatum als Textfeld (Patrycja 13.07.): der native Date-Picker
# ist fuer Geburtsdaten muehsam. Eintippen als TT.MM.JJJJ, Punkte kommen
# automatisch, runCheck wandelt intern nach ISO (JJJJ-MM-TT) fuer die Engine.
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

# --- 3. Zweites Geocoding (Reiseziel), gleiche Open-Meteo-Suche -------------
repl("  let chosenPlace = null;\n  let placeDebounce = null;",
     "  let chosenPlace = null;\n  let placeDebounce = null;\n  let chosenDest = null;\n  let destDebounce = null;",
     "dest-vars")

dest_geo = '''  function closeDestResults(){ const r = $('destResults'); if(r){ r.classList.remove('open'); r.innerHTML=''; } }
  function clearChosenDest(){ chosenDest = null; const c = $('destChosen'); if(c){ c.classList.remove('show'); c.textContent=''; } }

  async function searchDest(q){
    const r = $('destResults');
    r.innerHTML = '<div class="place-loading">suche…</div>';
    r.classList.add('open');
    try{
      const data = await (await fetch(GEO(q))).json();
      const results = data.results || [];
      if(!results.length){ r.innerHTML = '<div class="place-loading">Kein Ort gefunden</div>'; return; }
      r.innerHTML = results.map(res => {
        const region = [res.admin1, res.country].filter(Boolean).join(', ');
        const label = res.name + (region ? ', ' + region : '');
        return '<div class="place-item" data-lat="' + res.latitude + '" data-lon="' + res.longitude +
               '" data-label="' + label.replace(/"/g,'&quot;') + '"><strong>' + res.name + '</strong> <small>' + region + '</small></div>';
      }).join('');
      Array.prototype.forEach.call(r.querySelectorAll('.place-item'), el => {
        el.addEventListener('click', () => {
          chosenDest = { lat: parseFloat(el.dataset.lat), lon: parseFloat(el.dataset.lon), label: el.dataset.label };
          $('destPlace').value = el.dataset.label;
          const c = $('destChosen'); c.textContent = '✓ ' + el.dataset.label; c.classList.add('show');
          closeDestResults();
        });
      });
    }catch(e){ r.innerHTML = '<div class="place-loading">Suche fehlgeschlagen. Internetverbindung?</div>'; }
  }

  async function ensureDest(){
    if(chosenDest) return chosenDest;
    const q = ($('destPlace').value || '').trim();
    if(q.length < 2) return null;
    try{
      const data = await (await fetch(GEO(q))).json();
      const res = (data.results || [])[0];
      if(!res) return null;
      chosenDest = { lat: res.latitude, lon: res.longitude, label: res.name + (res.country ? ', ' + res.country : '') };
      return chosenDest;
    }catch(e){ return null; }
  }

  function engineReady(){'''
repl("  function engineReady(){", dest_geo, "dest-geocode-fns")

# --- 4. Eingabe-Verkabelung fuer beide Ortsfelder ---------------------------
repl('''  document.addEventListener('DOMContentLoaded', function(){
    const inp = $('birthPlace');
    if(!inp) return;
    inp.addEventListener('input', function(){
      clearChosen();
      const q = inp.value.trim();
      if(placeDebounce) clearTimeout(placeDebounce);
      if(q.length < 2){ closeResults(); return; }
      placeDebounce = setTimeout(function(){ searchPlace(q); }, 300);
    });
    document.addEventListener('click', function(e){
      if(!e.target.closest('.place-group')) closeResults();
    });
  });''',
'''  document.addEventListener('DOMContentLoaded', function(){
    const inp = $('birthPlace');
    if(inp){
      inp.addEventListener('input', function(){
        clearChosen();
        closeDestResults();
        const q = inp.value.trim();
        if(placeDebounce) clearTimeout(placeDebounce);
        if(q.length < 2){ closeResults(); return; }
        placeDebounce = setTimeout(function(){ searchPlace(q); }, 300);
      });
    }
    const dst = $('destPlace');
    if(dst){
      dst.addEventListener('input', function(){
        clearChosenDest();
        closeResults();
        const q = dst.value.trim();
        if(destDebounce) clearTimeout(destDebounce);
        if(q.length < 2){ closeDestResults(); return; }
        destDebounce = setTimeout(function(){ searchDest(q); }, 300);
      });
    }
    const bd = $('birthDate');
    if(bd){
      bd.addEventListener('input', function(){
        let v = bd.value.replace(/[^\\d.]/g, '');
        if(v.indexOf('.') === -1 && v.length > 4){
          v = v.slice(0,2) + '.' + v.slice(2,4) + '.' + v.slice(4,8);
        }
        bd.value = v.slice(0, 10);
      });
    }
    document.addEventListener('click', function(e){
      if(!e.target.closest('.place-group')){ closeResults(); closeDestResults(); }
    });
  });''', "dom-wiring")

# --- 5. Reiseziel-Validierung in runCheck -----------------------------------
repl('''      const place = await ensurePlace();
      if(!place){ return fail('Bitte wähle deinen Geburtsort aus der Vorschlagsliste aus.'); }
''',
'''      const place = await ensurePlace();
      if(!place){ return fail('Bitte wähle deinen Geburtsort aus der Vorschlagsliste aus.'); }
      const dest = await ensureDest();
      if(!dest){ return fail('Bitte wähle dein Reiseziel aus der Vorschlagsliste aus.'); }
''', "dest-validation")

# --- 6. Ergebnis-Kopf + Zurueck-Button ------------------------------------
repl("<h2>Dein Business-Code${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Dein Chart als Business-Blueprint'}</p>",
     "<h2>Dein Reise-Code${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Dein astrologischer Wegweiser'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Anderes Reiseziel prüfen", "back-btn")

# --- 7. Relokations-Berechnung in runCheck einhaengen -----------------------
# Anker NACH window.__chart, damit __fullChart und __aspects bereits gesetzt sind.
calc_anchor = "      window.__chart = chart;\n      generateReading();"
reise_calc = """      window.__chart = chart;

      // Reise-Code: Relokationschart fuer das Reiseziel rechnen.
      // Exakt derselbe Geburtsmoment (origin.julianDate), nur der Ort wechselt.
      // Die lokale Wanduhrzeit am Ziel wird iterativ bestimmt, damit die Engine
      // die Zeitzone des Ziels selbst aufloest (inkl. Sommerzeit).
      // __REISE_CALC_START__
      (function(){
        try{
          const jdToMs = function(jd){ return (jd - 2440587.5) * 86400000; };
          const mkOrigin = function(naiveMs){
            const d = new Date(naiveMs);
            return new Origin({ year: d.getUTCFullYear(), month: d.getUTCMonth(), date: d.getUTCDate(), hour: d.getUTCHours(), minute: d.getUTCMinutes(), latitude: dest.lat, longitude: dest.lon });
          };
          const targetMs = jdToMs(origin.julianDate);
          let naive = Math.round(targetMs / 60000) * 60000;
          let o2 = mkOrigin(naive);
          for(let i = 0; i < 4; i++){
            const diffMs = targetMs - jdToMs(o2.julianDate);
            if(Math.abs(diffMs) < 45000) break;
            naive = Math.round((naive + diffMs) / 60000) * 60000;
            o2 = mkOrigin(naive);
          }
          if(Math.abs(targetMs - jdToMs(o2.julianDate)) > 120000) throw new Error('Zeitzonen-Abgleich fehlgeschlagen');
          const horo2 = new Horoscope({ origin: o2, houseSystem: 'placidus', zodiac: 'tropical', language: 'en', aspectTypes: ['major'] });

          const lonOf = function(b){ try{ return b.ChartPosition.Ecliptic.DecimalDegrees; }catch(e){ return null; } };
          const sep = function(a, b){ return Math.abs(((a - b + 540) % 360) - 180); };
          const rAC = lonOf(horo2.Ascendant);
          const rMC = lonOf(horo2.Midheaven);
          if(rAC == null || rMC == null) throw new Error('keine Achsen');
          const ANGLES = [ ['AC', rAC], ['MC', rMC], ['DC', (rAC + 180) % 360], ['IC', (rMC + 180) % 360] ];
          const CB2 = horo2.CelestialBodies, CP2 = horo2.CelestialPoints;
          const BODIES2 = [
            ['Sonne', CB2.sun], ['Mond', CB2.moon], ['Merkur', CB2.mercury], ['Venus', CB2.venus],
            ['Mars', CB2.mars], ['Jupiter', CB2.jupiter], ['Saturn', CB2.saturn], ['Uranus', CB2.uranus],
            ['Neptun', CB2.neptune], ['Pluto', CB2.pluto], ['Chiron', CB2.chiron], ['Lilith', CP2.lilith]
          ];

          // Linien: Planeten nah an einer der vier Achsen des Zielorts (Orb bis 10 Grad)
          const lines = [];
          BODIES2.forEach(function(pair){
            const L = lonOf(pair[1]);
            if(L == null) return;
            ANGLES.forEach(function(ang){
              const orb = sep(L, ang[1]);
              if(orb <= 10) lines.push({ planet: pair[0], angle: ang[0], orb: Math.round(orb * 10) / 10 });
            });
          });
          lines.sort(function(a, b){ return a.orb - b.orb; });

          // Haeuser-Verschiebung: Geburtshaus vs. Haus am Zielort (Zeichen bleiben gleich)
          const dhouse2 = function(b){ return (b && b.House && b.House.id) ? b.House.id : ''; };
          const NAT_HOUSE = {}; (window.__fullChart || []).forEach(function(e){ NAT_HOUSE[e.label] = e.house; });
          const relocated = BODIES2.map(function(pair){
            return { label: pair[0], natalHouse: NAT_HOUSE[pair[0]] || '', destHouse: dhouse2(pair[1]) };
          }).filter(function(e){ return e.destHouse; });

          const SIGNS_DE = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische'];
          window.__reise = {
            dest: dest.label,
            lines: lines,
            acDeg: rAC,
            mcDeg: rMC,
            acSign: SIGNS_DE[Math.floor(rAC / 30) % 12] || '',
            mcSign: SIGNS_DE[Math.floor(rMC / 30) % 12] || '',
            relocated: relocated
          };
        }catch(e){ window.__reise = null; }
      })();
      // __REISE_CALC_END__

      generateReading();"""
repl(calc_anchor, reise_calc, "reise-calc-injection")

# --- 8a. Ergebnis-Seite verschlanken (Patrycja 13.07.): Platzierungen, ------
# Aspekte und Element-Block raus. Nur der Linien-Block bleibt sichtbar.
# Chart + Aspekte stecken weiter unsichtbar im kopierten Wegweiser-Prompt.
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

# --- 8. Reading-Block: sichtbare Linien + Prompt-CTA ------------------------
old_cta = """  html += `
  <div class="cta-block">
    <h3>Dein Business-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, wie du dein Business führst, wie du dich positionierst, wo deine Zone of Genius liegt und wie du am natürlichsten Geld verdienst.</p>
    <button class="copy-btn" id="copyBizBtn" onclick="copyBusinessReading()">Business-Prompt + Daten kopieren</button>
  </div>`;"""

new_cta = """  // Sichtbare Linien am Reiseziel
  const R = window.__reise || null;
  if(R){
    const strengthWord = function(orb){ return orb <= 3 ? 'direkt an deinem Ziel' : (orb <= 6 ? 'stark spürbar' : 'im Umfeld spürbar'); };
    let rHtml = `
    <div class="data-block">
      <h3>Deine Linien in ${R.dest}</h3>
      <div class="data-grid">`;
    if(R.lines.length){
      R.lines.forEach(function(l){
        rHtml += `<div class="data-row"><span class="data-planet">${l.planet}-${l.angle}-Linie</span><span class="data-values"><span class="badge sign-badge">${strengthWord(l.orb)}</span><span class="badge house-badge">Orb ${String(l.orb).replace('.', ',')}°</span></span></div>`;
      });
    } else {
      rHtml += `<div class="data-row"><span class="data-planet">Deine Linien</span><span class="data-values"><span class="badge sign-badge">keine im Umkreis von 10°, dieser Ort ist bei dir linienleise</span></span></div>`;
    }
    if(R.acSign) rHtml += `<div class="data-row"><span class="data-planet">Dein Aszendent an diesem Ort</span><span class="data-values"><span class="badge sign-badge">${R.acSign}</span></span></div>`;
    if(R.mcSign) rHtml += `<div class="data-row"><span class="data-planet">Dein MC an diesem Ort</span><span class="data-values"><span class="badge sign-badge">${R.mcSign}</span></span></div>`;
    rHtml += `</div></div>`;
    html += rHtml;
  }

  html += `
  <div class="cta-block">
    <h3>Dein Wegweiser mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Wegweiser zeigt dir, welche Linien durch dein Reiseziel laufen, was dich an diesem Ort erwartet, was du dort erleben kannst und wo dein Fokus liegen darf.</p>
    <button class="copy-btn" id="copyReiseBtn" onclick="copyReiseReading()">Wegweiser-Prompt + Daten kopieren</button>
  </div>`;"""
repl(old_cta, new_cta, "cta-block")

# --- 9. Abschluss-CTA: DeinAstroCode-Portal (Patrycjas Text 13.07., 1:1) ----
repl('''  html += `
  <div class="cta-block">
    <p class="cta-kicker">Möchtest du noch tiefer in deine Chart eintauchen?</p>
    <h3>Lerne dich tiefer kennen, als Jahre der Selbstreflexion es je konnten.</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Hier erfährst du mehr: Dein AstroCode &rarr;</a>
  </div>`;''',
'''  html += `
  <div class="cta-block">
    <p class="cta-kicker">DU findest die Antwort von diesem KI-Prompt genial?</p>
    <h3>Weißt du, dass du dank meiner Prompts und meinem passenden Reader dein gesamtes Geburtshoroskop analysieren kannst?</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Öffne das Portal von AstroCode &rarr;</a>
  </div>`;''',
"astrocode-cta")

# --- 10. Prompt-Gehirn + Copy-Funktion austauschen --------------------------
new_region = r"""  const REISE_PROMPT = `Du bist eine erfahrene Bewusstseinsastrologin mit Fokus auf Astrokartographie und Relokation. Du liest meine Chart in Schichten und schreibst klar, tief und direkt, so dass mich jeder Satz trifft. Keine Floskeln, keine allgemeinen Astro-Sätze, kein Lehrbuchton.

Worum es geht: Ich plane eine Reise. Mein Reiseziel steht unten in meinen Daten. Astrokartographie legt mein Geburtshoroskop über die Landkarte. An jedem Ort der Welt stehen meine Planeten anders zu den vier Achsen: Aszendent (wie ich dort auftrete und ankomme), Deszendent (welche Menschen und Begegnungen der Ort mir schickt), MC (was der Ort an mir sichtbar macht und nach außen ruft) und IC (wie tief ich dort wurzeln kann, mein Gefühl von Zuhause). Ein Planet nah an einer dieser Achsen ist eine Linie. Je enger der Orb, desto stärker färbt dieser Planet den Ort für mich.

Unten bekommst du:
- mein Reiseziel
- meine Linien an diesem Ort (Planet, Achse, Orb, je enger desto stärker)
- meinen Aszendenten und mein MC am Zielort
- meine Häuser am Zielort im Vergleich zu meinen Geburtshäusern (der Ort verschiebt meine Lebensbühnen)
- mein vollständiges Geburtshoroskop und meine wichtigsten Aspekte als Kontext

Schreibe mir auf dieser Basis meinen Wegweiser für diesen Ort:

1. Meine Linien. Geh jede Linie durch, die engste zuerst. Sag mir für jede, welcher Planet dort auf welcher Achse steht, was diese Verbindung an genau diesem Ort bedeutet und wie sie sich im Alltag vor Ort anfühlt. Verbinde jede Linie mit der natalen Stellung dieses Planeten in meinem Chart (Zeichen und Haus), denn so trage ich diese Energie in mir. Habe ich keine enge Linie an diesem Ort, dann sag mir das ehrlich und arbeite mit meinen Häusern am Zielort.

2. Was mich dort erwartet. Beschreib, wie dieser Ort mich empfängt: die Stimmung der ersten Tage, welches Lebensthema dort aufwacht, was sich anders anfühlt als zu Hause. Nutz dafür auch die Verschiebung meiner Häuser. Planeten, die am Zielort in ein anderes Haus rutschen, zeigen, welche Bühne dort neu bespielt wird.

3. Was ich dort erleben kann. Mach konkret, welche Erfahrungen, Begegnungen und Möglichkeiten dieser Ort für mich bereithält. Beschreib eine Alltagsszene vor Ort, in der ich meine stärkste Linie spüren kann.

4. Wo mein Fokus liegen darf. Gib mir den einen Auftrag dieses Ortes: worauf ich meine Aufmerksamkeit lege, was ich dort bewusst tue, wofür ich diesen Ort nutze. Dazu eine konkrete Handlung für die ersten Tage.

5. Der Schatten des Ortes. Jede Linie hat eine Schattenseite. Sag mir, wie sich der Schatten meiner stärksten Linie an diesem Ort zeigen kann und woran ich erkenne, dass ich in den Schatten rutsche.

6. Mein Wegweiser-Satz. Ein einziger Satz, den ich für diesen Ort mitnehme, und eine einzige Frage, die ich mir vor Ort stelle.

Schreib auf Deutsch, in der Du-Form, in Tiefe statt in Breite. Jeder Satz konkret. Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker.

Hier sind meine Daten:`;

  window.copyReiseReading = function(){
    const FULL = window.__fullChart || [];
    const ASP = window.__aspects || [];
    const R = window.__reise || {};
    const m = window.__meta || {};
    const ANGLE_PHRASE = { AC: 'auf dem Aszendenten', DC: 'auf dem Deszendenten', MC: 'auf dem MC', IC: 'auf dem IC' };
    const data = [];
    if(m.name) data.push('Name: ' + m.name);
    if(m.date){ const dp = m.date.split('-'); data.push('Geburtsdatum: ' + dp[2]+'.'+dp[1]+'.'+dp[0] + (m.time ? (' um ' + m.time + ' Uhr') : '')); }
    if(m.place) data.push('Geburtsort: ' + m.place);
    if(R.dest) data.push('Mein Reiseziel: ' + R.dest);
    data.push('');
    data.push('MEINE LINIEN AN DIESEM ORT (je enger der Orb, desto stärker):');
    const lines = R.lines || [];
    if(lines.length){
      lines.forEach(function(l){ data.push('- ' + l.planet + ' ' + (ANGLE_PHRASE[l.angle] || l.angle) + ' des Zielorts (Orb ' + String(l.orb).replace('.', ',') + '°)'); });
    } else {
      data.push('Keine Linie im Umkreis von 10°. Dieser Ort ist bei mir linienleise. Arbeite mit meinen Häusern am Zielort.');
    }
    if(R.acSign) data.push('Mein Aszendent am Zielort: ' + R.acSign + '.');
    if(R.mcSign) data.push('Mein MC am Zielort: ' + R.mcSign + '.');
    const rel = R.relocated || [];
    if(rel.length){
      data.push('');
      data.push('MEINE HÄUSER AM ZIELORT (Geburtshaus, dann Haus am Reiseziel):');
      rel.forEach(function(e){
        const from = e.natalHouse ? (e.natalHouse + '. Haus') : 'ohne Haus';
        const same = String(e.natalHouse) === String(e.destHouse);
        data.push('- ' + e.label + ': zu Hause ' + from + ', am Zielort ' + e.destHouse + '. Haus' + (same ? ' (bleibt gleich)' : ''));
      });
    }
    data.push('');
    data.push('MEIN GEBURTSHOROSKOP:');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });
    if(ASP.length){
      data.push('');
      data.push('MEINE WICHTIGSTEN NATALEN ASPEKTE:');
      ASP.forEach(function(a){ data.push(a.p1 + (a.s1 ? (' in ' + a.s1) : '') + ' ' + a.type + ' ' + a.p2 + (a.s2 ? (' in ' + a.s2) : '')); });
    }
    const full = REISE_PROMPT + '\n\n' + data.join('\n');
    const btn = document.getElementById('copyReiseBtn');
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
