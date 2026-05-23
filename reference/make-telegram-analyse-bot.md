# Make Blueprint: Weekly Instagram Report via Telegram

Jeden Montag früh analysiert Claude automatisch deinen Instagram-Account der letzten Woche und schickt dir den Report direkt in Telegram.

**Bot:** Patrycjas Analyse bot  
**Chat-ID:** 1720110580  
**Lieferzeit:** Montag, 08:00 Uhr

---

## Voraussetzungen

- **Make-Account** ✅
- **Telegram Bot** ✅ (Token: gespeichert)
- **Instagram Business oder Creator Account** mit verknüpfter Facebook Page
- **Claude API Key** — console.anthropic.com → API Keys → Create Key

---

## Szenario-Übersicht (8 Module)

```
[1] Schedule: Jeden Montag 08:00 Uhr
        ↓
[2] Instagram: Get Account Insights (Follower, Reichweite, Profilbesuche)
        ↓
[3] Instagram: List User's Media (letzte 7 Tage)
        ↓
[4] Iterator: Pro Post
        ↓
[5] Instagram: Get Media Insights (pro Post)
        ↓
[6] Aggregator: Alle Daten zusammenführen
        ↓
[7] HTTP: Claude API aufrufen
        ↓
[8] Telegram: Report senden
```

---

## Modul 1 — Schedule

**App:** Schedule  
**Modul:** Every week  
**Einstellungen:**
- Day: Monday
- Time: 08:00
- Timezone: Europe/Berlin

---

## Modul 2 — Instagram: Account Insights

**App:** Instagram for Business  
**Modul:** Get Account Insights  
**Einstellungen:**
- Connection: Dein Instagram Business Account
- Metrics: `follower_count, reach, profile_views, impressions`
- Period: `week`

> Falls kein Make-Modul: HTTP GET gegen Graph API (siehe Anhang)

---

## Modul 3 — Instagram: List User's Media

**App:** Instagram for Business  
**Modul:** List User's Media  
**Einstellungen:**
- Connection: Dein Instagram Business Account
- Fields: `id, caption, media_type, timestamp, permalink`
- Limit: 20
- Filter: Nur Posts der letzten 7 Tage (timestamp >= Montag der letzten Woche)

---

## Modul 4 — Iterator

**App:** Flow Control  
**Modul:** Iterator  
**Array:** Output aus Modul 3 (Liste der Posts)

---

## Modul 5 — Instagram: Get Media Insights

**App:** Instagram for Business  
**Modul:** Get Media Insights  
**Einstellungen:**
- Media ID: `{{4.id}}`
- Metrics: `impressions, reach, saved, comments_count, like_count, shares`

> Für Reels zusätzlich: `plays, video_views`

---

## Modul 6 — Aggregator

**App:** Tools → Text Aggregator  
**Zweck:** Alle Post-Daten als JSON-String zusammenführen

**Ausgabe-Struktur pro Post:**
```json
{
  "datum": "{{formatDate(4.timestamp; \"YYYY-MM-DD\")}}",
  "format": "{{4.media_type}}",
  "hook": "{{substring(4.caption; 0; 120)}}",
  "reichweite": "{{5.reach}}",
  "likes": "{{5.like_count}}",
  "kommentare": "{{5.comments_count}}",
  "saves": "{{5.saved}}",
  "shares": "{{5.shares}}"
}
```

Account-Daten separat als Variable speichern:
```json
{
  "neue_follower": "{{2.follower_count}}",
  "gesamtreichweite": "{{2.reach}}",
  "profilbesuche": "{{2.profile_views}}"
}
```

---

## Modul 7 — HTTP: Claude API

**App:** HTTP  
**Modul:** Make a Request  

**URL:** `https://api.anthropic.com/v1/messages`  
**Methode:** POST  
**Headers:**
```
x-api-key: DEIN_CLAUDE_API_KEY
anthropic-version: 2023-06-01
content-type: application/json
```

**Body (JSON):**
```json
{
  "model": "claude-opus-4-7",
  "max_tokens": 2000,
  "messages": [
    {
      "role": "user",
      "content": "Du bist mein persönlicher Instagram Analyst für meinen Account im Bereich Network Marketing und Social Media Coaching.\n\nHier sind meine Instagram Posts und Insights der letzten Woche:\n{{6.text}}\n\nAnalysiere folgendes und antworte auf Deutsch, klar und direkt:\n\nBESTE BEITRÄGE\nWelche Posts haben am besten performt? Warum? Was haben sie gemeinsam (Hook, Thema, Format)?\n\nKOMMENTARE & ENGAGEMENT\nWelche Beiträge haben die meisten Kommentare bekommen? Was hat die Zielgruppe dazu bewogen zu reagieren?\n\nREICHWEITE & WACHSTUM\nWie war die Reichweite diese Woche? Gab es Ausreißer nach oben oder unten?\n\nMARKT & TRENDS\nWas passiert gerade im Network Marketing und Social Media Bereich? Worauf sollte ich als Coach achten?\n\nFOKUS NÄCHSTE WOCHE\nWas soll ich nächste Woche konkret mehr machen? Welche Themen, welche Formate, welche Hooks?\n\nKeine langen Erklärungen. Ich will klare Antworten und konkrete Empfehlungen."
    }
  ]
}
```

---

## Modul 8 — Telegram: Report senden

**App:** Telegram Bot  
**Modul:** Send a Message  
**Einstellungen:**
- Connection: Patrycjas Analyse bot
- Chat ID: `1720110580`
- Text: `{{7.data.content[].text}}`
- Parse Mode: Markdown

---

## Anhang: Instagram via HTTP (falls kein Make-Modul)

**Access Token besorgen:**
1. developers.facebook.com → App erstellen
2. Instagram Graph API aktivieren
3. Langlebigen Token generieren (60 Tage, verlängerbar via System User)

**Account Insights:**
```
GET https://graph.instagram.com/me?fields=followers_count,media_count&access_token=TOKEN
```

```
GET https://graph.instagram.com/{ig-user-id}/insights
  ?metric=reach,impressions,profile_views,follower_count
  &period=week
  &access_token=TOKEN
```

**Posts der letzten 7 Tage:**
```
GET https://graph.instagram.com/me/media
  ?fields=id,caption,media_type,timestamp,permalink
  &access_token=TOKEN
  &limit=20
```

**Insights pro Post:**
```
GET https://graph.instagram.com/{media-id}/insights
  ?metric=impressions,reach,saved,comments_count,like_count,shares
  &access_token=TOKEN
```

---

## Fehlerquellen

| Problem | Lösung |
|---------|--------|
| Instagram liefert keine Insights | Account muss mit Facebook Page verknüpft sein |
| Token läuft ab | Langlebigen Token via System User in Facebook Business Manager holen |
| Claude-Response leer | `max_tokens` erhöhen, Body-JSON prüfen |
| Weniger als 7 Posts | Kein Fehler — Claude analysiert was da ist |
| Telegram-Nachricht zu lang | Telegram-Limit 4096 Zeichen — `max_tokens` auf 1500 reduzieren falls nötig |

---

## Erweiterungen (optional)

- **On-Demand:** Zusätzlich `/analyse` in Telegram triggern (zweites Szenario mit Watch Messages)
- **Ergebnisse archivieren:** Zusatzmodul schreibt Report in Google Drive oder Notion
- **Zeitraum anpassen:** Schedule auf Sonntag abend 20:00 ändern für Wochenplanung
