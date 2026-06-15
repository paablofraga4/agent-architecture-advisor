"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getRun } from "@/lib/api";
import Report from "@/components/Report";
import ArchitectureImage from "@/components/ArchitectureImage";
import ExportBar from "@/components/ExportBar";
import ReportBrandHeader from "@/components/ReportBrandHeader";

function Stat({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="rounded-lg border border-border bg-bg p-3">
      <div className="text-[10px] uppercase tracking-wide text-muted">{label}</div>
      <div className="mt-1 text-sm">{value}</div>
    </div>
  );
}

export default function RunDetailPage({
  params,
}: {
  params: { run_id: string };
}) {
  const [rec, setRec] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getRun(params.run_id)
      .then(setRec)
      .catch((e) => setError(String(e)));
  }, [params.run_id]);

  if (error)
    return (
      <div className="space-y-3">
        <div className="text-err">{error}</div>
        <Link href="/runs" className="text-accent text-sm">
          ← Volver al historial
        </Link>
      </div>
    );
  if (!rec) return <div className="text-muted">Cargando run…</div>;

  const exec = rec.execution || {};
  const verdict = rec.verdict;
  const summary = rec.result_summary || {};

  return (
    <div className="space-y-6">
      <div className="no-print flex flex-wrap items-center justify-between gap-3">
        <div>
          <Link href="/runs" className="text-accent text-sm">
            ← Historial
          </Link>
          <h1 className="mt-1 font-mono text-lg">{rec.run_id}</h1>
          <p className="text-sm text-muted">
            Workspace {rec.client_id} · {rec.timestamp_utc}
          </p>
        </div>
        <ExportBar
          markdown={rec.final_architecture_proposal || ""}
          baseName={`recomendacion-${rec.client_id}-${rec.run_id}`}
          json={rec}
        />
      </div>

      <div className="print-area space-y-6">
        <ReportBrandHeader
          workspaceId={rec.client_id}
          subtitle={summary.project_summary}
          runId={rec.run_id}
          date={rec.timestamp_utc}
        />
        <section className="rounded-xl border border-border bg-panel p-5">
          <h2 className="mb-3 text-lg font-semibold">{summary.project_summary}</h2>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            <Stat
              label="Ganador"
              value={
                <span className="font-semibold text-accent">
                  {verdict?.winner?.toUpperCase() || "—"}
                </span>
              }
            />
            <Stat label="Confianza" value={verdict?.confidence || "—"} />
            <Stat label="Gap" value={`${verdict?.score_gap ?? "—"}/100`} />
            <Stat label="Duración" value={`${rec.duration_seconds}s`} />
          </div>
          {verdict?.reasoning_summary && (
            <p className="mt-3 text-sm text-muted">{verdict.reasoning_summary}</p>
          )}
        </section>

        {rec.mermaid_diagram && (
          <section>
            <h2 className="mb-2 text-lg font-semibold">Arquitectura</h2>
            <ArchitectureImage d2={rec.mermaid_diagram} />
          </section>
        )}

        {rec.final_architecture_proposal && (
          <section>
            <h2 className="mb-2 text-lg font-semibold">Propuesta detallada</h2>
            <Report markdown={rec.final_architecture_proposal} />
          </section>
        )}

        <section className="rounded-xl border border-border bg-panel p-5 text-xs text-muted">
          <h3 className="mb-2 text-sm font-semibold text-white">Firma auditable</h3>
          <div className="grid grid-cols-1 gap-1 sm:grid-cols-2">
            <div>Modelo: <code className="font-mono">{exec.model}</code></div>
            <div>Seed: <code className="font-mono">{exec.seed}</code> · Temp: {exec.temperature}</div>
            <div className="truncate">KB hash: <code className="font-mono">{exec.kb_hash}</code></div>
            <div className="truncate">Prompts hash: <code className="font-mono">{exec.prompts_hash}</code></div>
            <div className="truncate sm:col-span-2">
              Firma: <code className="font-mono">{rec.signature_sha256}</code>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
