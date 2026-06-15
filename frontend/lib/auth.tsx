"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import type { Session } from "@supabase/supabase-js";
import { getSupabaseBrowser, AUTH_CONFIGURED } from "./supabase/client";
import { API_BASE } from "./api";

export type Quota = {
  id: string;
  email: string | null;
  role: string;
  run_limit: number;
  runs_used: number;
  has_quota: boolean;
  is_admin: boolean;
};

type Ctx = {
  ready: boolean;
  authConfigured: boolean;
  session: Session | null;
  email: string | null;
  quota: Quota | null;
  signInWithEmail: (email: string, next?: string) => Promise<{ error?: string }>;
  signInWithGoogle: (next?: string) => Promise<void>;
  signOut: () => Promise<void>;
  refreshQuota: () => Promise<void>;
};

const AuthContext = createContext<Ctx | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [ready, setReady] = useState(false);
  const [session, setSession] = useState<Session | null>(null);
  const [quota, setQuota] = useState<Quota | null>(null);

  const refreshQuota = useCallback(async () => {
    if (!AUTH_CONFIGURED) {
      setQuota(null);
      return;
    }
    try {
      const sb = getSupabaseBrowser();
      const { data } = await sb.auth.getSession();
      const token = data.session?.access_token;
      if (!token) {
        setQuota(null);
        return;
      }
      const r = await fetch(`${API_BASE}/me`, {
        headers: { Authorization: `Bearer ${token}` },
        cache: "no-store",
      });
      if (r.ok) setQuota(await r.json());
    } catch {
      /* ignore */
    }
  }, []);

  useEffect(() => {
    if (!AUTH_CONFIGURED) {
      setReady(true);
      return;
    }
    const sb = getSupabaseBrowser();
    sb.auth.getSession().then(({ data }: { data: { session: Session | null } }) => {
      setSession(data.session);
      setReady(true);
      if (data.session) refreshQuota();
    });
    const { data: sub } = sb.auth.onAuthStateChange((_e: unknown, s: Session | null) => {
      setSession(s);
      if (s) refreshQuota();
      else setQuota(null);
    });
    return () => sub.subscription.unsubscribe();
  }, [refreshQuota]);

  const signInWithEmail = useCallback(async (email: string, next?: string) => {
    const sb = getSupabaseBrowser();
    const redirectTo = `${window.location.origin}/auth/callback${
      next ? `?next=${encodeURIComponent(next)}` : ""
    }`;
    const { error } = await sb.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: redirectTo },
    });
    return { error: error?.message };
  }, []);

  const signInWithGoogle = useCallback(async (next?: string) => {
    const sb = getSupabaseBrowser();
    const redirectTo = `${window.location.origin}/auth/callback${
      next ? `?next=${encodeURIComponent(next)}` : ""
    }`;
    await sb.auth.signInWithOAuth({ provider: "google", options: { redirectTo } });
  }, []);

  const signOut = useCallback(async () => {
    const sb = getSupabaseBrowser();
    await sb.auth.signOut();
    setSession(null);
    setQuota(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{
        ready,
        authConfigured: AUTH_CONFIGURED,
        session,
        email: session?.user.email ?? null,
        quota,
        signInWithEmail,
        signInWithGoogle,
        signOut,
        refreshQuota,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): Ctx {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
