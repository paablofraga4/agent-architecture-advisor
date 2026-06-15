"use client";

import { Suspense, useEffect, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import PipelineGraph, { EVENT_MAP, emptyState, PipelineState } from "@/components/PipelineGraph";
import Report from "@/components/Report";
import ArchitectureImage from "@/components/ArchitectureImage";
import ExportBar from "@/components/ExportBar";
import { streamArenaRun } from "@/lib/sse";

function RunInner() {
  const params = useSearchParams();
  const idea = params.get("idea") || "";
  const clientId = params.get("client_id") || "default";

  const [state, setState] = useState<PipelineState>(emptyState());
  const [log, setLog] = useState<string[]>([]);
  const [finalProposal, setFinalProposal] = useState<string>("");
  const [diagramSrc, setDiagramSrc] = useState<string>("");
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState(false);

  const startedRef = useRef(false);
  useEffect(() => {
    if (startedRef.current || !idea) return;
    startedRef.current = true;
    const ctrl = new AbortController();

    streamArenaRun(
      { idea, client_id: clientId },
      (evt) => {
        setLog((l) => [...l, `[${evt.event}]`]);

        const map = EVENT_MAP[evt.event];
        if (map) {
          setState((s) => ({ ...s, [map[0]]: map[1] }));
        }

        if (evt.event === "final_architecture_finished" && evt.data?.proposal) {
          setFinalProposal(evt.data.proposal);
        }
        if (evt.event === "diagram_generation_finished" && evt.data?.mermaid_diagram) {
          setDiagramSrc(evt.data.mermaid_diagram); // field is actually D2 now
        }
        if (evt.event === "result") {
          setResult(evt.data);
          if (evt.data?.final_architecture_proposal)
            setFinalProposal(evt.data.final_architecture_proposal);
          if (evt.data?.mermaid_diagram) setDiagramSrc(evt.data.mermaid_diagram);
        }
        if (evt.event === "error") {
          setError(typeof evt.data === "string" ? evt.data : evt.data?.error || "unknown");
        }
        if (evt.event === "done") setDone(true);
      },
      ctrl.signal
    ).catch((e) => {
      // React StrictMode double-mounts in dev — ignore the resulting abort.
      if (e?.name === "AbortError" || String(e).includes("aborted")) return;
      setError(String(e));
    });

    return () => ctrl.abort();
  }, [idea, clientId]);

  return (
    <div className="space-y-6">
      <section className="no-print flex items-start justify-between gap-4 rounded-xl border border-border bg-panel p-4">
        <div>
          <div className="text-xs text-muted">Workspace: {clientId}</div>
          <div className="text-sm">{idea}</div>
        </div>
        {finalProposal && (
          <ExportBar
            markdown={finalProposal}
            baseName={`recomendacion-${clientId}-${result?.run_id || "draft"}`}
            json={result ?? undefined}
          />
        )}
      </section>

      <section className="no-print">
        <h2 className="text-lg font-semibold mb-2">Pipeline en vivo</h2>
        <PipelineGraph state={state} />
      </section>

      <div className="print-area space-y-6">

      {result?.verdict && (
        <section className="rounded-xl border border-border bg-panel p-5">
          <h2 className="text-lg font-semibold mb-2">Veredicto</h2>
          <div className="text-2xl font-bold text-accent">
            {result.verdict.winner?.toUpperCase()}{" "}
            <span className="text-sm font-normal text-muted">
              · confianza {result.verdict.confidence} · gap {result.verdict.score_gap}/100
            </span>
          </div>
          <p className="text-sm text-muted mt-2">{result.verdict.reasoning_summary}</p>
        </section>
      )}

      {diagramSrc && (
        <section>
          <h2 className="text-lg font-semibold mb-2">Arquitectura propuesta</h2>
          <ArchitectureImage d2={diagramSrc} />
        </section>
      )}

      {finalProposal && (
        <section>
          <h2 className="text-lg font-semibold mb-2">Propuesta detallada</h2>
          <Report markdown={finalProposal} />
        </section>
      )}

      {result?.specialist_findings?.length > 0 && (
        <section>
          <h2 className="text-lg font-semibold mb-2">Hallazgos de especialistas</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {result.specialist_findings.map((r: any, i: number) => (
              <div key={i} className="rounded-xl border border-border bg-panel p-4">
                <div className="font-semibold uppercase text-accent">{r.agent}</div>
                {r.overall_concern && (
                  <p className="text-sm text-muted italic mt-1">{r.overall_concern}</p>
                )}
                <ul className="text-sm mt-2 space-y-1">
                  {r.findings?.map((f: any, j: number) => (
                    <li key={j}>
                      <span
                        className={
                          f.severity === "high"
                            ? "text-err"
                            : f.severity === "medium"
                            ? "text-warn"
                            : "text-ok"
                        }
                      >
                        ●
                      </span>{" "}
                      <strong>{f.topic}</strong> ({f.applies_to?.join("/")}) — {f.recommendation}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>
      )}
      </div>

      {result?.run_id && (
        <footer className="text-xs text-muted">
          Run firmado: <code className="font-mono">{result.run_id}</code> ·{" "}
          cliente <code className="font-mono">{result.client_id}</code>
        </footer>
      )}

      {error && (
        <div className="rounded-xl border border-err bg-err/10 p-4 text-err">{error}</div>
      )}

      {!done && !error && (
        <div className="text-xs text-muted">
          Streaming… {log.length} eventos recibidos.
        </div>
      )}
    </div>
  );
}

export default function RunPage() {
  return (
    <Suspense fallback={<div className="text-muted">Cargando…</div>}>
      <RunInner />
    </Suspense>
  );
}
