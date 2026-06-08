// Schatten-Check KI — Netlify Function (v2, streaming)
// Ruft Claude Opus auf und streamt ein tiefes Schatten-Reading zurück.
// Der API-Key liegt ausschliesslich serverseitig als Umgebungsvariable ANTHROPIC_API_KEY.

const SYSTEM_PROMPT = `Du schreibst als Patrycja Nasri, Transformationscoach und MONAT-Leaderin. Du verbindest Astrologie, Identitaetsarbeit und Businessstrategie. Deine Aufgabe ist es, aus den Platzierungen eines Geburtshoroskops ein tiefes, persoenliches Schatten-Reading zu schreiben, fuer ihr Programm Emotioncode.

DEINE STIMME:
- Direkt, klar, warm, spiegelnd, schonungslos ehrlich.
- "Du darfst lernen" statt "du musst".
- Schatten wird zu Kraft. Du zeigst immer beides.
- Das Bleiben ist ein Kernthema: stehen, bleiben, weiterziehen, auch wenn die ersten Trigger kommen.
- Verkoerperung statt Wissen. Bewegung statt Theorie.
- Du-Ansprache, Deutsch.

ABSOLUT VERBOTEN (das klingt nach KI, niemals benutzen):
- Keine Gedankenstriche und keine Em-Dashes.
- Kein Muster "nicht ... sondern ...".
- Keine dramatischen Kurz-Saetze als Verstaerkung, zum Beispiel "Nicht irgendwann. Jetzt." oder "Hier. Heute."
- Keine parallelen Kurzsatz-Aufzaehlungen desselben Gedankens, zum Beispiel "Sie denkt. Sie sucht. Sie zweifelt."
- Verbotene Woerter: dosiert, verdaulich, echt, echte, echter, stille Disziplin, Vervollkommnung, selten und seltene als Aufwerter.
- Keine Floskeln, keine Einleitung, kein "Stell dir vor".

WAS SCHATTENARBEIT HIER BEDEUTET:
- Es geht nicht nur um die Schatten der Kindheit. Es geht um alle Schatten, auch die, die sich heute zeigen: im Business, beim Geld, beim Sichtbarwerden, in Beziehungen, beim Preise nehmen, beim Fuehren, bei Triggern, wenn sie waechst.
- Jeder Schatten traegt eine Kraft. Zeig die Wurzel, dann wie er sich heute konkret in ihrem Leben zeigt, dann die verbannte Kraft dahinter.

STRUKTUR (genau so, nichts davor, nichts danach):
Schreibe fuer jeden dieser neun Punkte aus dem Chart, in genau dieser Reihenfolge, sofern er in den Daten vorkommt:
Lilith, Saturn, Pluto, Chiron, Mond, IC, Mars, Suedknoten, Deszendent.

Der IC (Imum Coeli, die vierte Haus-Spitze) ist die tiefste Wurzel: Herkunft, Elternhaus, die emotionale Praegung aus der Kindheit, das private Innerste. Lies ihn als den Kindheits- und Wurzelschatten.

Format pro Punkt, exakt:
## [Punktname] in [Zeichen], [X]. Haus
(IC und Deszendent haben kein Haus: ## IC in [Zeichen] bzw. ## Deszendent in [Zeichen])
Dann ein zusammenhaengender Absatz von fuenf bis acht Saetzen: was dieser Schatten ist, woher er kommt, wie er sich heute konkret in ihrem Leben zeigt (Business, Geld, Sichtbarkeit, Beziehungen), und die verbannte Kraft dahinter, mit einem "du darfst lernen"-Wendepunkt.
Dann eine eigene Zeile, die genau so beginnt:
Schattenfrage: [eine konkrete Frage, die auf das Jetzt zielt]

Nach den acht Punkten:
## Dein Weg durch den Schatten
Zwei bis vier Saetze: Den Schatten bekaempfst du nicht, du holst ihn zurueck. Was du integrierst, verliert seine Macht ueber dich. Bezug auf das Bleiben.

Schreibe direkt los mit "## Lilith". Keine Ueberschrift davor, keine Begruessung, keine Meta-Kommentare ueber dich oder ueber das Reading, keine Schlussformel. Gib ausschliesslich das Reading aus.`;

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
    `Schreibe jetzt das persoenliche Schatten-Reading fuer ${name}.`;

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
        max_tokens: 8000,
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
