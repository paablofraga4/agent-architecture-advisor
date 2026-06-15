"use client";

import { useMemo } from "react";
import ReactFlow, {
  Background,
  Controls,
  Edge,
  Node,
  Position,
} from "reactflow";
import "reactflow/dist/style.css";

export type NodeStatus = "pending" | "running" | "done" | "error";
export type PipelineState = Record<string, NodeStatus>;

const NODES: { id: string; label: string; sub: string; col: number; row: number }[] = [
  { id: "planner",     label: "1. Planner",      sub: "Extrae requisitos",     col: 0, row: 1 },
  { id: "retrieval",   label: "2. Retrieval",    sub: "Qdrant + reranker",     col: 1, row: 1 },
  { id: "azure",       label: "3. Azure",        sub: "Propuesta cloud",       col: 2, row: 0 },
  { id: "aws",         label: "4. AWS",          sub: "Propuesta cloud",       col: 2, row: 1 },
  { id: "gcp",         label: "5. GCP",          sub: "Propuesta cloud",       col: 2, row: 2 },
  { id: "validation",  label: "6. Validator",    sub: "Verifica citas",        col: 3, row: 1 },
  { id: "judge",       label: "7. Judge",        sub: "Compara propuestas",    col: 4, row: 1 },
  { id: "specialists", label: "8. Specialists",  sub: "Sec/FinOps/Comp/Data",  col: 5, row: 1 },
  { id: "final",       label: "9. Final Arch.",  sub: "Síntesis con citas",    col: 6, row: 1 },
  { id: "cost",        label: "10. Cost",        sub: "Costes mensuales",      col: 7, row: 0 },
  { id: "diagram",     label: "11. Diagram",     sub: "D2 arquitectura",       col: 7, row: 1 },
  { id: "audit",       label: "12. Audit",       sub: "Snapshot firmado",      col: 7, row: 2 },
];

const EDGES: [string, string][] = [
  ["planner", "retrieval"],
  ["retrieval", "azure"],
  ["retrieval", "aws"],
  ["retrieval", "gcp"],
  ["azure", "validation"],
  ["aws", "validation"],
  ["gcp", "validation"],
  ["validation", "judge"],
  ["judge", "specialists"],
  ["specialists", "final"],
  ["final", "cost"],
  ["final", "diagram"],
  ["final", "audit"],
];

const COL_W = 200;
const ROW_H = 110;

function statusStyle(s: NodeStatus): { bg: string; border: string; icon: string } {
  switch (s) {
    case "running": return { bg: "#0ea5e9", border: "#38bdf8", icon: "●" };
    case "done":    return { bg: "#10b981", border: "#34d399", icon: "✓" };
    case "error":   return { bg: "#ef4444", border: "#f87171", icon: "✕" };
    default:        return { bg: "#1f2937", border: "#374151", icon: "○" };
  }
}

export default function PipelineGraph({ state }: { state: PipelineState }) {
  const nodes = useMemo<Node[]>(
    () =>
      NODES.map((n) => {
        const st = state[n.id] || "pending";
        const s = statusStyle(st);
        return {
          id: n.id,
          position: { x: n.col * COL_W, y: n.row * ROW_H },
          data: {
            label: (
              <div style={{ padding: 4, fontFamily: "Inter, system-ui" }}>
                <div style={{ fontWeight: 600, color: "white", fontSize: 13 }}>
                  {s.icon} {n.label}
                </div>
                <div style={{ fontSize: 11, color: "rgba(255,255,255,0.85)" }}>{n.sub}</div>
              </div>
            ),
          },
          sourcePosition: Position.Right,
          targetPosition: Position.Left,
          style: {
            background: s.bg,
            border: `1.5px solid ${s.border}`,
            borderRadius: 10,
            width: 170,
            color: "white",
          },
        };
      }),
    [state]
  );

  const edges = useMemo<Edge[]>(
    () =>
      EDGES.map(([a, b], i) => {
        const active = state[a] === "done" && (state[b] === "running" || state[b] === "done");
        return {
          id: `e${i}`,
          source: a,
          target: b,
          animated: active,
          style: { stroke: active ? "#10b981" : "#475569", strokeWidth: active ? 2.5 : 1.5 },
        };
      }),
    [state]
  );

  return (
    <div className="rounded-xl border border-border bg-panel" style={{ height: 380 }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        nodesDraggable={false}
        nodesConnectable={false}
        zoomOnScroll={false}
        panOnScroll={false}
      >
        <Background color="#1f2937" gap={20} />
        <Controls showInteractive={false} />
      </ReactFlow>
    </div>
  );
}

// Map an SSE event name to (node id, new status).
export const EVENT_MAP: Record<string, [string, NodeStatus]> = {
  planner_started: ["planner", "running"],
  planner_finished: ["planner", "done"],
  retrieval_started: ["retrieval", "running"],
  retrieval_finished: ["retrieval", "done"],
  azure_agent_started: ["azure", "running"],
  azure_agent_finished: ["azure", "done"],
  aws_agent_started: ["aws", "running"],
  aws_agent_finished: ["aws", "done"],
  gcp_agent_started: ["gcp", "running"],
  gcp_agent_finished: ["gcp", "done"],
  citation_validation_started: ["validation", "running"],
  citation_validation_finished: ["validation", "done"],
  judge_started: ["judge", "running"],
  judge_finished: ["judge", "done"],
  specialists_started: ["specialists", "running"],
  specialists_finished: ["specialists", "done"],
  final_architecture_started: ["final", "running"],
  final_architecture_finished: ["final", "done"],
  cost_estimation_started: ["cost", "running"],
  cost_estimation_finished: ["cost", "done"],
  cost_estimation_error: ["cost", "error"],
  diagram_generation_started: ["diagram", "running"],
  diagram_generation_finished: ["diagram", "done"],
  diagram_generation_error: ["diagram", "error"],
  audit_saved: ["audit", "done"],
  audit_error: ["audit", "error"],
};

export function emptyState(): PipelineState {
  return Object.fromEntries(NODES.map((n) => [n.id, "pending" as NodeStatus]));
}
