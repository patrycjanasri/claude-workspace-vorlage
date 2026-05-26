#!/usr/bin/env python3
"""Steuerleitfaden Network Marketing — sauberes PDF via ReportLab."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

OUTPUT = "/Users/patrycjakaczorowska/Downloads/Vorlagen/claude-workspace-vorlage/outputs/steuerleitfaden-network-marketing.pdf"

# ── Farben ─────────────────────────────────────────────────────────────────────
GOLD    = HexColor('#C9A05A')
DUNKEL  = HexColor('#1A1A2E')
MITTEL  = HexColor('#3A3A5C')
HELL    = HexColor('#F7F5F0')
CREME   = HexColor('#F5F0E8')
GRAU    = HexColor('#6B6B6B')
HELLGRAU= HexColor('#F0F0F0')
ROT_BG  = HexColor('#FFF0F0')
BLAU_BG = HexColor('#EEF4FB')
ROT_RND = HexColor('#CC4444')
BLAU_RND= HexColor('#3A3A5C')
TABELLEZEILE_A = HexColor('#FAFAF7')
TABELLEZEILE_B = HexColor('#F2EDE5')
TABELLE_KOPF   = HexColor('#1A1A2E')

# ── Seitenmaße ──────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN_L = 3.0 * cm
MARGIN_R = 2.5 * cm
MARGIN_T = 2.5 * cm
MARGIN_B = 2.5 * cm
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

# ── Styles ─────────────────────────────────────────────────────────────────────
def make_styles():
    s = {}
    base = dict(fontName='Helvetica', fontSize=11, leading=16,
                textColor=DUNKEL, spaceAfter=4)

    s['title'] = ParagraphStyle('title', fontSize=28, fontName='Helvetica-Bold',
        textColor=DUNKEL, spaceAfter=4, spaceBefore=0, leading=34)
    s['subtitle'] = ParagraphStyle('subtitle', fontSize=16, fontName='Helvetica',
        textColor=GOLD, spaceAfter=4, spaceBefore=0, leading=22)
    s['tagline'] = ParagraphStyle('tagline', fontSize=12, fontName='Helvetica',
        textColor=GRAU, spaceAfter=16, spaceBefore=0, leading=16)
    s['h1'] = ParagraphStyle('h1', fontSize=14, fontName='Helvetica-Bold',
        textColor=DUNKEL, spaceAfter=6, spaceBefore=18, leading=20)
    s['h2'] = ParagraphStyle('h2', fontSize=11.5, fontName='Helvetica-Bold',
        textColor=MITTEL, spaceAfter=4, spaceBefore=10, leading=16)
    s['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=11,
        textColor=DUNKEL, spaceAfter=6, leading=17, alignment=TA_JUSTIFY)
    s['bullet'] = ParagraphStyle('bullet', fontName='Helvetica', fontSize=11,
        textColor=DUNKEL, spaceAfter=2, spaceBefore=1, leading=16,
        leftIndent=14, firstLineIndent=0)
    s['italic'] = ParagraphStyle('italic', fontName='Helvetica-Oblique', fontSize=10,
        textColor=GRAU, spaceAfter=6, leading=15, alignment=TA_JUSTIFY)
    s['small'] = ParagraphStyle('small', fontName='Helvetica', fontSize=9,
        textColor=GRAU, spaceAfter=2, leading=13)
    s['cell'] = ParagraphStyle('cell', fontName='Helvetica', fontSize=10,
        textColor=DUNKEL, leading=15, spaceAfter=0)
    s['cell_bold'] = ParagraphStyle('cell_bold', fontName='Helvetica-Bold', fontSize=10,
        textColor=DUNKEL, leading=15, spaceAfter=0)
    s['cell_header'] = ParagraphStyle('cell_header', fontName='Helvetica-Bold', fontSize=10,
        textColor=white, leading=15, spaceAfter=0)
    s['hint_title'] = ParagraphStyle('hint_title', fontName='Helvetica-Bold', fontSize=10.5,
        textColor=MITTEL, spaceAfter=3, leading=15)
    s['hint_body'] = ParagraphStyle('hint_body', fontName='Helvetica', fontSize=10,
        textColor=DUNKEL, spaceAfter=0, leading=15)
    s['hint_body_dark'] = ParagraphStyle('hint_body_dark', fontName='Helvetica', fontSize=10,
        textColor=white, spaceAfter=0, leading=15)
    s['checklist'] = ParagraphStyle('checklist', fontName='Helvetica', fontSize=11,
        textColor=DUNKEL, spaceAfter=2, spaceBefore=1, leading=16, leftIndent=4)
    return s

ST = make_styles()

# ── Hilfsfunktionen ────────────────────────────────────────────────────────────

def sp(n=6): return Spacer(1, n)

def hr_gold(): return HRFlowable(width=CONTENT_W, thickness=2, color=GOLD,
                                  spaceAfter=4, spaceBefore=4)

def hr_thin(): return HRFlowable(width=CONTENT_W, thickness=0.5, color=GOLD,
                                  spaceAfter=8, spaceBefore=2)

def h1(text):
    """Kapitelüberschrift mit goldener Linie davor."""
    return [hr_gold(),
            Paragraph(text, ST['h1'])]

def h2(text): return Paragraph(text, ST['h2'])

def body(text): return Paragraph(text, ST['body'])

def bullet(text): return Paragraph(f'• {text}', ST['bullet'])

def sub_bullet(text): return Paragraph(f'  – {text}', ST['bullet'])

def hint_box(title, text, bg=CREME, border_color=GOLD, dark=False):
    """Farbige Info-Box mit linker Akzentlinie."""
    txt_style = ST['hint_body_dark'] if dark else ST['hint_body']
    ttl_style = ParagraphStyle('ht', fontName='Helvetica-Bold', fontSize=10.5,
        textColor=white if dark else MITTEL, spaceAfter=3, leading=15)
    rows = []
    if title:
        rows.append([Paragraph(title, ttl_style)])
    # Text kann Newlines enthalten
    for line in text.split('\n'):
        rows.append([Paragraph(line or ' ', txt_style)])
    inner = Table([[r[0]] for r in rows], colWidths=[CONTENT_W - 1.2*cm])
    inner.setStyle(TableStyle([
        ('BACKGROUND',  (0,0), (-1,-1), bg),
        ('LEFTPADDING',  (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING',   (0,0), (0, 0), 10),
        ('BOTTOMPADDING',(0,-1),(-1,-1), 10),
        ('TOPPADDING',   (0,1), (-1,-1), 2),
        ('VALIGN',       (0,0), (-1,-1), 'TOP'),
    ]))
    # Wrapper-Tabelle mit linkem Farbstreifen
    wrapper = Table([[None, inner]], colWidths=[4, CONTENT_W - 4])
    wrapper.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (0,-1), border_color),
        ('BACKGROUND',   (1,0), (1,-1), bg),
        ('LEFTPADDING',  (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING',   (0,0), (-1,-1), 0),
        ('BOTTOMPADDING',(0,0), (-1,-1), 0),
        ('VALIGN',       (0,0), (-1,-1), 'TOP'),
    ]))
    return [wrapper, sp(8)]

def two_col_table(rows_data, header=None, col_w=(5.5*cm, None)):
    """Zweispaltige Tabelle mit alternierenden Zeilen."""
    cw1 = col_w[0]
    cw2 = CONTENT_W - cw1
    ts = [
        ('LEFTPADDING',  (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING',   (0,0), (-1,-1), 6),
        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
        ('VALIGN',       (0,0), (-1,-1), 'TOP'),
        ('GRID',         (0,0), (-1,-1), 0.5, HexColor('#E0D8CC')),
    ]
    table_rows = []
    offset = 0
    if header:
        table_rows.append([
            Paragraph(header[0], ST['cell_header']),
            Paragraph(header[1], ST['cell_header']),
        ])
        ts += [
            ('BACKGROUND', (0,0), (-1,0), TABELLE_KOPF),
            ('TEXTCOLOR',  (0,0), (-1,0), white),
        ]
        offset = 1
    for i, (left, right) in enumerate(rows_data):
        bg = TABELLEZEILE_A if i % 2 == 0 else TABELLEZEILE_B
        ts.append(('BACKGROUND', (0, offset+i), (-1, offset+i), bg))
        table_rows.append([
            Paragraph(left,  ST['cell_bold']),
            Paragraph(right, ST['cell']),
        ])
    t = Table(table_rows, colWidths=[cw1, cw2])
    t.setStyle(TableStyle(ts))
    return [t, sp(8)]

def checklist_item(text):
    return Paragraph(f'☐ {text}', ST['checklist'])

# ── Header/Footer ──────────────────────────────────────────────────────────────
def draw_header_footer(canvas, doc):
    canvas.saveState()
    # Footer: goldene Linie + Text
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1)
    canvas.line(MARGIN_L, MARGIN_B - 4*mm, PAGE_W - MARGIN_R, MARGIN_B - 4*mm)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(GRAU)
    canvas.drawString(MARGIN_L, MARGIN_B - 9*mm,
        'Steuerleitfaden Network Marketing & MONAT · Kein Ersatz für individuelle Steuerberatung')
    canvas.drawRightString(PAGE_W - MARGIN_R, MARGIN_B - 9*mm,
        f'Seite {doc.page}')
    canvas.restoreState()

# ══════════════════════════════════════════════════════════════════════════════
# INHALT AUFBAUEN
# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── TITELBEREICH ───────────────────────────────────────────────────────────────
story += [
    HRFlowable(width=CONTENT_W, thickness=3, color=GOLD,
               spaceAfter=14, spaceBefore=0),
    Paragraph('STEUERLEITFADEN', ST['title']),
    Paragraph('Network Marketing &amp; MONAT', ST['subtitle']),
    Paragraph('Steuerliche Grundlagen für Partnerinnen in Deutschland', ST['tagline']),
]
story += hint_box(
    'Expertin: Nancy Wackerhagen',
    'Steuerfachwirtin (seit 2003)  ·  Steuerberaterin (seit 2010)\n'
    'Geschäftsführerin einer Kanzlei mit 6 Niederlassungen und 60 Mitarbeitern.',
    bg=DUNKEL, border_color=GOLD, dark=True
)
story += [
    HRFlowable(width=CONTENT_W, thickness=0.8, color=GOLD,
               spaceAfter=6, spaceBefore=4),
    Paragraph(
        'Dieser Leitfaden fasst die wichtigsten Inhalte des Steuer-Calls zusammen. '
        'Er ersetzt keine individuelle steuerrechtliche Beratung.',
        ST['italic']
    ),
    sp(12),
]

# ── 01 STATUS ALS UNTERNEHMERIN ────────────────────────────────────────────────
story += h1('01  Dein Status als Unternehmerin')
story += [
    body('Als MONAT-Partnerin bist du rechtlich gesehen Unternehmerin — unabhängig davon, '
         'ob du ein Gewerbe im Haupt- oder Nebenerwerb angemeldet hast oder ob du als '
         'Kleinunternehmerin oder mit Umsatzsteuerpflicht tätig bist.'),
    sp(6),
]
story += two_col_table([
    ('Nebenerwerb',
     'Du hast zusätzlich einen Angestelltenjob. Du bleibst über deinen Arbeitgeber '
     'krankenversichert, solange dein Angestelltengehalt höher ist als dein Gewinn aus dem Business.'),
    ('Haupterwerb',
     'MONAT ist deine einzige oder primäre Einkommensquelle. Du bist für deine '
     'Krankenversicherung selbst zuständig.'),
], header=('Beschäftigungsform', 'Was das bedeutet'))
story += hint_box(
    'Wichtig: Krankenversicherung',
    'Die Krankenkasse prüft immer den Gewinn (nicht den Umsatz!). Übersteigt dein Gewinn '
    'aus MONAT dein Angestelltengehalt, wird der KV-Beitrag auf Basis des Gewinns neu '
    'berechnet — auch wenn du formal im Nebenerwerb bist.',
    bg=CREME, border_color=GOLD
)

# ── 02 B2B-UMSATZ ─────────────────────────────────────────────────────────────
story += h1('02  B2B-Umsatz &amp; MONAT: Die Besonderheit')
story += [
    body('MONAT hat seinen Sitz in Irland. Das ist steuerrechtlich entscheidend, '
         'denn der "Ort der sonstigen Leistung" bei zwei Unternehmern (B2B) liegt immer '
         'dort, wo der Leistungsempfänger seinen Sitz hat.'),
    sp(6),
]
story += two_col_table([
    ('Leistende',          'Du — die MONAT-Partnerin in Deutschland'),
    ('Leistungsempfänger', 'MONAT Global — Sitz in Irland (EU)'),
    ('Art der Leistung',   'Vermittlung (sonstige Leistung im B2B-Bereich)'),
    ('Ort der Leistung',   'Irland — dort, wo MONAT sitzt'),
    ('Folge',              'Der Umsatz ist in Deutschland NICHT steuerbar. Die Umsatzsteuerpflicht verlagert sich nach Irland.'),
], header=('Begriff', 'In deinem Fall'))
story += hint_box(
    'Das bedeutet für dich',
    'Deine Provisionsabrechnung ist immer NETTO — du weist keine deutsche Umsatzsteuer aus. '
    'MONAT führt die Umsatzsteuer in Irland ab. Das Verfahren heißt: Reverse-Charge (§13b UStG).',
    bg=BLAU_BG, border_color=BLAU_RND
)

# ── 03 UST-IDNR ──────────────────────────────────────────────────────────────
story += h1('03  Die Umsatzsteuer-Identifikationsnummer (USt-IdNr.)')
story += [
    body('Für EU-weite B2B-Umsätze braucht JEDE Partnerin eine USt-IdNr. — auch '
         'Kleinunternehmerinnen. Ohne diese Nummer ist das Reverse-Charge-Verfahren '
         'nicht anwendbar und die Rechnung gilt als unvollständig.'),
    sp(4),
    h2('So beantragst du die USt-IdNr.'),
    bullet('Neu-Anmeldung: Im Eröffnungsfragebogen des Finanzamts das entsprechende Kreuz anklicken.'),
    bullet('Nachträgliche Beantragung: Direkt beim Bundeszentralamt für Steuern in Saarlouis — auch elektronisch möglich (ca. 1 Woche Bearbeitungszeit).'),
    bullet('Alternativ: Über den Steuerberater beantragen lassen.'),
    sp(6),
]
story += hint_box(
    None,
    '\U0001f511  Deine USt-IdNr. beginnt mit "DE" + 8 Stellen (z.B. DE123456789). '
    'Die USt-IdNr. von MONAT (Irland) beginnt mit "IE". '
    'Jede EU-USt-IdNr. lässt sich kostenlos verifizieren: vies.ec.europa.eu',
    bg=CREME, border_color=GOLD
)
story += hint_box(
    'Gilt nur in der EU!',
    'Die USt-IdNr. gilt ausschließlich innerhalb der Europäischen Union. '
    'Für Networks mit Sitz in der Schweiz, den USA oder anderen Drittländern gelten '
    'andere Regeln — Einzelfallprüfung mit dem Steuerberater notwendig.',
    bg=ROT_BG, border_color=ROT_RND
)

# ── 04 REVERSE CHARGE ────────────────────────────────────────────────────────
story += h1('04  Das Reverse-Charge-Verfahren (§13b UStG)')
story += [
    body('Bei grenzüberschreitenden B2B-Leistungen innerhalb der EU geht die '
         'Steuerschuldnerschaft auf den Leistungsempfänger über — in diesem Fall auf MONAT. '
         'Das nennt man Reverse Charge.'),
    sp(4),
    h2('Was das praktisch bedeutet'),
    bullet('Du stellst deine Rechnung netto aus (0% Umsatzsteuer).'),
    bullet('MONAT meldet und zahlt die Umsatzsteuer in Irland.'),
    bullet('MONAT kann die Umsatzsteuer als Vorsteuer zurückholen — deshalb ist die Abrechnung immer netto.'),
    bullet('Erhältst du 1.000 € Provision, sind das 1.000 € — nicht 1.190 €.'),
    sp(6),
    h2('Pflichtangabe auf jeder Rechnung/Abrechnung'),
]
story += hint_box(
    None,
    '"Steuerschuldnerschaft geht auf den Leistungsempfänger über" (Hinweis nach §13b UStG)',
    bg=CREME, border_color=GOLD
)

# ── 05 PROVISIONSABRECHNUNG ──────────────────────────────────────────────────
story += h1('05  Deine Provisionsabrechnung')
story += [
    body('MONAT erstellt für jede Auszahlung automatisch eine Gutschrift — diese gilt als '
         'deine Rechnung. Das Template ist steuerrechtlich geprüft und enthält bereits alle '
         'Pflichtangaben. Zu finden: MONAT-Archiv unter Business-Infos / Onboarding.'),
    sp(4),
    h2('Pflichtangaben auf der Abrechnung'),
]
story += two_col_table([
    ('Leistende & Empfänger',  'Dein Name / Firma + MONAT Ireland'),
    ('Rechnungsnummer',        'Nummer der Gutschrift = deine Rechnungsnummer'),
    ('Datum',                  'Ausstellungsdatum der Abrechnung'),
    ('Leistungsbeschreibung',  'Vermittlung von Kundinnen und Partnerinnen'),
    ('Leistungszeitraum',      'z.B. 01.01.2026 – 31.01.2026'),
    ('Nettobetrag',            'Der Provisionsbetrag ohne Umsatzsteuer'),
    ('Umsatzsteuer',           '0 € / 0 % — mit Hinweis auf §13b UStG'),
    ('USt-IdNr. beider Parteien', 'Deine DE... und MONATs IE...-Nummer'),
], header=('Pflichtangabe', 'In deiner Abrechnung'))
story += [
    h2('Empfohlene Vorgehensweise'),
    bullet('Erstelle eine monatliche Zusammenfassung aller Provisionen (MONAT zahlt wöchentlich + monatlich zum 15.).'),
    bullet('Trage den Gesamtbetrag pro Monat in die Excel-Vorlage von MONAT ein.'),
    bullet('Speichere alles als PDF ab und hefte alle Original-Abrechnungen dahinter.'),
    bullet('Schicke die komplette Zusammenfassung monatlich an deinen Steuerberater.'),
    sp(6),
]
story += hint_box(
    'Warum monatlich?',
    'Monatliche Abrechnungen geben dir einen klaren Überblick — und helfen dir frühzeitig '
    'zu erkennen, ob du Rücklagen für Steuerzahlungen bilden musst.',
    bg=CREME, border_color=GOLD
)

# ── 06 ZUSAMMENFASSENDE MELDUNG ──────────────────────────────────────────────
story += h1('06  Die Zusammenfassende Meldung (ZM)')
story += [
    body('Zusätzlich zur Umsatzsteuervoranmeldung muss eine Zusammenfassende Meldung (ZM) '
         'eingereicht werden. Sie dokumentiert deine EU-grenzüberschreitenden Umsätze '
         'gegenüber dem deutschen Fiskus.'),
    sp(6),
]
story += two_col_table([
    ('Was wird gemeldet?', 'Deine USt-IdNr., MONATs USt-IdNr. und die Gesamtsumme der Umsätze im Meldezeitraum'),
    ('Turnus',             'Meistens quartalsweise — gleicher Turnus wie die Umsatzsteuervoranmeldung'),
    ('Betrag',             'Nur Meldepflicht — KEINE Zahlung. Die Summe muss mit der Voranmeldung übereinstimmen.'),
    ('Einreichung',        'Zeitgleich mit der Umsatzsteuervoranmeldung'),
    ('Aufwand',            'Beim Steuerberater wird sie automatisch erstellt und übermittelt. Auch selbst möglich.'),
], header=('Frage', 'Antwort'))

# ── 07 KLEINUNTERNEHMERIN ────────────────────────────────────────────────────
story += h1('07  Kleinunternehmerin oder Umsatzsteuerpflichtig?')
story += [
    body('Diese Entscheidung triffst du bei der Gewerbeanmeldung. Für MONAT-Partnerinnen '
         'gibt es eine wichtige Besonderheit bei der 25.000-€-Grenze.'),
    sp(4),
    h2('Kleinunternehmerregelung (§19 UStG) — Die Fakten'),
]
story += two_col_table([
    ('Grenze laufendes Jahr', '25.000 € Umsatz im INLAND'),
    ('Grenze Folgejahr',      '100.000 € Gesamtumsatz im laufenden Jahr'),
    ('Maßstab',               'Immer UMSATZ — nicht Gewinn!'),
    ('MONAT-Besonderheit',    'Dein MONAT-Umsatz wird in IRLAND erbracht → zählt NICHT zum deutschen Inlandsumsatz!'),
    ('Folge',                 'Auch mit 50.000 € MONAT-Provision bist du ggf. noch Kleinunternehmerin (wenn kein anderes Inlandsgewerbe über 25.000 €).'),
], header=('Regelung', 'Details'))
story += hint_box(
    None,
    '→  Klare Empfehlung: Direkt umsatzsteuerpflichtig wählen!\n\n'
    'Als Umsatzsteuerpflichtige zahlst du keine deutsche Umsatzsteuer auf MONAT-Provisionen '
    '(Umsatz liegt in Irland). Gleichzeitig bekommst du aus ALLEN Betriebsausgaben die '
    'Vorsteuer zurück. Als Kleinunternehmerin verlierst du diesen Vorteil komplett.',
    bg=BLAU_BG, border_color=BLAU_RND
)
story += [
    h2('Wechsel ist möglich'),
    bullet('Einfacher Zweizeiler ans Finanzamt: "Ich möchte ab sofort der Umsatzsteuerpflicht unterliegen."'),
    bullet('Das Finanzamt bestätigt und setzt den Turnus für die Voranmeldung (meistens quartalsweise).'),
    bullet('Als Umsatzsteuerpflichtige bekommst du pro Quartal eine Erstattung (Umsatz steuerfrei, Vorsteuer aus Kosten wird erstattet).'),
    sp(6),
]

# ── 08 BETRIEBSAUSGABEN ──────────────────────────────────────────────────────
story += h1('08  Was kannst du absetzen? Betriebsausgaben &amp; Vorsteuer')
story += [
    body('Als Unternehmerin kannst du alle Kosten absetzen, die der "Sicherung und Erhaltung '
         'der Einnahmen" dienen. Es gibt keine vorgeschriebene Höhe — aber: alle Belege aufheben!'),
    sp(4),
    h2('Abzugsfähige Betriebsausgaben (Auswahl)'),
]
story += two_col_table([
    ('Weiterbildung & Seminare',  'Vollständig absetzbar (Kurse, Bücher, Coachings)'),
    ('Telefon & Internet',        'Anteilig oder vollständig absetzbar'),
    ('Hardware',                  'Laptop, Handy, Headset — vollständig absetzbar'),
    ('Reisekosten',               '30 Cent/km (Auto) oder tatsächliche Kosten (Zug, Flug, Taxi) — auch Anfahrt zum Flughafen'),
    ('Business-Events & Trips',   'Hotel, Unterkunft, Verpflegung — vollständig absetzbar'),
    ('Teamgeschenke',             'z.B. bei Rang-Erreichen — vollständig absetzbar (mit Beleg)'),
    ('Bewirtungskosten',          '70% absetzbar. Pflicht: Anlass + Namen der bewirteten Personen auf dem Beleg.'),
    ('Vorführprodukte (MONAT)',   'Demo-Produkte vollständig absetzbar. Von deutschen Rechnungen 19% Vorsteuer zurückfordern!'),
    ('Home-Party',                'Einkäufe, Getränke, Deko — absetzbar mit Dokumentation: Wann? Wer eingeladen?'),
    ('Steuerberatungskosten',     'Vollständig absetzbar'),
    ('Branding & Design',         'Logo, Grafiken, Website-Design — vollständig absetzbar'),
    ('Assistenz & Aushilfen',     'Lohnkosten für Mitarbeiterinnen — vollständig absetzbar'),
], header=('Kostenart', 'Regelung'))
story += hint_box(
    'MONAT-Produkte aus Deutschland: Vorsteuer zurückfordern!',
    'Da MONAT Produkte von einer deutschen Adresse liefert, enthalten die Rechnungen 19% USt. '
    'Als umsatzsteuerpflichtige Unternehmerin kannst du diese Vorsteuer vollständig zurückfordern — '
    'vorausgesetzt, die Produkte dienen dem Business (z.B. als Vorführware).',
    bg=BLAU_BG, border_color=BLAU_RND
)
story += hint_box(
    None,
    '📎  Wer schreibt, der bleibt. Dokumentiere bei jedem Beleg:\n'
    '• Datum · Was wurde gekauft? · Business-Zweck\n'
    '• Bei Bewirtung: wer war dabei?\n\n'
    'Belege monatlich scannen — nicht alles auf Jahresende schieben!',
    bg=CREME, border_color=GOLD
)

# ── 09 FRISTEN ───────────────────────────────────────────────────────────────
story += h1('09  Steuererklärungen &amp; Fristen im Überblick')
story += two_col_table([
    ('Einkommensteuererklärung',
     'Einmal jährlich — alle Einkünfte (Lohn + MONAT + sonstige). Abgabefrist: 31.07. des Folgejahres (ohne steuerliche Vertretung).'),
    ('Umsatzsteuervoranmeldung',
     'Quartalsweise (bei Gewerbestart). Enthält Spalte für Irland-Umsätze. Ergebnis: Erstattung, da Umsatz steuerfrei, Vorsteuer aus Kosten wird erstattet.'),
    ('Umsatzsteuerjahreserklärung',
     'Einmal jährlich — muss jeder Unternehmer abgeben.'),
    ('Zusammenfassende Meldung (ZM)',
     'Quartalsweise, zeitgleich mit der Voranmeldung. Nur Meldung, keine Zahlung.'),
    ('Gewerbesteuererklärung',
     'Fällig wenn Gewinn > 24.500 € (Freibetrag Einzelunternehmen). ACHTUNG: Keine Ratenzahlung möglich!'),
], header=('Erklärungsart', 'Details & Besonderheiten'), col_w=(5.0*cm, None))
story += hint_box(
    'Gewerbesteuer: Gewinn, nicht Umsatz!',
    'Die Gewerbesteuer fällt erst an, wenn dein GEWINN — also was nach Abzug aller '
    'Betriebsausgaben übrig bleibt — den Freibetrag von 24.500 € übersteigt.',
    bg=ROT_BG, border_color=ROT_RND
)

# ── 10 RÜCKLAGEN ─────────────────────────────────────────────────────────────
story += h1('10  Rücklagen bilden &amp; finanziell planen')
story += [
    body('Als Unternehmerin gibt es keine automatischen Steuerabzüge. Du trägst die volle '
         'Verantwortung — das ist dein größter Vorteil und deine wichtigste Pflicht.'),
    sp(4),
]
story += hint_box(
    None,
    '💡  Daumenregel: Lege ca. 1/3 deines Gewinns als Steuerrücklage zurück. '
    'Das schützt vor unangenehmen Überraschungen bei der Jahressteuererklärung.',
    bg=CREME, border_color=GOLD
)
story += [
    h2('Praktische Maßnahmen'),
    bullet('Monatlicher Kassensturz: Einnahmen vs. Ausgaben — wie viel bleibt wirklich übrig?'),
    bullet('Vorauszahlungen anpassen: Steuervorauszahlungen können jederzeit nach oben oder unten angepasst werden.'),
    bullet('Verlustjahre nutzen: Verluste können ins Folgejahr übertragen oder ins Vorjahr zurückgetragen werden.'),
    bullet('Krankenkasse: Die KK passt Beiträge nach letztem Steuerbescheid an — proaktiv kommunizieren.'),
    bullet('Buchhaltungs-App: Belege direkt scannen und digital archivieren — monatlich, nicht jährlich.'),
    sp(8),
]

# ── 11 HÄUFIGE FEHLER ────────────────────────────────────────────────────────
story += h1('11  Häufige Fehler &amp; Was tun wenn ...')
story += two_col_table([
    ('Versehentlich Umsatzsteuer abgeführt (ohne Reverse Charge)',
     'Solange der Bescheid noch nicht bestandskräftig ist (Einspruchsfrist: 1 Monat), kann korrigiert werden. Sofort Steuerberaterin kontaktieren und Irland-Umsatz nachweisen.'),
    ('Noch keine USt-IdNr.',
     'Sofort beim Bundeszentralamt für Steuern in Saarlouis online beantragen. Ca. 1 Woche Bearbeitungszeit. Rückwirkende Beantragung möglich.'),
    ('Seit Jahren Kleinunternehmerin',
     'Wechsel zur Umsatzsteuerpflicht ist jederzeit möglich — Zweizeiler ans Finanzamt. Bereits verlorene Vorsteuer ist in den meisten Fällen nicht mehr rückforderbar.'),
    ('Steuererklärungen nicht abgegeben',
     'Unbedingt nachreichen! Steuerberater beauftragen. Das Finanzamt schätzt sonst. Ratenzahlungen können beantragt werden.'),
    ('Steuerberater kennt MONAT / Reverse Charge nicht',
     'Provisionsabrechnungen vorlegen und diesen Leitfaden mitbringen. Ggf. spezialisierte Beraterin suchen.'),
], header=('Situation', 'Lösung'), col_w=(5.0*cm, None))

# ── 12 CHECKLISTE ────────────────────────────────────────────────────────────
story += h1('12  Deine Checkliste')
story += [
    body('Hake Schritt für Schritt ab — so bist du steuerlich auf der sicheren Seite.'),
    sp(4),
    h2('Setup & Anmeldung'),
    checklist_item('Gewerbe angemeldet (Haupt- oder Nebenerwerb)'),
    checklist_item('Eröffnungsfragebogen beim Finanzamt ausgefüllt'),
    checklist_item('Umsatzsteuer-Identifikationsnummer (USt-IdNr.) beantragt'),
    checklist_item('Umsatzsteuerpflicht gewählt (empfohlen!) — nicht Kleinunternehmer-Option'),
    checklist_item('USt-IdNr. in meinem MONAT-Account hinterlegt'),
    sp(8),
    h2('Laufende Buchhaltung'),
    checklist_item('Monatliche Provisionsabrechnungen heruntergeladen und als PDF gespeichert'),
    checklist_item('Monatliche Gesamtübersicht (Excel/PDF) erstellt und abgeheftet'),
    checklist_item('Alle Betriebsausgaben-Belege gesammelt (digital oder Papier)'),
    checklist_item('Bei Bewirtungen: Anlass + Namen auf dem Beleg notiert'),
    checklist_item('Monatliche Zusammenfassung an den Steuerberater geschickt'),
    sp(8),
    h2('Steuerliche Meldungen'),
    checklist_item('Umsatzsteuervoranmeldung quartalsweise eingereicht'),
    checklist_item('Zusammenfassende Meldung (ZM) quartalsweise eingereicht'),
    checklist_item('Einkommensteuererklärung jährlich bis 31.07. abgegeben'),
    checklist_item('Umsatzsteuerjahreserklärung abgegeben'),
    sp(8),
    h2('Finanzplanung'),
    checklist_item('Ca. 1/3 des Gewinns als Steuerrücklage auf separatem Konto'),
    checklist_item('Monatlichen Kassensturz gemacht'),
    checklist_item('Steuerberaterin gefunden und regelmäßiger Kontakt hergestellt'),
    sp(12),
]

# ── RECHTLICHER HINWEIS ───────────────────────────────────────────────────────
story += hint_box(
    'Rechtlicher Hinweis',
    'Dieser Leitfaden wurde auf Basis eines praxisbezogenen Steuer-Calls erstellt und dient '
    'ausschließlich der allgemeinen Information. Er stellt keine steuerrechtliche Beratung dar '
    'und ersetzt nicht die individuelle Beratung durch eine qualifizierte Steuerberaterin. '
    'Jeder Steuerfall ist individuell.',
    bg=HELLGRAU, border_color=GRAU
)

# ══════════════════════════════════════════════════════════════════════════════
# PDF BAUEN
# ══════════════════════════════════════════════════════════════════════════════
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=MARGIN_L, rightMargin=MARGIN_R,
    topMargin=MARGIN_T,  bottomMargin=MARGIN_B + 1.2*cm,
    title='Steuerleitfaden Network Marketing & MONAT',
    author='Nancy Wackerhagen / Patrycja Nasri',
    subject='Steuerliche Grundlagen für MONAT-Partnerinnen in Deutschland',
)
doc.build(story, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)
print(f"Gespeichert: {OUTPUT}")
