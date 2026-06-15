"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { WORKSPACES, useWorkspace } from "@/lib/workspace";
import BrandMark from "@/components/BrandMark";

const NAV = [
  { href: "/", label: "Advisor" },
  { href: "/runs", label: "Historial" },
  { href: "/kb", label: "Base de conocimiento" },
];

export default function Header() {
  const { workspace, setWorkspaceId } = useWorkspace();
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

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
          <button
            onClick={() => setOpen((o) => !o)}
            className="flex items-center gap-2 rounded-lg border border-border bg-bg px-2 py-1.5 text-sm hover:border-accent"
          >
            <BrandMark workspace={workspace} size={26} />
            <span className="hidden sm:block text-left leading-tight">
              <span className="block">{workspace.name}</span>
              <span className="block text-[10px] text-muted">{workspace.plan}</span>
            </span>
            <span className="text-muted">▾</span>
          </button>

          {open && (
            <>
              <div
                className="fixed inset-0 z-10"
                onClick={() => setOpen(false)}
              />
              <div className="absolute right-0 z-20 mt-2 w-72 rounded-xl border border-border bg-panel p-1.5 shadow-xl">
                <div className="px-2 py-1.5 text-[10px] uppercase tracking-wide text-muted">
                  Cambiar de workspace
                </div>
                {WORKSPACES.map((w) => (
                  <button
                    key={w.id}
                    onClick={() => {
                      setWorkspaceId(w.id);
                      setOpen(false);
                    }}
                    className={`flex w-full items-center gap-3 rounded-lg px-2 py-2 text-left hover:bg-bg ${
                      w.id === workspace.id ? "bg-bg" : ""
                    }`}
                  >
                    <BrandMark workspace={w} size={32} className="shrink-0" />
                    <span className="min-w-0">
                      <span className="block text-sm">{w.name}</span>
                      <span className="block truncate text-xs text-muted">
                        {w.role}
                      </span>
                    </span>
                    {w.id === workspace.id && (
                      <span className="ml-auto text-accent">✓</span>
                    )}
                  </button>
                ))}
                <div className="border-t border-border px-2 py-1.5 text-[10px] text-muted">
                  Sin login · cada workspace aísla historial y KB por{" "}
                  <code className="font-mono">client_id</code>.
                </div>
              </div>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
