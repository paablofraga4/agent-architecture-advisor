"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { listRuns, RunSummary } from "@/lib/api";

export default function RunsPage() {
  const [clientId, setClientId] = useState<string>("");
  const [runs, setRuns] = useState<RunSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await listRuns(clientId || undefined);
      setRuns(r);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Historial de runs</h1>
      <div className="flex items-center gap-2">
        <input
          value={clientId}
          onChange={(e) => setClientId(e.target.value)}
          placeholder="filtrar por cliente (vacío = todos)"
          className="bg-bg border border-border rounded px-3 py-1 text-sm flex-1 max-w-xs"
        />
        <button
          onClick={load}
          className="bg-accent text-bg rounded px-3 py-1 text-sm"
        >
          Recargar
        </button>
      </div>

      {error && <div className="text-err text-sm">{error}</div>}
      {loading && <div className="text-muted text-sm">Cargando…</div>}

      <table className="w-full text-sm">
        <thead className="text-left text-muted border-b border-border">
          <tr>
            <th className="py-2">Run ID</th>
            <th>Cliente</th>
            <th>Fecha</th>
            <th>Proyecto</th>
            <th>Winner</th>
            <th>Confianza</th>
          </tr>
        </thead>
        <tbody>
          {runs.map((r) => (
            <tr key={r.run_id} className="border-b border-border/50">
              <td className="py-2 font-mono text-xs">{r.run_id}</td>
              <td>{r.client_id}</td>
              <td className="text-muted">{r.timestamp_utc}</td>
              <td>{r.project_summary || "—"}</td>
              <td className="font-semibold">{r.verdict_winner?.toUpperCase() || "—"}</td>
              <td>{r.verdict_confidence || "—"}</td>
            </tr>
          ))}
          {!loading && runs.length === 0 && (
            <tr>
              <td colSpan={6} className="text-muted py-4 text-center">
                No hay runs todavía. <Link href="/" className="text-accent">Lanza uno</Link>.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
