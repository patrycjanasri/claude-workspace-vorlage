#!/usr/bin/env python3
"""Baut die Womancode-Salespage (index.html, self-contained fuer Netlify Drop).
Copy = womancode-salespage-v3-2026-06-26.md (1:1, Patrycjas Voice).
Design = echtes Womancode Wein/Gold: Lotus/Lichtstrahl/Goldschwingen-Hintergrund,
Benzin/Collidge-Fonts und Gold-Logo -- alles direkt aus womancode-reader.html extrahiert."""
import pathlib, re, base64

READER = pathlib.Path('womancode-reader.html').read_text(encoding='utf-8', errors='replace')

def font_blocks(s):
    out=[]
    for m in re.finditer(r'@font-face', s):
        i=s.index('{', m.start()); depth=1; j=i+1
        while depth>0 and j<len(s):
            depth += 1 if s[j]=='{' else -1 if s[j]=='}' else 0; j+=1
        out.append(s[m.start():j])
    return '\n'.join(out)

FONTS = font_blocks(READER)
# Gold-"Woman CODE"-Logo (PNG-Data-URI aus dem Reader-Header)
LOGO = re.search(r'class="wc-logo"\s+src="(data:image/png;base64,[^"]+)"', READER).group(1)
# Echtes Womancode-Hintergrundbild: Wein/Lotus/Lichtstrahl/Goldschwingen (das eingebettete JPEG)
_jpg = re.search(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', READER).group(0)
HERO_BG = _jpg

# >>> Hier den echten Anmelde-/Checkout-Link eintragen (Tentary/Digistore) <<<
CTA_LINK = "#anmelden"
CTA_TEXT = "Ich komme zurück zu mir"

HTML = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Womancode &middot; 6 Wochen zurück zu deiner Weiblichkeit</title>
<meta name="description" content="Womancode. 6 Wochen zurück zu deiner Weiblichkeit. Und damit zu dem Erfolg, der nur aus ihr entsteht. Start 22.07.2026.">
<style>
{FONTS}
:root{{
  --gold:#E1BE7E; --gold-light:#F6E6C2; --gold-deep:#B4884A;
  --bg:#1A060C; --burgundy:#3A0D1A; --burgundy-deep:#2A0710;
  --wine:#5C0A28; --wine-soft:#7A1230;
  --text:#F0E4D6; --text-muted:#C6A896; --accent:#E1BE7E;
}}
*{{box-sizing:border-box;margin:0;padding:0;}}
html{{scroll-behavior:smooth;}}
body{{
  background-color:var(--bg);
  color:var(--text);
  font-family:'Georgia',serif;
  line-height:1.75;
  overflow-x:hidden;
}}
/* Weinrote Tiefe im Hintergrund */
body::before{{
  content:"";position:fixed;inset:0;z-index:-2;
  background:
    radial-gradient(circle at 18% 12%, rgba(92,10,40,0.55), transparent 44%),
    radial-gradient(circle at 82% 80%, rgba(58,13,26,0.7), transparent 48%),
    radial-gradient(circle at 50% 118%, rgba(225,190,126,0.12), transparent 55%),
    linear-gradient(180deg,#1A060C 0%,#2A0710 52%,#12040A 100%);
}}
.sparkle{{position:fixed;width:3px;height:3px;border-radius:50%;background:var(--gold-light);
  box-shadow:0 0 8px 2px rgba(201,169,110,.7);z-index:-1;opacity:.6;animation:tw 5s ease-in-out infinite;}}
.s1{{top:14%;left:22%;}} .s2{{top:30%;left:78%;animation-delay:1.4s;}}
.s3{{top:64%;left:12%;animation-delay:2.6s;}} .s4{{top:82%;left:86%;animation-delay:.8s;}}
@keyframes tw{{0%,100%{{opacity:.2;transform:scale(.8);}}50%{{opacity:.9;transform:scale(1.3);}}}}

.wrap{{max-width:820px;margin:0 auto;padding:0 22px;}}
section{{padding:52px 0;}}

/* ---------- HERO ---------- */
.hero{{position:relative;text-align:center;padding:0 22px 60px;}}
.hero-bg{{position:absolute;top:0;left:0;right:0;height:640px;z-index:-1;
  background:
    linear-gradient(180deg,rgba(26,6,12,.45) 0%,rgba(26,6,12,.15) 30%,rgba(26,6,12,.6) 78%,#1A060C 100%),
    url("{HERO_BG}") center top / cover no-repeat;
  -webkit-mask-image:linear-gradient(180deg,#000 0%,#000 62%,transparent 100%);
  mask-image:linear-gradient(180deg,#000 0%,#000 62%,transparent 100%);}}
.wc-logo{{display:block;width:min(360px,74%);height:auto;margin:56px auto 10px;
  filter:drop-shadow(0 10px 34px rgba(0,0,0,.6));}}
h1{{font-family:'Benzin',sans-serif;font-weight:700;
  font-size:clamp(1.9rem,7vw,3.4rem);letter-spacing:.06em;line-height:1.08;
  color:#fff;margin:6px 0 20px;
  text-shadow:0 0 42px rgba(123,16,64,.6),0 0 90px rgba(201,169,110,.25);}}
.hero-sub{{font-family:'Collidge',serif;font-size:clamp(1.15rem,2.8vw,1.6rem);
  color:var(--gold-light);max-width:640px;margin:0 auto 26px;line-height:1.5;}}
.start-pill{{display:inline-block;font-family:'Benzin',sans-serif;letter-spacing:.14em;
  font-size:.8rem;text-transform:uppercase;color:var(--bg);
  background:linear-gradient(135deg,var(--gold-light),var(--gold));
  padding:9px 22px;border-radius:40px;margin-bottom:34px;
  box-shadow:0 8px 26px rgba(201,169,110,.35);}}

/* ---------- CTA ---------- */
.cta{{display:inline-block;font-family:'Benzin',sans-serif;letter-spacing:.06em;
  font-size:1.02rem;text-transform:uppercase;text-decoration:none;color:var(--bg);
  background:linear-gradient(135deg,#F0DCA8,var(--gold) 55%,#B4884A);
  padding:19px 46px;border-radius:48px;font-weight:700;
  box-shadow:0 14px 40px rgba(201,169,110,.4);
  transition:transform .25s ease,box-shadow .25s ease;}}
.cta:hover{{transform:translateY(-3px) scale(1.02);box-shadow:0 20px 54px rgba(201,169,110,.55);}}
.cta-wrap{{text-align:center;margin:40px 0 8px;}}

/* ---------- Typografie Sektionen ---------- */
.eyebrow{{display:block;text-align:center;font-family:'Benzin',sans-serif;
  letter-spacing:.22em;font-size:.72rem;text-transform:uppercase;
  color:var(--gold);margin-bottom:14px;}}
h2{{font-family:'Collidge',serif;font-weight:400;
  font-size:clamp(1.4rem,3.6vw,2.1rem);line-height:1.5;text-align:center;
  color:#fff;margin-bottom:26px;text-wrap:balance;}}
h2 .accent{{color:var(--gold-light);}}
p{{margin-bottom:20px;font-size:1.07rem;color:var(--text);}}
p.lead{{font-size:1.18rem;color:var(--gold-light);}}
strong{{color:var(--gold-light);font-weight:700;}}
.divider{{width:120px;height:1px;margin:0 auto;
  background:linear-gradient(90deg,transparent,var(--gold),transparent);}}
.diamond{{text-align:center;color:var(--gold);letter-spacing:1.2em;margin:6px 0 0;font-size:.7rem;}}

/* ---------- Karten (Weinglas-Look) ---------- */
.card{{background:linear-gradient(160deg,rgba(92,10,40,.42),rgba(42,7,16,.62));
  border:1px solid rgba(201,169,110,.34);border-radius:20px;
  padding:34px 30px;margin:22px 0;
  box-shadow:inset 0 1px 0 rgba(201,169,110,.14),0 20px 50px rgba(0,0,0,.4);}}
.card h3{{font-family:'Collidge',serif;font-weight:400;color:var(--gold-light);
  font-size:1.3rem;line-height:1.45;margin-bottom:10px;}}
.feature-list{{list-style:none;}}
.feature-list li{{position:relative;padding-left:38px;margin-bottom:18px;
  font-size:1.07rem;line-height:1.6;}}
.feature-list li::before{{content:"✦";position:absolute;left:0;top:1px;
  color:var(--gold);font-size:1.1rem;}}

/* ---------- VIP ---------- */
.vip{{background:linear-gradient(160deg,rgba(123,16,64,.5),rgba(58,6,25,.75));
  border:1.5px solid var(--gold);border-radius:24px;padding:40px 32px;
  box-shadow:0 26px 70px rgba(0,0,0,.5),inset 0 1px 0 rgba(201,169,110,.25);position:relative;}}
.vip-badge{{position:absolute;top:-15px;left:50%;transform:translateX(-50%);
  font-family:'Benzin',sans-serif;letter-spacing:.14em;font-size:.7rem;text-transform:uppercase;
  color:var(--bg);background:linear-gradient(135deg,var(--gold-light),var(--gold));
  padding:7px 20px;border-radius:30px;white-space:nowrap;box-shadow:0 8px 22px rgba(0,0,0,.4);}}
.vip h3{{margin-top:10px;}}
.worth{{display:inline-block;margin-top:6px;font-family:'Benzin',sans-serif;
  font-size:.78rem;letter-spacing:.1em;color:var(--gold);
  border:1px solid rgba(201,169,110,.5);border-radius:30px;padding:6px 16px;}}

/* ---------- Fakten ---------- */
.facts{{text-align:center;}}
.facts .card{{max-width:520px;margin:0 auto;}}
.fact-row{{display:flex;justify-content:space-between;gap:16px;
  padding:12px 0;border-bottom:1px solid rgba(201,169,110,.18);text-align:left;}}
.fact-row:last-child{{border-bottom:none;}}
.fact-row .k{{color:var(--text-muted);font-size:.98rem;}}
.fact-row .v{{color:var(--gold-light);font-family:'Benzin',sans-serif;font-size:.92rem;letter-spacing:.03em;}}
.call-dates{{margin-top:20px;font-family:'Collidge',serif;font-size:1.15rem;color:var(--gold-light);}}

/* ---------- Story ---------- */
.story p{{color:var(--text);}}

/* ---------- Closing ---------- */
.closing{{text-align:center;}}
.closing .big{{font-family:'Collidge',serif;font-size:clamp(1.3rem,3vw,1.75rem);line-height:1.55;
  color:var(--gold-light);margin:24px 0;}}

/* ---------- Footer ---------- */
footer{{text-align:center;padding:50px 22px 60px;border-top:1px solid rgba(201,169,110,.16);
  margin-top:30px;}}
footer .sig{{font-family:'Collidge',serif;color:var(--gold-light);font-size:1.2rem;margin-bottom:14px;}}
footer a{{color:var(--text-muted);text-decoration:none;margin:0 10px;font-size:.86rem;}}
footer a:hover{{color:var(--gold);}}
footer .cr{{margin-top:16px;color:var(--text-muted);font-size:.78rem;}}

@media(max-width:560px){{
  section{{padding:40px 0;}}
  .card,.vip{{padding:28px 22px;}}
  .fact-row{{flex-direction:column;gap:2px;}}
}}
</style>
</head>
<body>
<!-- ============================================================
     WOMANCODE SALESPAGE  ·  self-contained fuer Netlify Drop
     CTA-Link austauschen:  suche  href="{CTA_LINK}"  und ersetze durch deinen Anmeldelink
     ============================================================ -->
<span class="sparkle s1"></span><span class="sparkle s2"></span>
<span class="sparkle s3"></span><span class="sparkle s4"></span>

<!-- HERO -->
<header class="hero">
  <div class="hero-bg" aria-hidden="true"></div>
  <img class="wc-logo" src="{LOGO}" alt="Womancode">
  <h1>WOMANCODE</h1>
  <p class="hero-sub">6 Wochen zurück zu deiner Weiblichkeit. Und damit zu dem Erfolg, der nur aus ihr entsteht.</p>
  <span class="start-pill">Start &middot; 22.07.2026</span>
  <div class="cta-wrap">
    <a class="cta" href="{CTA_LINK}">{CTA_TEXT}</a>
  </div>
</header>

<!-- PROBLEM -->
<section class="wrap">
  <span class="eyebrow">Kennst du das?</span>
  <h2>Jeder steht bei dir an erster Stelle.<br><span class="accent">Nur du nicht.</span></h2>
  <p>Kennst du das? Jeder steht bei dir an erster Stelle, nur du nicht.</p>
  <p>Eben mal schnell duschen, irgendwas anziehen, und schon hetzt du zum nächsten Termin. Zeit und Genuss für dein Leben? Dafür hast du keine Zeit.</p>
  <p class="lead">Sinnlichkeit? Was ist das eigentlich?</p>
  <p>Seit Jahren versuchst du, dir etwas aufzubauen. Und hast dabei das Gefühl, du bewegst dich im Kreis. Alles fühlt sich schwer an. Du hast kaum Ideen, schaust ständig auf Social Media, was die anderen Frauen machen, siehst die perfekte Fassade eines Lebens, das du auch gerne hättest. Und dein eigener Erfolg bleibt aus.</p>
</section>
<div class="divider"></div>

<!-- STIMME IM KOPF -->
<section class="wrap">
  <span class="eyebrow">Diese Stimme im Kopf kennst du</span>
  <h2>Aus Druck. Aus Kontrolle.</h2>
  <p>Was, wenn die Uschi was sagt. Was, wenn ich im Elternchat lande. Sehe ich gut genug aus. Ist das nicht zu viel.</p>
  <p>Den ganzen Tag verkaufst du aus dieser Anspannung. Aus Druck. Aus Kontrolle. Aus der tiefsten männlichen Energie, die es gibt.</p>
  <p>Und dann fragst du dich, warum sich alles so schwer anfühlt und warum der Erfolg ausbleibt.</p>
  <p class="lead">Ich sag dir, warum. Weil Money niemals aus männlicher Energie kreiert wird. Weiblichkeit ist der Schlüssel.</p>
</section>
<div class="divider"></div>

<!-- SCHLUSS -->
<section class="wrap">
  <span class="eyebrow">Was wäre, wenn damit Schluss ist</span>
  <h2>Ein Raum, den ich öffne.</h2>
  <p>Was wäre, wenn ich dir sage, dass damit ab sofort Schluss ist?</p>
  <p>Ein Raum, den ich öffne, für die Frauen, die es satt haben, sich unter ihrem Wert zu verkaufen. Für die Frauen, die es satt haben, immer und immer wieder den gleichen Alltag zu durchleben und keine Lebendigkeit mehr zu fühlen.</p>
</section>

<!-- URWUNDE -->
<section class="wrap">
  <span class="eyebrow">Die weibliche Urwunde</span>
  <h2>Brich den <span class="accent">Womancycle.</span></h2>
  <p>Wenn ich zurückblicke auf die Gesellschaft, sehe ich Frauen, die für ihre Göttlichkeit verbannt wurden.</p>
  <p>Ich sehe Frauen, die nach der Kriegszeit dieses Land wieder aufgebaut haben. Trümmerfrauen nannte man sie. Vielleicht erinnerst du dich an die Geschichten deiner Oma oder Uroma.</p>
  <p>Dann sehe ich Frauen, die in den 90ern und 2000ern in einem Ideal von Size Zero groß geworden sind. Frauen, die in dieser Welt als Objekt dargestellt werden.</p>
  <p>Und genau damit ist ab sofort Schluss.</p>
  <p class="lead">Brich den Womancycle. Brich die Urwunde, die von Generation zu Generation weitergegeben wird.</p>
</section>
<div class="divider"></div>

<!-- FUNDAMENT -->
<section class="wrap">
  <span class="eyebrow">Das Fundament, auf dem alles steht</span>
  <h2>Diese Energie macht dich <span class="accent">magnetisch.</span></h2>
  <p>Du hast es satt. Diesen ständigen inneren Antrieb: Ich muss noch mehr leisten. Was macht die und die anders. Was ist, wenn mein Business nicht tragbar ist.</p>
  <p>Aber hast du es schon mal aus deiner Sinnlichkeit heraus probiert? Hast du deiner weiblichen Energie schon mal Präsenz geschenkt?</p>
  <p>Nein? Und warum nicht?</p>
  <p>Diese Energie macht dich magnetisch. Sie ist dein Oxytocin, dein Bindungshormon, das dich in Verbindung bringt und anziehend macht. Napoleon Hill hat schon vor hundert Jahren davon geschwärmt, diese Energie zu nutzen, um Reichtum zu kreieren.</p>
  <p class="lead">Genau diese Kraft holen wir zurück. Und sie wird dein Erfolgskanal.</p>
</section>
<div class="divider"></div>

<!-- MEINE GESCHICHTE -->
<section class="wrap story">
  <span class="eyebrow">Meine Geschichte</span>
  <h2>Ich bin <span class="accent">WILD.</span></h2>
  <p>Lass mich ein bisschen über meine eigene Geschichte mit Womancode ausholen.</p>
  <p>Ich bin gefühlt mein halbes Leben übergewichtig. In den 2000ern habe ich mich niemals dazugehörig gefühlt. Verstecken wollte ich mich, mein ganzes Leben. Und immer habe ich die Schuld bei mir gesucht, bei meinem Körper. Ich habe meinen Körper verurteilt und versteckt. Versteckt in weiter, schwarzer, dunkler Kleidung.</p>
  <p>Es war sogar so manifestiert, dass ich meine Periode nicht bekommen habe. Höchstens zweimal im Jahr. Die Worte vom Gynäkologen sind dir bestimmt bewusst: Es liegt an Ihrem hohen Gewicht, Sie müssen abnehmen.</p>
  <p>Bis zu dem Tag, als ich vor einigen Jahren das Buch „Die Wolfsfrau“ gelesen habe. Mir wurde bewusst, was für eine krasse Fähigkeit wir Frauen haben. Unser Sakralchakra, unsere Intuition, unsere Weiblichkeit. Die Lust, die Sinnlichkeit, die Bewegung. Alles. Wir sind in der Lage, einen Menschen zu erschaffen und zu ernähren. Jeder Mensch auf dieser Erde ist durch den Körper einer Frau geboren. Durch dieses Portal.</p>
  <p>Ich fing an, mich mehr damit zu beschäftigen. Ich begann, meine Weiblichkeit und meine Lust immer mehr zu leben.</p>
  <p>2023 bekam ich sogar meine Periode zurück, und seitdem habe ich einen Zyklus. Ich kleide mich bunt, ich kleide mich sinnlich, ich kreise mein Becken, ich tanze, ich lebe, und ich bin WILD.</p>
  <p>Und nicht nur das. Ich bin finanziell unabhängig. In 12 Monaten habe ich über 100.000 Euro generiert. Davor hatte ich 4.500 Euro im Monat, manchmal weniger. Denn Weiblichkeit und die weibliche Energie sind der Schlüssel für unseren Erfolgsflow. Money wird nicht aus männlicher Energie kreiert. Weiblichkeit ist der Schlüssel.</p>
  <p class="lead">Genau diesen Weg möchte ich in Womancode an dich weitergeben.</p>
</section>

<div class="cta-wrap"><a class="cta" href="{CTA_LINK}">{CTA_TEXT}</a></div>
<div class="diamond">&#9670; &#9670; &#9670;</div>

<!-- WAS DICH ERWARTET -->
<section class="wrap">
  <span class="eyebrow">Was dich in Womancode erwartet</span>
  <h2>Sechs intensive Wochen zurück zu dir.</h2>
  <p>Sechs intensive Wochen zurück zu dir, zu deiner Weiblichkeit, zu mehr Sinnlichkeit.</p>
  <p>Du kommst zurück in deinen Körper, raus aus dem Kopf. Du entdeckst deine Sinnlichkeit im Alltag wieder, an einem ganz normalen Dienstag. Du lernst deinen Zyklus als Kraft kennen statt als Störung. Und du verstehst, wie deine weibliche Energie dein Erfolgsflow wird, im Leben und im Geld.</p>
  <div class="card">
    <h3>Dein Kleiderschrank ist ein Anfang.</h3>
    <p>Es fängt klein an. Ein roter Lippenstift für 2 Euro bei dm. Damit habe ich angefangen. Die löchrige Unterwäsche, die du noch zum Schlafen anziehst, fliegt raus. Der kaputte BH fliegt raus. Du kleidest dich nicht mehr in kaputter Energie. Hier beginnt Energielehre.</p>
  </div>
  <div class="card">
    <h3>Dein Körper wird wieder dein Zuhause.</h3>
    <p>Becken kreisen, tanzen, dich bewegen, dich fühlen.</p>
  </div>
  <div class="card">
    <h3>Deine Lust für das Leben kommt zurück.</h3>
    <p>Auf den Tag, auf Schönheit, auf dich.</p>
  </div>
  <div class="card">
    <h3>Deine Weiblichkeit wird dein Erfolgskanal.</h3>
    <p>Du erschaffst aus weiblicher Energie statt aus Druck und Funktionieren.</p>
  </div>
</section>

<!-- ALLES DRIN -->
<section class="wrap">
  <span class="eyebrow">Das ist alles drin</span>
  <h2>Dein Raum für sechs Wochen.</h2>
  <div class="card">
    <ul class="feature-list">
      <li>Vier Live-Calls, je 20:00 Uhr.</li>
      <li>Sensual Canva Call: Wie designe ich aus meiner weiblichen Kreativität.</li>
      <li>Intensive Telegram-Begleitung über die gesamten sechs Wochen.</li>
      <li>Dein Promptguide zu deiner Weiblichkeit. Wie liebst du, wie fühlst du, was ist dir in einer Partnerschaft wirklich wichtig. Allein dieses Wissen wird dein Sinnlichkeitsbooster.</li>
      <li>Eine intensive Deep Sensual Transmission.</li>
      <li>Eine Goodiebag mit einem sinnlichen Secret-Öl, das deine Leidenschaft für das Leben wieder entfacht.</li>
    </ul>
  </div>
</section>

<!-- VIP -->
<section class="wrap">
  <span class="eyebrow">Dein VIP-Raum</span>
  <h2>Nur 2 Plätze.</h2>
  <div class="vip">
    <span class="vip-badge">Nur 2 Plätze</span>
    <p>In diesem Raum gebe ich dir die Möglichkeit, mit mir ins VIP zu gehen. Es gibt nur zwei Plätze.</p>
    <h3>Im VIP kreieren wir deinen Raum. Dein Business.</h3>
    <p>Du hast Ideen, aber wo bleibt die Umsetzung? Irgendwie fühlt sich dein Business für dich an wie ein riesen Wirrwarr. In meiner Präsenz erlebst du pure Klarheit. Dein Ausdruck darf Raum einnehmen, und in diesem Raum erschaffst du dein Empire. In zwei tiefen 1:1 Calls gehen wir gemeinsam dort hin. Ich sehe, was du nicht siehst, und allein meine Präsenz bewegt.</p>
    <h3>Ein Branddesign von meiner Branddesignerin Patricia.</h3>
    <p>Patricia ist keine Grafikerin, die dir schnell ein Logo baut. Ich habe sie in Mailand getroffen und sofort gespürt, dass sie special ist. Sie hat mein Leben in Bilder verfasst. Das kann keine KI. Sie legt ihre eigene Sinnlichkeit in jedes Design, sie tanzt sich vorher ein, und genau diese Energie wird dein Branding tragen. Du bekommst einen Creationcall mit ihr und mir, einen Schriftzug für deinen Namen oder dein Team, ein Symbol wie deine Initiale und zehn Canva-Vorlagen.</p>
    <span class="worth">Allein der Designpart hat einen Wert von 2222 Euro.</span>
  </div>
</section>
<div class="divider"></div>

<!-- FAKTEN -->
<section class="wrap facts">
  <span class="eyebrow">Die Fakten</span>
  <h2>Sechs Wochen. Ein Raum.</h2>
  <div class="card">
    <div class="fact-row"><span class="k">Start</span><span class="v">22.07.2026</span></div>
    <div class="fact-row"><span class="k">Zeitraum</span><span class="v">22.07.2026 – 26.08.2026</span></div>
    <div class="fact-row"><span class="k">Dauer</span><span class="v">6 intensive Wochen</span></div>
    <p class="call-dates">Die vier Live-Calls je 20:00 Uhr:<br>22.07.2026 &middot; 29.07.2026 &middot; 12.08.2026 &middot; 26.08.2026</p>
  </div>
</section>

<!-- FUER WEN -->
<section class="wrap closing">
  <span class="eyebrow">Für wen Womancode ist</span>
  <h2>Komm zurück zu dir.</h2>
  <p>Für die Frau, die es satt hat, sich unter ihrem Wert zu verkaufen. Für die Frau, die jeden Tag denselben Alltag durchlebt und keine Lebendigkeit mehr fühlt. Für die Frau, die ihr Business jetzt wirklich aufbauen will, aus ihrer absoluten weiblichen Präsenz heraus, und die bereit ist, ihre Energie zu verändern.</p>
  <p>Du musst dich nicht länger verstecken. Du musst dich nicht länger an die letzte Stelle setzen. Du musst nicht länger aus Druck funktionieren.</p>
  <p class="big">Komm zurück in deinen Körper. Komm zurück in deine Sinnlichkeit. Komm zurück zu dir.</p>
  <p class="lead">Womancode öffnet den Raum. Am 22.07.2026.</p>
  <div class="cta-wrap" id="anmelden"><a class="cta" href="{CTA_LINK}">{CTA_TEXT}</a></div>
</section>

<footer>
  <div class="sig">Patrycja Nasri</div>
  <div>
    <a href="https://patrycja-nasri.de/impressum/" target="_blank" rel="noopener">Impressum</a>
    <a href="https://patrycja-nasri.de/datenschutz/" target="_blank" rel="noopener">Datenschutz</a>
  </div>
  <div class="cr">&copy; 2026 Patrycja Nasri &middot; Womancode</div>
</footer>
</body>
</html>
"""

out = pathlib.Path('/Users/patrycjakaczorowska/Downloads/Vorlagen/claude-workspace-vorlage/outputs/womancode-salespage-netlify/index.html')
out.write_text(HTML, encoding='utf-8')
print(f"geschrieben: {out}  ({len(HTML)/1024:.0f} KB)")
