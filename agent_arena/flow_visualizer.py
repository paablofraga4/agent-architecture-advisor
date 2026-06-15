"""Live pipeline flow visualizer.

Renders a Mermaid flowchart of the Agent Arena pipeline whose node styles
update as events fire (pending -> running -> done -> error). Designed to be
emitted into a single Chainlit message that gets re-rendered on every event,
so the user sees the data physically flowing from node to node.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

NodeStatus = Literal["pending", "running", "done", "error"]

PIPELINE_NODES: list[tuple[str, str]] = [
    ("planner",       "1. Planner<br/>Extrae requisitos"),
    ("retrieval",     "2. Retrieval<br/>Qdrant + reranker"),
    ("azure",         "3. Azure Agent"),
    ("aws",           "4. AWS Agent"),
    ("gcp",           "5. GCP Agent"),
    ("validation",    "6. Citation validator"),
    ("judge",         "7. Judge"),
    ("final",         "8. Final Architecture"),
    ("cost",          "9. Cost estimator"),
    ("diagram",       "10. Diagram"),
]

EDGES: list[tuple[str, str]] = [
    ("planner", "retrieval"),
    ("retrieval", "azure"),
    ("retrieval", "aws"),
    ("retrieval", "gcp"),
    ("azure", "validation"),
    ("aws", "validation"),
    ("gcp", "validation"),
    ("validation", "judge"),
    ("judge", "final"),
    ("final", "cost"),
    ("final", "diagram"),
]

# Map of arena event name -> (node_id, status_to_set)
EVENT_MAP: dict[str, tuple[str, NodeStatus]] = {
    "planner_started":             ("planner", "running"),
    "planner_finished":            ("planner", "done"),
    "planner_rerun_started":       ("planner", "running"),
    "planner_rerun_finished":      ("planner", "done"),
    "retrieval_started":           ("retrieval", "running"),
    "retrieval_finished":          ("retrieval", "done"),
    "azure_agent_started":         ("azure", "running"),
    "azure_agent_finished":        ("azure", "done"),
    "aws_agent_started":           ("aws", "running"),
    "aws_agent_finished":          ("aws", "done"),
    "gcp_agent_started":           ("gcp", "running"),
    "gcp_agent_finished":          ("gcp", "done"),
    "citation_validation_started": ("validation", "running"),
    "citation_validation_finished":("validation", "done"),
    "judge_started":               ("judge", "running"),
    "judge_finished":              ("judge", "done"),
    "final_architecture_started":  ("final", "running"),
    "final_architecture_finished": ("final", "done"),
    "cost_estimation_started":     ("cost", "running"),
    "cost_estimation_finished":    ("cost", "done"),
    "cost_estimation_error":       ("cost", "error"),
    "diagram_generation_started":  ("diagram", "running"),
    "diagram_generation_finished": ("diagram", "done"),
    "diagram_generation_error":    ("diagram", "error"),
}


@dataclass
class FlowState:
    nodes: dict[str, NodeStatus] = field(
        default_factory=lambda: {nid: "pending" for nid, _ in PIPELINE_NODES}
    )

    def apply_event(self, event: str) -> bool:
        """Returns True if the event mutated visible state."""
        if event in EVENT_MAP:
            node, status = EVENT_MAP[event]
            if self.nodes.get(node) != status:
                self.nodes[node] = status
                return True
        if event == "error":
            for nid, st in self.nodes.items():
                if st == "running":
                    self.nodes[nid] = "error"
            return True
        return False

    def render_mermaid(self) -> str:
        lines = ["flowchart LR"]
        for nid, label in PIPELINE_NODES:
            icon = {
                "pending": "&#9675;",   # circle
                "running": "&#9881;",   # gear
                "done":    "&#10003;",  # check
                "error":   "&#10007;",  # cross
            }[self.nodes[nid]]
            lines.append(f'  {nid}["{icon} {label}"]')
        for a, b in EDGES:
            lines.append(f"  {a} --> {b}")
        # Style classes
        lines.extend([
            "  classDef pending fill:#1f2937,stroke:#4b5563,color:#9ca3af",
            "  classDef running fill:#0ea5e9,stroke:#0284c7,color:#ffffff,stroke-width:3px",
            "  classDef done    fill:#10b981,stroke:#059669,color:#ffffff",
            "  classDef error   fill:#ef4444,stroke:#b91c1c,color:#ffffff",
        ])
        for status in ("pending", "running", "done", "error"):
            ids = [nid for nid, st in self.nodes.items() if st == status]
            if ids:
                lines.append(f"  class {','.join(ids)} {status}")
        return "\n".join(lines)

    def render_message(self) -> str:
        return (
            "## Pipeline en vivo\n\n"
            "```mermaid\n"
            f"{self.render_mermaid()}\n"
            "```"
        )
