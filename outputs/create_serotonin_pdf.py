# -*- coding: utf-8 -*-
"""
Generates Serotonin_Call_Praesentation_v2.pdf
Uses reportlab with proper German umlauts, no Gedankenstriche.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable

# ── Colours ──────────────────────────────────────────────────────────────────
PURPLE       = colors.Color(122/255, 59/255, 166/255)
LAVENDER     = colors.Color(237/255, 231/255, 246/255)
WHITE        = colors.white
BLACK        = colors.black

# ── Output path ──────────────────────────────────────────────────────────────
OUTPUT_DIR = "/Users/patrycjakaczorowska/Downloads/Vorlagen/claude-workspace-vorlage/outputs"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "Serotonin_Call_Praesentation_v2.pdf")

# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    s = {}

    s["body"] = ParagraphStyle(
        "body", fontName="Helvetica", fontSize=10, leading=14,
        textColor=BLACK, spaceAfter=6
    )
    s["body_white"] = ParagraphStyle(
        "body_white", fontName="Helvetica", fontSize=10, leading=14,
        textColor=WHITE, spaceAfter=4
    )
    s["heading"] = ParagraphStyle(
        "heading", fontName="Helvetica-Bold", fontSize=22, leading=26,
        textColor=PURPLE, spaceBefore=6, spaceAfter=4
    )
    s["subheading"] = ParagraphStyle(
        "subheading", fontName="Helvetica-Bold", fontSize=12, leading=15,
        textColor=BLACK, spaceBefore=8, spaceAfter=4
    )
    s["cover_title"] = ParagraphStyle(
        "cover_title", fontName="Helvetica-Bold", fontSize=36, leading=42,
        textColor=WHITE, alignment=TA_CENTER
    )
    s["cover_sub"] = ParagraphStyle(
        "cover_sub", fontName="Helvetica", fontSize=13, leading=18,
        textColor=WHITE, alignment=TA_CENTER
    )
    s["closing_big"] = ParagraphStyle(
        "closing_big", fontName="Helvetica-Bold", fontSize=18, leading=26,
        textColor=WHITE, alignment=TA_CENTER
    )
    s["italic_small"] = ParagraphStyle(
        "italic_small", fontName="Helvetica-Oblique", fontSize=9, leading=12,
        textColor=colors.Color(0.3, 0.3, 0.3), alignment=TA_CENTER, spaceBefore=10
    )
    s["booster_body"] = ParagraphStyle(
        "booster_body", fontName="Helvetica", fontSize=10, leading=14,
        textColor=BLACK, spaceAfter=6,
        backColor=LAVENDER,
        borderPad=6
    )
    s["purple_highlight"] = ParagraphStyle(
        "purple_highlight", fontName="Helvetica-Bold", fontSize=11, leading=15,
        textColor=PURPLE, spaceAfter=8
    )
    return s


# ── Helper: purple header box (full-width coloured rectangle with white text) ─
def purple_box(text_lines, styles, height_cm=8, font_size_first=36):
    """Returns a Table that mimics a full-width purple box with white text."""
    cell_parts = []
    for i, line in enumerate(text_lines):
        fs = font_size_first if i == 0 else 13
        bold = "Bold" if i == 0 else ""
        cell_parts.append(
            Paragraph(line, ParagraphStyle(
                f"pb{i}", fontName=f"Helvetica-{bold}" if bold else "Helvetica",
                fontSize=fs, leading=fs + 6, textColor=WHITE, alignment=TA_CENTER
            ))
        )
        if i < len(text_lines) - 1:
            cell_parts.append(Spacer(1, 4))

    t = Table([[cell_parts]], colWidths=[17 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PURPLE),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 30),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 30),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
    ]))
    return t


def page_heading(title, styles):
    """Purple bold heading + purple rule."""
    return [
        Paragraph(title, styles["heading"]),
        HRFlowable(width="100%", thickness=2, color=PURPLE, spaceAfter=8),
    ]


def two_col_table(rows, header=None, col_widths=None):
    """Generic 2-column table with purple header row and lavender alternating rows."""
    col_widths = col_widths or [5 * cm, 12 * cm]
    data = []
    if header:
        data.append(header)
    data.extend(rows)

    style_cmds = [
        ("FONTNAME",  (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE",  (0, 0), (-1, -1), 10),
        ("VALIGN",    (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("GRID",     (0, 0), (-1, -1), 0.5, colors.Color(0.7, 0.7, 0.7)),
        ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
    ]
    if header:
        style_cmds += [
            ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
            ("TEXTCOLOR",  (0, 0), (-1, 0), WHITE),
            ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
        row_start = 1
    else:
        row_start = 0

    for i in range(row_start, len(data)):
        if (i - row_start) % 2 == 1:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), LAVENDER))

    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    t.setStyle(TableStyle(style_cmds))
    return t


def three_col_table(rows, header=None, col_widths=None):
    """Generic 3-column table."""
    col_widths = col_widths or [1.2 * cm, 4.8 * cm, 11 * cm]
    data = []
    if header:
        data.append(header)
    data.extend(rows)

    style_cmds = [
        ("FONTNAME",  (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE",  (0, 0), (-1, -1), 10),
        ("VALIGN",    (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.Color(0.7, 0.7, 0.7)),
    ]
    if header:
        style_cmds += [
            ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
            ("TEXTCOLOR",  (0, 0), (-1, 0), WHITE),
            ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
        row_start = 1
    else:
        row_start = 0

    for i in range(row_start, len(data)):
        if (i - row_start) % 2 == 1:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), LAVENDER))

    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    t.setStyle(TableStyle(style_cmds))
    return t


def booster_section(number_name, body_text, styles):
    """Purple header bar + lavender content block for each booster."""
    header = Table(
        [[Paragraph(number_name, ParagraphStyle(
            "bh", fontName="Helvetica-Bold", fontSize=11, leading=15,
            textColor=WHITE
        ))]],
        colWidths=[17 * cm]
    )
    header.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), PURPLE),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    content = Table(
        [[Paragraph(body_text, ParagraphStyle(
            "bc", fontName="Helvetica", fontSize=10, leading=14, textColor=BLACK
        ))]],
        colWidths=[17 * cm]
    )
    content.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), LAVENDER),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    return KeepTogether([header, content, Spacer(1, 8)])


# ── Build document ─────────────────────────────────────────────────────────────
def build():
    styles = make_styles()

    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Serotonin Call Präsentation v2",
        author="Patrycja Nasri",
    )

    story = []

    # ── PAGE 1: Cover ──────────────────────────────────────────────────────────
    story.append(purple_box([
        "SEROTONIN",
        "Dein Glückshormon verstehen & aktivieren",
        "Präparation für deinen Call",
    ], styles))
    story.append(Spacer(1, 14))

    story.append(Paragraph(
        "Serotonin ist der Botenstoff, der über dein Wohlbefinden, deine Stimmung und "
        "deine Energie entscheidet. Hier hast du alles, was du für deinen Call brauchst.",
        styles["body"]
    ))
    story.append(Spacer(1, 8))

    cover_rows = [
        ["Was ist Serotonin?", "Botenstoff, Stimmung, Energie, Körper-Geist-Verbindung"],
        ["Wo entsteht es?",    "90-95% im Darm. Nicht im Gehirn."],
        ["Mangel-Symptome",    "Ängste, Müdigkeit, Energielosigkeit, schlechte Laune"],
        ["Ursachen Mangel",    "Ernährung, Schlaf, fehlende Natur, wenig Sonnenlicht"],
        ["5 Booster",          "Natur, Sonnenlicht, Darmgesundheit, Runterkommen, Tiefschlaf"],
    ]
    story.append(two_col_table(cover_rows, header=["Thema", "Inhalt"]))

    story.append(PageBreak())

    # ── PAGE 2: Was ist Serotonin? ─────────────────────────────────────────────
    story.extend(page_heading("1. Was ist Serotonin?", styles))

    story.append(Paragraph(
        "Serotonin ist kein Zufall. Dieser Botenstoff bestimmt direkt, wie du dich "
        "fühlst, wie viel Energie du hast und wie klar dein Kopf ist.",
        styles["body"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Die 2 Hauptfunktionen", styles["subheading"]))
    story.append(Paragraph(
        "<b>Stimmung:</b> Serotonin reguliert direkt, wie du dich fühlst. "
        "Positiv, ausgeglichen, ruhig.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>Energie:</b> Ein ausgewogener Serotoninspiegel hält dein Energieniveau stabil "
        "und versorgt dich den ganzen Tag.",
        styles["body"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Die 2 Serotonin-Prinzipien", styles["subheading"]))
    p2_rows = [
        ["Prinzip 1",
         "90% wird in deinem Darm gebildet. Nicht im Gehirn. Das ist der größte "
         "Unterschied zu allen anderen Botenstoffen."],
        ["Prinzip 2",
         "Je glücklicher dein Körper, desto glücklicher dein Geist. Was gut für deinen "
         "Darm ist, steigert direkt deine Stimmung."],
    ]
    story.append(two_col_table(p2_rows, header=["Prinzip", "Inhalt"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Gefühle sind Botschaften deines Körpers", styles["subheading"]))
    story.append(Paragraph(
        "Das Wort Emotion bedeutet wörtlich 'Energie in Bewegung'. Wenn du schwierige "
        "Gefühle verspürst, sendet dir dein Körper eine klare Botschaft. Bauchgefühle "
        "sind echte Serotonin-Signale aus deinem Darm. Hör hin.",
        styles["body"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Die Verbindung: Gehirn-Darm-Achse & Vagusnerv", styles["subheading"]))
    story.append(Paragraph(
        "Der Vagusnerv (lat. 'vagus' = wandernd) ist die Hauptverbindung zwischen Darm "
        "und Gehirn. Er überwacht Herzfrequenz, Atmung, Verdauung, Stimmung, Energie "
        "und dein Immunsystem. Was du körperlich fühlst, beeinflusst direkt, wie du "
        "emotional bist.",
        styles["body"]
    ))

    story.append(PageBreak())

    # ── PAGE 3: Symptome & Ursachen ────────────────────────────────────────────
    story.extend(page_heading(
        "2. Niedriger Serotoninspiegel. Symptome & Ursachen", styles
    ))

    story.append(Paragraph(
        "So fühlt sich ein <b>niedriger</b> Serotoninspiegel an:", styles["body"]
    ))
    for item in [
        "Antriebslosigkeit, Müdigkeit",
        "Ängste und Sorgen",
        "Schlechte Stimmung, Reizbarkeit",
        "Konzentrationsprobleme",
        "Heißhunger auf Süßes (Dopaminkick-Suche)",
    ]:
        story.append(Paragraph(f"• {item}", styles["body"]))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "So fühlt sich ein <b>hoher</b> Serotoninspiegel an:", styles["body"]
    ))
    for item in [
        "Gute Laune und innere Ruhe",
        "Hohe Energie und Fokus",
        "Positiver Blick auf das Leben",
        "Stabile Emotionen",
    ]:
        story.append(Paragraph(f"• {item}", styles["body"]))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Die 4 Hauptursachen für Serotonin-Mangel", styles["subheading"]))

    urs_rows = [
        ["1", "Ungesunde Ernährung",
         "Stark verarbeitete Lebensmittel (UPF) schädigen die Darmflora und hemmen "
         "die Serotoninproduktion direkt."],
        ["2", "Zu wenig Schlaf",
         "Schlafmangel senkt die Serotoninproduktion massiv. Ein Teufelskreis."],
        ["3", "Zu wenig Natur",
         "Unsere Neurobiologie ist auf regelmäßigen Naturkontakt ausgelegt. "
         "Digitale Welt bedeutet Serotonin-Mangel."],
        ["4", "Zu wenig Sonne",
         "Jeder Kontakt mit Tageslicht aktiviert Serotonin. Egal ob drinnen oder draußen."],
    ]
    story.append(three_col_table(urs_rows, header=["#", "Ursache", "Erklärung"]))

    story.append(PageBreak())

    # ── PAGE 4: Die 5 Serotonin-Booster ───────────────────────────────────────
    story.extend(page_heading("3. Die 5 Serotonin-Booster", styles))

    boosters = [
        ("1. NATUR",
         "Regelmäßige Zeit in der Natur. Ohne Kopfhörer. Aktiviere alle Sinne: "
         "Sehen (Farben zählen), Hören (Geräusche), Riechen (tief einatmen). "
         "Waldbaden (Shinrin-Yoku) senkt Stress und erhöht natürliche Killerzellen. "
         "Challenge: 3 Spaziergänge pro Woche ohne Handy."),
        ("2. SONNENLICHT",
         "Sonnenlicht ist der wichtigste Faktor zur Erhöhung des Serotoninspiegels. "
         "Morgens 5-10 Min. Sonne (sonnige Tage), 10-15 Min. (bewölkt), 30 Min. (dunkel). "
         "Mittags kurz raus. Abends Sonnenuntergang mit warmem Licht für guten Schlaf. "
         "Zirkadianer Rhythmus ist dein natürlicher Tag-Nacht-Takt. "
         "Meta-Analyse: 85.000 Studien belegen es. Regelmäßiges Tageslicht ist eine "
         "effektive und evidenzbasierte Methode zur Verbesserung der psychischen Gesundheit."),
        ("3. DARMGESUNDHEIT",
         "90-95% des Serotonins entsteht im Darm. Ernähre dich gut für einen gesunden "
         "Darm: 80% satt essen, Obst als Snack, Eiweißzufuhr erhöhen, Gemüse als "
         "Kohlenhydratquelle, verarbeitete Lebensmittel weglassen, Intervallfasten. "
         "Beste Getränke: Wasser, Kräutertee, Kaffee (richtig konsumiert), Probiotika. "
         "Alkohol und Zucker deutlich reduzieren."),
        ("4. RUNTERKOMMEN",
         "Dein parasympathisches Nervensystem (Vagusnerv) ist entscheidend. "
         "Atemstrategien: Resonanzatmung (6 Atemzüge pro Minute durch die Nase), "
         "Seufzeratmung (doppeltes Einatmen plus langer Ausatem). "
         "Gedanken kreisen stoppen: Gedanken aussprechen, Journaling, dankbar sein. "
         "Täglich 5 Min. Morgenmeditation reicht."),
        ("5. TIEFSCHLAF",
         "Tiefschlaf ist die wichtigste Serotoninquelle. Ziel: 7-9 Stunden. "
         "Morgensonne nach dem Aufwachen, täglich Bewegung, Schlafumgebung optimieren "
         "(Temperatur, Beleuchtung, Komfort), abends kein Bildschirm, kein Koffein nach "
         "12 Uhr, kein Zucker und Alkohol abends. 6 Strategien: Morgensonne, Bewegung, "
         "Schlafumgebung, Technik in der Nacht, Ernährung, Geist beruhigen."),
    ]
    for name, text in boosters:
        story.append(booster_section(name, text, styles))

    story.append(PageBreak())

    # ── PAGE 5: Überblick & Aktionen ───────────────────────────────────────────
    story.extend(page_heading("4. Serotonin im Überblick. Deine Aktionen", styles))

    story.append(Paragraph(
        "<b>Was wird deine wichtigste Serotonin-Aktion?</b> Du musst nicht alles auf "
        "einmal umsetzen. Nur das, was sich für dich instinktiv richtig und machbar anfühlt.",
        styles["body"]
    ))
    story.append(Spacer(1, 8))

    action_rows = [
        ["Natur",
         "Heute spazieren gehen. Ohne Handy.",
         "3x/Woche Natur-Spaziergang ohne Kopfhörer"],
        ["Sonnenlicht",
         "Morgen direkt nach dem Aufstehen raus.",
         "Jede Woche Morgensonne, Mittagspause, Sonnenuntergang beobachten"],
        ["Darm",
         "Mehr Eiweiß und Gemüse bei nächster Mahlzeit.",
         "Eine Essen- und eine Trinkstrategie auswählen und umsetzen"],
        ["Runterkommen",
         "Jetzt 5 Min. Resonanzatmung ausprobieren.",
         "Jede Woche morgens 5 Min. Atemübung"],
        ["Schlaf",
         "Heute Abend Handy ab 20 Uhr auf Nicht stören.",
         "Eine Schlaf-Strategie priorisieren und umsetzen"],
    ]
    story.append(three_col_table(
        action_rows,
        header=["Bereich", "Sofort-Aktion", "Challenge"],
        col_widths=[3 * cm, 7 * cm, 7 * cm]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Dein Kern-Satz für den Call:", styles["subheading"]))
    story.append(Paragraph(
        "Wissen ist okay. Aber erst die Bewegung, die aktive Umsetzung, macht dich nicht "
        "nur gesund, sondern magnetisch. Serotonin entsteht durch das, was du täglich tust. "
        "Nicht durch das, was du weißt.",
        ParagraphStyle(
            "kern", fontName="Helvetica-Bold", fontSize=11, leading=16,
            textColor=PURPLE, spaceAfter=10
        )
    ))

    story.append(Paragraph("Tiefschlaf & Atemstrategien. Quick Reference", styles["subheading"]))
    atem_rows = [
        ["Resonanzatmung",
         "6 Atemzüge pro Min. durch die Nase. Senkt Herzfrequenz, hebt Stimmung."],
        ["Seufzeratmung",
         "Doppeltes Einatmen plus langer Ausatem. Sofortige Beruhigung."],
        ["Körper-Scan",
         "5 Min. morgens: Körper von Kopf bis Fuß scannen, Augen geschlossen."],
    ]
    story.append(two_col_table(
        atem_rows,
        header=["Atemtechnik", "Anwendung"],
        col_widths=[5 * cm, 12 * cm]
    ))

    story.append(PageBreak())

    # ── PAGE 6: Closing ────────────────────────────────────────────────────────
    story.append(Spacer(1, 40))

    closing = Table(
        [[
            [
                Paragraph("Runterkommen ist machbar.", styles["closing_big"]),
                Spacer(1, 8),
                Paragraph("Serotonin ist machbar.", styles["closing_big"]),
                Spacer(1, 8),
                Paragraph("Ab heute geht es los.", styles["closing_big"]),
            ]
        ]],
        colWidths=[17 * cm]
    )
    closing.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), PURPLE),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING",    (0, 0), (-1, -1), 50),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 50),
        ("LEFTPADDING",   (0, 0), (-1, -1), 20),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 20),
    ]))
    story.append(closing)

    story.append(Paragraph(
        "Basierend auf dem Buch 'Der DOSE-Effekt' | Teil 3: Serotonin",
        styles["italic_small"]
    ))

    # ── Build ──────────────────────────────────────────────────────────────────
    doc.build(story)
    print(f"PDF saved: {OUTPUT_PATH}")
    print(f"File size: {os.path.getsize(OUTPUT_PATH):,} bytes")


if __name__ == "__main__":
    build()
