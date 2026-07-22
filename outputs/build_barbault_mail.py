#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut die Barbault-Reader-Verkaufsmail als HTML im DUNKLEN Kosmos-Design
von Patrycjas Banner (BARBAULT MAIL / TENTARY BARBAULT MAIL aus Canva,
15.07.2026): tiefes Nachtblau, Sterne, Binaer-Zahlen, helle Schrift,
cremeweisser Button. NICHT das helle Astrocode-Mail-Design — Patrycja
wollte diese Mail explizit im Look ihres Banners.

Text = ihre uebernommene Fassung (15.07. abends, ihre Kuerzungen) +
Schluss-Block (Link-Button, Bewegung-Closer, Signatur).

Erzeugt:
  outputs/email-barbault-reader/index.html
  outputs/email-barbault-reader/barbault-hero.jpg   (ihr Banner, 1200x300)
  outputs/email-barbault-reader/barbault-bg.jpg     (dunkler Sternen/Binaer-Verlauf)
  outputs/email-barbault-reader-getresponse.zip     (GetResponse: HTML + Bilder, KEIN Base64)

Body-Hoehe des bg anpassen: BODY_H unten (Faustregel wie Astrocode-Mail:
geometrisches Mittel aus Desktop-/Mobil-Hoehe der fertigen Mail).
"""
import os, random, zipfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "email-barbault-reader")
HERO_SRC = "/Users/patrycjakaczorowska/Downloads/TENTARY BARBAULT MAIL.png"
CHECKOUT = "https://erfolgsqueen.tentary.com/p/jNjITH"
BODY_H = 4600
BW = 600

os.makedirs(OUT, exist_ok=True)
random.seed(15072026)  # reproduzierbar

# ---- Hero: Patrycjas Banner (1200x300, wird bei 600px angezeigt = Retina) --
hero = Image.open(HERO_SRC).convert("RGB")
hero.save(os.path.join(OUT, "barbault-hero.jpg"), quality=88)

# ---- Body-Hintergrund: dunkler Verlauf + Sterne + Binaer-Zahlen ------------
# Durchschnittsfarbe der Banner-Unterkante als Verlaufs-Start (nahtloser Uebergang ohne Schmieren)
_strip = hero.crop((0, hero.size[1] - 8, hero.size[0], hero.size[1])).resize((1, 1))
top_col = _strip.getpixel((0, 0))
bot_col = (9, 11, 24)
bg = Image.new("RGB", (BW, BODY_H), bot_col)
px = bg.load()
for y in range(BODY_H):
    t = y / BODY_H
    r = int(top_col[0] + (bot_col[0] - top_col[0]) * t)
    g = int(top_col[1] + (bot_col[1] - top_col[1]) * t)
    b = int(top_col[2] + (bot_col[2] - top_col[2]) * t)
    for x in range(BW):
        px[x, y] = (r, g, b)

draw = ImageDraw.Draw(bg, "RGBA")

# v3 (Patrycja 15.07.: "Was sollen die ganzen Zahlen dahinter?"):
# KEINE Binaer-Zahlen im Body — die leben nur im Banner. Reiner Sternenhimmel.

# Sterne (ruhiger als v1)
for _ in range(1500):
    x = random.randint(0, BW - 1)
    y = random.randint(0, BODY_H - 1)
    a = random.randint(20, 110)
    r = random.choice([1, 1, 1, 2])
    draw.ellipse([x, y, x + r, y + r], fill=(255, 255, 255, a))
# ein paar hellere Glanzpunkte, bevorzugt am Rand
for _ in range(40):
    x = random.choice([random.randint(4, 80), random.randint(BW - 84, BW - 5)])
    y = random.randint(4, BODY_H - 5)
    draw.ellipse([x - 1, y - 1, x + 2, y + 2], fill=(255, 255, 255, 170))

bg = bg.filter(ImageFilter.GaussianBlur(0.4))

# v4 (Patrycja: Uebergang war verschwommen): KEINE Pixel-Verblendung mehr —
# die schmierte die Banner-Streifen nach unten. Stattdessen startet der
# Verlauf einfach in der Durchschnittsfarbe der Banner-Unterkante.

bg.save(os.path.join(OUT, "barbault-bg.jpg"), quality=82)

# ---- HTML ------------------------------------------------------------------
TXT = "color:#E9EAF4;"
P = "margin:0 0 20px 0;font-family:'Inter','Helvetica Neue',Helvetica,Arial,sans-serif;font-size:16px;line-height:27px;" + TXT

html = """<!DOCTYPE html>
<html lang="de" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="x-apple-disable-message-reformatting">
<title>Er sagte die Pandemie voraus.</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
body{margin:0;padding:0;width:100%!important;-webkit-text-size-adjust:100%;background:#10132a;}
table{border-collapse:collapse!important;}
img{border:0;height:auto;line-height:100%;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;display:block;}
a{text-decoration:none;}
p.txt{__P__}
@media only screen and (max-width:620px){
  .wrap{width:100%!important;}
  .px{padding-left:26px!important;padding-right:26px!important;}
  p.txt{font-size:15.5px!important;line-height:26px!important;}
}
</style>
</head>
<body style="margin:0;padding:0;background-color:#10132a;background:linear-gradient(180deg,#1A1E38 0%,#10132A 45%,#0B0D1C 100%);">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:#10132a;">
Was passiert 2026 bis 2030?&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
</div>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#10132a" style="background-color:#10132a;background:linear-gradient(180deg,#1A1E38 0%,#10132A 45%,#0B0D1C 100%);">
<tr><td align="center" style="padding:0;">

<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;">

<!-- ===== HERO: Patrycjas Banner, verlinkt ===== -->
<tr><td style="padding:0;">
  <a href="__CHECKOUT__" target="_blank"><img src="barbault-hero.jpg" alt="Barbault Basket Reader" width="600" style="width:100%;max-width:600px;height:auto;"></a>
</td></tr>

<!-- ===== BODY auf dunklem Sternen-Verlauf ===== -->
<tr><td background="barbault-bg.jpg" bgcolor="#10132a" style="background-color:#10132a;background-image:url('barbault-bg.jpg');background-repeat:no-repeat;background-size:100% 100%;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">

  <tr><td height="30" style="font-size:0;line-height:0;">&nbsp;</td></tr>

  <tr><td class="px" align="left" style="padding:0 46px;">
    <p class="txt">Heute Nacht wird das Sextil zwischen Uranus und Neptun exakt. Uranus läuft durch die Zwillinge und befreit das Denken. Neptun steht im Widder und weckt die Sehnsucht nach einem neuen Anfang. Zwei langsam laufende Planeten, die sich gegenseitig fördern, und ihr Sextil begleitet uns bis in den Sommer 2027.</p>
    <p class="txt">Dieses Sextil ist erst der Auftakt.</p>
    <p class="txt">Es ist die erste Konstellation vom sogenannten Barbault-Korb.</p>
  </td></tr>

  <!-- Kicker -->
  <tr><td class="px" align="center" style="padding:14px 46px 20px 46px;">
    <p style="margin:0;font-family:'Inter','Helvetica Neue',Helvetica,Arial,sans-serif;font-size:18px;line-height:26px;font-weight:700;color:#FFFFFF;text-shadow:0 0 14px rgba(255,255,255,0.55);letter-spacing:0.04em;">&#10022;&nbsp; WER WAR BARBAULT EIGENTLICH? &nbsp;&#10022;</p>
  </td></tr>

  <tr><td class="px" align="left" style="padding:0 46px;">
    <p class="txt">Falls du es noch nicht auf Social Media entdeckt hast: Fast jeder Astrologe spricht gerade darüber.</p>
    <p class="txt">André Barbault wurde 1921 in Frankreich geboren und starb 2019 mit 98 Jahren. Er gilt als einer der bedeutendsten Mundanastrologen des letzten Jahrhunderts. Während die meisten Astrologen Geburtshoroskope deuten, wollte Barbault verstehen, warum Geschichte sich in manchen Jahren verdichtet und in anderen scheinbar stillsteht.</p>
    <p class="txt">Wie treffsicher er damit war, zeigt seine bekannteste Prognose. Schon 1955 schrieb er, dass die zweite Hälfte der 1980er Jahre für das sowjetische System kritisch wird. Damals klang das absurd, der Kalte Krieg schien ein Dauerzustand. 1989 fiel die Berliner Mauer. Und auf Basis seines planetaren Konzentrationsindex hielt er für 2020 und 2021 eine weltweite Gesundheitskrise für möglich. Er schrieb das Jahre, bevor die Pandemie begann.</p>
    <p class="txt">Am Ende seines Lebens schaute dieser Mann auf die Jahre 2026 bis 2030. In einem seiner letzten Bücher heißt es:</p>
  </td></tr>

  <!-- Zitat: leuchtend -->
  <tr><td class="px" align="center" style="padding:16px 52px 26px 52px;">
    <p style="margin:0 0 10px 0;font-size:22px;line-height:24px;color:#FFFFFF;text-shadow:0 0 12px rgba(255,255,255,0.6);">&#10022;</p>
    <p style="margin:0;font-family:'Inter','Helvetica Neue',Helvetica,Arial,sans-serif;font-size:22px;line-height:34px;font-weight:700;font-style:italic;color:#FFFFFF;text-shadow:0 0 18px rgba(255,255,255,0.45);">&#8222;Wir stehen vor der Möglichkeit einer Veränderung, die Begriffe wie &#8218;Wandel&#8216; oder &#8218;Umbruch&#8216; zu schwach erscheinen&nbsp;<span style="white-space:nowrap">lässt.&#8220;</span></p>
  </td></tr>

  <tr><td class="px" align="left" style="padding:0 46px;">
    <p class="txt">Genau diese Zeit beginnt jetzt. Um den 20. Juli stehen vier gesellschaftliche Planeten gleichzeitig auf dem 4. Grad von vier Zeichen: Pluto im Wassermann, Neptun im Widder, Uranus in den Zwillingen, Jupiter im Löwen. Die Aspekte dazwischen ergeben gezeichnet eine Figur wie ein Korb mit Henkel. Am 20. Juli trennen die vier nur 13 Bogenminuten.</p>
    <p class="txt">Erwarte trotzdem keinen großen Knall. Geschichte fühlt sich im Moment ihres Geschehens meistens gewöhnlich an. Im Sommer 1989 wusste niemand, dass gerade eine Weltordnung zu Ende ging.</p>
    <p class="txt">Und wie immer gilt: Eine kollektive Konstellation wirkt bei jeder von uns anders, entscheidend ist deine eigene Chart. In welche Lebensbereiche fallen die vier Planeten bei dir? Welcher Anteil in dir möchte in den kommenden Jahren wachsen?</p>
    <p class="txt" style="__P__font-weight:700;color:#FFFFFF;">Genau dafür habe ich meinen BARBAULT BASKET READER gebaut.</p>
    <p class="txt">Du gibst deine Geburtsdaten ein (wichtig: mit deiner exakten Geburtszeit), der Reader berechnet dein Geburtshoroskop und kreiert deinen individuellen KI-Prompt. Einfügen bei ChatGPT, und du bekommst dein persönliches Reading: welche Lebensbereiche diese Konstellationen bei dir berühren und wo dein Fokus bis 2030 liegen darf.</p>
    <p class="txt">Ich habe ihn heute selbst getestet und war baff, wie genau das Ergebnis auf mich zutrifft.</p>
    <p class="txt">Während andere Astrologen über das Allgemeine sprechen, gebe ich dir was an die Hand, was exakt auf dich abgestimmt ist.</p>
  </td></tr>

  <!-- Button: cremeweiss gefuellt (Banner-Schriftfarbe), massiv -->
  <tr><td align="center" style="padding:16px 40px 30px 40px;">
    <a href="__CHECKOUT__" target="_blank" style="display:inline-block;background-color:#F2EDE1;color:#10132A;font-family:'Inter','Helvetica Neue',Helvetica,Arial,sans-serif;font-size:17px;line-height:22px;font-weight:700;padding:17px 38px;border-radius:40px;">Hol dir deinen Barbault Basket Reader</a>
  </td></tr>

  <tr><td class="px" align="left" style="padding:0 46px;">
    <p class="txt">Erinnere dich: Erst die Bewegung bewirkt Veränderung. Wie oft hast du schon was über dich gehört, aber nicht umgesetzt?</p>
    <p class="txt" style="__P__font-size:19px;line-height:28px;font-weight:700;color:#FFFFFF;margin-bottom:8px;">The Woman, who breaks the cycle!</p>
    <p class="txt" style="__P__font-size:24px;line-height:32px;font-weight:700;color:#FFFFFF;margin-bottom:6px;">Patrycja</p>
    <p class="txt" style="__P__font-size:15.5px;line-height:24px;color:#C6CBE6;">Bewusstseinsastrologin &middot; Identitycode &middot; Moneycode &middot; Emotioncode</p>
  </td></tr>

  <tr><td height="34" style="font-size:0;line-height:0;">&nbsp;</td></tr>

</table>
</td></tr>

</table>

</td></tr>
</table>
</body>
</html>
"""
html = html.replace("__P__", P).replace("__CHECKOUT__", CHECKOUT)

with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)

# ---- GetResponse-ZIP (HTML + Bilder, kein Base64) --------------------------
zpath = os.path.join(HERE, "email-barbault-reader-getresponse.zip")
with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
    for name in ["index.html", "barbault-hero.jpg", "barbault-bg.jpg"]:
        z.write(os.path.join(OUT, name), name)

print("OK ->", OUT)
print("OK ->", zpath)
