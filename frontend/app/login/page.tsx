"use client";

import { Suspense, useState } from "react";
import { useSearchParams } from "next/navigation";
import { useAuth } from "@/lib/auth";

function LoginInner() {
  const params = useSearchParams();
  const next = params.get("next") || "/run";
  const { signInWithEmail, signInWithGoogle, authConfigured } = useAuth();
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  if (!authConfigured) {
    return (
      <div className="mx-auto max-w-md rounded-xl border border-border bg-panel p-6 text-sm text-muted">
        Auth no configurada en este entorno (modo local abierto). Puedes ir
        directamente a <a className="text-accent" href={next}>la app</a>.
      </div>
    );
  }

  async function onEmail(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const { error } = await signInWithEmail(email, next);
    setLoading(false);
    if (error) setError(error);
    else setSent(true);
  }

  return (
    <div className="mx-auto max-w-md space-y-6 rounded-2xl border border-border bg-panel p-8">
      <div>
        <h1 className="text-2xl font-semibold">Entrar</h1>
        <p className="mt-1 text-sm text-muted">
          Tu primera recomendación es gratis. Accede para empezar.
        </p>
      </div>

      {sent ? (
        <div className="rounded-lg border border-ok/40 bg-ok/10 p-4 text-sm">
          Te hemos enviado un enlace mágico a <strong>{email}</strong>. Ábrelo
          para entrar.
        </div>
      ) : (
        <>
          <button
            onClick={() => signInWithGoogle(next)}
            className="w-full rounded-lg border border-border bg-bg px-4 py-2.5 text-sm font-medium hover:border-accent"
          >
            Continuar con Google
          </button>

          <div className="flex items-center gap-3 text-xs text-muted">
            <div className="h-px flex-1 bg-border" />o<div className="h-px flex-1 bg-border" />
          </div>

          <form onSubmit={onEmail} className="space-y-3">
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="tu@email.com"
              className="w-full rounded-lg border border-border bg-bg px-4 py-2.5 text-sm outline-none focus:border-accent"
            />
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-accent px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-60"
            >
              {loading ? "Enviando…" : "Enviar enlace mágico"}
            </button>
          </form>

          {error && <div className="text-sm text-err">{error}</div>}
        </>
      )}
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense fallback={<div className="text-muted">Cargando…</div>}>
      <LoginInner />
    </Suspense>
  );
}
