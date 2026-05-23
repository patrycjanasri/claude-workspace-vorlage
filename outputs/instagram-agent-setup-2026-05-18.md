# Instagram Analyse Agent — Setup Status
Datum: 2026-05-18

## Was gebaut wurde

**Plattform:** Make.com
**Ziel:** Wöchentlicher Instagram-Report automatisch jeden Montag 08:00 Uhr via Telegram

---

## Szenario-Struktur (5 Module)

```
[1] Instagram for Business — Get user insights
        ↓
[2] Instagram for Business — List public user posts
        ↓
[4] Tools — Text aggregator
        ↓
[5] HTTP — Claude API (POST /v1/messages)
        ↓
[6] Telegram Bot — Send a Text Message or a Reply
```

---

## Zugangsdaten & Konfiguration

**Telegram Bot:** Patrycja Analyse Bot
**Bot Token:** 8852600357:AAEDaz7MjSBJaWIptICz7oHjlbjjXbtn53o
**Chat ID:** 1720110580

**Instagram Account:** @patrycjanasri (Patrycja.Nasri)
**Make Connection:** Patrycjas Instagram

**Schedule:** Weekly — Monday — 08:00 — Europe/Berlin

---

## Claude Prompt (im HTTP Modul)

```
Du bist mein persönlicher Instagram Analyst für meinen Account im Bereich Network Marketing und Social Media Coaching.

Hier sind meine Instagram Posts und Insights der letzten Woche:
{{4.text}}

Analysiere folgendes und antworte auf Deutsch, klar und direkt:

BESTE BEITRÄGE
Welche Posts haben am besten performt? Warum? Was haben sie gemeinsam (Hook, Thema, Format)?

KOMMENTARE & ENGAGEMENT
Welche Beiträge haben die meisten Kommentare bekommen? Was hat die Zielgruppe dazu bewogen zu reagieren?

REICHWEITE & WACHSTUM
Wie war die Reichweite diese Woche? Gab es Ausreißer nach oben oder unten?

MARKT & TRENDS
Was passiert gerade im Network Marketing und Social Media Bereich? Worauf sollte ich als Coach achten?

FOKUS NÄCHSTE WOCHE
Was soll ich nächste Woche konkret mehr machen? Welche Themen, welche Formate, welche Hooks?

Keine langen Erklärungen. Ich will klare Antworten und konkrete Empfehlungen.
```

**Model:** claude-opus-4-7
**Max tokens:** 2000

---

## Text Aggregator (Modul 4) — Felder

```
Post vom {{2.Timestamp}}:
Caption: {{2.Caption}}
Likes: {{2.likeCount}} | Kommentare: {{2.commentsCount}} | Views: {{2.viewCount}} | Saves: {{2.savedCount}}
Link: {{2.postURL}}
---
```

---

## Bekannte Einschränkung

"List public user posts" liefert keine Engagement-Metriken (Likes, Kommentare, Saves).
Caption und Timestamp kommen durch — Claude analysiert Content-Qualität und gibt Markt-Trends + Empfehlungen.

**Fix für später:** "Get post insights" Modul zwischen Modul 2 und Modul 4 einfügen für echte Zahlen.

---

## Status

- [x] Instagram Connection verbunden (@patrycjanasri)
- [x] Claude API verbunden
- [x] Telegram Bot verbunden (Patrycja Analyse Bot)
- [x] Report läuft durch — Telegram empfängt Nachrichten
- [x] Schedule eingestellt: Montag 08:00
- [ ] Schedule heute (2026-05-18) nicht ausgelöst — prüfen ob Szenario aktiv ist
- [ ] Contentideen-Agent (Option 2 — separates Szenario via /ideen)

---

## Nächste Schritte

1. **Sofort:** Prüfen ob Szenario in Make aktiv ist (blauer "Custom schedule" Schalter)
2. **Nächste Session:** Contentideen-Agent bauen (/ideen Trigger in Telegram)
3. **Optional:** Get post insights hinzufügen für echte Engagement-Zahlen
