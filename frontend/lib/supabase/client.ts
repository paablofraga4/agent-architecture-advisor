import { createBrowserClient } from "@supabase/ssr";

/**
 * Browser-side Supabase client (singleton). Reads the public anon key — safe to
 * ship to the client. Auth tokens are kept in cookies by @supabase/ssr so the
 * Next.js middleware can refresh the session on every request.
 */
let _client: ReturnType<typeof createBrowserClient> | null = null;

export function getSupabaseBrowser() {
  if (_client) return _client;
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anon = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!url || !anon) {
    throw new Error(
      "Faltan NEXT_PUBLIC_SUPABASE_URL / NEXT_PUBLIC_SUPABASE_ANON_KEY en el entorno."
    );
  }
  _client = createBrowserClient(url, anon);
  return _client;
}

/** True when Supabase env is configured (auth on). */
export const AUTH_CONFIGURED = Boolean(
  process.env.NEXT_PUBLIC_SUPABASE_URL && process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);
