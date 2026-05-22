import json
import os
import logging
import re
from datetime import time
from pathlib import Path
from zoneinfo import ZoneInfo

from anthropic import Anthropic
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
BERLIN = ZoneInfo("Europe/Berlin")
EXAMPLES_FILE = Path("learned_examples.json")
MAX_EXAMPLES_IN_PROMPT = 10

client = Anthropic(api_key=ANTHROPIC_API_KEY)

BASE_SYSTEM_PROMPT = """Du schreibst Content für Patrycja Nasri — Transformationscoach, MONAT-Leader, Unternehmerin. In ihrer Stimme, nicht in deiner.

THEMEN: Astrologie, Identitätsarbeit, Businessstrategie, Mindset, Frauenempowerment, finanzielle Freiheit, MONAT-Produkte, Community-Building.
PROGRAMME: Moneycode · Identitycode · Emotioncode
ZIELGRUPPE: Frauen, die ein profitables Business aufbauen wollen und bereit für Transformation sind.

PATRYCJAS STIMME — so klingt sie wirklich:
- Kurze Sätze. Einer nach dem anderen. Kein Fließtext.
- Direkte Ansprache: immer "du", nie "man"
- Roh und gesprochen, nicht glatt und gecoacht
- Wiederholungen die Energie tragen: "Noch ein Buch. Noch ein Kurs. Noch eine Strategie."
- Fragen die sitzen: "Was hält dich wirklich zurück?"
- Polarisierende Aussagen: "Das ist kein Wissen-Problem."

IHRE KERNBOTSCHAFTEN:
"Es geht nicht um Wissen. Es geht um Verkörperung. Es geht um deine Bewegung."
"Transformation ist Reibung. Ohne Reibung kein Wachstum."
"Du brauchst keine neue Strategie. Du brauchst die Version von dir, die durchzieht."

ABSOLUT VERBOTEN:
- Gedankenstriche (—) im Text
- "nicht... sondern..."-Konstruktionen
- Glatte Coaching-Sätze
- "Ich hatte X. Ich hatte Y."-Listen
- "Und genau da..." als Übergang
- "Echt X. Echt Y. Echt Z."-Wiederholungen
- Leere Floskeln und generische Motivationssätze

Immer auf Deutsch."""


def load_examples() -> list[dict]:
    if not EXAMPLES_FILE.exists():
        return []
    try:
        return json.loads(EXAMPLES_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def save_example(content: str) -> None:
    from datetime import datetime
    examples = load_examples()
    examples.append({
        "date": datetime.now(BERLIN).strftime("%Y-%m-%d"),
        "content": content.strip(),
    })
    EXAMPLES_FILE.write_text(
        json.dumps(examples, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_system_prompt() -> str:
    examples = load_examples()
    if not examples:
        return BASE_SYSTEM_PROMPT

    recent = examples[-MAX_EXAMPLES_IN_PROMPT:]
    examples_text = "\n\n---\n\n".join(
        f"[{ex['date']}]\n{ex['content']}" for ex in recent
    )
    return (
        BASE_SYSTEM_PROMPT
        + f"\n\nPATRYCJAS ECHTE POSTS — lerne daraus, das ist ihre wahre Stimme:\n\n{examples_text}"
    )


def generate_story_ideas() -> tuple[str, list[str]]:
    from datetime import datetime

    today = datetime.now(BERLIN).strftime("%A, %d. %B %Y")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=build_system_prompt(),
        messages=[
            {
                "role": "user",
                "content": f"""Heute ist {today}.

Erstelle 5 fertige Instagram-Story-Ideen für Patrycja — direkt umsetzbar, passend zu aktuellen Trends und ihrer Nische.

Format für jede Idee (Trennlinie zwischen den Ideen mit ---):

Story [Nr]: [Titel]
🎯 Hook: [erster Satz der Story — direkt, packend, 1 Satz]
📖 Konzept: [Was zeigt oder erzählt sie? 2-3 konkrete Sätze]

---

Variiere die Formate: Persönliche Story, Behind-the-Scenes, Strategie-Tipp, Frage an die Community, Ergebnis/Transformation.

Sei konkret. Patrycjas Energie: direkt, mutig, klar.""",
            }
        ],
    )

    full_text = response.content[0].text
    ideas = [idea.strip() for idea in re.split(r"\n---\n", full_text) if idea.strip()]
    return full_text, ideas


def generate_slides(idea_text: str, cta: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=3000,
        system=build_system_prompt(),
        messages=[
            {
                "role": "user",
                "content": f"""Erstelle 6-7 Instagram Story Slides für Patrycja basierend auf dieser Idee.

Story-Idee:
{idea_text}

CTA (letzter Slide — exakt so verwenden, kein Wort ändern):
{cta}

Struktur:
- Slide 1: Hook — 1-2 Sätze, sitzt sofort, macht neugierig
- Slide 2: Persönlicher Einstieg — echte Situation, roh, Zuschauer erkennt sich wieder
- Slide 3-5: Geschichte entfalten — eine Erkenntnis pro Slide, echter Mehrwert
- Slide 6: Brücke zur CTA — warum jetzt
- Slide 7: CTA-Text exakt wie oben

Format:
Slide [Nr]:
[Text — max 3 Zeilen, direkt auf dem Bildschirm]

---

Jeder Slide steht für sich. Kurz. Kraftvoll. Gesprochen.""",
            }
        ],
    )

    return response.content[0].text


def split_for_telegram(text: str, max_len: int = 4096) -> list[str]:
    if len(text) <= max_len:
        return [text]
    parts = []
    while len(text) > max_len:
        split_at = text.rfind("\n---\n", 0, max_len)
        if split_at == -1:
            split_at = max_len
        parts.append(text[:split_at])
        text = text[split_at:].lstrip("-").lstrip()
    if text:
        parts.append(text)
    return parts


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Story-Agent aktiv!\n\n"
        "Jeden Morgen um 8:00 Uhr bekommst du 5 Story-Ideen.\n"
        "Wähle eine Nummer, gib deinen CTA an — ich erstelle die Slides.\n\n"
        "Nach dem Posten: /meinversion [deine fertige Story]\n"
        "Der Agent lernt daraus und wird täglich besser.\n\n"
        "/ideen — Ideen jetzt generieren\n"
        "/beispiele — Wie viele Lernbeispiele gespeichert sind\n"
        "/chatid — Deine Chat-ID"
    )


async def cmd_chatid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Deine Chat-ID: {update.effective_chat.id}")


async def cmd_beispiele(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    examples = load_examples()
    if not examples:
        await update.message.reply_text(
            "Noch keine Lernbeispiele gespeichert.\n"
            "Nach deinem ersten Post: /meinversion [deine Story]"
        )
        return
    last = examples[-1]
    await update.message.reply_text(
        f"{len(examples)} Lernbeispiele gespeichert.\n"
        f"Letztes Beispiel: {last['date']}\n\n"
        f"Vorschau:\n{last['content'][:300]}..."
    )


async def cmd_meinversion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.replace("/meinversion", "").strip()

    if not text:
        context.user_data["waiting_for_example"] = True
        await update.message.reply_text(
            "Schick mir jetzt deine fertige Story — genau so wie du sie gepostet hast."
        )
        return

    save_example(text)
    examples = load_examples()
    await update.message.reply_text(
        f"Gespeichert. Ich habe jetzt {len(examples)} Lernbeispiel(e) von dir.\n"
        f"Ab der nächsten Story lerne ich daraus."
    )
    logger.info("New example saved. Total: %d", len(examples))


async def cmd_ideen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = await update.message.reply_text("Generiere deine Story-Ideen...")
    try:
        full_text, ideas = generate_story_ideas()
        context.bot_data["last_ideas"] = ideas

        header = "5 Story-Ideen für heute:\n\n"
        chunks = split_for_telegram(header + full_text)

        await msg.edit_text(chunks[0])
        for chunk in chunks[1:]:
            await update.message.reply_text(chunk)

        await update.message.reply_text(
            "Welche Story willst du heute umsetzen?\n"
            "Antworte mit der Nummer, z.B. '2'"
        )

    except Exception as e:
        logger.error("Error generating ideas: %s", e)
        await msg.edit_text("Fehler beim Generieren. Bitte /ideen erneut versuchen.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()

    # Save example if waiting
    if context.user_data.get("waiting_for_example"):
        context.user_data["waiting_for_example"] = False
        save_example(text)
        examples = load_examples()
        await update.message.reply_text(
            f"Gespeichert. Ich habe jetzt {len(examples)} Lernbeispiel(e) von dir.\n"
            f"Ab der nächsten Story lerne ich daraus."
        )
        return

    # Waiting for CTA
    if context.user_data.get("waiting_for_cta"):
        selected_idea = context.user_data.pop("selected_idea")
        story_number = context.user_data.pop("story_number")
        context.user_data.pop("waiting_for_cta")

        cta = text
        msg = await update.message.reply_text(f"Erstelle Slides fur Story {story_number}...")
        try:
            slides = generate_slides(selected_idea, cta)
            header = f"Slides fur Story {story_number}:\n\n"
            chunks = split_for_telegram(header + slides)
            await msg.edit_text(chunks[0])
            for chunk in chunks[1:]:
                await update.message.reply_text(chunk)

            await update.message.reply_text(
                "Wenn du die Story gepostet hast, schick mir deine finale Version:\n"
                "/meinversion [deine Story]\n\n"
                "Ich lerne daraus und werde jeden Tag besser."
            )
        except Exception as e:
            logger.error("Error generating slides: %s", e)
            await msg.edit_text("Fehler beim Generieren. Bitte nochmal versuchen.")
        return

    # Story selection
    match = re.search(r"\b([1-5])\b", text)
    if not match:
        return

    number = int(match.group(1))
    ideas = context.bot_data.get("last_ideas", [])

    if not ideas:
        await update.message.reply_text(
            "Keine Ideen gespeichert. Starte mit /ideen."
        )
        return

    if number > len(ideas):
        await update.message.reply_text(f"Bitte wahle eine Zahl zwischen 1 und {len(ideas)}.")
        return

    context.user_data["selected_idea"] = ideas[number - 1]
    context.user_data["story_number"] = number
    context.user_data["waiting_for_cta"] = True

    await update.message.reply_text(
        f"Story {number} ausgewahlt.\n\n"
        "Was ist dein CTA diese Woche?\n"
        "Schreib ihn einfach rein, z.B.:\n"
        "Kommentiere MONEYCODE und ich schicke dir die Aktivierung!"
    )


async def send_daily_ideas(context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        full_text, ideas = generate_story_ideas()
        context.bot_data["last_ideas"] = ideas

        header = "Guten Morgen! Deine Story-Ideen fur heute:\n\n"
        chunks = split_for_telegram(header + full_text)

        for chunk in chunks:
            await context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=chunk)

        await context.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text="Welche Story willst du heute umsetzen?\nAntworte einfach mit der Nummer, z.B. '2'"
        )

        logger.info("Daily story ideas sent.")
    except Exception as e:
        logger.error("Error sending daily ideas: %s", e)


def main() -> None:
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("chatid", cmd_chatid))
    app.add_handler(CommandHandler("ideen", cmd_ideen))
    app.add_handler(CommandHandler("beispiele", cmd_beispiele))
    app.add_handler(CommandHandler("meinversion", cmd_meinversion))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.job_queue.run_daily(
        send_daily_ideas,
        time=time(hour=8, minute=0, tzinfo=BERLIN),
        name="daily_story_ideas",
    )

    logger.info("Bot started — daily delivery at 08:00 Europe/Berlin")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
