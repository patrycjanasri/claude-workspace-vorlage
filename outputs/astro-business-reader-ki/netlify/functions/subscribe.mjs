// Business-Code Reader — Netlify Function
// Traegt eine Lead ueber die GetResponse-API in die Liste (Campaign) ein.
// Der API-Key liegt ausschliesslich serverseitig als Umgebungsvariable GETRESPONSE_API_KEY.
//
// Benoetigte Umgebungsvariablen im Netlify-Dashboard:
//   GETRESPONSE_API_KEY    (Pflicht)  — dein API-Key aus GetResponse (Einstellungen -> API)
//   GETRESPONSE_LIST_NAME  (einfach)  — der Name deiner Liste, z.B. "Business-Code"
//     ODER
//   GETRESPONSE_CAMPAIGN_ID (direkt)  — die Listen-ID, falls du sie kennst
//
// Wenn GETRESPONSE_LIST_NAME gesetzt ist, sucht die Funktion die ID selbst.

const GR = "https://api.getresponse.com/v3";

let cachedCampaignId = null;

async function grFetch(path, apiKey, options = {}) {
  return fetch(GR + path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-Auth-Token": "api-key " + apiKey,
      ...(options.headers || {})
    }
  });
}

async function resolveCampaignId(apiKey) {
  if (process.env.GETRESPONSE_CAMPAIGN_ID) return process.env.GETRESPONSE_CAMPAIGN_ID;
  if (cachedCampaignId) return cachedCampaignId;

  const wanted = (process.env.GETRESPONSE_LIST_NAME || "").trim().toLowerCase();
  if (!wanted) return null;

  const res = await grFetch("/campaigns?perPage=1000", apiKey);
  if (!res.ok) return null;
  const list = await res.json();
  const hit = (Array.isArray(list) ? list : []).find(
    c => (c.name || "").trim().toLowerCase() === wanted
  );
  if (hit) { cachedCampaignId = hit.campaignId; return hit.campaignId; }
  return null;
}

export default async (req) => {
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  const apiKey = process.env.GETRESPONSE_API_KEY;
  if (!apiKey) {
    return json({ ok: false, error: "Server nicht konfiguriert (GETRESPONSE_API_KEY fehlt)." }, 500);
  }

  let body;
  try { body = await req.json(); } catch (e) {
    return json({ ok: false, error: "Ungueltige Anfrage." }, 400);
  }

  const email = (body && body.email ? String(body.email) : "").trim();
  const name = (body && body.name ? String(body.name) : "").trim().slice(0, 120);
  const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  if (!emailOk) {
    return json({ ok: false, error: "Keine gueltige E-Mail-Adresse." }, 400);
  }

  const campaignId = await resolveCampaignId(apiKey);
  if (!campaignId) {
    return json({ ok: false, error: "Liste nicht gefunden. Pruefe GETRESPONSE_LIST_NAME oder GETRESPONSE_CAMPAIGN_ID." }, 500);
  }

  const payload = { email, campaign: { campaignId } };
  if (name) payload.name = name;

  let res;
  try {
    res = await grFetch("/contacts", apiKey, { method: "POST", body: JSON.stringify(payload) });
  } catch (e) {
    return json({ ok: false, error: "GetResponse nicht erreichbar." }, 502);
  }

  // 202 Accepted = neuer Kontakt wird verarbeitet.
  if (res.status === 202) return json({ ok: true });

  // 409 = Kontakt existiert schon. Fuer uns kein Fehler.
  if (res.status === 409) return json({ ok: true, existing: true });

  let detail = "";
  try { detail = JSON.stringify(await res.json()); } catch (e) {}
  return json({ ok: false, error: "GetResponse hat abgelehnt (" + res.status + ").", detail }, 502);
};

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" }
  });
}
