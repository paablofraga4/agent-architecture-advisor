"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/lib/auth";

const NAV = [
  { href: "/", label: "Advisor" },
  { href: "/runs", label: "Historial" },
  { href: "/kb", label: "Base de conocimiento" },
];

export default function Header() {
  const { authConfigured, email, quota, signOut } = useAuth();
  const [open, setOpen] = useState(false);
  const pathname = usePathname();
  const router = useRouter();

  const loggedIn = !authConfigured || Boolean(email);
  const initials = (email || "yo").slice(0, 2).toUpperCase();
  const planLabel = !authConfigured
    ? "Local"
    : quota?.is_admin
    ? "Admin · ilimitado"
    : quota
    ? `Free · ${quota.runs_used}/${quota.run_limit}`
    : "Free";

  return (
    <header className="no-print sticky top-0 z-20 border-b border-border bg-panel/80 backdrop-blur">
      <nav className="mx-auto max-w-7xl px-4 py-3 flex items-center gap-6">
        <Link href="/" className="flex items-center gap-2 font-semibold">
          <span
            className="grid h-7 w-7 place-items-center rounded-md text-xs font-bold text-bg"
            style={{ backgroundColor: "rgb(var(--accent))" }}
          >
            AA
          </span>
          <span>Architecture&nbsp;Advisor</span>
        </Link>

        <div className="flex items-center gap-1 text-sm">
          {NAV.map((n) => {
            const active =
              n.href === "/" ? pathname === "/" : pathname.startsWith(n.href);
            return (
              <Link
                key={n.href}
                href={n.href}
                className={`rounded px-2 py-1 ${
                  active ? "text-accent" : "text-muted hover:text-white"
                }`}
              >
                {n.label}
              </Link>
            );
          })}
        </div>

        <div className="relative ml-auto">
          {!loggedIn ? (
            <Link
              href="/login"
              className="rounded-lg bg-accent px-3 py-1.5 text-sm font-medium text-bg"
            >
              Entrar
            </Link>
          ) : (
            <>
              <button
                onClick={() => setOpen((o) => !o)}
                className="flex items-center gap-2 rounded-lg border border-border bg-bg px-2 py-1.5 text-sm hover:border-accent"
              >
                <span
                  className="grid h-7 w-7 place-items-center rounded-full text-[11px] font-bold text-bg"
                  style={{ backgroundColor: "rgb(var(--accent))" }}
                >
                  {initials}
                </span>
                <span className="hidden sm:block text-left leading-tight">
                  <span className="block max-w-[160px] truncate">
                    {email || "Sesión local"}
                  </span>
                  <span className="block text-[10px] text-muted">{planLabel}</span>
                </span>
                <span className="text-muted">▾</span>
              </button>

              {open && (
                <>
                  <div
                    className="fixed inset-0 z-10"
                    onClick={() => setOpen(false)}
                  />
                  <div className="absolute right-0 z-20 mt-2 w-64 rounded-xl border border-border bg-panel p-1.5 shadow-xl">
                    <div className="px-2 py-2">
                      <div className="truncate text-sm">{email || "Sesión local"}</div>
                      <div className="text-[11px] text-muted">{planLabel}</div>
                    </div>
                    {quota && !quota.is_admin && (
                      <div className="border-t border-border px-2 py-2 text-[11px] text-muted">
                        Has usado {quota.runs_used} de {quota.run_limit} runs.
                      </div>
                    )}
                    {authConfigured && (
                      <button
                        onClick={async () => {
                          setOpen(false);
                          await signOut();
                          router.push("/login");
                        }}
                        className="mt-1 w-full rounded-lg px-2 py-2 text-left text-sm hover:bg-bg"
                      >
                        Cerrar sesión
                      </button>
                    )}
                  </div>
                </>
              )}
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
