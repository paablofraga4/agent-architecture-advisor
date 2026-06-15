"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const EXAMPLES = [
  "Asistente RAG sobre normativa interna de un banco español con auditoría regulatoria, datos en residencia europea y ~500 usuarios concurrentes.",
  "Pipeline de detección de fraude en tiempo real sobre transacciones de tarjeta. Latencia p99 <200ms, ~10k TPS pico.",
  "Copiloto interno para PMO que lea Jira/SharePoint/Outlook y mande resúmenes por Teams. Empresa Microsoft 365.",
  "Extracción de PDFs farmacéuticos a BI con human-in-the-loop, GDPR estricto, sin salida del tenant.",
];

export default function Home() {
  const [idea, setIdea] = useState("");
  const [clientId, setClientId] = useState("default");
  const router = useRouter();

  const submit = () => {
    if (!idea.trim()) return;
    const params = new URLSearchParams({ idea, client_id: clientId });
    router.push(`/run?${params.toString()}`);
  };

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-3xl font-semibold mb-2">Multi-agent cloud architecture advisor</h1>
        <p className="text-muted">
          Describe tu idea de proyecto. El sistema debate entre 3 clouds + 4 especialistas
          (Seguridad/FinOps/Compliance/Data) y produce una arquitectura justificada con
          citas, costes, diagrama y firma auditable.
        </p>
      </section>

      <section className="space-y-3 rounded-xl border border-border bg-panel p-5">
        <div className="flex items-center gap-3">
          <label className="text-sm text-muted">Cliente:</label>
          <input
            value={clientId}
            onChange={(e) => setClientId(e.target.value)}
            className="bg-bg border border-border rounded px-3 py-1 text-sm"
            placeholder="acme"
          />
        </div>
        <textarea
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
          rows={5}
          placeholder="Describe el proyecto…"
          className="w-full bg-bg border border-border rounded-lg p-3 text-sm font-mono focus:outline-none focus:border-accent"
        />
        <div className="flex flex-wrap gap-2">
          {EXAMPLES.map((ex, i) => (
            <button
              key={i}
              onClick={() => setIdea(ex)}
              className="text-xs border border-border rounded px-2 py-1 text-muted hover:text-white hover:border-accent"
            >
              Ejemplo {i + 1}
            </button>
          ))}
        </div>
        <button
          onClick={submit}
          disabled={!idea.trim()}
          className="bg-accent text-bg font-medium rounded px-4 py-2 disabled:opacity-50"
        >
          Lanzar arena
        </button>
      </section>
    </div>
  );
}
