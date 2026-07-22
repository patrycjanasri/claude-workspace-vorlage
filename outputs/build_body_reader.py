#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut den Body-Reader ("Dein Body-Code") aus dem Business-Reader.
Patrycjas persoenliches Test-Tool (18.07.2026): Was sagt meine Chart zu
Ernaehrung, Bewegung, Routinen und Gewicht?

Gleiches Design + gleiche Astro-Engine (Placidus). Der Reader zieht
automatisch diese Schichten in window.__body:
  - Mond (Zeichen, Haus) + alle Mond-Aspekte  -> Nahrungs-Kern
  - 6. Haus: Zeichen auf der Spitze, Herrscher (moderne Herrscher wie im
    Chartruler-Reader) + Planeten im Haus     -> Routinen
  - Aszendent + Punkte im 1. Haus             -> Koerper/Konstitution
  - Mars                                      -> Bewegung
  - Venus                                     -> Genuss
  - Jupiter + Saturn                          -> Gewichts-Achse
  - Lilith                                    -> unterdrueckte wilde Kraft
  - Ceres                                     -> Urthema Naehren/Genaehrt-werden
    (aus der eingebackenen JPL-Horizons-Ephemeride des Womancode-Readers,
     Abdeckung Geburtsjahrgaenge 1950-2015; ausserhalb faellt Ceres still weg)

Haltung des Prompts: kein Diaetplan, keine Kalorien, nichts Medizinisches.
Der Koerper ist ein Bote.

Geburtsdatum als Tippfeld TT.MM.JJJJ (Muster build_reise_reader.py).
Ergebnis-Seite schlank (REGEL seit 14.07.): nur Body-Block + Prompt-Button,
volles Chart + Aspekte stecken unsichtbar im kopierten Prompt.
Kein E-Mail-Gate, kein Abschluss-CTA (persoenliches Tool, werbefrei).

Quelle:  astro-business-reader.html (+ Ceres aus womancode-asteroids-data.js)
Ziel:    astro-body-reader.html (+ astro-body-reader-netlify/index.html)
"""
import os, re, sys, json, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-body-reader.html")
NETLIFY = os.path.join(HERE, "astro-body-reader-netlify")

# --- Ceres-Ephemeride aus der Womancode-Datendatei ziehen -------------------
with open(os.path.join(HERE, "womancode-asteroids-data.js"), encoding="utf-8") as f:
    _ast_js = f.read()
_m = re.search(r"window\.WC_AST = (\{.*\});", _ast_js, re.S)
if not _m:
    sys.exit("FEHLT: WC_AST in womancode-asteroids-data.js")
_ast = json.loads(_m.group(1))
_ceres = _ast["bodies"]["Ceres"]
BODY_CERES_JSON = json.dumps(
    {"jd0": _ast["jd0"], "step": _ast["step"], "vals": _ceres["vals"]},
    separators=(",", ":"))

with open(SRC, "r", encoding="utf-8") as f:
    s = f.read()

def repl(old, new, label):
    global s
    if old not in s:
        sys.exit("FEHLT (" + label + "): " + old[:80])
    s = s.replace(old, new, 1)

# --- 1. Branding / sichtbare Texte ---------------------------------------
repl("<title>Dein Business-Code</title>",
     "<title>Dein Body-Code</title>", "title")

# Eyebrow-Zeile komplett raus (Patrycja 18.07.: "Das lassen wir weg")
repl('<p class="header-eyebrow">Dein kosmischer Business-Blueprint</p>',
     '', "eyebrow-remove")

repl("<h1>Dein Business-Code</h1>",
     "<h1>Dein Body-Code</h1>", "h1")

repl('<p class="subtitle">Gib deine Geburtsdaten ein. Auf der nächsten Seite bekommst du dein Geburtshoroskop angezeigt und einen fertigen KI-Prompt, der dir sagt, wie du dein Business führst, dich positionierst, skalierst und Geld verdienst.</p>',
     '<p class="subtitle">Gib deine Geburtsdaten ein. Die Seite berechnet dein Geburtshoroskop und erstellt einen fertigen KI-Prompt: was deine Chart über deine Ernährung sagt, über deine Bewegung, deine Routinen und dein Gewicht.</p>',
     "subtitle")

repl('onclick="runCheck()">Meinen Business-Code aufdecken</button>',
     'onclick="runCheck()">Meinen Body-Code aufdecken</button>', "submit-btn")

# --- E-Mail komplett entfernen (kein Opt-in) --------------------------------
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
     "<h2>Dein Body-Code${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Was deine Chart über deinen Körper sagt'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Neuen Body-Code erstellen", "back-btn")

# --- 4. Ceres-Ephemeride + Helfer VOR generateReading einhaengen ------------
# Decode/Interpolation/Haus-Zuordnung 1:1 aus dem Womancode-Reader (dort
# gegen JPL Horizons und die Engine-Haeuser verifiziert).
ceres_helpers = r"""window.BODY_CERES = __CERES_JSON__;
function bodyDecode(s){ const out=[]; for(let i=0;i<s.length;i+=3){ out.push(parseInt(s.substr(i,3),36)/100); } return out; }
function bodyInterp(vals, jd0, step, J){
  const x=(J-jd0)/step; let i=Math.floor(x); const f=x-i;
  if(i<0) i=0; if(i>=vals.length-1) i=vals.length-2;
  let a=vals[i], b=vals[i+1];
  if(b-a>180) b-=360; else if(a-b>180) b+=360;
  return (((a+(b-a)*f)%360)+360)%360;
}
function bodyHouseCusps(horo){
  const c=[];
  if(!horo || !horo.Houses) return c;
  for(let h=0;h<12;h++){
    const H=horo.Houses[h];
    const deg=(H && H.ChartPosition && H.ChartPosition.StartPosition && H.ChartPosition.StartPosition.Ecliptic)
      ? H.ChartPosition.StartPosition.Ecliptic.DecimalDegrees : null;
    c.push(deg);
  }
  return c;
}
function bodyAssignHouse(lon, cusps){
  if(!cusps || cusps.length!==12 || cusps.some(x=>x==null)) return '';
  lon=((lon%360)+360)%360;
  for(let h=0;h<12;h++){
    let a=cusps[h], b=cusps[(h+1)%12];
    if(b<=a) b+=360;
    let L=lon; if(L<a) L+=360;
    if(L>=a && L<b) return h+1;
  }
  return '';
}

function generateReading() {""".replace("__CERES_JSON__", BODY_CERES_JSON)
repl("function generateReading() {", ceres_helpers, "ceres-helpers-injection")

# --- 5. Body-Schichten in runCheck berechnen --------------------------------
# Anker NACH window.__chart, damit __fullChart und __aspects bereits gesetzt sind.
calc_anchor = "      window.__chart = chart;\n      generateReading();"
body_calc = """      window.__chart = chart;

      // Body-Schichten: Mond, 6. Haus, Koerper, Bewegung, Genuss,
      // Gewichts-Achse, Lilith, Ceres.
      (function(){
        try{
          const SIGNS_DE = ['Widder','Stier','Zwillinge','Krebs','Löwe','Jungfrau','Waage','Skorpion','Schütze','Steinbock','Wassermann','Fische'];
          const FULL = window.__fullChart || [];
          const byLabel = function(l){ return FULL.find(function(e){ return e.label === l; }) || null; };

          // 6. Haus: Zeichen auf der Placidus-Spitze + moderner Herrscher
          // (Zuordnung wie im Chartruler-Reader) + Planeten im Haus
          let cusp6Sign = '';
          try{
            const H6 = horo.Houses[5];
            const deg6 = H6.ChartPosition.StartPosition.Ecliptic.DecimalDegrees;
            cusp6Sign = SIGNS_DE[Math.floor((((deg6 % 360) + 360) % 360) / 30)] || '';
          }catch(e){}
          const RULER = { 'Widder':'Mars','Stier':'Venus','Zwillinge':'Merkur','Krebs':'Mond','Löwe':'Sonne','Jungfrau':'Merkur','Waage':'Venus','Skorpion':'Pluto','Schütze':'Jupiter','Steinbock':'Saturn','Wassermann':'Uranus','Fische':'Neptun' };
          const rulerName = RULER[cusp6Sign] || '';
          const rulerEntry = rulerName ? byLabel(rulerName) : null;
          const h6points = FULL.filter(function(e){ return Number(e.house) === 6; }).map(function(e){ return e.label; });
          const h1points = FULL.filter(function(e){ return Number(e.house) === 1 && e.label !== 'Aszendent'; }).map(function(e){ return e.label; });
          const moonAspects = (window.__aspects || []).filter(function(a){ return a.p1 === 'Mond' || a.p2 === 'Mond'; });

          // Ceres aus der eingebackenen JPL-Ephemeride (Muster Womancode-Reader).
          // Abdeckung 1950-2015; ausserhalb faellt Ceres still weg.
          let ceres = null;
          try{
            const D = window.BODY_CERES;
            const J = origin.julianDate;
            if(D && typeof J === 'number'){
              const vals = bodyDecode(D.vals);
              const maxJ = D.jd0 + D.step * (vals.length - 1);
              if(J >= D.jd0 && J <= maxJ){
                const lon = bodyInterp(vals, D.jd0, D.step, J);
                const cusps = bodyHouseCusps(horo);
                ceres = { sign: SIGNS_DE[Math.floor(((((lon % 360) + 360) % 360)) / 30)] || '', house: bodyAssignHouse(lon, cusps) };
              }
            }
          }catch(e){}

          window.__body = {
            moon: byLabel('Mond'),
            moonAspects: moonAspects,
            house6: { sign: cusp6Sign, ruler: rulerName, rulerEntry: rulerEntry, points: h6points },
            asc: byLabel('Aszendent'),
            house1Points: h1points,
            mars: byLabel('Mars'),
            venus: byLabel('Venus'),
            jupiter: byLabel('Jupiter'),
            saturn: byLabel('Saturn'),
            lilith: byLabel('Lilith'),
            ceres: ceres
          };
        }catch(e){ window.__body = null; }
      })();

      generateReading();"""
repl(calc_anchor, body_calc, "body-calc-injection")

# --- 6. Ergebnis-Seite verschlanken (REGEL seit 14.07.) ---------------------
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

# --- 7. Reading-Block: sichtbares Body-Thema + Prompt-CTA -------------------
old_cta = """  html += `
  <div class="cta-block">
    <h3>Dein Business-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, wie du dein Business führst, wie du dich positionierst, wo deine Zone of Genius liegt und wie du am natürlichsten Geld verdienst.</p>
    <button class="copy-btn" id="copyBizBtn" onclick="copyBusinessReading()">Business-Prompt + Daten kopieren</button>
  </div>`;"""

new_cta = """  // Sichtbarer Body-Block: die Schichten auf einen Blick
  const B = window.__body || null;
  if(B){
    const row = function(label, entry){
      if(!entry || !entry.sign) return '';
      return `<div class="data-row"><span class="data-planet">${label}</span><span class="data-values"><span class="badge sign-badge">${entry.sign}</span>${entry.house ? `<span class="badge house-badge">${entry.house}. Haus</span>` : ''}</span></div>`;
    };
    let bHtml = `
    <div class="data-block">
      <h3>Dein Body-Code auf einen Blick</h3>
      <div class="data-grid">`;
    bHtml += row('Mond (was dich nährt)', B.moon);
    if(B.house6 && B.house6.sign){
      bHtml += `<div class="data-row"><span class="data-planet">6. Haus (deine Routinen)</span><span class="data-values"><span class="badge sign-badge">${B.house6.sign}</span></span></div>`;
      if(B.house6.rulerEntry) bHtml += row('Herrscher des 6. Hauses: ' + B.house6.ruler, B.house6.rulerEntry);
      bHtml += `<div class="data-row"><span class="data-planet">Planeten im 6. Haus</span><span class="data-values"><span class="badge sign-badge">${B.house6.points.length ? B.house6.points.join(', ') : 'keine'}</span></span></div>`;
    }
    if(B.asc && B.asc.sign) bHtml += `<div class="data-row"><span class="data-planet">Aszendent (dein Körper)</span><span class="data-values"><span class="badge sign-badge">${B.asc.sign}</span></span></div>`;
    bHtml += row('Mars (deine Bewegung)', B.mars);
    bHtml += row('Venus (dein Genuss)', B.venus);
    bHtml += row('Jupiter (dein Übermaß)', B.jupiter);
    bHtml += row('Saturn (deine Struktur)', B.saturn);
    bHtml += row('Lilith (deine wilde Kraft)', B.lilith);
    bHtml += row('Ceres (dein Nähren)', B.ceres);
    const mAsp = (B.moonAspects || []).map(function(a){ return a.p1 === 'Mond' ? (a.type + ' ' + a.p2) : (a.type + ' ' + a.p1); }).join(', ');
    bHtml += `<div class="data-row"><span class="data-planet">Deine Mond-Aspekte</span><span class="data-values"><span class="badge sign-badge">${mAsp || 'keine engen Aspekte'}</span></span></div>`;
    bHtml += `</div></div>`;
    html += bHtml;
  }

  html += `
  <div class="cta-block">
    <h3>Dein Body-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, was dich wirklich nährt, welche Bewegung und welche Routinen zu deiner Chart passen und was deine Chart über dein Gewicht sagt.</p>
    <button class="copy-btn" id="copyBodyBtn" onclick="copyBodyReading()">Body-Prompt + Daten kopieren</button>
  </div>`;"""
repl(old_cta, new_cta, "cta-block")

# --- 8. Abschluss-CTA: AstroCode-Kurs mit Patrycjas Text 1:1 (18.07.) -------
repl('''  html += `
  <div class="cta-block">
    <p class="cta-kicker">Möchtest du noch tiefer in deine Chart eintauchen?</p>
    <h3>Lerne dich tiefer kennen, als Jahre der Selbstreflexion es je konnten.</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Hier erfährst du mehr: Dein AstroCode &rarr;</a>
  </div>`;

''', '''  html += `
  <div class="cta-block">
    <p class="cta-kicker">Willst du noch tiefer in deine Chart eintauchen?</p>
    <h3>Dann hol dir jetzt meinen AstroCode! Ein etwas anderer Kurs! Eine intensive Reise in dein Geburtshoroskop!</h3>
    <a href="https://patrycja-nasri.de/dein-astrocode/" target="_blank" class="cta-link">Hol dir jetzt meinen AstroCode &rarr;</a>
  </div>`;

''', "astrocode-cta")

# --- 9. Prompt-Gehirn + Copy-Funktion austauschen --------------------------
new_region = r"""  const BODY_PROMPT = `Du bist eine erfahrene Bewusstseinsastrologin mit Fokus auf Körper, Ernährung und Alltag. Du liest meine Chart in Schichten und schreibst klar, tief und direkt, so dass mich jeder Satz trifft. Keine Floskeln, keine allgemeinen Astro-Sätze, kein Lehrbuchton.

Worum es geht: Ich will verstehen, was meine Chart über meinen Körper sagt. Über meine Ernährung, meine Bewegung, meine Routinen und mein Gewicht. Deine Haltung dabei: Mein Körper ist ein Bote. Er zeigt mir, was in mir Aufmerksamkeit braucht. Du schreibst keinen Diätplan, du zählst keine Kalorien und du gibst keine medizinischen Ratschläge. Du zeigst mir, warum ich esse, wie ich esse, warum mein Körper hält, was er hält, und welche Art von Ernährung, Bewegung und Routine zu meiner Chart passt.

Wichtig: Ich arbeite mit Placidus-Häusern. Alle Häuser in meinen Daten unten sind Placidus-Häuser.

Unten bekommst du:
- meinen Mond mit seinen Aspekten (mein Nahrungs-Kern)
- mein 6. Haus: das Zeichen auf der Häuserspitze, den Herrscher des Hauses und die Planeten im Haus (meine Routinen)
- meinen Aszendenten und die Punkte in meinem 1. Haus (mein Körper)
- meinen Mars (meine Bewegung) und meine Venus (mein Genuss)
- meinen Jupiter und meinen Saturn (meine Gewichts-Achse)
- meine Lilith und meine Ceres (meine wilde Kraft und mein Urthema des Nährens)
- mein vollständiges Chart und meine wichtigsten Aspekte als Kontext

Schreibe mir auf dieser Basis:

1. Mein Nahrungs-Kern. Lies meinen Mond nach Zeichen und Haus: was mich wirklich nährt und was ich mit Essen fülle, wenn mir genau das fehlt. Geh dann jeden Mond-Aspekt einzeln durch und sag mir, wie er mein Essverhalten prägt. Ein Mond im Aspekt zu Jupiter greift anders zum Essen als ein Mond im Aspekt zu Saturn oder Pluto. Sag mir konkret, in welchen Momenten ich esse, ohne Hunger zu haben, und wonach ich in diesen Momenten wirklich hungere.

2. Meine Routinen. Lies mein 6. Haus: das Zeichen auf der Spitze, den Herrscher des Hauses mit seiner Position und die Planeten im Haus. Sag mir, welche Art von Ernährungs- und Bewegungsroutine zu mir passt und wie sie aussehen darf, damit ich sie über Monate halte. Sag mir auch, warum Routinen, die für andere funktionieren, bei mir gescheitert sind.

3. Mein Körper. Lies meinen Aszendenten und die Punkte in meinem 1. Haus: meine Konstitution, wie ich in meinem Körper wohne und wie mein Körper auf mein Leben antwortet, wenn ich ihn überhöre.

4. Meine Bewegung. Lies meinen Mars nach Zeichen und Haus: welche Bewegung meine Energie wirklich in Fluss bringt und welche mich Überwindung kostet, weil sie gegen meine Natur läuft. Nenne konkrete Bewegungsformen, die zu meinem Mars passen.

5. Mein Genuss. Lies meine Venus nach Zeichen und Haus: wie ich genieße, was Essen bei mir mit Liebe und Belohnung zu tun hat und woran ich im Moment selbst erkenne, ob ich gerade genieße oder betäube.

6. Meine Gewichts-Achse. Lies Jupiter und Saturn zusammen. Jupiter zeigt, wo mein Übermaß sitzt und was sich in mir ausdehnen will. Saturn zeigt, ob Struktur mich trägt oder ob ich mich mit Härte und Verzicht bestrafe. Sag mir, was diese Achse über mein Gewicht sagt: warum mein Körper hält, was er hält, und was sich verändern darf, wenn ich das Thema dahinter ernst nehme.

7. Meine wilde Kraft. Lies meine Lilith: welche Lust und welche Wildheit ich unterdrücke und wo mein Körper sich holt, was ich mir verbiete. Lies dann meine Ceres: mein Urthema von Nähren und Genährt-werden. Ob ich alle versorge und selbst leer ausgehe. Verbinde beide: Was darf ich mir erlauben, damit mein Körper das Thema nicht mehr für mich tragen muss?

8. Mein Weg. Der rote Faden: Welches eine Kernthema zieht sich durch alle Punkte? Dann drei konkrete Handlungen für meinen Alltag, die zu meiner Chart passen: eine für mein Essen, eine für meine Bewegung, eine für meine Routine. Klein genug, dass ich diese Woche anfangen kann. Zum Schluss eine einzige, ehrliche Frage an mich zu meinem Körper und dem, was er mir seit Jahren sagen will.

Schreib auf Deutsch, in der Du-Form, in Tiefe statt in Breite. Jeder Satz konkret. Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker. Kein Diätplan, keine Kalorien, keine medizinischen Aussagen.

Hier sind meine Daten:`;

  window.copyBodyReading = function(){
    const FULL = window.__fullChart || [];
    const ASP = window.__aspects || [];
    const B = window.__body || {};
    const m = window.__meta || {};
    const fmt = function(e){ return e ? (e.sign + (e.house ? (', ' + e.house + '. Haus') : '')) : ''; };
    const data = [];
    if(m.name) data.push('Name: ' + m.name);
    if(m.date){ const dp = m.date.split('-'); data.push('Geburtsdatum: ' + dp[2]+'.'+dp[1]+'.'+dp[0] + (m.time ? (' um ' + m.time + ' Uhr') : '')); }
    if(m.place) data.push('Geburtsort: ' + m.place);
    data.push('');
    data.push('MEIN BODY-CODE (die Schichten für dieses Reading):');
    if(B.moon) data.push('Mein Mond (Nahrungs-Kern): ' + fmt(B.moon));
    const mAsp = (B.moonAspects || []);
    if(mAsp.length){
      data.push('Meine Mond-Aspekte:');
      mAsp.forEach(function(a){
        const other = (a.p1 === 'Mond') ? (a.p2 + (a.s2 ? (' in ' + a.s2) : '')) : (a.p1 + (a.s1 ? (' in ' + a.s1) : ''));
        data.push('- Mond ' + a.type + ' ' + other);
      });
    } else {
      data.push('Mein Mond bildet keine engen Aspekte. Arbeite mit Zeichen und Haus.');
    }
    if(B.house6 && B.house6.sign){
      data.push('Mein 6. Haus (Routinen): Zeichen auf der Spitze: ' + B.house6.sign + '. Herrscher des Hauses: ' + B.house6.ruler + (B.house6.rulerEntry ? (' in ' + fmt(B.house6.rulerEntry)) : '') + '. Planeten im 6. Haus: ' + (B.house6.points.length ? B.house6.points.join(', ') : 'keine') + '.');
    }
    if(B.asc && B.asc.sign) data.push('Mein Aszendent (Körper): ' + B.asc.sign + '. Punkte in meinem 1. Haus: ' + ((B.house1Points || []).length ? B.house1Points.join(', ') : 'keine') + '.');
    if(B.mars) data.push('Mein Mars (Bewegung): ' + fmt(B.mars));
    if(B.venus) data.push('Meine Venus (Genuss): ' + fmt(B.venus));
    if(B.jupiter) data.push('Mein Jupiter (Übermaß): ' + fmt(B.jupiter));
    if(B.saturn) data.push('Mein Saturn (Struktur): ' + fmt(B.saturn));
    if(B.lilith) data.push('Meine Lilith (wilde Kraft): ' + fmt(B.lilith));
    if(B.ceres) data.push('Meine Ceres (Nähren): ' + fmt(B.ceres));
    data.push('');
    data.push('MEIN VOLLSTÄNDIGES CHART (Placidus-Häuser):');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });
    if(ASP.length){
      data.push('');
      data.push('MEINE WICHTIGSTEN NATALEN ASPEKTE:');
      ASP.forEach(function(a){ data.push(a.p1 + (a.s1 ? (' in ' + a.s1) : '') + ' ' + a.type + ' ' + a.p2 + (a.s2 ? (' in ' + a.s2) : '')); });
    }
    const full = BODY_PROMPT + '\n\n' + data.join('\n');
    const btn = document.getElementById('copyBodyBtn');
    const done = function(){ if(btn){ const o = btn.getAttribute('data-label') || btn.textContent; btn.setAttribute('data-label', o); btn.textContent = '✓ Kopiert! Jetzt in ChatGPT einfügen'; setTimeout(function(){ btn.textContent = o; }, 2800); } };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(full).then(done).catch(function(){ fallbackCopy(full, done); });
    } else { fallbackCopy(full, done); }
  };"""

pat = re.compile(r"  const BUSINESS_PROMPT = `.*?\n  window\.copyBusinessReading = function\(\)\{.*?\n  \};", re.DOTALL)
if not pat.search(s):
    sys.exit("FEHLT: BUSINESS_PROMPT / copyBusinessReading Region")
s = pat.sub(lambda _: new_region, s, count=1)

# --- 10. Kopf beruhigen (REGEL seit 14.07.): Display-Schrift nur fuer die H1,
# Eyebrow + Intro klein in Lesschrift. Basis-Design bleibt sonst unveraendert.
extra_css = '''<style>
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
  max-width:520px !important; margin:0 auto !important;
}
</style>
</head>'''
repl('</head>', extra_css, "kopf-beruhigen-css")

# Sicherheitscheck: keine Business-Reste mehr
for leftover in ["copyBusinessReading", "copyBizBtn", "BUSINESS_PROMPT", "subscribeLead", "userEmail", "Business-Code", "Business-Blueprint", '<p class="header-eyebrow">']:
    if leftover in s:
        sys.exit("REST gefunden: " + leftover)

with open(DST, "w", encoding="utf-8") as f:
    f.write(s)

os.makedirs(NETLIFY, exist_ok=True)
shutil.copyfile(DST, os.path.join(NETLIFY, "index.html"))

print("OK ->", DST)
print("OK ->", os.path.join(NETLIFY, "index.html"))
print("Groesse:", len(s), "Zeichen")
