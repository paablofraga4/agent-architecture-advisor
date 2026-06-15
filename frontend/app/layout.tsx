import "./globals.css";
import Link from "next/link";
import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Agent Architecture Advisor",
  description: "Multi-agent cloud architecture advisor.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen font-sans">
        <header className="border-b border-border bg-panel/60 backdrop-blur">
          <nav className="mx-auto max-w-7xl px-4 py-3 flex items-center gap-6">
            <Link href="/" className="font-semibold text-accent">
              Agent Arena
            </Link>
            <Link href="/runs" className="text-muted hover:text-white">
              Historial
            </Link>
            <Link href="/kb" className="text-muted hover:text-white">
              KB upload
            </Link>
          </nav>
        </header>
        <main className="mx-auto max-w-7xl px-4 py-6">{children}</main>
      </body>
    </html>
  );
}
