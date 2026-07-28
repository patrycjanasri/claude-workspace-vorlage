#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bestaetigungsseite (Danke-Seite nach Kauf) "Der Eclipse Navigator"
fuer Bernadette Hirschfelder (lieblingsastrologin.de).

TEXT: von Patrycja diktiert (27.07.2026): Dank + Link zum Navigator +
      Passwort-Hinweis (Finsternis2026) + die 8 FAQ 1:1 von der Salespage.
Design: identisch zur Salespage (build_eclipse_salespage.py) —
      Blush Pink / Soft Apricot / Light Lavender, Anton + Great Vibes,
      ECLIPSE-SEASON-Tapes, schwarzer Pill-Button, Copyright-Fussleiste.

WICHTIG: Das Passwort hier muss zum Gate in build_eklipsen_reader.py passen
(dort PASSWORT = "Finsternis2026", Stand 27.07.). Aendert sich das Passwort,
BEIDE Generatoren anpassen und neu laufen lassen.

Seite ist auf noindex gestellt (steht das Passwort drauf, soll Google sie
nicht finden).
"""

import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- Konstanten
PASSWORT = "Finsternis2026"   # = PASSWORT in build_eklipsen_reader.py
NAVIGATOR_URL = "https://eclipsenavigator.netlify.app"  # finale URL (Patrycja 27.07.), Passwort-Gate schuetzt jetzt statt Zufallsname
IMPRESSUM_URL = "https://lieblingsastrologin.de/impressum/"
DATENSCHUTZ_URL = "https://lieblingsastrologin.de/datenschutzerklaerung/"

C_ROSA = "#FFD1DC"      # Blush Pink
C_PEACH = "#FEC89A"     # Soft Apricot
C_FLIEDER = "#E0B0FF"   # Light Lavender
C_INK = "#111111"
C_CREAM = "#FAF4EA"
C_GOLD = "#D9A94F"


def b64file(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


FONT_ANTON = b64file(os.path.join(HERE, "bernadette-anton.woff2"))
FONT_SCRIPT = b64file(os.path.join(HERE, "bernadette-greatvibes.woff2"))
FOTO = b64file(os.path.join(HERE, "bernadette-salespage-900.png"))

TAPE = ("ECLIPSE SEASON ✦  " * 14).strip()

HTML = r"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Danke | Der Eclipse Navigator</title>
<style>
@font-face{ font-family:'BAnton'; src:url(data:font/woff2;base64,__ANTON__) format('woff2'); font-weight:400; font-style:normal; font-display:swap; }
@font-face{ font-family:'BScript'; src:url(data:font/woff2;base64,__SCRIPT__) format('woff2'); font-weight:400; font-style:normal; font-display:swap; }

*{ margin:0; padding:0; box-sizing:border-box; }
body{ font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  color:__INK__; background:__ROSA__; font-size:17px; line-height:1.65; }

.anton{ font-family:'BAnton', Impact, sans-serif; text-transform:uppercase; line-height:1.02; letter-spacing:.5px; }
.script{ font-family:'BScript', cursive; font-weight:400; text-transform:none; }

.wrap{ max-width:860px; margin:0 auto; padding:0 22px; }
.narrow{ max-width:660px; margin:0 auto; }

section{ padding:64px 0; }

/* ------------------------------------------------ Hero (Danke) */
.hero{ background:__ROSA__; padding:60px 0 44px; text-align:center; }
.hero-eyebrow{ font-family:'BAnton',sans-serif; text-transform:uppercase; font-size:13px; letter-spacing:4px; margin-bottom:26px; }
.berna-photo{ width:170px; height:170px; border-radius:50%; overflow:hidden; margin:0 auto 22px;
  border:4px solid __INK__; background:__CREAM__; }
.berna-photo img{ width:150%; margin-left:-25%; margin-top:6%; display:block; }
.hero-script{ font-family:'BScript',cursive; font-size:clamp(38px, 7vw, 54px); line-height:1.1; display:block; }
.hero-h1{ font-size:clamp(56px, 11vw, 104px); margin-top:2px; }
.hero-sub{ max-width:560px; margin:22px auto 0; font-size:20px; }
.hero-sub strong{ font-weight:700; }

/* ------------------------------------------------ Buttons */
.btn{ display:inline-block; background:__INK__; color:#fff; text-decoration:none;
  font-family:'BAnton',sans-serif; text-transform:uppercase; letter-spacing:2px;
  font-size:18px; padding:20px 38px; margin-top:26px; border-radius:2px;
  box-shadow:6px 6px 0 rgba(17,17,17,.16); transition:transform .15s ease, box-shadow .15s ease; }
.btn:hover{ transform:translate(-2px,-2px); box-shadow:9px 9px 0 rgba(17,17,17,.2); }

/* ------------------------------------------------ Tape */
.tape-zone{ position:relative; height:130px; overflow:hidden; }
.tape{ position:absolute; left:-6%; right:-6%; padding:9px 0; white-space:nowrap; overflow:hidden;
  font-family:'BAnton',sans-serif; text-transform:uppercase; font-size:15px; letter-spacing:3px; text-align:center; }
.tape-ink{ background:__INK__; color:#fff; top:26px; transform:rotate(-2.4deg); }
.tape-peach{ background:__PEACH__; color:__INK__; top:74px; transform:rotate(1.6deg); }
.tape-flieder{ background:__FLIEDER__; color:__INK__; top:74px; transform:rotate(1.6deg); }

/* ------------------------------------------------ Abschnitts-Header */
.sec-script{ font-family:'BScript',cursive; font-size:42px; line-height:1; display:block; margin-bottom:2px; }
.sec-h2{ font-size:clamp(36px, 6.5vw, 58px); margin-bottom:26px; }
.sec-head{ text-align:center; margin-bottom:34px; }

/* ------------------------------------------------ Goldstrich */
.gold{ display:block; width:110px; height:3px; margin:26px auto; border-radius:3px;
  background:linear-gradient(90deg, rgba(217,169,79,0), __GOLD__ 18%, __GOLD__ 82%, rgba(217,169,79,0)); }

/* ------------------------------------------------ Zugang (flieder) */
.sec-zugang{ background:__FLIEDER__; text-align:center; }
.sec-zugang .zu-p{ font-size:19px; max-width:560px; margin:0 auto 18px; }
.pw-karte{ background:rgba(255,255,255,.6); border-radius:4px; max-width:480px; margin:26px auto 0; padding:30px 26px; }
.pw-karte .pw-label{ font-size:17px; margin-bottom:14px; }
.pw-wort{ font-family:'BAnton',sans-serif; font-size:clamp(30px, 6.5vw, 44px); letter-spacing:2px; line-height:1.1;
  display:block; user-select:all; -webkit-user-select:all; }
.pw-copy{ display:inline-block; margin-top:16px; background:transparent; border:2px solid __INK__; border-radius:999px;
  padding:8px 20px; font-family:'BAnton',sans-serif; text-transform:uppercase; letter-spacing:2px; font-size:13px;
  color:__INK__; cursor:pointer; }
.pw-copy:hover{ background:__INK__; color:#fff; }
.pw-hint{ font-size:14px; opacity:.75; margin-top:12px; }

/* ------------------------------------------------ FAQ (cream) */
.sec-faq{ background:__CREAM__; }
.faq{ max-width:680px; margin:0 auto; }
details{ background:#fff; border-radius:4px; margin-bottom:12px; box-shadow:4px 4px 0 rgba(17,17,17,.07); }
summary{ cursor:pointer; list-style:none; padding:18px 22px; font-family:'BAnton',sans-serif;
  text-transform:uppercase; font-size:17px; letter-spacing:2px; line-height:1.3;
  display:flex; justify-content:space-between; align-items:center; gap:14px; }
summary::-webkit-details-marker{ display:none; }
summary::after{ content:"+"; font-size:22px; flex:0 0 auto; }
details[open] summary::after{ content:"\2013"; }
details .a{ padding:0 22px 20px; font-size:16px; }
details .a p{ margin-bottom:10px; }

/* ------------------------------------------------ Footer */
.legal{ background:__INK__; color:#fff; text-align:center; padding:26px 18px; }
.legal p{ font-family:'BAnton',sans-serif; text-transform:uppercase; letter-spacing:2.5px; font-size:12px; }
.legal a{ color:__PEACH__; text-decoration:none; margin:0 8px; }
</style>
</head>
<body>

<!-- ================================================== HERO / DANKE -->
<header class="hero">
  <div class="wrap">
    <p class="hero-eyebrow">Bernadette Hirschfelder &middot; Lieblingsastrologin</p>
    <div class="berna-photo"><img src="data:image/png;base64,__FOTO__" alt="Bernadette Hirschfelder"></div>
    <h1><span class="hero-script">Vielen herzlichen</span><span class="anton hero-h1" style="display:block">Dank!</span></h1>
    <p class="hero-sub">f&uuml;r den Kauf des Eclipse Navigators.<br><strong>Ich freu mich riesig, dass Du mehr &uuml;ber die Eclipse Season erfahren m&ouml;chtest.</strong></p>
  </div>
</header>

<div class="tape-zone" style="background:__ROSA__"><div class="tape tape-ink">__TAPE__</div><div class="tape tape-peach">__TAPE__</div></div>

<!-- ================================================== ZUGANG -->
<section class="sec-zugang">
  <div class="wrap narrow">
    <div class="sec-head" style="margin-bottom:20px">
      <span class="sec-script">Dein</span>
      <h2 class="anton sec-h2" style="margin-bottom:0">Eclipse Navigator</h2>
    </div>
    <p class="zu-p">Unter diesem Link kommst Du direkt zu Deinem Eclipse Navigator.</p>
    <div class="pw-karte">
      <p class="pw-label">Bevor Du starten kannst, musst Du ein Passwort eingeben.<br>Dein Passwort lautet:</p>
      <span class="pw-wort" id="pw-wort">__PASSWORT__</span>
      <button class="pw-copy" id="pw-copy" type="button">Passwort kopieren</button>
      <p class="pw-hint">Gib es genau so ein, mit gro&szlig;em F und ohne Leerzeichen.</p>
    </div>
    <a class="btn" href="__NAVIGATOR__">Zu Deinem Eclipse Navigator</a>
  </div>
</section>

<div class="tape-zone" style="background:__FLIEDER__"><div class="tape tape-ink">__TAPE__</div><div class="tape tape-flieder" style="background:__PEACH__">__TAPE__</div></div>

<!-- ================================================== FAQ -->
<section class="sec-faq">
  <div class="wrap">
    <div class="sec-head">
      <span class="sec-script">Deine Fragen</span>
      <h2 class="anton sec-h2">Meine Antworten</h2>
    </div>
    <div class="faq">
      <details><summary>Brauche ich Astro-Vorkenntnisse?</summary><div class="a"><p>Nein. Du gibst nur Deine Geburtsdaten ein, alles andere macht der Eclipse Navigator. Dein Reading kommt in klarer Sprache, ohne Fachchinesisch.</p></div></details>
      <details><summary>Was brauche ich f&uuml;r mein Reading?</summary><div class="a"><p>Dein Geburtsdatum, Deine Geburtszeit und Deinen Geburtsort. Die Geburtszeit findest Du in Deiner Geburtsurkunde. Wenn Du sie nicht kennst, hilft ein Anruf beim Standesamt Deines Geburtsorts.</p></div></details>
      <details><summary>Wie bekomme ich Zugang?</summary><div class="a"><p>Direkt nach dem Kauf bekommst Du Deinen pers&ouml;nlichen Zugangslink per E-Mail. Funktioniert am Handy und am Computer.</p></div></details>
      <details><summary>Wie l&auml;uft es genau ab?</summary><div class="a"><p>Du gibst Deine Geburtsdaten ein und kopierst Deinen pers&ouml;nlichen Prompt mit einem Klick. Den f&uuml;gst Du komplett bei ChatGPT oder Claude ein.</p></div></details>
      <details><summary>Brauche ich einen bezahlten KI-Account?</summary><div class="a"><p>Die kostenlose Version funktioniert. Die Antworten k&ouml;nnen dort aber k&uuml;rzer ausfallen und das Tageslimit kann Dich mitten im Reading stoppen. Mit der Bezahlversion bekommst Du das beste Ergebnis.</p><p>Mein Tipp: Gib Deinem Reading das kl&uuml;gste KI-Modell, das Du hast. Bei ChatGPT und Claude w&auml;hlst Du das Modell oben im Men&uuml;. Nimm das st&auml;rkste, nicht das schnelle.</p></div></details>
      <details><summary>Kann die KI Fehler machen?</summary><div class="a"><p>Ja. Dein Reading wird von einer KI geschrieben, auf Basis Deiner echten Horoskop-Daten und meiner astrologischen Struktur dahinter. Eine KI kann Fehler machen. Nimm Dein Reading als Spiegel und Impuls f&uuml;r Deine Entscheidungen. Die letzte Instanz bist immer Du.</p><p>Dieses Reading ersetzt keinen medizinischen, psychotherapeutischen, rechtlichen oder finanziellen Rat.</p></div></details>
      <details><summary>Was passiert mit meinen Daten?</summary><div class="a"><p>Deine Geburtsdaten werden nur in Deinem Browser berechnet und nirgendwo gespeichert. Was Du bei ChatGPT oder Claude eingibst, liegt beim Datenschutz des jeweiligen Anbieters. Wenn Dir das wichtig ist, kannst Du dort die Nutzung Deiner Chats f&uuml;r Trainingszwecke ausschalten.</p></div></details>
      <details><summary>Was mache ich, wenn etwas hakt?</summary><div class="a"><p>Die Seite l&auml;dt oder rechnet nicht? Leere den Browser-Cache oder nutze einen anderen Browser, am besten ein aktuelles Chrome oder Safari. Dein Geburtsort wird nicht gefunden? Gib die n&auml;chstgr&ouml;&szlig;ere Stadt ein. Du kommst nicht weiter? Schreib mir, ich helfe Dir.</p></div></details>
    </div>
  </div>
</section>

<footer class="legal">
  <p>Copyright Bernadette Hirschfelder - 2026 - lieblingsastrologin.de</p>
  <p style="margin-top:8px"><a href="__IMPRESSUM__" target="_blank" rel="noopener">Impressum</a> &middot; <a href="__DATENSCHUTZ__" target="_blank" rel="noopener">Datenschutz</a></p>
</footer>

<script>
(function(){
  var knopf = document.getElementById("pw-copy");
  var wort = document.getElementById("pw-wort");
  function zeigeKopiert(){
    knopf.textContent = "Kopiert!";
    setTimeout(function(){ knopf.textContent = "Passwort kopieren"; }, 2000);
  }
  knopf.addEventListener("click", function(){
    var pw = wort.textContent;
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(pw).then(zeigeKopiert, function(){ fallback(pw); });
    } else {
      fallback(pw);
    }
  });
  function fallback(pw){
    var feld = document.createElement("textarea");
    feld.value = pw;
    feld.setAttribute("readonly", "");
    feld.style.position = "fixed";
    feld.style.left = "-9999px";
    document.body.appendChild(feld);
    feld.select();
    try{ document.execCommand("copy"); zeigeKopiert(); }catch(e){}
    document.body.removeChild(feld);
  }
})();
</script>

</body>
</html>
"""

html = (HTML
        .replace("__ANTON__", FONT_ANTON)
        .replace("__SCRIPT__", FONT_SCRIPT)
        .replace("__FOTO__", FOTO)
        .replace("__TAPE__", TAPE)
        .replace("__PASSWORT__", PASSWORT)
        .replace("__NAVIGATOR__", NAVIGATOR_URL)
        .replace("__IMPRESSUM__", IMPRESSUM_URL)
        .replace("__DATENSCHUTZ__", DATENSCHUTZ_URL)
        .replace("__ROSA__", C_ROSA)
        .replace("__PEACH__", C_PEACH)
        .replace("__FLIEDER__", C_FLIEDER)
        .replace("__INK__", C_INK)
        .replace("__CREAM__", C_CREAM)
        .replace("__GOLD__", C_GOLD))

out1 = os.path.join(HERE, "eclipse-navigator-danke.html")
netlify_dir = os.path.join(HERE, "eclipse-navigator-danke-netlify")
os.makedirs(netlify_dir, exist_ok=True)
out2 = os.path.join(netlify_dir, "index.html")

for path in (out1, out2):
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("geschrieben:", path, f"({os.path.getsize(path)/1024:.0f} KB)")
print("PASSWORT auf der Seite:", PASSWORT)
print("NAVIGATOR-LINK:", NAVIGATOR_URL)
