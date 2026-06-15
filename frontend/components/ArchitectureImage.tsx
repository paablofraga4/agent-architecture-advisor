"use client";

import { useEffect, useState } from "react";

/**
 * Renders the D2 architecture diagram by POSTing the source to kroki.io/d2/svg
 * via the browser. Falls back to a plain code block if kroki is unreachable.
 */
export default function ArchitectureImage({ d2 }: { d2: string }) {
  const [svgUrl, setSvgUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!d2) return;
    let url: string | null = null;
    const ctrl = new AbortController();
    fetch("https://kroki.io/d2/svg", {
      method: "POST",
      headers: { "Content-Type": "text/plain" },
      body: d2,
      signal: ctrl.signal,
    })
      .then((r) => {
        if (!r.ok) throw new Error(`kroki ${r.status}`);
        return r.blob();
      })
      .then((blob) => {
        url = URL.createObjectURL(blob);
        setSvgUrl(url);
      })
      .catch((e) => setError(String(e)));
    return () => {
      ctrl.abort();
      if (url) URL.revokeObjectURL(url);
    };
  }, [d2]);

  if (error)
    return (
      <pre className="bg-panel border border-border rounded p-3 text-xs overflow-auto">
        <code>{d2}</code>
      </pre>
    );
  if (!svgUrl) return <div className="text-muted text-sm">Renderizando diagrama…</div>;

  return (
    <div className="rounded-xl border border-border bg-white p-3">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={svgUrl} alt="Arquitectura" className="w-full" />
    </div>
  );
}
