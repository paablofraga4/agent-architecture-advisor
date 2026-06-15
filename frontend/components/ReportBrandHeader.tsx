"use client";

import BrandMark from "@/components/BrandMark";
import { getWorkspace, type Workspace } from "@/lib/workspace";

export default function ReportBrandHeader({
  workspace,
  workspaceId,
  title = "Informe de Arquitectura",
  subtitle,
  runId,
  date,
}: {
  workspace?: Workspace;
  workspaceId?: string;
  title?: string;
  subtitle?: string;
  runId?: string;
  date?: string;
}) {
  const ws = workspace ?? getWorkspace(workspaceId ?? "default");
  return (
    <div className="flex items-center gap-4 rounded-2xl border border-border bg-panel p-5">
      <BrandMark workspace={ws} size={48} />
      <div className="min-w-0 flex-1">
        <div className="flex items-baseline gap-2">
          <span className="font-semibold">{ws.name}</span>
          <span className="text-xs text-muted">· {ws.role}</span>
        </div>
        <div className="text-lg font-semibold">{title}</div>
        {subtitle && (
          <div className="truncate text-sm text-muted">{subtitle}</div>
        )}
      </div>
      <div className="hidden text-right text-xs text-muted sm:block">
        {date && <div>{date}</div>}
        {runId && <div className="font-mono">{runId}</div>}
        <div>Architecture Advisor</div>
      </div>
    </div>
  );
}
