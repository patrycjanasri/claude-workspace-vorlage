#!/usr/bin/env python3
"""
Astro Workbook PDF Generator
Business · Identität · Geldcode · Nervensystem · Leadership
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

PAGE_W, PAGE_H = A4

# Color palette — warm mystical cream
BG_COLOR      = colors.HexColor('#FAF6EF')
BOX_COLOR     = colors.HexColor('#EDE5D8')
BOX_BORDER    = colors.HexColor('#B8A48A')
DARK_BG       = colors.HexColor('#1C1410')
HEADING_COLOR = colors.HexColor('#2C1810')
TEXT_COLOR    = colors.HexColor('#3D2B1F')
ACCENT_GOLD   = colors.HexColor('#8B6914')
LIGHT_GOLD    = colors.HexColor('#C9A96E')
LINE_COLOR    = colors.HexColor('#CFC0AD')
MUTED_COLOR   = colors.HexColor('#7A6A5A')
WHITE         = colors.HexColor('#FAF6EF')

# ─── DATA ────────────────────────────────────────────────────────────────────

TEIL1_PROMPTS = [
    ("SONNE", [
        ("Meine Sonne in Zeichen ________ und Haus ___ ist der Kern meiner Identität als Unternehmerin. Welche Art von Leader bin ich in meiner tiefsten Essenz — und welche Form von Sichtbarkeit, Ausdruckskraft und Führungsrolle entspricht wirklich meiner Natur? Was würde sich in meinem Business verändern, wenn ich aufhöre, mich an anderen zu orientieren, und vollständig diese Version von mir verkörpere?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Was sagt meine Sonne in Zeichen ________ und Haus ___ über mein Business-Potenzial, das ich noch nicht vollständig lebe? Welche Qualitäten machen mich unverwechselbar in meinem Markt — und warum ist genau das mein größter Wettbewerbsvorteil?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("MOND", [
        ("Mein Mond in Zeichen ________ und Haus ___ zeigt, wie ich emotional funktioniere — als Unternehmerin, als Führungspersönlichkeit, als Frau. Welche Arbeitsweise, welcher Rhythmus und welches Umfeld bringen mich in meine natürliche Schöpfungskraft? Was brauche ich, um konstant zu verkaufen, ohne mich emotional zu entleeren?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Wo sabotiere ich mein Business durch emotionale Muster, die in meinem Mond in Zeichen ________ und Haus ___ verwurzelt sind? Was sind meine emotionalen Trigger als Unternehmerin — und wie baue ich ein inneres Fundament, das unabhängig von äußeren Ergebnissen stabil bleibt?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("MERKUR", [
        ("Mein Merkur in Zeichen ________ und Haus ___ definiert, wie ich denke, kommuniziere und überzeuge. Welche Art von Content, welche Sprache und welche Botschaften entsprechen meiner natürlichen Denkweise — sodass mein Marketing nicht nur gesehen, sondern wirklich gefühlt wird?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Wie überzeuge und verkaufe ich am stärksten? Was sagt mein Merkur in Zeichen ________ und Haus ___ darüber, wie ich meine Angebote pitchen, meine Storys erzählen und meine Kundinnen in Entscheidungen führen sollte — auf eine Weise, die sich für mich nicht nach Verkaufen anfühlt?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("VENUS", [
        ("Meine Venus in Zeichen ________ und Haus ___ zeigt meinen Wert, meinen Überfluss-Code und wie ich Geld und Kundinnen anziehe. Wo blockiere ich diesen Fluss — durch zu niedrige Preise, durch das falsche Angebot oder durch eine Identität, die meinen wahren Wert noch nicht vollständig verkörpert?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Was sagt meine Venus in Zeichen ________ und Haus ___ über meine ideale Kundin? Wen ziehe ich wirklich an — welche Energie, welche Werte, welchen Reifegrad — und wie baue ich ein Business, das genau diese Frau magnetisch anzieht?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("MARS", [
        ("Mein Mars in Zeichen ________ und Haus ___ ist mein Antrieb, meine Durchsetzungskraft und mein natürlicher Verkaufsstil. Was passiert, wenn ich gegen meine Mars-Energie arbeite — und wie sieht Verkaufen aus, wenn ich vollständig in meiner Mars-Kraft bin? Was ist mein Flow-State im Business?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Wie kämpfe ich für meine Ziele — und wo halte ich mich durch Angst oder falsche Bescheidenheit zurück? Was sagt mein Mars in Zeichen ________ und Haus ___ darüber, welche konkreten Aktionen und Strategien meiner natürlichen Energie entsprechen — und welche mich unnötig Kraft kosten?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("JUPITER", [
        ("Mein Jupiter in Zeichen ________ und Haus ___ zeigt, wo Wachstum und Überfluss für mich natürlich fließen. In welchen Bereichen meines Business habe ich einen natürlichen Vorteil — und wo lasse ich gerade Geld und Wachstumspotenzial liegen, weil ich es nicht erkenne oder nicht traue?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Was ist mein persönlicher Expansions-Code? Wie und wo wächst mein Business am natürlichsten, wenn ich dem Fluss meines Jupiter in Zeichen ________ und Haus ___ vertraue — statt durch Überarbeitung und Kontrolle zu erzwingen?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("SATURN", [
        ("Mein Saturn in Zeichen ________ und Haus ___ ist mein strengster Lehrer. Welche Strukturen, welche Disziplin und welche Verantwortungsbereiche muss ich in meinem Business aufbauen, um dauerhaft — nicht kurzfristig — erfolgreich zu sein? Was will Saturn von mir lernen?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Wo limitiert mich Saturn in Zeichen ________ und Haus ___ durch Angst, Kontrollzwang oder übertriebenen Perfektionismus — und wo ist genau das meine größte Business-Schwäche? Wie verwandle ich diese Energie in echte Kompetenz, Autorität und unerschütterliche Verlässlichkeit?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("URANUS", [
        ("Mein Uranus in Zeichen ________ und Haus ___ ist meine rebellische Brillanz. Wo bin ich als Unternehmerin wirklich disruptiv — wo kann ich Denkweisen, Systeme und Märkte verändern auf eine Weise, die andere noch nicht sehen? Was ist die Revolution, die ich auslösen kann?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Wo werde ich durch Uranus in Zeichen ________ und Haus ___ dazu gerufen, einen völlig eigenen Weg zu gehen — weg vom Mainstream, weg von dem, was andere als \"richtig\" definieren? Was ist meine unkonventionelle Superkraft im Business?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("NEPTUN", [
        ("Mein Neptun in Zeichen ________ und Haus ___ zeigt meine Vision, meine Intuition und meine spirituelle Gabe. Wie integriere ich diese Energie in ein profitables Business — und wo schwäche ich mich durch Neptuns Illusionen, durch unrealistische Erwartungen oder durch fehlende Grenzen?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Was ist meine höchste Business-Vision, wenn ich meinen Neptun in Zeichen ________ und Haus ___ vollständig zum Ausdruck bringe? Was liegt jenseits von Angst, jenseits von Logik — das Größte, was ich aufbauen und hinterlassen kann?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("PLUTO", [
        ("Mein Pluto in Zeichen ________ und Haus ___ ist meine Transformationskraft. Was ist die tiefste Veränderung, die ich bei meinen Kundinnen auslöse — und warum ist genau das meine stärkste Marktposition? Wo liegt die Macht, die ich noch nicht vollständig annehme?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Wo muss ich in meinem Business sterben und neu geboren werden? Was halte ich fest — alte Identitäten, alte Strategien, alte Rollen — und was wird möglich, wenn ich der Pluto-Energie in Zeichen ________ und Haus ___ vollständig vertraue?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("NÖRDLICHER MONDKNOTEN", [
        ("Mein nördlicher Mondknoten in Zeichen ________ und Haus ___ zeigt, wohin ich wachsen soll — mein karmisches Business-Ziel in diesem Leben. Welche Version meiner selbst als Unternehmerin will ich werden — und was hält mich davon ab, diesen Schritt jetzt zu wagen?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Was ist die Business-Mission am nördlichen Mondknoten in Zeichen ________ und Haus ___? Was muss ich loslassen, riskieren und annehmen, damit diese höchste Version meines Business Wirklichkeit wird?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("SÜDLICHER MONDKNOTEN", [
        ("Mein südlicher Mondknoten in Zeichen ________ und Haus ___ zeigt, welche Stärken und Talente ich aus vergangenen Erfahrungen mitbringe — aber auch, welche alten Muster und Überzeugungen mich in der Komfortzone halten und mein Wachstum bremsen. Was sind meine verborgenen Ressourcen — und was sind meine versteckten Fallen?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Welche alten Business-Strategien, Rollen oder Identitäten bringe ich durch meinen südlichen Mondknoten in Zeichen ________ und Haus ___ mit — die vielleicht mal funktioniert haben, aber jetzt veraltet sind? Was darf ich integrieren, ohne mich darin zu verlieren?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("LILITH", [
        ("Meine Lilith in Zeichen ________ und Haus ___ ist meine wilde, unterdrückte Kraft — die Seite von mir, die ich im Business vielleicht verstecke, weil sie zu viel, zu direkt, zu roh erscheint. Was wird möglich in meinem Marketing, meinen Verkaufsgesprächen und meiner Sichtbarkeit, wenn ich diese Energie vollständig freigebe?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Welche Macht liegt in meiner Lilith in Zeichen ________ und Haus ___, die ich noch nicht eingesetzt habe? Wie würde mein Auftreten, meine Sprache und mein Angebot aussehen, wenn ich meine wilde Authentizität nicht mehr zähme?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("CHIRON", [
        ("Mein Chiron in Zeichen ________ und Haus ___ ist meine tiefste Wunde — und gleichzeitig meine stärkste Gabe für meine Kundinnen. Wie wird aus meinem persönlichsten Schmerz mein überzeugendster Content, mein stärkstes Angebot und mein unverwechselbares Vermächtnis?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Wo sabotiere ich mich durch die ungeheilte Seite meines Chiron in Zeichen ________ und Haus ___ — durch das innere Gefühl, nicht qualifiziert genug, nicht gut genug, nicht weit genug zu sein? Wie sieht die geheilte Version dieser Energie aus — und was wird in meinem Business möglich, wenn ich von dieser Stelle heraus führe?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("ASZENDENT", [
        ("Mein Aszendent in Zeichen ________ ist meine erste Wirkung auf die Welt — das, was Menschen sofort von mir wahrnehmen, bevor ich ein Wort sage. Was signalisiere ich auf Instagram, in meinen Salespages und im ersten Kontakt — und wie setze ich diese Energie bewusst ein, um die richtigen Kundinnen magnetisch anzuziehen?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Wie erscheine ich als Marke durch meinen Aszendenten in Zeichen ________ — visuell, energetisch, kommunikativ? Was ist mein natürlicher erster Eindruck — und wo wirke ich anders als ich bin, weil ich meine Aszendenten-Energie noch nicht voll verkörpere?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("DESZENDENT", [
        ("Mein Deszendent in Zeichen ________ zeigt, wen ich wirklich anziehe — als Kundinnen, als Partner, als Team. Was sind die Qualitäten meiner idealen Kundin — und was braucht sie von mir, das ich ihr durch mein Angebot geben kann?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Welche Art von Kooperationen, Partnerschaften und Team-Dynamiken entsprechen meinem Deszendent in Zeichen ________ — und wo erschöpfe ich mich durch Beziehungen, die nicht zu meiner Energie passen? Wen brauche ich wirklich um mich, um mein volles Potenzial zu entfalten?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("MEDIUM COELI (MC)", [
        ("Mein MC in Zeichen ________ ist meine öffentliche Mission und mein beruflicher Ruf. Wofür will ich in meiner Nische bekannt sein — welche Transformation, welche Botschaft, welches Vermächtnis? Was muss ich tun, um diesen Ruf bewusst aufzubauen?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Was ist der höchste berufliche Ausdruck meines MC in Zeichen ________? Wenn alles möglich wäre — wie sieht mein Business in seiner vollsten Form aus? Was halte ich noch zurück — und warum?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("IMUM COELI (IC)", [
        ("Mein IC in Zeichen ________ ist mein inneres Fundament — die Wurzel, aus der mein gesamtes Business wächst. Was brauche ich innerlich, um als Unternehmerin wirklich stabil zu sein — unabhängig von Umsatz, Reichweite oder äußerer Bestätigung?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Was ist die tiefste Wahrheit über mich als Unternehmerin, die ich nur im Inneren kenne und noch nicht vollständig annehme? Was liegt in meinem IC in Zeichen ________, das ich als Schwäche betrachte — das aber in Wirklichkeit meine stärkste Grundlage ist?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
]

TEIL2_PROMPTS = [
    ("1. GELDCODE", "Deine finanzielle Identität", [
        ("Schaue auf deine Venus in Zeichen ________ und Haus ___, deinen Jupiter in Zeichen ________ und Haus ___ und deinen Pluto in Zeichen ________ und Haus ___. Was zeigen diese drei Planeten zusammen über deinen Geld-Blueprint? Wo ist Überfluss für dich natürlich — und wo hast du eine tiefe, unbewusste Überzeugung, dass Geld limitiert, gefährlich oder unehrlich ist?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Wenn deine Venus in Zeichen ________ ein Preisschild auf deinen Wert kleben würde — welchen Betrag würde sie nennen? Und warum rechnest du in deinem Business gerade mit einem anderen Betrag? Was musst du in dir heilen, damit dein Preis und dein inneres Wertgefühl sich decken?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Dein Saturn in Zeichen ________ und Haus ___ zeigt, welche Lektionen du über Geld, Arbeit und Verdienen gelernt hast. Welche dieser Lektionen stärken dich — und welche sind eigentlich nur alte Überzeugungen deiner Eltern, deiner Herkunft, deiner Vergangenheit? Was ist der Unterschied zwischen deinem wahren Geldcode und dem, der dir beigebracht wurde?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Stell dir vor, dein Jupiter in Zeichen ________ und Haus ___ schreibt dir einen Brief über dein finanzielles Potenzial. Was würde er dir sagen, das du noch nicht glaubst? Welche Geldversion von dir wartet darauf, dass du sie endlich annimmst — und was steht genau jetzt noch im Weg?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("2. IDENTITYCODE", "Wer du wirklich bist", [
        ("Deine Sonne in Zeichen ________ und Haus ___, dein Aszendent in Zeichen ________ und dein Mond in Zeichen ________ und Haus ___ bilden zusammen dein Identitäts-Dreieck. Welche Version von dir zeigt sich nach außen — und welche lebst du noch nicht? Wo ist dein größter Widerspruch zwischen dem, was du nach außen zeigst, und dem, was du innerlich weißt?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Wer wärst du als Unternehmerin, wenn du keine Angst vor Ablehnung, Vergleichen oder Kritik hättest? Was sagt deine Sonne in Zeichen ________ und Haus ___ über diese Version von dir — und was hält dich davon ab, sie heute zu sein?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Deine Lilith in Zeichen ________ und Haus ___ ist die Seite von dir, die du vielleicht selbst nicht ganz akzeptierst. Wenn diese wilde, unzähmbare Energie Teil deiner Marke wäre — was würde sich in deinem Content, deiner Sprache und deiner Positionierung verändern? Was würde deine Community über diese Version von dir denken — und warum hält dich diese Antwort zurück?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Dein nördlicher Mondknoten in Zeichen ________ und Haus ___ zeigt die Identität, in die du in diesem Leben hineinwachsen sollst. Beschreibe diese Unternehmerin konkret: Wie spricht sie? Was verkauft sie? Was ist ihr Preis? Wie führt sie ihr Team? Und was unterscheidet sie von der Version, die du gerade lebst?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("3. SCHATTENARBEIT", "Business-Schattenarbeit", [
        ("Schaue auf deinen Chiron in Zeichen ________ und Haus ___ und deinen südlichen Mondknoten in Zeichen ________ und Haus ___. Was ist die Geschichte, die du dir selbst über dein Business erzählst — die, die dich klein hält? Formuliere diese Geschichte in einem Satz. Dann formuliere die Gegenwart: Was ist die Wahrheit, wenn du diese Geschichte weglässt?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Dein Saturn in Zeichen ________ und Haus ___ sitzt mit deinem Chiron in Zeichen ________ und Haus ___ an einem Tisch. Was diskutieren sie über dein Business? Was sagt der eine — und was antwortet der andere? Welche Botschaft haben sie gemeinsam für dich?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Was ist die Unternehmerin, die du niemals sein wolltest — aber manchmal erkennst du sie in dir? Welche Qualitäten, welche Ängste, welche Verhaltensweisen gehören zu ihr? Was sagt dein Mond in Zeichen ________ und Haus ___ darüber, warum du diese Seite von dir entwickelt hast — und was sie eigentlich schützen wollte?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Schaue auf deinen Saturn in Zeichen ________ und Haus ___, deinen Chiron in Zeichen ________ und Haus ___ und deinen südlichen Mondknoten in Zeichen ________ und Haus ___. Diese drei bilden zusammen das Gesicht deines inneren Saboteurs. Was ist sein größtes Argument dafür, dass du kleiner bleiben sollst — und was ist deine Antwort an ihn?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("4. SICHTBARKEIT", "Sichtbarkeit & Personal Brand", [
        ("Dein Aszendent in Zeichen ________ und dein MC in Zeichen ________ sind deine öffentliche Identität. Was ist der Kern deiner Marke — nicht was du tust, sondern wer du bist? In einem Satz: Was ist die unverwechselbare Energie, die du in jeden Raum bringst, den du betrittst?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Was hält dich davon ab, wirklich sichtbar zu sein? Schaue auf deinen Mond in Zeichen ________ und Haus ___ und deinen Saturn in Zeichen ________ und Haus ___. Was fürchtest du, wenn zu viele Menschen sehen, wer du wirklich bist — und welches alte Erlebnis hat diese Angst gepflanzt?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Deine Venus in Zeichen ________ und Haus ___ definiert deine ästhetische Energie — was Menschen visuell und energetisch in dir anzieht. Welches Bild, welche Farben, welcher Ton entsprechen deiner Venus-Energie — und wo weicht dein aktueller Auftritt davon ab?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Wenn deine Sonne in Zeichen ________ und Haus ___ deinen Instagram-Kanal führen würde — wie würde er aussehen? Welche Themen, welche Energie, welche Frequenz? Vergleiche das mit dem, was du gerade zeigst. Was willst du ändern?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("5. IDEALE KUNDIN", "Deine ideale Kundin & Resonanz", [
        ("Dein Deszendent in Zeichen ________ zeigt, wen du wirklich anziehen sollst. Beschreibe deine ideale Kundin durch die Linse dieser Energie: Wie denkt sie? Was glaubt sie über sich selbst? Was hält sie noch zurück — und was braucht sie von dir, um den nächsten Schritt zu machen?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Deine Venus in Zeichen ________ und Haus ___ und dein Chiron in Zeichen ________ und Haus ___ zusammen: Welchen Schmerz deiner Kundin verstehst du auf einem Level, das andere Coaches nicht verstehen — weil du ihn selbst erlebt hast? Was macht das mit deiner Arbeit?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Stell dir vor, deine ideale Kundin hat sich für dein Angebot entschieden. Welcher Punkt war der Wendepunkt — welches Wort, welche Geschichte, welche Energie hat sie über die Grenze gebracht? Was sagt dein Merkur in Zeichen ________ und Haus ___ darüber, wie du genau diesen Moment in deinem Marketing erschaffst?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("6. SALES POWER", "Sales Power & Conversion", [
        ("Dein Mars in Zeichen ________ und Haus ___ ist dein natürlicher Verkaufsstil. Nicht der Verkaufsstil, den du dir angeeignet hast — sondern der, der dir in Fleisch und Blut liegt. Beschreibe ihn. Wie würde Verkaufen aussehen, wenn es sich so natürlich anfühlt wie atmen?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Was passiert in dir, kurz bevor du ein Angebot machst — kurz bevor du den Preis nennst? Was fühlt dein Mond in Zeichen ________ und Haus ___ in diesem Moment? Und was ist die Geschichte dahinter — wann hast du gelernt, dass dein Wert verhandelt werden muss?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Dein Jupiter in Zeichen ________ und Haus ___ zeigt deinen Überfluss-Code. Wenn du aus dieser Energie heraus verkaufst — ohne Überzeugungsdruck, ohne Angst vor Ablehnung, aus echter Großzügigkeit — wie klingt dann dein Angebot? Schreibe es.\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Schaue auf deinen Mars in Zeichen ________ und Haus ___ und deinen Mond in Zeichen ________ und Haus ___. Was sagen diese beiden über den Moment, in dem du deinen Preis nennst? Welcher Satz in deinem Verkaufsgespräch klingt durch diese Energie noch hohl — und was muss sich in dir verändern, damit er aus voller Überzeugung kommt?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("7. DEIN ANGEBOT", "Dein Angebot — Deine Gabe", [
        ("Was ist dein Kerngeschenk — die eine Transformation, für die du auf diese Welt gekommen bist? Schaue auf deinen Chiron in Zeichen ________ und Haus ___, deinen Pluto in Zeichen ________ und Haus ___ und dein MC in Zeichen ________. Was sagen diese drei zusammen über deine tiefste, unverwechselbarste Gabe?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Schaue auf deine Sonne in Zeichen ________ und Haus ___, deinen Chiron in Zeichen ________ und Haus ___ und dein MC in Zeichen ________. Welches deiner Angebote entspricht am vollständigsten dieser Kombination — das Angebot, das sich leicht anfühlt, weil es so nah an deiner Seele ist? Warum ist genau das dein stärkstes?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Was ist das Angebot, das du noch nicht gebaut hast — aber das in dir wartet? Was sagt dein nördlicher Mondknoten in Zeichen ________ und Haus ___ darüber, in welche Richtung du dein Portfolio noch entwickeln sollst?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("8. LEADERSHIP", "Leadership & Team", [
        ("Dein Saturn in Zeichen ________ und Haus ___ und dein Mars in Zeichen ________ und Haus ___ definieren, wie du führst. Was ist dein natürlicher Führungsstil — und wo weicht er von dem ab, was du für \"richtige Führung\" hältst? Was wäre möglich in deinem Team, wenn du vollständig so führst, wie du wirklich bist?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Was ist deine größte Angst als Führungskraft? Schaue auf deinen Mond in Zeichen ________ und Haus ___. Woher kommt diese Angst — und welches alte Muster aus deiner Vergangenheit führst du gerade in deinem Team weiter?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Schaue auf deinen nördlichen Mondknoten in Zeichen ________ und Haus ___ und deinen Jupiter in Zeichen ________ und Haus ___. Beschreibe die Unternehmerin, die du in 3 Jahren bist — durch die Linse dieser beiden Energien: Wie führt sie ihr Team? Welche Entscheidungen trifft sie? Welche Version von dir ist das — und was unterscheidet sie von heute?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("9. NERVENSYSTEM", "Nervensystem & Selbstführung", [
        ("Dein Mond in Zeichen ________ und Haus ___ ist dein emotionales Nervensystem. Was bringt es in Regulation — und was triggert es in Stunden, Tagen, Wochen der Dysregulation? Was ist dein persönliches Regulationsprotokoll als Unternehmerin — das, was dich immer wieder in deine Kraft zurückbringt?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Schaue auf deinen Mond in Zeichen ________ und Haus ___ und deinen Mars in Zeichen ________ und Haus ___. Welche Business-Situationen triggern genau diese Kombination — wann wirst du reaktiv, klein oder überwältigt? Was ist der astrologische Hintergrund — und was hilft dir, in diesen Momenten bei dir zu bleiben?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Schaue auf deinen Mond in Zeichen ________ und Haus ___ und deinen Saturn in Zeichen ________ und Haus ___. Beschreibe dein reguliertes Ich durch diese Energien — wie verkauft sie, wie kommuniziert sie, wie entscheidet sie? Und jetzt das deregulierte Ich: Was verändert sich? Was brauchst du, um öfter die erste Version zu sein?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("10. FEMININE POWER", "Feminine Power & Intuition", [
        ("Dein Neptun in Zeichen ________ und Haus ___ und dein Mond in Zeichen ________ und Haus ___ sind deine intuitive Intelligenz. Wann hat deine Intuition dich zuletzt klar geführt — im Business, in einer Entscheidung, in einem Gespräch? Und wann hast du ihr zuletzt nicht vertraut — und was war die Konsequenz?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Schaue auf deinen Mond in Zeichen ________ und Haus ___, deine Venus in Zeichen ________ und Haus ___ und deinen Neptun in Zeichen ________ und Haus ___. Was sagen diese drei Planeten darüber, was es für dich bedeutet, ein weibliches Business zu führen — mit Zyklen, Intuition, Pausen als Strategie? Was musst du durch diese Energien heilen, um diesen Weg vollständig zu gehen?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Deine Lilith in Zeichen ________ und Haus ___ ist deine rohe feminine Kraft. Wo unterdrückst du diese Energie, weil sie zu viel für den Markt, für dein Team oder für deine Kundinnen sein könnte — und was würde passieren, wenn du sie vollständig zum Ausdruck bringst?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("11. KARMA", "Karma & Business-Lektionen", [
        ("Was ist die tiefste Business-Lektion, die du in diesem Leben lernen sollst? Schaue auf deinen nördlichen Mondknoten in Zeichen ________ und Haus ___ und deinen Saturn in Zeichen ________ und Haus ___. Was wollen diese beiden Energien gemeinsam von dir?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Dein südlicher Mondknoten in Zeichen ________ und Haus ___ zeigt, welche Business-Identitäten du schon lebst — vielleicht aus vergangenen Leben, vielleicht aus deiner Herkunftsfamilie. Was davon dient dir noch — und was hält dich zurück von der Frau, die du werden sollst?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Schaue auf deinen südlichen Mondknoten in Zeichen ________ und Haus ___ und deinen Saturn in Zeichen ________ und Haus ___. Welches Business-Muster wiederholt sich in deinem Leben — immer wieder dieselbe Blockade, dieselbe Situation im neuen Gewand? Was wollen diese beiden Energien dir zeigen — und was verändert sich, wenn du die Lektion endlich annimmst?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("12. TRANSFORMATION", "Transformation & Wachstum", [
        ("Dein Pluto in Zeichen ________ und Haus ___ und dein Chiron in Zeichen ________ und Haus ___ sind deine Transformationsachse. Was ist die Unternehmerin, die du warst — und die du nie wieder sein willst? Was ist durch dich hindurchgegangen, das dich für immer verändert hat?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Schaue auf deinen Pluto in Zeichen ________ und Haus ___ und deinen nördlichen Mondknoten in Zeichen ________ und Haus ___. Welche Transformation liegt vor dir — die, die du schon siehst, aber noch nicht bereit bist zu gehen? Was müsstest du durch diese beiden Energien loslassen — und was wartet auf der anderen Seite?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Schaue auf deinen Pluto in Zeichen ________ und Haus ___ und deinen Chiron in Zeichen ________ und Haus ___. In welchem Bereich deines Business hast du dich durch diese Energien in den letzten 12 Monaten am stärksten transformiert — und was ist der konkrete Beweis? Was ist jetzt möglich, das vorher nicht möglich war?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("13. DEINE STIMME", "Deine Stimme & Content", [
        ("Dein Merkur in Zeichen ________ und Haus ___ ist deine Kommunikationsintelligenz. Was ist deine unverwechselbare Stimme — nicht der Ton, den du für Instagram kultivierst, sondern der, der entsteht, wenn du einfach redest? Was an deiner natürlichen Sprache ist dein größter Content-Vorteil?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Welcher Content kommt dir mühelos — bei dem du vergisst, dass du arbeitest? Was sagt dein Merkur in Zeichen ________ und Haus ___ darüber, welche Content-Formate, Themen und Rhythmen wirklich zu dir passen?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Was ist der Content, den du noch nicht erstellt hast — der, der dir zu roh, zu persönlich, zu direkt erscheint? Was sagt deine Lilith in Zeichen ________ und Haus ___ darüber, welche Wahrheit du noch nicht ausgesprochen hast — und wie viel Kraft in genau diesem Content liegt?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("14. GRENZEN", "Grenzen & Energiemanagement", [
        ("Dein Saturn in Zeichen ________ und Haus ___ ist der Planet der Grenzen. Wo hast du im Business Grenzen gesetzt — und wo sagst du noch immer Ja, obwohl dein Körper, dein Mond, deine Energie Nein sagt? Was kostet dich das wirklich?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Schaue auf deinen Mond in Zeichen ________ und Haus ___ und deinen Mars in Zeichen ________ und Haus ___. Was sagen diese beiden über deinen natürlichen Energie-Rhythmus als Unternehmerin — wann bist du auf dem Höhepunkt, wann brauchst du Rückzug? Wie baut dein aktuelles Business diesen Rhythmus ein — und wo ignorierst du ihn noch?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Schaue auf deinen Mond in Zeichen ________ und Haus ___, deinen Saturn in Zeichen ________ und Haus ___ und deinen Deszendent in Zeichen ________. Welche Kundinnen, Projekte oder Situationen stehen in Konflikt mit diesen Energien — und welche sind in totaler Resonanz? Was ist die Konsequenz für die Struktur deines Business?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("15. ABUNDANCE", "Abundance & Überfluss anziehen", [
        ("Schaue auf deinen Saturn in Zeichen ________ und Haus ___, deinen Pluto in Zeichen ________ und Haus ___ und deine Venus in Zeichen ________ und Haus ___. Was zeigen diese drei über deine tiefste, ungefilterte Überzeugung über Geld? Woher kommt sie — und was müsste sich durch diese Energien in dir verändern, damit Geld natürlich zu dir fließt?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Dein Jupiter in Zeichen ________ und Haus ___ zeigt deinen Überfluss-Kanal. Wenn dieser Kanal vollständig geöffnet wäre — wie viel verdienst du? Wie lebst du? Was gibst du — und was empfängst du? Schreibe diese Version deines Lebens in der Gegenwart.\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Schaue auf deinen Jupiter in Zeichen ________ und Haus ___ und deine Venus in Zeichen ________ und Haus ___. Welche Investition — in dich, dein Business, dein Wachstum — halten diese beiden Energien für dich bereit, die du noch nicht gemacht hast? Was sagt deine Angst davor über deine Beziehung zu deinem eigenen Wert — und was würde die Version von dir tun, die Jupiter und Venus vollständig verkörpert?\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
    ("16. DEIN VERMÄCHTNIS", "Dein Vermächtnis", [
        ("Was will dein MC in Zeichen ________ in die Welt bringen — nicht nur in Form von Umsatz oder Reichweite, sondern als echte Veränderung? Was ist die Transformation, die deine Kundinnen durch dich erfahren — und die über das Programm, den Kurs, das Gespräch hinausgeht?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Schaue auf dein MC in Zeichen ________ und deinen nördlichen Mondknoten in Zeichen ________ und Haus ___. Wenn du in 20 Jahren zurückschaust — was hast du durch diese beiden Energien gebaut, berührt, verändert? Was ist das Vermächtnis, das MC und Mondknoten gemeinsam von dir wollen — und für das es sich lohnt, heute alles zu geben?\nSchreibe auf Deutsch, direkt und konkret.",),
        ("Dein Pluto in Zeichen ________ und Haus ___ ist die Kraft, durch die du andere wirklich transformierst. Welche Frau ist nach der Arbeit mit dir eine andere? Beschreibe sie konkret — was hat sich in ihr verändert, was denkt sie jetzt, wie lebt sie jetzt? Das ist dein wahres Angebot.\nSchreibe auf Deutsch, direkt und konkret.",),
    ]),
]

# ─── DRAWING FUNCTIONS ───────────────────────────────────────────────────────

def draw_bg(c):
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

def draw_border_lines(c):
    c.setStrokeColor(ACCENT_GOLD)
    c.setLineWidth(1.2)
    c.line(1.4*cm, PAGE_H - 1.4*cm, PAGE_W - 1.4*cm, PAGE_H - 1.4*cm)
    c.line(1.4*cm, 1.4*cm, PAGE_W - 1.4*cm, 1.4*cm)

def draw_writing_lines(c, start_y, end_y, n=20):
    c.setStrokeColor(LINE_COLOR)
    c.setLineWidth(0.5)
    gap = (start_y - end_y) / max(n, 1)
    for i in range(n):
        y = start_y - i * gap
        c.line(1.8*cm, y, PAGE_W - 1.8*cm, y)

def draw_cover(c):
    # Dark background
    c.setFillColor(DARK_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Subtle gold top bar
    c.setFillColor(ACCENT_GOLD)
    c.rect(0, PAGE_H - 0.6*cm, PAGE_W, 0.6*cm, fill=1, stroke=0)
    c.rect(0, 0, PAGE_W, 0.6*cm, fill=1, stroke=0)

    # Decorative circle
    c.setStrokeColor(LIGHT_GOLD)
    c.setFillColor(colors.HexColor('#2A1F14'))
    c.setLineWidth(1.0)
    cx, cy = PAGE_W / 2, PAGE_H / 2 + 1.5*cm
    c.circle(cx, cy, 5.5*cm, fill=1, stroke=1)

    # Inner circle
    c.setStrokeColor(ACCENT_GOLD)
    c.setLineWidth(0.5)
    c.circle(cx, cy, 4.8*cm, fill=0, stroke=1)

    # Star symbol in circle
    c.setFont("Times-Roman", 40)
    c.setFillColor(LIGHT_GOLD)
    c.drawCentredString(cx, cy - 0.6*cm, "✦")

    # Title
    c.setFont("Times-Roman", 34)
    c.setFillColor(WHITE)
    c.drawCentredString(PAGE_W/2, PAGE_H/2 - 3.0*cm, "ASTRO WORKBOOK")

    # Subtitle
    c.setFont("Helvetica", 11)
    c.setFillColor(LIGHT_GOLD)
    c.drawCentredString(PAGE_W/2, PAGE_H/2 - 4.2*cm, "Business · Identität · Geldcode · Nervensystem · Leadership")

    # Tagline
    c.setFont("Times-Roman", 13)
    c.setFillColor(colors.HexColor('#9C8C7A'))
    c.drawCentredString(PAGE_W/2, PAGE_H/2 - 5.4*cm, "KI-Prompts für die Horoskop-Analyse")

    # Author line bottom
    c.setFont("Helvetica", 9)
    c.setFillColor(ACCENT_GOLD)
    c.drawCentredString(PAGE_W/2, 2.0*cm, "© PATRYCJA NASRI")

    c.showPage()

def draw_section_divider(c, teil_num, title, subtitle=""):
    c.setFillColor(DARK_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Gold side stripe
    c.setFillColor(ACCENT_GOLD)
    c.rect(0, 0, 0.5*cm, PAGE_H, fill=1, stroke=0)

    # Teil label
    c.setFont("Helvetica", 9)
    c.setFillColor(ACCENT_GOLD)
    c.drawCentredString(PAGE_W/2, PAGE_H/2 + 5.0*cm, f"TEIL {teil_num}")

    # Decorative line
    c.setStrokeColor(ACCENT_GOLD)
    c.setLineWidth(0.8)
    c.line(PAGE_W/2 - 2*cm, PAGE_H/2 + 4.4*cm, PAGE_W/2 + 2*cm, PAGE_H/2 + 4.4*cm)

    # Main title
    c.setFont("Times-Roman", 28)
    c.setFillColor(WHITE)
    c.drawCentredString(PAGE_W/2, PAGE_H/2 + 2.8*cm, title)

    if subtitle:
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.HexColor('#9C8C7A'))
        c.drawCentredString(PAGE_W/2, PAGE_H/2 + 1.6*cm, subtitle)

    c.showPage()

def draw_planet_divider(c, planet_name):
    draw_bg(c)
    draw_border_lines(c)

    # Planet name large centered
    c.setFont("Times-Roman", 9)
    c.setFillColor(ACCENT_GOLD)
    c.drawCentredString(PAGE_W/2, PAGE_H/2 + 2.5*cm, "✦")

    c.setFont("Times-Roman", 32)
    c.setFillColor(HEADING_COLOR)
    c.drawCentredString(PAGE_W/2, PAGE_H/2 + 0.5*cm, planet_name)

    c.setStrokeColor(ACCENT_GOLD)
    c.setLineWidth(0.8)
    c.line(PAGE_W/2 - 3*cm, PAGE_H/2 - 0.8*cm, PAGE_W/2 + 3*cm, PAGE_H/2 - 0.8*cm)

    c.showPage()

def draw_theme_divider(c, num_label, title, subtitle):
    draw_bg(c)
    draw_border_lines(c)

    c.setFont("Helvetica", 9)
    c.setFillColor(ACCENT_GOLD)
    c.drawCentredString(PAGE_W/2, PAGE_H/2 + 3.0*cm, num_label)

    c.setFont("Times-Roman", 26)
    c.setFillColor(HEADING_COLOR)
    c.drawCentredString(PAGE_W/2, PAGE_H/2 + 1.0*cm, title)

    c.setStrokeColor(ACCENT_GOLD)
    c.setLineWidth(0.8)
    c.line(PAGE_W/2 - 3*cm, PAGE_H/2 - 0.2*cm, PAGE_W/2 + 3*cm, PAGE_H/2 - 0.2*cm)

    c.setFont("Helvetica", 11)
    c.setFillColor(MUTED_COLOR)
    c.drawCentredString(PAGE_W/2, PAGE_H/2 - 1.0*cm, subtitle)

    c.showPage()

def wrap_text_to_lines(text, font_name, font_size, max_width, cv):
    """Wrap text into lines that fit max_width."""
    words = text.replace('\n', ' \n ').split(' ')
    lines = []
    current_line = ''
    for word in words:
        if word == '\n':
            lines.append(current_line.strip())
            current_line = ''
            continue
        test_line = (current_line + ' ' + word).strip() if current_line else word
        if cv.stringWidth(test_line, font_name, font_size) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line.strip())
            current_line = word
    if current_line:
        lines.append(current_line.strip())
    return lines

def draw_prompt_page(c, prompt_text, planet_label, page_num):
    draw_bg(c)
    draw_border_lines(c)

    # Planet label top left
    c.setFont("Helvetica", 8)
    c.setFillColor(ACCENT_GOLD)
    c.drawString(1.9*cm, PAGE_H - 2.0*cm, planet_label.upper())

    # Measure text for box
    box_x = 1.8*cm
    box_w = PAGE_W - 3.6*cm
    inner_w = box_w - 2.0*cm
    font_size = 11.5
    line_height = 17

    # Handle italic instruction line (last line starting with "Schreibe")
    parts = prompt_text.rsplit('\n', 1)
    main_text = parts[0]
    instruction = parts[1] if len(parts) > 1 else ""

    main_lines = wrap_text_to_lines(main_text, 'Times-Roman', font_size, inner_w, c)
    instr_lines = wrap_text_to_lines(instruction, 'Helvetica-Oblique', 9.5, inner_w, c) if instruction else []

    total_text_h = (len(main_lines) + len(instr_lines)) * line_height
    if instr_lines:
        total_text_h += 6  # small gap between main and instruction
    box_h = total_text_h + 1.8*cm
    box_top = PAGE_H - 2.8*cm
    box_bottom = box_top - box_h

    # Draw box
    c.setFillColor(BOX_COLOR)
    c.setStrokeColor(BOX_BORDER)
    c.setLineWidth(0.8)
    c.roundRect(box_x, box_bottom, box_w, box_h, 6, fill=1, stroke=1)

    # Draw main text centered in box
    text_x = box_x + 1.0*cm
    text_y_start = box_top - 0.9*cm

    c.setFillColor(TEXT_COLOR)
    for i, line in enumerate(main_lines):
        y = text_y_start - i * line_height
        c.setFont('Times-Roman', font_size)
        # Center each line
        line_w = c.stringWidth(line, 'Times-Roman', font_size)
        x = box_x + (box_w - line_w) / 2
        c.drawString(x, y, line)

    if instr_lines:
        c.setFillColor(MUTED_COLOR)
        offset = len(main_lines) * line_height + 6
        for i, line in enumerate(instr_lines):
            y = text_y_start - offset - i * line_height
            c.setFont('Helvetica-Oblique', 9.5)
            line_w = c.stringWidth(line, 'Helvetica-Oblique', 9.5)
            x = box_x + (box_w - line_w) / 2
            c.drawString(x, y, line)

    # Writing lines
    lines_start = box_bottom - 1.3*cm
    lines_end = 2.5*cm
    n_lines = max(int((lines_start - lines_end) / 13), 10)
    draw_writing_lines(c, lines_start, lines_end, n_lines)

    # Page number
    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED_COLOR)
    c.drawCentredString(PAGE_W/2, 1.0*cm, str(page_num))

    c.showPage()


def draw_legal_page(c):
    """Rechtliche Hinweisseite — letzte Seite des Workbooks."""
    # Dark background wie Cover
    c.setFillColor(DARK_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Gold top + bottom bar
    c.setFillColor(ACCENT_GOLD)
    c.rect(0, PAGE_H - 0.6*cm, PAGE_W, 0.6*cm, fill=1, stroke=0)
    c.rect(0, 0, PAGE_W, 0.6*cm, fill=1, stroke=0)

    # Dekoratives Symbol oben
    c.setFont("Times-Roman", 22)
    c.setFillColor(LIGHT_GOLD)
    c.drawCentredString(PAGE_W/2, PAGE_H - 3.2*cm, "✦")

    # Haupttitel
    c.setFont("Times-Roman", 18)
    c.setFillColor(WHITE)
    c.drawCentredString(PAGE_W/2, PAGE_H - 4.5*cm, "RECHTLICHE HINWEISE")

    # Goldene Trennlinie
    c.setStrokeColor(ACCENT_GOLD)
    c.setLineWidth(0.8)
    c.line(PAGE_W/2 - 4*cm, PAGE_H - 5.1*cm, PAGE_W/2 + 4*cm, PAGE_H - 5.1*cm)

    # Textblock — zentriert, mehrzeilig
    legal_lines = [
        ("Patrycja Nasri  |  Alle Rechte vorbehalten.", "Helvetica-Bold", 10, WHITE),
        ("", "Helvetica", 9, WHITE),
        ("Dieses Workbook und alle enthaltenen Inhalte, Texte und Designs", "Helvetica", 9, colors.HexColor('#C8B89A')),
        ("unterliegen dem Urheberrecht.", "Helvetica", 9, colors.HexColor('#C8B89A')),
        ("", "Helvetica", 9, WHITE),
        ("Jede Vervielfältigung, Verbreitung oder Weitergabe —", "Helvetica", 9, colors.HexColor('#C8B89A')),
        ("auch auszugsweise — ist ohne ausdrückliche schriftliche", "Helvetica", 9, colors.HexColor('#C8B89A')),
        ("Genehmigung von Patrycja Nasri nicht gestattet.", "Helvetica", 9, colors.HexColor('#C8B89A')),
        ("", "Helvetica", 9, WHITE),
        ("Dieses Workbook ist ausschließlich im Rahmen des Kurses", "Helvetica-Bold", 9.5, LIGHT_GOLD),
        ("DEIN ASTROCODE", "Times-Roman", 13, LIGHT_GOLD),
        ("erhältlich und für den persönlichen Gebrauch bestimmt.", "Helvetica-Bold", 9.5, LIGHT_GOLD),
        ("", "Helvetica", 9, WHITE),
        ("Eine private Nutzung — einschließlich des Ausdrucks für den", "Helvetica", 9, colors.HexColor('#C8B89A')),
        ("eigenen Gebrauch — ist ausdrücklich gestattet.", "Helvetica", 9, colors.HexColor('#C8B89A')),
        ("Eine Weitergabe an Dritte ist nicht erlaubt.", "Helvetica", 9, colors.HexColor('#C8B89A')),
        ("", "Helvetica", 9, WHITE),
        ("Design by Patricia — Visual Venus Design", "Helvetica-Oblique", 9, colors.HexColor('#8B7355')),
        ("", "Helvetica", 9, WHITE),
        ("www.patrycja-nasri.de", "Helvetica-Bold", 9.5, LIGHT_GOLD),
    ]

    start_y = PAGE_H - 6.2*cm
    line_h = 16

    for text, font, size, color in legal_lines:
        if text == "":
            start_y -= line_h * 0.4
            continue
        c.setFont(font, size)
        c.setFillColor(color)
        c.drawCentredString(PAGE_W/2, start_y, text)
        start_y -= line_h

    # Untere Goldlinie
    c.setStrokeColor(ACCENT_GOLD)
    c.setLineWidth(0.8)
    c.line(PAGE_W/2 - 4*cm, 3.5*cm, PAGE_W/2 + 4*cm, 3.5*cm)

    # Copyright unten
    c.setFont("Helvetica", 8)
    c.setFillColor(ACCENT_GOLD)
    c.drawCentredString(PAGE_W/2, 2.8*cm, "© 2026 Patrycja Nasri  |  www.patrycja-nasri.de")

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor('#6B5B4E'))
    c.drawCentredString(PAGE_W/2, 2.2*cm, "Unbefugte Nutzung wird rechtlich verfolgt.")

    # Kontakt & Website
    c.setFont("Helvetica", 8.5)
    c.setFillColor(LIGHT_GOLD)
    c.drawCentredString(PAGE_W/2, 1.6*cm, "info@patrycja-nasri.de  |  www.patrycja-nasri.de")

    c.showPage()


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    output_path = "/Users/patrycjakaczorowska/Downloads/Vorlagen/claude-workspace-vorlage/outputs/astro-workbook-prompt-sammlung-2026-05-27.pdf"
    c = canvas.Canvas(output_path, pagesize=A4)

    # 1. Cover
    draw_cover(c)

    # 2. Teil 1 Section divider
    draw_section_divider(c, "1", "PLANETEN-PROMPTS",
                         "Die Bausteine deines kosmischen Business-Codes")

    # 3. Teil 1 pages
    page_num = 3
    for planet, prompts in TEIL1_PROMPTS:
        draw_planet_divider(c, planet)
        page_num += 1
        for (prompt_text,) in prompts:
            draw_prompt_page(c, prompt_text, planet, page_num)
            page_num += 1

    # 4. Teil 2 Section divider
    draw_section_divider(c, "2", "THEMATISCHE TIEFENPROMPTS",
                         "Deine Kernthemen — Business, Geld, Identität, Leadership")
    page_num += 1

    # 5. Teil 2 pages
    for num_label, subtitle, prompts in TEIL2_PROMPTS:
        draw_theme_divider(c, num_label, subtitle, "")
        page_num += 1
        for (prompt_text,) in prompts:
            draw_prompt_page(c, prompt_text, num_label, page_num)
            page_num += 1

    # 6. Rechtliche Seite
    draw_legal_page(c)

    c.save()
    print(f"PDF erstellt: {output_path}")
    print(f"Seiten: ~{page_num + 1}")


if __name__ == "__main__":
    main()
