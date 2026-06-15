"use client";

import { useState } from "react";
import { uploadDoc } from "@/lib/api";

export default function KbPage() {
  const [file, setFile] = useState<File | null>(null);
  const [clientId, setClientId] = useState("default");
  const [docType, setDocType] = useState("project_case");
  const [title, setTitle] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const submit = async () => {
    if (!file) return;
    setBusy(true);
    setStatus(null);
    setError(null);
    try {
      const r = await uploadDoc(file, clientId, docType, title || undefined);
      setStatus(
        `✅ Guardado en ${r.ingest?.path} (${r.ingest?.chars} chars). ${r.reindex?.message || ""}`
      );
    } catch (e) {
      setError(String(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-4 max-w-xl">
      <h1 className="text-2xl font-semibold">Subir documento al KB</h1>
      <p className="text-muted text-sm">
        Acepta markdown, texto plano y PDF. Tras la subida se lanza un reindex en background.
      </p>

      <div className="space-y-3 rounded-xl border border-border bg-panel p-5">
        <div>
          <label className="text-sm text-muted block mb-1">Cliente</label>
          <input
            value={clientId}
            onChange={(e) => setClientId(e.target.value)}
            className="w-full bg-bg border border-border rounded px-3 py-1 text-sm"
          />
        </div>
        <div>
          <label className="text-sm text-muted block mb-1">Tipo de documento</label>
          <select
            value={docType}
            onChange={(e) => setDocType(e.target.value)}
            className="w-full bg-bg border border-border rounded px-3 py-1 text-sm"
          >
            <option value="project_case">project_case</option>
            <option value="company_context">company_context</option>
            <option value="decisions">decisions</option>
          </select>
        </div>
        <div>
          <label className="text-sm text-muted block mb-1">Título (opcional)</label>
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full bg-bg border border-border rounded px-3 py-1 text-sm"
          />
        </div>
        <div>
          <label className="text-sm text-muted block mb-1">Archivo</label>
          <input
            type="file"
            accept=".md,.txt,.pdf,text/markdown,text/plain,application/pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="text-sm"
          />
        </div>
        <button
          onClick={submit}
          disabled={!file || busy}
          className="bg-accent text-bg rounded px-4 py-2 text-sm font-medium disabled:opacity-50"
        >
          {busy ? "Subiendo…" : "Subir y reindexar"}
        </button>
        {status && <div className="text-ok text-sm">{status}</div>}
        {error && <div className="text-err text-sm">{error}</div>}
      </div>
    </div>
  );
}
