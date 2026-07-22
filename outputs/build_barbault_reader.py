#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut den Barbault-Korb-Reader aus dem Business-Reader.
Muster: build_neumond_reader.py (Transit-Reader, Placidus, Womancode
Wein/Gold, schlanke Ergebnis-Seite, Tippfeld-Datum). Gleiches Design +
gleiche Astro-Engine, nur das Reading-Gehirn wird getauscht.

Der Reader rechnet ZWEI Charts mit derselben Engine:
  1. das Geburtshoroskop der Nutzerin (PLACIDUS)
  2. den Korb-Moment: 20.07.2026, 16:45 Uhr MESZ (Jupiter-Pluto-Opposition
     exakt, engine-verifiziert; alle vier Korb-Planeten auf dem 4. Grad:
     Pluto 4° Wassermann, Neptun 4° Widder, Uranus 4° Zwillinge,
     Jupiter 4° Löwe; Berlin als Ort, nur fuer die Zeitzone)

Der Reader zieht automatisch:
  - die exakten Grade der vier Korb-Planeten
  - das Placidus-Haus, in das jeder der vier bei der Nutzerin faellt
    (= welche Lebensbereiche die neuen Zyklen bei ihr umbauen)
  - Punkte auf der OFFENEN SEITE des Korbs (um 4° Waage, Orb 3 Grad):
    wer dort einen Punkt hat, macht die Figur mit dem eigenen Horoskop
    komplett (der Haken aus dem Kanaltext vom 15.07.)
  - Aspekte aller vier Korb-Planeten zu den natalen Punkten (Orb 3 Grad)
  - die natalen Positionen von Jupiter, Uranus, Neptun, Pluto (Verdrahtung)
und baut einen fertigen KI-Prompt zum Kopieren (Fokus 2026-2030, damit
der Reader auch nach dem 21.07. gueltig bleibt).

Geburtsdatum als Tippfeld TT.MM.JJJJ (Muster build_reise_reader.py).
Kein E-Mail-Gate. Abschluss-CTA -> AstroCode-Portal (Patrycjas Reise-Reader-Text 1:1).

DESIGN (Patrycjas Ansage 15.07.): ASTROCODE-Design aus reference/email-astrocode-design/
(Standard-Design 14.07.) statt Womancode Wein/Gold. Heller Vorlagen-Verlauf
(Hellviolett -> Lila -> Orange), Lesetext schwarz, Kaesten transparentes Weiss
(26px, weicher Schein), Buttons massiv NP-Indigo #312782 (Pill), Planeten+Haende
als Hero oben, Binaer-Zahlen als dezente Overlay-Kachel aus der Vorlage,
Abschluss NP-Logo + ASTROCODE-Schriftzug verlinkt aufs Portal.

Quelle:  astro-business-reader.html
Ziel:    astro-barbault-reader.html (+ astro-barbault-reader-netlify/index.html)
"""
import os, re, sys, shutil, io, base64
from PIL import Image, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-barbault-reader.html")
NETLIFY = os.path.join(HERE, "astro-barbault-reader-netlify")
TPL = os.path.join(HERE, "..", "reference", "email-astrocode-design", "vorlage-astrocode-original.webp")

# --- ASTROCODE-Slices aus Patrycjas Original-Vorlage (1080x1920) -------------
def jpg64(img, q):
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=q)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

_tpl = Image.open(TPL).convert("RGB")
# Hero: Planeten + Haende OHNE Headline-Zone (Headline bleibt HTML-H1)
HERO = jpg64(_tpl.crop((0, 0, 1080, 560)).resize((1300, 674), Image.LANCZOS), 85)
# Abschluss: NP-Logo + ASTROCODE-Schriftzug
FOOT = jpg64(_tpl.crop((0, 1560, 1080, 1920)).resize((1200, 400), Image.LANCZOS), 85)
# Binaer-Zahlen als Overlay-Kachel: Detail-Schicht der Vorlage auf Neutralgrau
# (mix-blend-mode overlay laesst nur die Zahlen-Geister auf dem CSS-Verlauf durch)
_strip = _tpl.crop((0, 700, 1080, 1560)).resize((600, 478), Image.LANCZOS)
_diff = ImageChops.subtract(_strip, _strip.filter(ImageFilter.GaussianBlur(14)))
TILE = jpg64(ImageChops.add(Image.new("RGB", _diff.size, (128, 128, 128)), _diff), 80)

# --- Korb-Moment (lokale Zeit, Engine loest Zeitzone ueber Koordinaten) -----
# Jupiter-Pluto-Opposition (Henkel/Kernaspekt) exakt am 20.07.2026 ~16:45 MESZ.
T_YEAR, T_MONTH, T_DATE = 2026, 7, 20
T_HOUR, T_MINUTE = 16, 45
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
     "<title>Der Barbault-Korb Reader</title>", "title")

# Eyebrow-Zeile komplett raus (Patrycja 15.07.: "Lass das weg!")
repl('<p class="header-eyebrow">Dein kosmischer Business-Blueprint</p>',
     '', "eyebrow-remove")

repl("<h1>Dein Business-Code</h1>",
     "<h1>Der Barbault-Korb Reader</h1>", "h1")

repl('<p class="subtitle">Gib deine Geburtsdaten ein. Auf der nächsten Seite bekommst du dein Geburtshoroskop angezeigt und einen fertigen KI-Prompt, der dir sagt, wie du dein Business führst, dich positionierst, skalierst und Geld verdienst.</p>',
     '<p class="subtitle">Vier langsam laufende Planeten stehen gleichzeitig auf dem 4. Grad und bilden die Konstellation, über die gerade alle sprechen: Pluto, Neptun, Uranus und Jupiter. Gib deine Geburtsdaten ein. Die Seite berechnet dein Geburtshoroskop, zeigt dir, welche Lebensbereiche der Korb bei dir berührt, und erstellt einen fertigen KI-Prompt für dein persönliches Reading.</p>',
     "subtitle")

repl('onclick="runCheck()">Meinen Business-Code aufdecken</button>',
     'onclick="runCheck()">Meinen individuellen KI-Prompt kreieren</button>', "submit-btn")

# Tip-Box raus (Patrycja 15.07.: "Gib deine Geburtsdaten ein." steht schon im Intro)
repl('''<div class="tip-box">
    <p><strong>Gib deine Geburtsdaten ein.</strong></p>
  </div>''', '', "tip-box-remove")

# --- E-Mail komplett entfernen (kein Opt-in, wie beim Neumond-Reader) -------
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
     "<h2>Dein Barbault-Korb${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Vier Planeten auf dem 4. Grad'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Neue Chart erstellen", "back-btn")

# --- 4. Korb-Berechnung in runCheck einhaengen ------------------------------
# Anker NACH window.__chart, damit __fullChart und __aspects bereits gesetzt sind.
calc_anchor = "      window.__chart = chart;\n      generateReading();"
transit_calc = """      window.__chart = chart;

      // Barbault-Korb: zweites Chart fuer den Kernaspekt-Moment rechnen
      // (Jupiter-Pluto-Opposition exakt). Ort Berlin, weil die Planeten-
      // Laengen ortsunabhaengig sind; die Engine braucht die Koordinaten
      // nur fuer die Zeitzone (16:45 Uhr Sommerzeit).
      (function(){
        try{
          const tOrigin = new Origin({ year: __T_YEAR__, month: __T_MONTH0__, date: __T_DATE__, hour: __T_HOUR__, minute: __T_MINUTE__, latitude: __T_LAT__, longitude: __T_LON__ });
          const tHoro = new Horoscope({ origin: tOrigin, houseSystem: 'placidus', zodiac: 'tropical', language: 'en', aspectTypes: ['major'] });
          const lonOf = function(b){ try{ return b.ChartPosition.Ecliptic.DecimalDegrees; }catch(e){ return null; } };
          const KORB = [
            ['Pluto', lonOf(tHoro.CelestialBodies.pluto)],
            ['Neptun', lonOf(tHoro.CelestialBodies.neptune)],
            ['Uranus', lonOf(tHoro.CelestialBodies.uranus)],
            ['Jupiter', lonOf(tHoro.CelestialBodies.jupiter)]
          ];
          if(KORB.some(function(p){ return p[1] == null; })) return;
          const SIGNS_DE = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische'];
          const fmtDeg = function(L){
            const inSign = L % 30;
            let d = Math.floor(inSign);
            let m = Math.round((inSign - d) * 60);
            if(m === 60){ m = 0; d += 1; }
            return d + '°' + (m < 10 ? '0' : '') + m + "' " + (SIGNS_DE[Math.floor(L / 30)] || '');
          };

          // Placidus-Haus jedes Korb-Grads: ueber die natalen Haeuserspitzen
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
          const points = KORB.map(function(p){
            return { name: p[0], text: fmtDeg(p[1]), house: houseOfLong(p[1]), lon: p[1] };
          });

          // Aspekte aller vier Korb-Planeten zu den natalen Punkten (Orb 3 Grad)
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
          points.forEach(function(p){ collect(p.lon, p.name); });
          hits.sort(function(a, b){ return a.orb - b.orb; });

          // Offene Ecken des Korbs: die vier Planeten besetzen 4 von 6 Ecken
          // eines 60°-Sechsecks, frei sind 4° Waage (184,4°) und 4° Schuetze
          // (244,4°). Ein nataler Punkt dort (Orb 3°, Patrycja 15.07.: die
          // Astrologie arbeitet immer mit Orb) bildet Aspekte zu ALLEN vier
          // Korb-Planeten und macht die Figur komplett.
          const OPENS = [[184.4, 'Waage'], [244.4, 'Schütze']];
          const libraPoints = [];
          OPENS.forEach(function(op){
            NATAL.forEach(function(pair){
              const L = lonOf(pair[1]);
              if(L == null) return;
              const d = Math.abs(((L - op[0] + 540) % 360) - 180);
              if(d <= 3) libraPoints.push({ point: pair[0], where: op[1], house: HOUSEOF[pair[0]] || '', orb: Math.round(d * 10) / 10 });
            });
          });

          // Natale Korb-Planeten (Verdrahtung mit den vier Kraeften)
          const natalOf = function(lbl){
            const e = FULL.find(function(x){ return x.label === lbl; }) || {};
            return { sign: e.sign || '', house: e.house || '' };
          };
          window.__transit = {
            points: points,
            hits: hits,
            libraPoints: libraPoints,
            natalJupiter: natalOf('Jupiter'),
            natalUranus: natalOf('Uranus'),
            natalNeptun: natalOf('Neptun'),
            natalPluto: natalOf('Pluto')
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

# --- 4b. Ergebnis-Seite verschlanken (REGEL seit 14.07.): Platzierungen, ----
# Aspekte und Element-Block raus. Nur Korb-Thema + Prompt bleiben sichtbar.
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

# --- 5. Reading-Block: sichtbares Korb-Thema + Prompt-CTA -------------------
old_cta = """  html += `
  <div class="cta-block">
    <h3>Dein Business-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, wie du dein Business führst, wie du dich positionierst, wo deine Zone of Genius liegt und wie du am natürlichsten Geld verdienst.</p>
    <button class="copy-btn" id="copyBizBtn" onclick="copyBusinessReading()">Business-Prompt + Daten kopieren</button>
  </div>`;"""

new_cta = """  // Sichtbares Korb-Thema
  const T = window.__transit || null;
  if(T){
    let tHtml = `
    <div class="data-block">
      <h3>Dein Platz im Barbault-Korb</h3>
      <div class="data-grid">`;
    (T.points || []).forEach(function(p){
      tHtml += `<div class="data-row"><span class="data-planet">${p.name} (${p.text}) fällt in dein</span><span class="data-values">${p.house ? `<span class="badge house-badge">${p.house}. Haus</span>` : `<span class="badge sign-badge">Haus unbestimmt</span>`}</span></div>`;
    });
    const lib = (T.libraPoints || []).map(function(e){ return e.point + ' (' + (e.where || 'Waage') + (e.house ? (', ' + e.house + '. Haus') : '') + ')'; });
    tHtml += `<div class="data-row"><span class="data-planet">Offene Ecken des Korbs (um 4° Waage und 4° Schütze)</span><span class="data-values"><span class="badge sign-badge">${lib.length ? lib.join(', ') : 'keine Punkte'}</span></span></div>`;
    const hitStr = (T.hits || []).map(function(h){ return h.who + ' ' + h.type + ' ' + h.point; }).join(', ');
    tHtml += `<div class="data-row"><span class="data-planet">Der Korb trifft bei dir</span><span class="data-values"><span class="badge sign-badge">${hitStr || 'keine engen Aspekte'}</span></span></div>`;
    tHtml += `</div></div>`;
    html += tHtml;
  }

  html += `
  <div class="cta-block">
    <h3>Dein Korb-Reading mit KI</h3>
    <p>Wie wirkt sich diese kollektive Energie der langsam laufenden Planeten auf dein eigenes Geburtshoroskop aus? Kopiere den Prompt und füge ihn bei ChatGPT oder Claude ein. Wo darf dein Fokus die nächsten Jahre liegen?</p>
    <button class="copy-btn" id="copyKorbBtn" onclick="copyBarbaultReading()">Korb-Prompt + Daten kopieren</button>
  </div>`;"""
repl(old_cta, new_cta, "cta-block")

# --- 6. Abschluss-CTA: AstroCode-Portal (Patrycjas NEUER Text 15.07., 1:1,
# nur Rechtschreibung: Barbault-Tippfehler, "dank" klein, "als" statt "wie",
# "aktive" klein, "haengen bleiben" ergaenzt, Bindestrich im Portal-Namen) ----
repl('''  html += `
  <div class="cta-block">
    <p class="cta-kicker">Möchtest du noch tiefer in deine Chart eintauchen?</p>
    <h3>Lerne dich tiefer kennen, als Jahre der Selbstreflexion es je konnten.</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Hier erfährst du mehr: Dein AstroCode &rarr;</a>
  </div>`;''',
'''  html += `
  <div class="cta-block astro-cta">
    <p class="cta-kicker">Dir gefallen die Antworten aus meinem Barbault-Korb Reader?</p>
    <h3>Weißt du, dass du dank meines Astrocode-Portals dein ganzes Geburtshoroskop analysieren kannst! Tiefer als jedes Astroreading, denn erst die Bewegung bewirkt Veränderung! Wie oft hast du schon was über dich gehört, aber nicht umgesetzt!</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Öffne dein Astrocode-Portal und begib dich auf eine unvergessliche Reise zurück zu dir!</a>
  </div>`;''',
"astrocode-cta")

# --- 7. Prompt-Gehirn + Copy-Funktion austauschen --------------------------
new_region = r"""  const BARBAULT_PROMPT = `Du bist eine erfahrene Bewusstseinsastrologin mit Fokus auf Mundanastrologie und Transite. Du liest meine Chart in Schichten und schreibst klar, tief und direkt, so dass mich jeder Satz trifft. Keine Floskeln, keine allgemeinen Astro-Sätze, kein Lehrbuchton.

Das Ereignis: Um den 20. Juli 2026 stehen vier gesellschaftliche Planeten gleichzeitig auf dem 4. Grad von vier Zeichen: Pluto auf 4° Wassermann, Neptun auf 4° Widder, Uranus auf 4° Zwillinge und Jupiter auf 4° Löwe. Die Aspekte dazwischen (zwei Sextile, zwei Trigone und die Opposition von Jupiter zu Pluto als Kernaspekt) ergeben gezeichnet eine Figur wie ein Korb mit Henkel. Astrologen nennen sie den Barbault-Korb, nach dem französischen Mundanastrologen André Barbault, der die Jahre 2026 bis 2030 als großen Wendepunkt beschrieb. Das Besondere: Alle vier Planeten haben gerade erst neue Zeichen betreten. Neptun steht zum ersten Mal seit 1861 im Widder, Uranus erreicht zum ersten Mal seit 1941 die Zwillinge, Pluto hat sich vor Kurzem dauerhaft im Wassermann eingerichtet. Mehrere große Zyklen beginnen gleichzeitig neu, und der Korb ist der Moment, in dem sie zum ersten Mal sichtbar zusammenwirken. Die Themen: Pluto im Wassermann stellt Machtfragen an Technologie und Daten, Neptun im Widder sucht neue Ideale, für die Menschen losgehen, Uranus in den Zwillingen verändert Kommunikation und Denken, Jupiter im Löwen vergrößert Sichtbarkeit und Machtansprüche. Die Figur hat zwei offene Ecken: 4° Waage und 4° Schütze. Wer dort einen Punkt hat, bildet Aspekte zu allen vier Korb-Planeten und macht die Figur mit dem eigenen Horoskop komplett. Die Astrologie arbeitet dabei immer mit einem Orb: Niemand muss exakt auf dem 4. Grad stehen, in meinen Daten unten ist jeder Treffer mit bis zu 3° Orb berücksichtigt. Die Aspekte des Korbs werden zwischen dem 15. und 25. Juli 2026 nacheinander exakt: den Auftakt macht das Uranus-Neptun-Sextil am 15. Juli, den Abschluss das Neptun-Pluto-Sextil am 25. Juli. Die Phase, die hier beginnt, trägt bis 2030.

Wichtig: Ich arbeite mit Placidus-Häusern. Alle Häuser in meinen Daten unten sind Placidus-Häuser. Der Korb ist eine kollektive Konstellation. Wie stark und wo sie mich persönlich berührt, zeigen die Häuser und die Aspekte zu meinen Punkten unten.

Unten bekommst du:
- die genauen Grade der vier Korb-Planeten und das Haus, in das jeder bei mir fällt
- meine Punkte auf den offenen Ecken des Korbs (um 4° Waage und 4° Schütze), falls vorhanden
- die Aspekte der Korb-Planeten zu meinen natalen Punkten (mit Orb, je enger, desto stärker)
- meine natalen Positionen von Jupiter, Uranus, Neptun und Pluto (meine eigene Verdrahtung mit diesen Kräften)
- mein vollständiges Chart als Kontext

Schreibe mir auf dieser Basis:

1. Das große Bild. Ein kraftvoller Absatz: was diese Konstellation kollektiv anzeigt und welcher der vier Bereiche mich nach meiner Chart am stärksten betrifft. Sprich mich direkt mit du an.

2. Die vier Häuser. Geh die vier Korb-Planeten einzeln durch. Für jeden: In welches Haus fällt er bei mir, wie zeigt sich dieser Lebensbereich in meinem Alltag, und was beginnt dort in den kommenden Jahren neu? Mach jeden Bereich konkret, keine Kategorien.

3. Direkte Treffer. Geh jeden Aspekt durch, den ein Korb-Planet zu meinen natalen Punkten bildet. Erkläre für jeden, was der Aspekt bedeutet und was er in genau diesem Punkt meiner Chart auslöst. Beginne mit dem engsten Orb, der wirkt am stärksten. Habe ich keine engen Aspekte, sag mir ehrlich: Der Korb läuft bei mir im Hintergrund, und die vier Häuser zeigen trotzdem, in welchen Lebensbereichen sich die neuen Zyklen bei mir auswirken.

4. Die offenen Ecken. Habe ich einen Punkt um 4° Waage oder 4° Schütze, lies ihn genau: Ich vervollständige die Figur mit meinem eigenen Horoskop, und dieser Punkt beschreibt meinen Beitrag. Die Waage steht für Begegnung, Ausgleich und Beziehung, der Schütze für Sinn, Wahrheit und Ausrichtung. Was heißt das für meine Rolle in dieser Zeit? Habe ich dort keinen Punkt, überspringe diesen Schritt ohne Ersatz.

5. Meine Verdrahtung. Lies meine natalen Positionen: Jupiter (wo ich wachse und Vertrauen habe), Uranus (wo ich frei sein will), Neptun (wo ich träume und mich hingebe), Pluto (wo ich Tiefe und Wandlungskraft lebe), jeweils nach Zeichen und Haus. Das ist meine angeborene Beziehung zu genau den Kräften, die jetzt kollektiv neu starten.

6. Schatten und Geschenk. Der Schatten dieser Zeit: Ich hänge in Nachrichten und fremden Meinungen fest, ich halte an einer Ordnung fest, die innerlich längst zu Ende ist, und ich verwechsle Dauerunruhe mit Wachheit. Das Geschenk: Ich erkenne, welches Kapitel in meinem Leben gleichzeitig mit der Welt neu beginnt, und ich beziehe Position, statt zuzuschauen. Sag mir, woran ich bei mir erkenne, ob ich im Schatten oder im Geschenk unterwegs bin.

7. Mein Platz in der neuen Zeit. Formuliere aus allem einen Fokus für die Jahre 2026 bis 2030: ein einziger Satz in der Ich-Form, den ich mir aufschreiben kann. Dazu eine kleine, konkrete Handlung für die Tage um den 20. Juli, die zu meiner Chart passt.

8. Meine Korb-Frage. Eine einzige, konfrontierende Frage zu der alten Ordnung in meinem Leben, die nur noch hält, weil ich sie gewohnt bin.

Schreib auf Deutsch, in der Du-Form, in Tiefe statt in Breite. Jeder Satz konkret. Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker.

Hier sind meine Daten:`;

  window.copyBarbaultReading = function(){
    const FULL = window.__fullChart || [];
    const ASP = window.__aspects || [];
    const T = window.__transit || {};
    const m = window.__meta || {};
    const data = [];
    if(m.name) data.push('Name: ' + m.name);
    if(m.date){ const dp = m.date.split('-'); data.push('Geburtsdatum: ' + dp[2]+'.'+dp[1]+'.'+dp[0] + (m.time ? (' um ' + m.time + ' Uhr') : '')); }
    if(m.place) data.push('Geburtsort: ' + m.place);
    data.push('');
    data.push('MEIN BARBAULT-KORB (Kernaspekt Jupiter-Pluto exakt am 20. Juli 2026):');
    (T.points || []).forEach(function(p){
      data.push(p.name + ' steht bei ' + p.text + (p.house ? (' und fällt in mein ' + p.house + '. Haus.') : '.'));
    });
    const lib = T.libraPoints || [];
    if(lib.length){
      data.push('Offene Ecken des Korbs (um 4° Waage und 4° Schütze, Orb bis 3°): ' + lib.map(function(e){ return e.point + ' auf der ' + (e.where || 'Waage') + '-Ecke' + (e.house ? (' (' + e.house + '. Haus, Orb ' + String(e.orb).replace('.', ',') + '°)') : (' (Orb ' + String(e.orb).replace('.', ',') + '°)')); }).join(', ') + '. Ich mache die Figur mit meinem Horoskop komplett.');
    } else {
      data.push('Offene Ecken des Korbs (um 4° Waage und 4° Schütze, Orb bis 3°): keine Punkte. Der Korb bleibt bei mir offen.');
    }
    const hits = T.hits || [];
    if(hits.length){
      data.push('Aspekte der Korb-Planeten zu meinen natalen Punkten (engster Orb wirkt am stärksten):');
      hits.forEach(function(h){ data.push('- Korb-' + h.who + ' ' + h.type + ' zu ' + h.point + (h.sign ? (' in ' + h.sign) : '') + (h.house ? (', ' + h.house + '. Haus') : '') + ' (Orb ' + String(h.orb).replace('.', ',') + '°)'); });
    } else {
      data.push('Die Korb-Planeten bilden keine engen Aspekte (Orb bis 3°) zu meinen natalen Punkten. Arbeite mit den vier Häusern und meiner Verdrahtung.');
    }
    data.push('Meine natalen Korb-Planeten (meine Verdrahtung):');
    if(T.natalJupiter && T.natalJupiter.sign) data.push('Jupiter: ' + T.natalJupiter.sign + (T.natalJupiter.house ? (', ' + T.natalJupiter.house + '. Haus') : ''));
    if(T.natalUranus && T.natalUranus.sign) data.push('Uranus: ' + T.natalUranus.sign + (T.natalUranus.house ? (', ' + T.natalUranus.house + '. Haus') : ''));
    if(T.natalNeptun && T.natalNeptun.sign) data.push('Neptun: ' + T.natalNeptun.sign + (T.natalNeptun.house ? (', ' + T.natalNeptun.house + '. Haus') : ''));
    if(T.natalPluto && T.natalPluto.sign) data.push('Pluto: ' + T.natalPluto.sign + (T.natalPluto.house ? (', ' + T.natalPluto.house + '. Haus') : ''));
    data.push('');
    data.push('MEIN VOLLSTÄNDIGES CHART (Placidus-Häuser):');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });
    if(ASP.length){
      data.push('');
      data.push('MEINE WICHTIGSTEN NATALEN ASPEKTE:');
      ASP.forEach(function(a){ data.push(a.p1 + (a.s1 ? (' in ' + a.s1) : '') + ' ' + a.type + ' ' + a.p2 + (a.s2 ? (' in ' + a.s2) : '')); });
    }
    const full = BARBAULT_PROMPT + '\n\n' + data.join('\n');
    const btn = document.getElementById('copyKorbBtn');
    const done = function(){ if(btn){ const o = btn.getAttribute('data-label') || btn.textContent; btn.setAttribute('data-label', o); btn.textContent = '✓ Kopiert! Jetzt in ChatGPT einfügen'; setTimeout(function(){ btn.textContent = o; }, 2800); } };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(full).then(done).catch(function(){ fallbackCopy(full, done); });
    } else { fallbackCopy(full, done); }
  };"""

pat = re.compile(r"  const BUSINESS_PROMPT = `.*?\n  window\.copyBusinessReading = function\(\)\{.*?\n  \};", re.DOTALL)
if not pat.search(s):
    sys.exit("FEHLT: BUSINESS_PROMPT / copyBusinessReading Region")
s = pat.sub(lambda _: new_region, s, count=1)

# --- 8. ASTROCODE-Design als Override-Layer (gewinnt, weil zuletzt im Head) --
# Heller Vorlagen-Verlauf, Lesetext schwarz, Kaesten transparentes Weiss,
# Buttons NP-Indigo, Planeten+Haende oben, Binaer-Kachel dezent im Hintergrund.
extra_css = '''<style>
html{ background:#8d7fc7 linear-gradient(180deg,#8B8ED9 0%,#A06AB5 18%,#8979C1 37%,#9267A8 58%,#B6697D 79%,#DB705C 100%) !important;
  background-size:100% 100% !important; }
body{ background:transparent !important; color:#111111 !important; }
#binary-canvas{ display:none !important; }
/* Binaer-Zahlen der Vorlage als dezente Overlay-Kachel */
body::after{ content:"" !important; position:fixed; inset:0; z-index:0; pointer-events:none;
  background:url("__TILE__") !important; background-size:620px auto !important; background-repeat:repeat !important;
  mix-blend-mode:overlay; opacity:0.5; }
/* Planeten + Haende aus der Vorlage als eigenes Bild oben — der Text
   beginnt DARUNTER (Patrycja 15.07.: das Bild nicht ueberschreiben).
   Negativer Abstand zieht den Text hoch in die ausgefadete Zone unter
   den Planeten (Patrycja 15.07.: "noch ein bisschen weiter hoch"). */
.moon-scene{ position:relative !important; top:auto !important;
  background:url("__HERO__") center top / cover no-repeat !important;
  height:clamp(220px, 42vw, 540px) !important; opacity:1 !important;
  margin-bottom:clamp(-100px, -6vw, -30px) !important; }
/* Ruhiger Kopf (REGEL seit 14.07.): Eyebrow + Intro in Lesschrift, Display-Schrift nur fuer die H1. */
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
/* Intro groesser, fett und in Indigo wie die Orts-Bestaetigung, und direkt
   an die Eingabe angeschlossen (Patrycja 15.07.) */
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
/* Orts-Bestaetigung (Haekchen) war gold und ging unter (Patrycja 15.07.) */
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
/* Mehr Luft zwischen den Kaesten (Patrycja 15.07.) */
.data-block, .reading-block, .summary-block, .cta-block{ margin:36px 0 !important; }
/* CTA-Ueberschrift muss auffallen (Patrycja 15.07.): Kicker gross und fett
   statt kursiv-klein, H3 im CTA-Block groesser */
.cta-kicker{
  font-size:clamp(1.15rem, 2.4vw, 1.45rem) !important;
  font-weight:800 !important;
  font-style:normal !important;
  color:#312782 !important;
  letter-spacing:0.01em !important;
  margin-bottom:16px !important;
}
.cta-block h3{ font-size:clamp(1.15rem, 2.2vw, 1.4rem) !important; line-height:1.5 !important; }
/* Text in den CTA-Kaesten schwarz (Patrycja 15.07.: "kaum zu erkennen") */
.cta-block p{ color:#111111 !important; }
/* AstroCode-Abschlussblock: langer Satz nicht in Display-Grossbuchstaben,
   sondern Lesschrift in Schwarz; Button darf zweizeilig sein */
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
  /* Keine Grossbuchstaben-Buttons (Patrycja 15.07.: "Meinen Platz im Korb aufdecken", nicht SCHREIEND) */
  text-transform:none !important;
  letter-spacing:0.04em !important;
  box-shadow:0 10px 32px rgba(49,39,130,0.40) !important; }
.submit-btn:hover, .cta-link:hover, .copy-btn:hover{ background:#3d31a0 !important; box-shadow:0 14px 44px rgba(49,39,130,0.55) !important; }
.back-btn{ color:#312782 !important; }
.legal-footer, .legal-footer a{ color:#1c1440 !important; }
.legal-logo{ display:none !important; }
/* ASTROCODE-Abschluss randlos in den Verlauf eingeblendet (kein Kasten,
   Patrycja 15.07.) — volle Breite, oben weich eingefadet */
.astrocode-footer{ display:block; position:relative; z-index:2; width:100%; margin:56px 0 0; }
.astrocode-footer img{ width:100%; height:auto; display:block;
  -webkit-mask-image:linear-gradient(to bottom, transparent 0, #000 22%);
  mask-image:linear-gradient(to bottom, transparent 0, #000 22%); }
</style>
</head>'''.replace("__HERO__", HERO).replace("__TILE__", TILE)
repl('</head>', extra_css, "astrocode-css")

# --- 8b. ASTROCODE-Abschluss (NP-Logo + Schriftzug) vor dem Footer, verlinkt aufs Portal
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
