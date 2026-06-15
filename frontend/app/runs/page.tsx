"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { listRuns, RunSummary } from "@/lib/api";

export default function RunsPage() {
  const [runs, setRuns] = useState<RunSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await listRuns();
      setRuns(r);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-semibold">Historial de runs</h1>
      </div>

      <p className="text-sm text-muted">Tus recomendaciones generadas.</p>

      {error && <div className="text-err text-sm">{error}</div>}
      {loading && <div className="text-muted text-sm">Cargando…</div>}

      <div className="overflow-hidden rounded-xl border border-border">
        <table className="w-full text-sm">
          <thead className="bg-panel text-left text-muted">
            <tr>
              <th className="px-3 py-2">Run ID</th>
              <th className="px-3">Workspace</th>
              <th className="px-3">Fecha</th>
              <th className="px-3">Proyecto</th>
              <th className="px-3">Ganador</th>
              <th className="px-3">Confianza</th>
            </tr>
          </thead>
          <tbody>
            {runs.map((r) => (
              <tr
                key={r.run_id}
                onClick={() => router.push(`/runs/${r.run_id}`)}
                className="cursor-pointer border-t border-border/60 hover:bg-panel"
              >
                <td className="px-3 py-2 font-mono text-xs text-accent">
                  {r.run_id}
                </td>
                <td className="px-3">{r.client_id}</td>
                <td className="px-3 text-muted">{r.timestamp_utc}</td>
                <td className="px-3">{r.project_summary || "—"}</td>
                <td className="px-3 font-semibold">
                  {r.verdict_winner?.toUpperCase() || "—"}
                </td>
                <td className="px-3">{r.verdict_confidence || "—"}</td>
              </tr>
            ))}
            {!loading && runs.length === 0 && (
              <tr>
                <td colSpan={6} className="px-3 py-6 text-center text-muted">
                  No hay runs en este workspace todavía.{" "}
                  <Link href="/" className="text-accent">
                    Lanza uno
                  </Link>
                  .
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
