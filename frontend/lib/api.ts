export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8080";

export type RunSummary = {
  run_id: string;
  client_id: string;
  timestamp_utc: string;
  project_summary: string | null;
  verdict_winner: string | null;
  verdict_confidence: string | null;
};

export async function listRuns(clientId?: string): Promise<RunSummary[]> {
  const url = new URL(`${API_BASE}/arena/runs`);
  if (clientId) url.searchParams.set("client_id", clientId);
  const r = await fetch(url.toString(), { cache: "no-store" });
  if (!r.ok) throw new Error(`listRuns failed: ${r.status}`);
  const data = await r.json();
  return data.runs ?? [];
}

export async function getRun(runId: string): Promise<any> {
  const r = await fetch(`${API_BASE}/arena/runs/${runId}`, { cache: "no-store" });
  if (!r.ok) throw new Error(`getRun failed: ${r.status}`);
  return r.json();
}

export async function uploadDoc(
  file: File,
  clientId: string,
  docType = "project_case",
  title?: string
) {
  const fd = new FormData();
  fd.append("file", file);
  fd.append("client_id", clientId);
  fd.append("doc_type", docType);
  if (title) fd.append("title", title);
  const r = await fetch(`${API_BASE}/arena/upload`, { method: "POST", body: fd });
  if (!r.ok) throw new Error(`upload failed: ${r.status}`);
  return r.json();
}
