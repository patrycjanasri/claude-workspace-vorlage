// AstroCheck KI — Netlify Function (streaming)
// Ruft Claude Opus auf und streamt ein Business-/Skalierungs-Reading aus dem Geburtshoroskop.
// Der API-Key liegt ausschliesslich serverseitig als Umgebungsvariable ANTHROPIC_API_KEY.

const SYSTEM_PROMPT = `Du schreibst als Patrycja Nasri, Transformationscoach und MONAT-Leaderin. Du verbindest Astrologie, Identitaetsarbeit und Businessstrategie. Deine Aufgabe ist es, aus den Platzierungen eines Geburtshoroskops ein praezises, persoenliches Reading darueber zu schreiben, WIE diese Frau ihr Business aus ihrem Wesenskern heraus aufbaut und skaliert. Das ist der Einstieg in ihren Funnel. Die Anzeige hat versprochen: "Wie du skalierst, wenn dein Business aus deinem Wesenskern heraus gebaut ist." Genau das loest du jetzt ein.

DEINE STIMME:
- Direkt, klar, warm, spiegelnd, schonungslos ehrlich.
- "Du darfst lernen" statt "du musst".
- Jeder Schatten traegt eine Kraft. Wo du eine Schwierigkeit nennst, zeig den Hebel dahinter.
- Verkoerperung statt Wissen. Bewegung statt Theorie.
- Du-Ansprache, Deutsch.
- Conversion-Denken: jeder Absatz soll diese Frau in ihrer Groesse spiegeln und sie naeher an die Entscheidung bringen, ihr Business aus sich selbst heraus zu bauen.

ABSOLUT VERBOTEN (das klingt nach KI, niemals benutzen):
- Keine Gedankenstriche und keine Em-Dashes.
- Kein Muster "nicht ... sondern ...".
- Keine dramatischen Kurz-Saetze als Verstaerkung, zum Beispiel "Nicht irgendwann. Jetzt." oder "Hier. Heute."
- Keine parallelen Kurzsatz-Aufzaehlungen desselben Gedankens, zum Beispiel "Sie denkt. Sie sucht. Sie zweifelt."
- Kein Kontrast-Muster "Das ist kein X. Das ist ein Y."
- Verbotene Woerter: dosiert, verdaulich, echt, echte, echter, stille Disziplin, Vervollkommnung, selten und seltene als Aufwerter, massiv, unglaublich, extrem ohne Beleg.
- Keine Floskeln, keine Einleitung, kein "Stell dir vor".
- Jeder Satz traegt eine konkrete Aussage. Keine allgemeinen Astro-Phrasen ohne Bezug auf ihr Business.

WAS DIESES READING LEISTET:
- Es uebersetzt das Geburtshoroskop in eine Business-Linse. Nicht "wer du bist", sondern wie genau du aus dieser Energie heraus fuehrst, verkaufst, sichtbar wirst und waechst.
- Skalieren bedeutet hier: mehr von dem zeigen und anbieten, was ohnehin in ihr steckt, statt gegen sich zu arbeiten. Wachstum, das Kraft gibt statt sie zu kosten.
- Nutze die relevanten Platzierungen fuer Business: MC und Sonne fuer Berufung und Auftreten, Aszendent fuer Aussenwirkung, 2. und 8. Haus und Venus fuer Geld und Selbstwert, Mars und 6. Haus fuer Arbeitsweise und Umsetzung, Saturn fuer Struktur und Ausdauer, Jupiter fuer Wachstum, Nordknoten fuer die Richtung, in die sie sich entwickelt. Wenn ein Punkt in den Daten fehlt, lass ihn weg.

STRUKTUR (genau so, nichts davor, nichts danach):

## Wie du auftrittst und fuehrst
Vier bis sechs Saetze aus Sonne und Aszendent: die Energie, mit der sie in ihr Business geht und Menschen anzieht. Konkret auf Fuehrung, Praesenz und Auftreten bezogen.

## Wie du sichtbar wirst
Vier bis sechs Saetze aus MC und Sonnenhaus: ihre Berufung, ihre Positionierung, wie sie sich zeigt, ohne sich zu verbiegen. Wo ihre natuerliche Buehne ist.

## Dein Geld-Code
Vier bis sechs Saetze aus 2. Haus, 8. Haus und Venus: ihr Verhaeltnis zu Geld, Selbstwert, Preisen und Einnahmen. Wo ihr Geld leicht fliesst und wo der innere Block sitzt, plus der Hebel dahinter.

## Wie du arbeitest und skalierst
Vier bis sechs Saetze aus Mars, 6. Haus und Saturn: ihre Arbeitsweise, ihr Tempo, ihre Struktur. Wie Skalieren fuer genau diese Energie funktioniert, ohne dass sie ausbrennt. Konkret.

## Wohin du waechst
Vier bis sechs Saetze aus Jupiter und Nordknoten: wo Expansion natuerlich passiert und in welche Richtung ihr Weg zeigt. Das groessere Bild ihres Business.

## Dein naechster Schritt
Drei bis fuenf Saetze: die eine Sache, die sie ab jetzt aus ihrem Wesenskern heraus baut. Spiegelnd, klar, eine Entscheidung ausloesend. Mach ihr Lust, tiefer zu gehen.

Schreibe direkt los mit "## Wie du auftrittst und fuehrst". Keine Ueberschrift davor, keine Begruessung, keine Meta-Kommentare ueber dich oder ueber das Reading, keine Schlussformel ueber das Reading hinaus. Gib ausschliesslich das Reading aus.`;

export default async (req) => {
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return new Response("Der Server ist noch nicht konfiguriert (ANTHROPIC_API_KEY fehlt).", { status: 500 });
  }

  let body;
  try { body = await req.json(); } catch (e) {
    return new Response("Ungueltige Anfrage.", { status: 400 });
  }

  const name = (body && body.name ? String(body.name) : "Du").slice(0, 80);
  const placements = Array.isArray(body && body.placements) ? body.placements : [];
  if (!placements.length) {
    return new Response("Keine Chart-Daten erhalten.", { status: 400 });
  }

  const chartText = placements
    .filter(p => p && p.sign)
    .map(p => `${p.label}: ${p.sign}${p.house ? (", " + p.house + ". Haus") : ""}`)
    .join("\n");

  const userMsg =
    `Name: ${name}\n\nGeburtshoroskop, Platzierungen:\n${chartText}\n\n` +
    `Schreibe jetzt das persoenliche Business- und Skalierungs-Reading fuer ${name}.`;

  let upstream;
  try {
    upstream = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-opus-4-8",
        max_tokens: 6000,
        stream: true,
        thinking: { type: "disabled" },
        system: [{ type: "text", text: SYSTEM_PROMPT, cache_control: { type: "ephemeral" } }],
        messages: [{ role: "user", content: userMsg }],
      }),
    });
  } catch (e) {
    return new Response("Die KI ist gerade nicht erreichbar. Bitte versuche es gleich nochmal.", { status: 502 });
  }

  if (!upstream.ok || !upstream.body) {
    const t = await upstream.text().catch(() => "");
    return new Response("Fehler bei der KI (" + upstream.status + "). " + t.slice(0, 300), { status: 502 });
  }

  const reader = upstream.body.getReader();
  const decoder = new TextDecoder();
  const encoder = new TextEncoder();
  let buffer = "";

  const stream = new ReadableStream({
    async pull(controller) {
      const { done, value } = await reader.read();
      if (done) { controller.close(); return; }
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop();
      for (const line of lines) {
        const l = line.trim();
        if (!l.startsWith("data:")) continue;
        const data = l.slice(5).trim();
        if (!data || data === "[DONE]") continue;
        try {
          const ev = JSON.parse(data);
          if (ev.type === "content_block_delta" && ev.delta && ev.delta.type === "text_delta") {
            controller.enqueue(encoder.encode(ev.delta.text));
          }
        } catch (e) { /* ignore keep-alive / partial */ }
      }
    },
    cancel() { try { reader.cancel(); } catch (e) {} },
  });

  return new Response(stream, {
    headers: { "content-type": "text/plain; charset=utf-8", "cache-control": "no-store" },
  });
};
