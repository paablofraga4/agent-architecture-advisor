import "./globals.css";
import type { Metadata } from "next";
import type { ReactNode } from "react";
import Providers from "@/components/Providers";
import Header from "@/components/Header";

export const metadata: Metadata = {
  title: "Architecture Advisor — multi-agent cloud advisory",
  description:
    "Agentes que debaten AWS / Azure / GCP y producen una arquitectura justificada, con citas, costes, diagrama y firma auditable.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="es" className="dark">
      <body className="min-h-screen font-sans">
        <Providers>
          <Header />
          <main className="mx-auto max-w-7xl px-4 py-6">{children}</main>
        </Providers>
      </body>
    </html>
  );
}
