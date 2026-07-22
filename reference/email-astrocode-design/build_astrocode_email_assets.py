#!/usr/bin/env python3
"""
Baut die drei Bild-Slices fuer eine Astrocode-E-Mail aus Patrycjas Vorlage.
Standard-Design fuer ALLE E-Mails rund um Astrologie (festgelegt 14.07.2026).

Referenz-Mail: outputs/email-astrocode-neumond/ (index.html als HTML-Vorlage kopieren!)

Aufruf:
    python3 build_astrocode_email_assets.py "Deine Headline" ZIELORDNER [BODY_HOEHE]

Erzeugt im Zielordner:
    astrocode-hero.jpg    - Planeten + Haende, Headline in Collidge unter den Planeten
    astrocode-bg.jpg      - Verlauf + Binaer-Zahlen fuer den Textbereich (background-size:100% 100%)
    astrocode-footer.jpg  - NP-Logo + ASTROCODE-Schriftzug (Abschluss der Mail, verlinkt aufs Portal)

BODY_HOEHE (Default 4520): Hoehe des Hintergrund-Bilds bei 600px Breite.
Faustregel: Body-Hoehe der Mail bei 600px Viewport messen, dann geometrisches
Mittel aus Desktop- und Mobil-Verhaeltnis nehmen (Neumond-Mail: 2937 Desktop /
4343 Mobil -> 4520). Bei aehnlich langen Mails passt der Default.
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, 'vorlage-astrocode-original.webp')   # 1080x1920
FONT = os.path.join(HERE, 'font-Collidge.ttf')

def build(headline, outdir, body_h=4520):
    os.makedirs(outdir, exist_ok=True)
    tpl = Image.open(TPL).convert('RGB')
    W, H = tpl.size  # 1080x1920

    # ---- Hero: Planeten-Zone + Headline (Collidge, weiss, weicher Schatten) ----
    hero = tpl.crop((0, 0, W, 700)).convert('RGBA')
    size = 120
    while size > 30:
        font = ImageFont.truetype(FONT, size)
        d = ImageDraw.Draw(hero)
        bb = d.textbbox((0, 0), headline, font=font)
        tw = bb[2] - bb[0]
        if tw <= 920:
            break
        size -= 2
    x = (W - tw) // 2 - bb[0]
    y = 560 - bb[1]
    sh = Image.new('RGBA', hero.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((x + 3, y + 5), headline, font=font, fill=(40, 20, 80, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(7))
    hero = Image.alpha_composite(hero, sh)
    ImageDraw.Draw(hero).text((x, y), headline, font=font, fill=(255, 255, 255, 255))
    hero = hero.convert('RGB').resize((1200, 778), Image.LANCZOS)
    hero.save(os.path.join(outdir, 'astrocode-hero.jpg'), quality=88)

    # ---- Footer: NP-Logo + ASTROCODE ----
    foot = tpl.crop((0, 1560, W, 1920)).resize((1200, 400), Image.LANCZOS)
    foot.save(os.path.join(outdir, 'astrocode-footer.jpg'), quality=88)

    # ---- Body-Hintergrund: Verlauf glatt gestreckt + Zahlen in Originalgroesse ----
    BW = 600
    strip = tpl.crop((0, 700, W, 1560)).resize((BW, 478), Image.LANCZOS)
    base = strip.resize((60, body_h), Image.LANCZOS).resize((BW, body_h), Image.LANCZOS)
    base = base.filter(ImageFilter.GaussianBlur(20))
    blur = strip.filter(ImageFilter.GaussianBlur(14))
    diff = ImageChops.subtract(strip, blur)
    canvas = Image.new('RGB', (BW, body_h), (0, 0, 0))
    yy = i = 0
    while yy < body_h:
        t = diff if i % 2 == 0 else ImageOps.mirror(diff)
        canvas.paste(t, (0, yy)); yy += 478; i += 1
    bg = ImageChops.add(base, canvas)

    # Kanten farblich exakt in Hero/Footer einblenden (keine sichtbare Naht)
    hero_row = hero.crop((0, hero.size[1] - 1, hero.size[0], hero.size[1])).resize((BW, 1)).load()
    foot_row = foot.crop((0, 0, foot.size[0], 1)).resize((BW, 1)).load()
    px = bg.load()
    BL = 70
    for yy in range(BL):
        a = 1 - yy / BL
        for xx in range(BW):
            r, g, b = px[xx, yy]; R, G, B = hero_row[xx, 0]
            px[xx, yy] = (int(r + (R - r) * a), int(g + (G - g) * a), int(b + (B - b) * a))
            y2 = body_h - 1 - yy
            r, g, b = px[xx, y2]; R, G, B = foot_row[xx, 0]
            px[xx, y2] = (int(r + (R - r) * a), int(g + (G - g) * a), int(b + (B - b) * a))
    bg.save(os.path.join(outdir, 'astrocode-bg.jpg'), quality=82)
    print(f'ok -> {outdir} (hero 1200x778, bg {BW}x{body_h}, footer 1200x400)')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    build(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 4520)
