#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut den Chiron-in-Stier-Reader aus dem Business-Reader.
Gleiches Design + gleiche Astro-Engine, nur das Reading-Gehirn wird getauscht:
Der Reader rechnet automatisch aus, in welchem Haus bei dir Stier liegt
(dort wirkt der Chiron-Transit die naechsten Jahre), wo dein natales Chiron
steht und welche Planeten du im Stier hast. Daraus + dem vollen Chart baut er
einen fertigen KI-Prompt zum Kopieren.

Quelle:  astro-business-reader.html
Ziel:    astro-chiron-reader.html
Bei Design-Updates am Business-Reader dieses Skript erneut laufen lassen.
"""
import re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "astro-business-reader.html")
DST = os.path.join(HERE, "astro-chiron-reader.html")

with open(SRC, "r", encoding="utf-8") as f:
    s = f.read()

def repl(old, new, label):
    global s
    if old not in s:
        sys.exit("FEHLT (" + label + "): " + old[:80])
    s = s.replace(old, new, 1)

# --- 1. Branding / sichtbare Texte ---------------------------------------
repl("<title>Dein Business-Code</title>",
     "<title>Dein Chiron-Code</title>", "title")

repl('<p class="header-eyebrow">Dein kosmischer Business-Blueprint</p>',
     '<p class="header-eyebrow">Chiron in Stier · dein Thema der naechsten Jahre</p>'.replace("naechsten", "nächsten"),
     "eyebrow")

repl("<h1>Dein Business-Code</h1>", "<h1>Dein Chiron-Code</h1>", "h1")

repl('<p class="subtitle">Gib deine Geburtsdaten ein. Auf der nächsten Seite bekommst du dein Geburtshoroskop angezeigt und einen fertigen KI-Prompt, der dir sagt, wie du dein Business führst, dich positionierst, skalierst und Geld verdienst.</p>',
     '<p class="subtitle">Chiron wandert die nächsten Jahre durch das Tierkreiszeichen Stier und berührt das Thema Selbstwert, Körper und Geld. Gib deine Geburtsdaten ein. Auf der nächsten Seite siehst du, in welchem Lebensbereich Chiron bei dir wirkt, und bekommst einen fertigen KI-Prompt für dein persönliches Chiron-Reading.</p>',
     "subtitle")

repl('onclick="runCheck()">Meinen Business-Code aufdecken</button>',
     'onclick="runCheck()">Mein Chiron-Thema aufdecken</button>', "submit-btn")

# --- E-Mail komplett entfernen (kein Opt-in) ------------------------------
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

repl("<h2>Dein Business-Code${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Dein Chart als Business-Blueprint'}</p>",
     "<h2>Dein Chiron-Code${(name && name !== 'Du') ? ', ' + name : ''}</h2><p>${metaLine || 'Dein Chart als Chiron-Landkarte'}</p>",
     "results-header")

repl("&#8592; Neuen Business-Code erstellen", "&#8592; Neuen Chiron-Code erstellen", "back-btn")

# --- 2. Chiron-Berechnung in runCheck einhaengen -------------------------
meta_anchor = "      window.__meta = { name: name, email: email, date: date, time: time, place: place.label };"
chiron_calc = meta_anchor + """

      // Chiron in Stier: in welchem Haus liegt Stier (dort wirkt der Transit),
      // wo steht das natale Chiron, welche Planeten habe ich im Stier
      (function(){
        const houses = horo.Houses || [];
        function houseOfLong(L){
          for(let i=0;i<houses.length;i++){
            const h = houses[i];
            let st, en;
            try { st = h.ChartPosition.StartPosition.Ecliptic.DecimalDegrees; en = h.ChartPosition.EndPosition.Ecliptic.DecimalDegrees; }
            catch(err){ continue; }
            const id = h.id || (i+1);
            if(st <= en){ if(L >= st && L < en) return id; }
            else { if(L >= st || L < en) return id; }
          }
          return null;
        }
        const hs = [];
        [30.01, 45, 59.99].forEach(function(L){ const id = houseOfLong(L); if(id && hs.indexOf(id) === -1) hs.push(id); });
        const chironEntry = (window.__fullChart || []).find(function(e){ return e.label === 'Chiron'; }) || {};
        const ANGLE = { 'Aszendent':1, 'Deszendent':1, 'MC':1, 'IC':1 };
        const taurusPlanets = (window.__fullChart || []).filter(function(e){ return e.sign === 'Stier' && e.label !== 'Chiron' && !ANGLE[e.label]; });
        window.__chiron = { houses: hs, natalSign: chironEntry.sign || '', natalHouse: chironEntry.house || '', taurusPlanets: taurusPlanets };
      })();"""
repl(meta_anchor, chiron_calc, "chiron-calc-injection")

# --- 3. Reading-Block: sichtbares Chiron-Thema + Prompt-CTA --------------
old_cta = """  html += `
  <div class="cta-block">
    <h3>Dein Business-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir, wie du dein Business führst, wie du dich positionierst, wo deine Zone of Genius liegt und wie du am natürlichsten Geld verdienst.</p>
    <button class="copy-btn" id="copyBizBtn" onclick="copyBusinessReading()">Business-Prompt + Daten kopieren</button>
  </div>`;"""

new_cta = """  // Sichtbares Chiron-in-Stier-Thema
  const C = window.__chiron || {};
  const chs = C.houses || [];
  const houseStr = chs.length ? (chs.length === 1 ? (chs[0] + '. Haus') : (chs.slice(0,-1).join('., ') + '. und ' + chs[chs.length-1] + '. Haus')) : '';
  const tps = (C.taurusPlanets || []).map(function(e){ return e.label; });
  let chiHtml = `
  <div class="data-block">
    <h3>Dein Chiron-in-Stier-Thema</h3>
    <div class="data-grid">`;
  if(houseStr) chiHtml += `<div class="data-row"><span class="data-planet">Stier liegt bei dir im</span><span class="data-values"><span class="badge house-badge">${houseStr}</span></span></div>`;
  if(C.natalSign) chiHtml += `<div class="data-row"><span class="data-planet">Dein natales Chiron</span><span class="data-values"><span class="badge sign-badge">${C.natalSign}</span>${C.natalHouse ? `<span class="badge house-badge">${C.natalHouse}. Haus</span>` : ''}</span></div>`;
  chiHtml += `<div class="data-row"><span class="data-planet">Planeten im Stier</span><span class="data-values"><span class="badge sign-badge">${tps.length ? tps.join(', ') : 'keine'}</span></span></div>`;
  chiHtml += `</div>`;
  if(C.natalSign === 'Stier') chiHtml += `<p style="margin-top:14px;opacity:.92">Dein Chiron steht selbst im Stier. Du erlebst gerade deinen Chiron-Return, einen großen Zyklus rund um deinen Selbstwert.</p>`;
  chiHtml += `</div>`;
  html += chiHtml;

  html += `
  <div class="cta-block">
    <h3>Dein Chiron-in-Stier-Reading mit KI</h3>
    <p>Kopiere den Prompt und füg ihn in ChatGPT oder Claude ein. Dein Reading zeigt dir dein persönliches Chiron-Thema für die nächsten Jahre: in welchem Lebensbereich dein Selbstwert berührt wird, was dein Schatten ist und welches Geschenk darin liegt.</p>
    <button class="copy-btn" id="copyChironBtn" onclick="copyChironReading()">Chiron-Prompt + Daten kopieren</button>
  </div>`;"""
repl(old_cta, new_cta, "cta-block")

# --- 4. Prompt-Gehirn + Copy-Funktion austauschen ------------------------
new_region = r"""  const CHIRON_PROMPT = `Du bist eine erfahrene Bewusstseinsastrologin mit dem Blick für die Urwunde Chiron. Du schreibst klar, tief und direkt, so dass mich jeder Satz trifft. Keine Floskeln, keine allgemeinen Astro-Sätze, kein Lehrbuchton.

Mein Thema: Chiron läuft die nächsten Jahre durch das Tierkreiszeichen Stier. Ich will wissen, was das ganz persönlich für mich bedeutet. Stier steht für Selbstwert, Körper, Sinnlichkeit, Genuss, Geld, Sicherheit, Besitz und die Frage "Was bin ich wert?". Chiron ist die Urwunde, die nicht heilt, die berührt und integriert werden will und die mein größtes Geschenk an die Welt in sich trägt.

Unten findest du die entscheidenden Punkte aus meinem Geburtshoroskop: in welchem Haus bei mir das Tierkreiszeichen Stier liegt (dort wirkt der Chiron-Transit die nächsten Jahre), wo mein natales Chiron steht und welche Planeten ich im Stier habe. Dazu mein vollständiges Chart als Kontext.

Schreibe mir auf dieser Basis:

1. Mein Kernthema. In einem kraftvollen Absatz: worum es in den nächsten Jahren für mich geht. Sprich mich direkt mit "du" an.

2. Wo es sich in meinem Leben zeigt. Nimm das Haus, in dem Stier bei mir liegt, und mach konkret, in welchem Lebensbereich diese Selbstwert-Wunde berührt wird, zum Beispiel Geld, Arbeit, Beziehungen, Körper, Zuhause oder Sichtbarkeit.

3. Der Schatten. Wo ich mich klein mache, festhalte, mir meinen Wert abspreche, mir Genuss verbiete oder Sicherheit im Außen suche, die es so nicht gibt.

4. Das Geschenk. Was sich öffnet, wenn ich die Wunde berühre statt sie zu meiden. Welcher neue Selbstwert in den nächsten Jahren in mir wachsen darf.

5. Der Weg durch den Körper. Eine konkrete, sinnliche Einladung, wie ich zurück in meinen Körper und in den Genuss komme.

6. Meine Schattenfrage. Eine einzige, konfrontierende Frage, die mich nicht mehr loslässt.

Wenn mein natales Chiron selbst im Stier steht, erlebe ich gerade meinen Chiron-Return. Geh in dem Fall besonders darauf ein, dass sich hier ein großer Lebenszyklus rund um meinen Selbstwert schließt.

Schreib auf Deutsch, in der Du-Form, in Tiefe statt in Breite. Jeder Satz konkret. Keine Gedankenstriche. Keine "nicht... sondern"-Konstruktionen. Keine leeren Verstärker.

Hier sind meine Daten:`;

  window.copyChironReading = function(){
    const FULL = window.__fullChart || [];
    const C = window.__chiron || {};
    const m = window.__meta || {};
    const data = [];
    if(m.name) data.push('Name: ' + m.name);
    if(m.date){ const dp = m.date.split('-'); data.push('Geburtsdatum: ' + dp[2]+'.'+dp[1]+'.'+dp[0] + (m.time ? (' um ' + m.time + ' Uhr') : '')); }
    if(m.place) data.push('Geburtsort: ' + m.place);
    data.push('');
    data.push('MEIN CHIRON-IN-STIER-THEMA:');
    const hs = C.houses || [];
    const houseStr = hs.length ? (hs.length === 1 ? (hs[0] + '. Haus') : (hs.slice(0,-1).join('., ') + '. und ' + hs[hs.length-1] + '. Haus')) : '';
    if(houseStr) data.push('Das Tierkreiszeichen Stier liegt in meinem ' + houseStr + '. Dort wirkt der Chiron-Transit die nächsten Jahre.');
    if(C.natalSign) data.push('Mein natales Chiron steht in ' + C.natalSign + (C.natalHouse ? (', ' + C.natalHouse + '. Haus') : '') + '.');
    const tp = (C.taurusPlanets || []).map(function(e){ return e.label; });
    data.push('Planeten, die ich im Stier habe: ' + (tp.length ? tp.join(', ') : 'keine') + '.');
    if(C.natalSign === 'Stier') data.push('Mein Chiron steht selbst im Stier: ich erlebe gerade meinen Chiron-Return.');
    data.push('');
    data.push('MEIN VOLLSTÄNDIGES CHART:');
    FULL.forEach(function(e){ data.push(e.label + ': ' + e.sign + (e.house ? (', ' + e.house + '. Haus') : '')); });
    const full = CHIRON_PROMPT + '\n\n' + data.join('\n');
    const btn = document.getElementById('copyChironBtn');
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
for leftover in ["copyBusinessReading", "copyBizBtn", "BUSINESS_PROMPT"]:
    if leftover in s:
        sys.exit("REST gefunden: " + leftover)

with open(DST, "w", encoding="utf-8") as f:
    f.write(s)

print("OK ->", DST)
print("Groesse:", len(s), "Zeichen")
