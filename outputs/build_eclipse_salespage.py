#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Salespage "Der Eclipse Navigator" fuer Bernadette Hirschfelder
(lieblingsastrologin.de).

TEXT: 1:1 von Patrycja geliefert (26.07.2026), Wort fuer Wort uebernommen,
      nichts hinzugedichtet. Einzige Interpretation: das kaputte Zeichen
      "Ø<ß" in den beiden Finsternis-Zeilen wurde als ✦ gesetzt und der
      Abschluss-Button "[Jetzt fuer 27€ sichern !']" als sauberer Button.
Design-Referenz: Bernadettes Eclipse Guide PDF (astrologin-eclipse-guide.pdf)
  -> Blush Pink / Soft Apricot / Light Lavender, Anton-Blockschrift,
     Great-Vibes-Script, ECLIPSE-SEASON-Tapes, Starburst-Badge,
     nummerierte Schritte, Copyright-Fussleiste.

Preis + Checkout: unten bei PRICE / PRICE2 / CTA_URL tauschen, neu laufen lassen.
"""

import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- Konstanten
PRICE = "27€"
PRICE2 = "47€"
CTA_URL = "#kaufen"        # <- Platzhalter: hier Bernadettes Checkout-Link rein
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
<title>Der Eclipse Navigator | Bernadette Hirschfelder</title>
<meta name="description" content="Du weisst, dass die Eclipse Season kommt. Aber weisst du, was sie in deinem Leben ausloest? Deine persoenliche Eklipsen-Deutung fuer beide Finsternisse.">
<style>
@font-face{ font-family:'BAnton'; src:url(data:font/woff2;base64,__ANTON__) format('woff2'); font-weight:400; font-style:normal; font-display:swap; }
@font-face{ font-family:'BScript'; src:url(data:font/woff2;base64,__SCRIPT__) format('woff2'); font-weight:400; font-style:normal; font-display:swap; }

*{ margin:0; padding:0; box-sizing:border-box; }
html{ scroll-behavior:smooth; }
body{ font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  color:__INK__; background:__ROSA__; font-size:17px; line-height:1.65; }

.anton{ font-family:'BAnton', Impact, sans-serif; text-transform:uppercase; line-height:1.02; letter-spacing:.5px; }
.script{ font-family:'BScript', cursive; font-weight:400; text-transform:none; }

.wrap{ max-width:860px; margin:0 auto; padding:0 22px; }
.narrow{ max-width:660px; margin:0 auto; }

section{ padding:64px 0; }

/* ------------------------------------------------ Hero */
.hero{ background:__ROSA__; padding:56px 0 40px; text-align:center; overflow:hidden; }
.hero-eyebrow{ font-family:'BAnton',sans-serif; text-transform:uppercase; font-size:13px; letter-spacing:4px; margin-bottom:18px; }
.hero-photo-zone{ position:relative; max-width:430px; margin:0 auto; }
.hero-photo-zone img{ width:100%; display:block; position:relative; z-index:1; }
.hero-h1{ font-size:clamp(52px, 10.5vw, 100px); position:relative; z-index:2; margin-top:-84px; text-shadow:3px 3px 0 __ROSA__; }
.hero-h1 .der{ display:block; font-size:.38em; letter-spacing:6px; margin-bottom:2px; }
.starburst{ position:absolute; top:6%; right:-30px; z-index:3; width:118px; height:118px; }
@media (max-width:560px){ .starburst{ width:92px; height:92px; right:-8px; } .hero-h1{ margin-top:-58px; } }
.hero-sub{ max-width:560px; margin:26px auto 0; font-size:20px; }
.hero-sub strong{ font-weight:700; }

/* ------------------------------------------------ Buttons */
.btn{ display:inline-block; background:__INK__; color:#fff; text-decoration:none;
  font-family:'BAnton',sans-serif; text-transform:uppercase; letter-spacing:2px;
  font-size:18px; padding:20px 38px; margin-top:26px; border-radius:2px;
  box-shadow:6px 6px 0 rgba(17,17,17,.16); transition:transform .15s ease, box-shadow .15s ease; }
.btn:hover{ transform:translate(-2px,-2px); box-shadow:9px 9px 0 rgba(17,17,17,.2); }
.btn .p{ color:__PEACH__; }

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

/* ------------------------------------------------ Intro (flieder) */
.sec-intro{ background:__FLIEDER__; text-align:center; }
.intro-anton{ font-size:clamp(24px, 4.5vw, 34px); margin-bottom:20px; }
.sec-intro .intro-p{ font-size:19px; margin-bottom:20px; max-width:560px; margin-left:auto; margin-right:auto; }
.intro-list{ margin:6px auto 20px; }
.intro-list p{ font-family:'BAnton',sans-serif; text-transform:uppercase; letter-spacing:1.5px;
  font-size:19px; margin-bottom:10px; }
.intro-list .st{ color:__GOLD__; margin-right:8px; }
.intro-frage{ font-weight:700; font-size:21px; margin-top:6px; }
.frage-script{ display:block; font-size:clamp(38px, 7vw, 52px); font-weight:400; line-height:1.15; margin-top:6px; }

/* ------------------------------------------------ Was ist das (peach) */
.sec-was{ background:__PEACH__; }
.sec-was p{ margin-bottom:18px; }
.berna-photo{ width:170px; height:170px; border-radius:50%; overflow:hidden; margin:0 auto 24px;
  border:4px solid __INK__; background:__CREAM__; }
.berna-photo img{ width:150%; margin-left:-25%; margin-top:6%; display:block; }
.standout{ background:rgba(255,255,255,.55); border-radius:4px; padding:24px 26px; margin-top:28px; text-align:center; }
.standout p{ margin-bottom:10px; }
.standout .big{ font-family:'BAnton',sans-serif; text-transform:uppercase; font-size:21px; letter-spacing:1px; margin-bottom:0; }

/* ------------------------------------------------ Was bekommst du (cream) */
.sec-bekommst{ background:__CREAM__; text-align:center; }
.bek-lead{ font-size:19px; margin-bottom:6px; }
.bek-zahl{ font-size:clamp(30px, 6vw, 46px); margin-bottom:6px; }
.bek-script{ font-size:34px; margin-bottom:26px; }
.bek-p{ font-size:18px; margin:0 auto 14px; max-width:560px; }
.pill-row{ display:flex; flex-wrap:wrap; justify-content:center; gap:10px; margin:4px 0 14px; }
.pill{ background:__FLIEDER__; border-radius:999px; padding:9px 22px;
  font-family:'BAnton',sans-serif; text-transform:uppercase; letter-spacing:2.5px; font-size:17px; }
.bek-ganze{ font-size:19px; font-weight:700; margin-top:24px; }
.event-grid{ display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-top:26px; }
@media (max-width:640px){ .event-grid{ grid-template-columns:1fr; } }
.event-card{ background:#fff; border-radius:4px; padding:22px; box-shadow:4px 4px 0 rgba(17,17,17,.07); text-align:center; }
.event-card .star{ font-size:22px; color:__GOLD__; display:block; margin-bottom:8px; }
.event-card h4{ font-family:'BAnton',sans-serif; text-transform:uppercase; font-size:clamp(24px, 3.4vw, 30px);
  letter-spacing:2.5px; line-height:1.15; margin-bottom:6px; }
.event-card .datum{ font-size:17px; }

/* ------------------------------------------------ Schritte (rosa) */
.sec-steps{ background:__ROSA__; }
.step{ display:flex; gap:22px; align-items:flex-start; margin-bottom:26px; }
.step-num{ flex:0 0 54px; width:54px; height:54px; border-radius:50%; background:__CREAM__; border:2px solid __INK__;
  display:flex; align-items:center; justify-content:center; font-family:'BAnton',sans-serif; font-size:20px; }
.step p{ font-size:18px; padding-top:12px; }
.steps-closing{ font-size:18px; margin-top:6px; text-align:center; }

/* ------------------------------------------------ Fuer wen (flieder) */
.sec-wen{ background:__FLIEDER__; }
.sec-wen p{ margin-bottom:18px; font-size:18px; }
.wen-honest{ font-style:italic; opacity:.85; }

/* ------------------------------------------------ Goldstrich */
.gold{ display:block; width:110px; height:3px; margin:26px auto; border-radius:3px;
  background:linear-gradient(90deg, rgba(217,169,79,0), __GOLD__ 18%, __GOLD__ 82%, rgba(217,169,79,0)); }

/* ------------------------------------------------ Angebot (peach) */
.sec-angebot{ background:__PEACH__; text-align:center; }
.sec-angebot p{ max-width:560px; margin:0 auto 18px; font-size:18px; }
.preis-karte{ background:rgba(255,255,255,.6); border-radius:4px; max-width:480px; margin:26px auto; padding:30px 26px; }
.preis-karte .zahl{ font-family:'BAnton',sans-serif; font-size:72px; line-height:1; display:block; margin-bottom:8px; }
.preis-karte p{ margin-bottom:10px; font-size:17px; }
.preis-karte p:last-child{ margin-bottom:0; }
.sec-angebot p.verfuegbar{ font-size:15px; opacity:.8; margin-top:20px; }

/* ------------------------------------------------ Footer */
.legal{ background:__INK__; color:#fff; text-align:center; padding:26px 18px; }
.legal p{ font-family:'BAnton',sans-serif; text-transform:uppercase; letter-spacing:2.5px; font-size:12px; }
.legal a{ color:__PEACH__; text-decoration:none; margin:0 8px; }
</style>
</head>
<body>

<!-- ================================================== HERO -->
<header class="hero">
  <div class="wrap">
    <p class="hero-eyebrow">Bernadette Hirschfelder &middot; Lieblingsastrologin</p>
    <div class="hero-photo-zone">
      <img src="data:image/png;base64,__FOTO__" alt="Bernadette Hirschfelder">
      <svg class="starburst" viewBox="0 0 120 120" aria-hidden="true">
        <polygon points="60,0 68,18 84,6 85,26 105,20 98,38 120,40 106,54 120,68 100,72 108,90 88,86 88,108 72,96 60,120 48,96 32,108 32,86 12,90 20,72 0,68 14,54 0,40 22,38 15,20 35,26 36,6 52,18" fill="__CREAM__" stroke="__INK__" stroke-width="1.5"/>
        <text x="60" y="53" text-anchor="middle" font-family="BAnton, sans-serif" font-size="13" fill="__INK__">ECLIPSE</text>
        <text x="60" y="68" text-anchor="middle" font-family="BAnton, sans-serif" font-size="13" fill="__INK__">SEASON</text>
        <text x="60" y="83" text-anchor="middle" font-family="BAnton, sans-serif" font-size="12" fill="__INK__">INCOMING</text>
      </svg>
      <h1 class="anton hero-h1"><span class="der">Der</span>Eclipse<br>Navigator</h1>
    </div>
    <p class="hero-sub">Du weißt, dass die Eclipse Season kommt,<br><strong>aber weißt Du, was sie in Deinem Leben aus astrologischer Sicht auslösen wird?</strong></p>
  </div>
</header>

<div class="tape-zone" style="background:__ROSA__"><div class="tape tape-ink">__TAPE__</div><div class="tape tape-peach">__TAPE__</div></div>

<!-- ================================================== INTRO -->
<section class="sec-intro">
  <div class="wrap narrow">
    <p class="anton intro-anton">Die Sonnenfinsternis in Löwe.<br>Die Mondfinsternis in Fische.</p>
    <p class="intro-p">Zwei der kraftvollsten astrologischen Ereignisse des Jahres und beide landen direkt in Deinem persönlichen Horoskop.</p>
    <span class="gold"></span>
    <p class="intro-p">Eklipsen sind keine gewöhnlichen Himmelsereignisse.</p>
    <div class="intro-list">
      <p><span class="st">&#10022;</span>Sie sind Wendepunkte.</p>
      <p><span class="st">&#10022;</span>Sie schlie&szlig;en Kapitel.</p>
      <p><span class="st">&#10022;</span>Sie &ouml;ffnen T&uuml;ren.</p>
    </div>
    <p class="intro-p">Ihre Wirkung zieht sich &uuml;ber ein ganzes Jahr.</p>
    <span class="gold"></span>
    <p class="intro-frage">Die Frage ist nicht, OB sie etwas in Deinem Leben bewegen wird.<span class="script frage-script">Die Frage ist, WAS genau.</span></p>
  </div>
</section>

<!-- ================================================== WAS IST DAS -->
<section class="sec-was">
  <div class="wrap narrow">
    <div class="sec-head">
      <span class="sec-script">Was ist der</span>
      <h2 class="anton sec-h2">Eclipse Navigator?</h2>
    </div>
    <div class="berna-photo"><img src="data:image/png;base64,__FOTO__" alt="Bernadette Hirschfelder"></div>
    <p>Täglich erreichen mich Anfragen für persönliche Horoskopdeutungen. Ja, ich würde so gerne jedes einzelne Horoskop anschauen, aber es ist schlicht unmöglich. Deswegen habe ich den Eclipse Navigator mitentworfen. Ein KI-Tool, das auf meiner Expertise basiert, damit Du eine Deutung bekommst, die wirklich zu Deinem Horoskop passt. Personalisiert. Sofort verfügbar für DICH.</p>
    <p>Der Eclipse Navigator ist Deine persönliche Eklipsen-Deutung, erstellt auf Basis Deiner Geburtsdaten, zugeschnitten auf Dein Horoskop. Yes, für beide Finsternisse!</p>
    <div class="standout">
      <p>Kein allgemeines &bdquo;L&ouml;we wird transformiert.&ldquo; Kein Copy-Paste f&uuml;r alle.</p>
      <p class="big">Deine Planeten. Deine Aspekte. Dein Leben.</p>
    </div>
  </div>
</section>

<!-- ================================================== WAS BEKOMMST DU -->
<section class="sec-bekommst">
  <div class="wrap narrow">
    <div class="sec-head">
      <span class="sec-script">Was</span>
      <h2 class="anton sec-h2">bekommst du?</h2>
    </div>
    <p class="bek-lead">Eine vollst&auml;ndige astrologische Deutung in drei Teilen,</p>
    <p class="anton bek-zahl">12.000 bis 18.000 W&ouml;rter</p>
    <p class="bek-lead">(rund 40 A4-Seiten)</p>
    <p class="script bek-script">nur f&uuml;r Dich.</p>
    <p class="bek-p">F&uuml;r jede Finsternis gehst Du Schicht f&uuml;r Schicht tiefer:</p>
    <div class="pill-row">
      <span class="pill">die Planeten</span>
      <span class="pill">die Aspekte</span>
      <span class="pill">der Hauptaspekt</span>
    </div>
    <p class="bek-p">und was es konkret f&uuml;r Dein Leben in den kommenden Monaten bedeutet.</p>
    <p class="bek-ganze">Das Ganze f&uuml;r beide Ereignisse:</p>
    <div class="event-grid">
      <div class="event-card"><span class="star">&#10022;</span><h4>Sonnenfinsternis in L&ouml;we</h4><p class="datum">12. August</p></div>
      <div class="event-card"><span class="star">&#10022;</span><h4>Mondfinsternis in Fische</h4><p class="datum">28. August</p></div>
    </div>
  </div>
</section>

<!-- ================================================== WIE FUNKTIONIERT ES -->
<section class="sec-steps">
  <div class="wrap narrow">
    <div class="sec-head">
      <span class="sec-script">Wie</span>
      <h2 class="anton sec-h2">funktioniert es?</h2>
    </div>
    <div class="step"><div class="step-num">01</div><p>Gib Deine Geburtsdaten ein, damit der Eclipse Navigator Deinen pers&ouml;nlichen Prompt erstellt.</p></div>
    <div class="step"><div class="step-num">02</div><p>Diesen Prompt gibst Du bei ChatGPT oder Claude ein.</p></div>
    <div class="step"><div class="step-num">03</div><p>Danach bekommst Du eine vollst&auml;ndige Deutung in drei Teilen, rund 40 A4-Seiten, nur f&uuml;r Dich.</p></div>
    <span class="gold"></span>
    <p class="steps-closing">Mit jedem Schritt gehst Du tiefer: Planeten, Aspekte, Hauptaspekt und was es konkret f&uuml;r Dein Leben in den n&auml;chsten Monaten bedeutet.</p>
  </div>
</section>

<!-- ================================================== FUER WEN -->
<section class="sec-wen">
  <div class="wrap narrow">
    <div class="sec-head">
      <span class="sec-script">F&uuml;r wen ist der</span>
      <h2 class="anton sec-h2">Eclipse Navigator?</h2>
    </div>
    <p>Du triffst jeden Tag Entscheidungen, ob zu Hause, in der Familie oder im Job. Du bist eine Macherin. Und gleichzeitig sp&uuml;rst Du: da ist noch mehr. Eine Frage, die immer &ouml;fter in Deinen Gedanken auftaucht. Was kommt noch f&uuml;r mich?</p>
    <p>Du wei&szlig;t, dass Finsternisse keine gew&ouml;hnlichen Ereignisse sind. Sie wirken rund ein Jahr und l&ouml;sen etwas aus. T&auml;glich verfolgst Du meine Storys, nickst oft und denkst, &bdquo;Ja, das trifft zu.&ldquo; Doch wenn die Sonnenfinsternis in L&ouml;we und die Mondfinsternis in Fische kommen, willst Du nicht raten. Du willst wissen, was sie in DEINEM Horoskop bedeuten.</p>
    <p class="wen-honest">Wenn Du noch nie von Astrologie geh&ouml;rt hast und Finsternisse f&uuml;r Dich nur Himmelsph&auml;nomene sind, dann ist das vielleicht nicht Dein n&auml;chster Schritt.</p>
  </div>
</section>

<div class="tape-zone" style="background:__PEACH__"><div class="tape tape-ink">__TAPE__</div><div class="tape tape-flieder">__TAPE__</div></div>

<!-- ================================================== ANGEBOT -->
<section class="sec-angebot" style="padding-top:30px">
  <div class="wrap">
    <div class="sec-head" style="margin-bottom:20px">
      <span class="sec-script">Dein</span>
      <h2 class="anton sec-h2" style="margin-bottom:0">Angebot</h2>
    </div>
    <p>Der Eclipse Navigator ist ab Mittwoch, 29. Juli verf&uuml;gbar.</p>
    <div class="preis-karte">
      <span class="anton zahl">__PRICE__</span>
      <p>F&uuml;r __PRICE__, allerdings nur am Mittwoch und Donnerstag.</p>
      <p>Ab Freitag, 31. Juli kostet er __PRICE2__.</p>
    </div>
    <p>Die Sonnenfinsternis in L&ouml;we ist am 12. August. Die Mondfinsternis in Fische am 28. August. Du willst vorbereitet sein, nicht erst danach verstehen, was hier gerade passiert ist.</p>
    <a class="btn" href="__CTA__">Jetzt f&uuml;r <span class="p">__PRICE__</span> sichern!</a>
    <p class="verfuegbar">Verf&uuml;gbar bis 28. September.</p>
  </div>
</section>

<footer class="legal">
  <p>Copyright Bernadette Hirschfelder - 2026 - lieblingsastrologin.de</p>
  <p style="margin-top:8px"><a href="__IMPRESSUM__" target="_blank" rel="noopener">Impressum</a> &middot; <a href="__DATENSCHUTZ__" target="_blank" rel="noopener">Datenschutz</a></p>
</footer>

</body>
</html>
"""

html = (HTML
        .replace("__ANTON__", FONT_ANTON)
        .replace("__SCRIPT__", FONT_SCRIPT)
        .replace("__FOTO__", FOTO)
        .replace("__TAPE__", TAPE)
        .replace("__PRICE2__", PRICE2)
        .replace("__PRICE__", PRICE)
        .replace("__CTA__", CTA_URL)
        .replace("__IMPRESSUM__", IMPRESSUM_URL)
        .replace("__DATENSCHUTZ__", DATENSCHUTZ_URL)
        .replace("__ROSA__", C_ROSA)
        .replace("__PEACH__", C_PEACH)
        .replace("__FLIEDER__", C_FLIEDER)
        .replace("__INK__", C_INK)
        .replace("__CREAM__", C_CREAM)
        .replace("__GOLD__", C_GOLD))

out1 = os.path.join(HERE, "eclipse-navigator-salespage.html")
netlify_dir = os.path.join(HERE, "eclipse-navigator-salespage-netlify")
os.makedirs(netlify_dir, exist_ok=True)
out2 = os.path.join(netlify_dir, "index.html")

for path in (out1, out2):
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("geschrieben:", path, f"({os.path.getsize(path)/1024/1024:.2f} MB)")
