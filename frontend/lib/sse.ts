import { API_BASE, getAccessToken, QuotaError } from "./api";

export type SseEvent = { event: string; data: any };

/**
 * POST-based SSE. EventSource only supports GET, so we use fetch + ReadableStream
 * to parse the text/event-stream body coming from /arena/run.
 *
 * The tenant (client_id) is derived server-side from the auth token, so the body
 * only carries the idea + optional model override.
 */
export async function streamArenaRun(
  body: { idea: string; model?: string },
  onEvent: (e: SseEvent) => void,
  signal?: AbortSignal
) {
  const token = await getAccessToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Accept: "text/event-stream",
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const r = await fetch(`${API_BASE}/arena/run`, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
    signal,
  });
  if (r.status === 402) {
    let detail: any = null;
    try {
      detail = (await r.json())?.detail;
    } catch {
      /* ignore */
    }
    throw new QuotaError(detail);
  }
  if (!r.ok) throw new Error(`run failed: ${r.status}`);
  if (!r.body) throw new Error("No response body");

  const reader = r.body.getReader();
  const decoder = new TextDecoder();
  let buf = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });

    // SSE events are separated by "\n\n"
    let sep: number;
    while ((sep = buf.indexOf("\n\n")) !== -1) {
      const chunk = buf.slice(0, sep);
      buf = buf.slice(sep + 2);
      const evt = parseSseChunk(chunk);
      if (evt) onEvent(evt);
    }
  }
}

function parseSseChunk(chunk: string): SseEvent | null {
  let event = "message";
  const dataLines: string[] = [];
  for (const line of chunk.split("\n")) {
    if (line.startsWith("event:")) event = line.slice(6).trim();
    else if (line.startsWith("data:")) dataLines.push(line.slice(5).trim());
  }
  if (dataLines.length === 0) return null;
  const raw = dataLines.join("\n");
  let data: any = raw;
  try {
    data = JSON.parse(raw);
  } catch {
    /* keep as string */
  }
  return { event, data };
}
