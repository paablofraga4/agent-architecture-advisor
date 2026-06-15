"use client";

import { useState } from "react";

function download(filename: string, content: string, mime = "text/markdown") {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export default function ExportBar({
  markdown,
  baseName,
  json,
}: {
  markdown: string;
  baseName: string;
  json?: unknown;
}) {
  const [copied, setCopied] = useState(false);

  return (
    <div className="no-print flex flex-wrap items-center gap-2">
      <button
        onClick={() => window.print()}
        className="rounded-lg bg-accent px-3 py-1.5 text-sm font-medium text-bg"
      >
        ⤓ Exportar PDF
      </button>
      <button
        onClick={() => download(`${baseName}.md`, markdown)}
        disabled={!markdown}
        className="rounded-lg border border-border px-3 py-1.5 text-sm text-muted hover:border-accent hover:text-white disabled:opacity-40"
      >
        Descargar .md
      </button>
      {json !== undefined && (
        <button
          onClick={() =>
            download(
              `${baseName}.json`,
              JSON.stringify(json, null, 2),
              "application/json"
            )
          }
          className="rounded-lg border border-border px-3 py-1.5 text-sm text-muted hover:border-accent hover:text-white"
        >
          Descargar .json
        </button>
      )}
      <button
        onClick={async () => {
          if (!markdown) return;
          await navigator.clipboard.writeText(markdown);
          setCopied(true);
          setTimeout(() => setCopied(false), 1500);
        }}
        disabled={!markdown}
        className="rounded-lg border border-border px-3 py-1.5 text-sm text-muted hover:border-accent hover:text-white disabled:opacity-40"
      >
        {copied ? "✓ Copiado" : "Copiar markdown"}
      </button>
    </div>
  );
}
