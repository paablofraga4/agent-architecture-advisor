"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useWorkspace } from "@/lib/workspace";

const EXAMPLES = [
  "Asistente RAG sobre normativa interna de un banco español con auditoría regulatoria, datos en residencia europea y ~500 usuarios concurrentes.",
  "Pipeline de detección de fraude en tiempo real sobre transacciones de tarjeta. Latencia p99 <200ms, ~10k TPS pico.",
  "Copiloto interno para PMO que lea Jira/SharePoint/Outlook y mande resúmenes por Teams. Empresa Microsoft 365.",
  "Extracción de PDFs farmacéuticos a BI con human-in-the-loop, GDPR estricto, sin salida del tenant.",
];

const FEATURES = [
  {
    icon: "⚖️",
    title: "3 clouds debaten",
    body: "Agentes Azure, AWS y GCP defienden su propuesta; un juez neutral puntúa 4 dimensiones y declara un ganador (o un empate honesto).",
  },
  {
    icon: "🔬",
    title: "4 especialistas",
    body: "Seguridad, FinOps, Compliance y Data revisan la arquitectura y levantan hallazgos priorizados por severidad.",
  },
  {
    icon: "📐",
    title: "Diagrama + costes",
    body: "Cada recomendación incluye un diagrama de arquitectura renderizado y una estimación de coste mensual.",
  },
  {
    icon: "🔏",
    title: "Firma auditable",
    body: "Cada run se firma con SHA256 sobre KB + prompts, reproducible y consultable en el historial.",
  },
];

export default function Home() {
  const { workspace } = useWorkspace();
  const [idea, setIdea] = useState("");
  const router = useRouter();

  const submit = () => {
    if (!idea.trim()) return;
    const params = new URLSearchParams({ idea, client_id: workspace.id });
    router.push(`/run?${params.toString()}`);
  };

  return (
    <div className="space-y-12">
      {/* Hero */}
      <section className="relative overflow-hidden rounded-2xl border border-border bg-panel p-8 md:p-12">
        <div
          className="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full opacity-20 blur-3xl"
          style={{ backgroundColor: "rgb(var(--accent))" }}
        />
        <div className="relative max-w-2xl space-y-4">
          <span
            className="inline-flex items-center gap-2 rounded-full border border-border px-3 py-1 text-xs text-muted"
          >
            <span
              className="h-2 w-2 rounded-full"
              style={{ backgroundColor: "rgb(var(--accent))" }}
            />
            Workspace activo · {workspace.name}
          </span>
          <h1 className="text-4xl font-semibold leading-tight md:text-5xl">
            La arquitectura cloud correcta,{" "}
            <span className="text-accent">debatida por agentes</span>.
          </h1>
          <p className="text-lg text-muted">
            Describe tu proyecto. Tres clouds compiten, cuatro especialistas
            auditan y recibes una arquitectura justificada con citas, costes,
            diagrama y firma reproducible.
          </p>
        </div>
      </section>

      {/* Prompt card */}
      <section className="space-y-3 rounded-2xl border border-border bg-panel p-6">
        <h2 className="text-lg font-semibold">Lanza una recomendación</h2>
        <textarea
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
          rows={5}
          placeholder="Describe el proyecto, restricciones, volumen, cumplimiento…"
          className="w-full rounded-lg border border-border bg-bg p-3 text-sm focus:border-accent focus:outline-none"
        />
        <div className="flex flex-wrap gap-2">
          {EXAMPLES.map((ex, i) => (
            <button
              key={i}
              onClick={() => setIdea(ex)}
              className="rounded border border-border px-2 py-1 text-xs text-muted hover:border-accent hover:text-white"
            >
              Ejemplo {i + 1}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={submit}
            disabled={!idea.trim()}
            className="rounded-lg bg-accent px-5 py-2.5 font-medium text-bg disabled:opacity-50"
          >
            Lanzar arena →
          </button>
          <span className="text-xs text-muted">
            Se ejecutará bajo el workspace{" "}
            <code className="font-mono">{workspace.id}</code>.
          </span>
        </div>
      </section>

      {/* Features */}
      <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {FEATURES.map((f) => (
          <div
            key={f.title}
            className="panel-card rounded-2xl border border-border bg-panel p-5"
          >
            <div className="text-2xl">{f.icon}</div>
            <h3 className="mt-2 font-semibold">{f.title}</h3>
            <p className="mt-1 text-sm text-muted">{f.body}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
