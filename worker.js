const ALLOWED_FIELDS = new Set([
  "event",
  "stage",
  "ms",
  "total_ms",
  "bytes",
  "message",
  "source",
  "line",
]);

const MAX_STRING = 300;
const MAX_BODY = 2048;

function sanitize(raw) {
  if (typeof raw !== "object" || raw === null || Array.isArray(raw)) return null;
  const clean = {};
  for (const key of Object.keys(raw)) {
    if (!ALLOWED_FIELDS.has(key)) continue; 
    const v = raw[key];
    if (typeof v === "number" && Number.isFinite(v)) clean[key] = v;
    else if (typeof v === "boolean") clean[key] = v;
    else if (typeof v === "string") clean[key] = v.slice(0, MAX_STRING);
  }
  return Object.keys(clean).length ? clean : null;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/_log" && request.method === "POST") {
      try {
        const body = await request.text();
        if (body.length <= MAX_BODY) {
          const event = sanitize(JSON.parse(body));
          if (event) {
            console.log(JSON.stringify({ ...event, ua: request.headers.get("user-agent") ?? "" }));
          }
        }
      } catch (e) {
      }
      return new Response(null, { status: 204 });
    }

    return env.ASSETS.fetch(request);
  },
};
