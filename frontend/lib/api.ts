import { getSupabaseBrowser, AUTH_CONFIGURED } from "./supabase/client";

export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8080";

/** Current Supabase access token, or null when auth is off / logged out. */
export async function getAccessToken(): Promise<string | null> {
  if (!AUTH_CONFIGURED) return null;
  try {
    const sb = getSupabaseBrowser();
    const { data } = await sb.auth.getSession();
    return data.session?.access_token ?? null;
  } catch {
    return null;
  }
}

/** fetch() that attaches the Bearer token when available. */
export async function authedFetch(input: string, init: RequestInit = {}) {
  const token = await getAccessToken();
  const headers = new Headers(init.headers);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  return fetch(input, { ...init, headers });
}

/** Thrown when the backend reports the free trial is spent (HTTP 402). */
export class QuotaError extends Error {
  constructor(public detail: any) {
    super("QUOTA_EXCEEDED");
    this.name = "QuotaError";
  }
}

export type RunSummary = {
  run_id: string;
  client_id: string;
  timestamp_utc: string;
  project_summary: string | null;
  verdict_winner: string | null;
  verdict_confidence: string | null;
};

export async function listRuns(): Promise<RunSummary[]> {
  const r = await authedFetch(`${API_BASE}/arena/runs`, { cache: "no-store" });
  if (!r.ok) throw new Error(`listRuns failed: ${r.status}`);
  const data = await r.json();
  return data.runs ?? [];
}

export async function getRun(runId: string): Promise<any> {
  const r = await authedFetch(`${API_BASE}/arena/runs/${runId}`, {
    cache: "no-store",
  });
  if (!r.ok) throw new Error(`getRun failed: ${r.status}`);
  return r.json();
}

export async function uploadDoc(
  file: File,
  docType = "project_case",
  title?: string
) {
  const fd = new FormData();
  fd.append("file", file);
  fd.append("doc_type", docType);
  if (title) fd.append("title", title);
  const r = await authedFetch(`${API_BASE}/arena/upload`, {
    method: "POST",
    body: fd,
  });
  if (!r.ok) throw new Error(`upload failed: ${r.status}`);
  return r.json();
}
