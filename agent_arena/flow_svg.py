"""Render the FlowState as an inline SVG embedded in markdown.

Avoids Mermaid rendering quirks in Chainlit and produces a much cleaner
visual: rounded cards arranged in 3 columns with arrows, colored by state.
"""
from __future__ import annotations

import base64
from .flow_visualizer import FlowState


# Layout grid (col, row) for each pipeline node id.
LAYOUT: dict[str, tuple[int, int]] = {
    "planner":    (0, 1),
    "retrieval":  (1, 1),
    "azure":      (2, 0),
    "aws":        (2, 1),
    "gcp":        (2, 2),
    "validation": (3, 1),
    "judge":      (4, 1),
    "final":      (5, 1),
    "cost":       (6, 0),
    "diagram":    (6, 2),
}

LABELS: dict[str, str] = {
    "planner":    "1. Planner",
    "retrieval":  "2. Retrieval",
    "azure":      "3. Azure",
    "aws":        "4. AWS",
    "gcp":        "5. GCP",
    "validation": "6. Validator",
    "judge":      "7. Judge",
    "final":      "8. Final Architecture",
    "cost":       "9. Cost",
    "diagram":    "10. Diagram",
}

SUBLABELS: dict[str, str] = {
    "planner":    "Extrae requisitos",
    "retrieval":  "Qdrant + reranker",
    "azure":      "Propuesta cloud",
    "aws":        "Propuesta cloud",
    "gcp":        "Propuesta cloud",
    "validation": "Verifica citas",
    "judge":      "Compara propuestas",
    "final":      "Síntesis con citas",
    "cost":       "Costes mensuales",
    "diagram":    "Mermaid arquitectura",
}

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

STATE_STYLE = {
    "pending": {"fill": "#1f2937", "stroke": "#374151", "text": "#9ca3af", "icon": "○"},
    "running": {"fill": "#0ea5e9", "stroke": "#38bdf8", "text": "#ffffff", "icon": "●"},
    "done":    {"fill": "#10b981", "stroke": "#34d399", "text": "#ffffff", "icon": "✓"},
    "error":   {"fill": "#ef4444", "stroke": "#f87171", "text": "#ffffff", "icon": "✕"},
}

# Geometry
COL_W = 165
ROW_H = 95
NODE_W = 140
NODE_H = 64
PAD_X = 24
PAD_Y = 24
COLS = 7
ROWS = 3
SVG_W = PAD_X * 2 + COL_W * (COLS - 1) + NODE_W
SVG_H = PAD_Y * 2 + ROW_H * (ROWS - 1) + NODE_H


def _node_xy(node_id: str) -> tuple[int, int]:
    col, row = LAYOUT[node_id]
    x = PAD_X + col * COL_W
    y = PAD_Y + row * ROW_H
    return x, y


def _node_center(node_id: str) -> tuple[int, int]:
    x, y = _node_xy(node_id)
    return x + NODE_W // 2, y + NODE_H // 2


def render_svg(state: FlowState) -> str:
    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W} {SVG_H}" '
        f'width="100%" style="max-width:{SVG_W}px;font-family:Inter,system-ui,sans-serif">'
    )
    # Background
    parts.append(
        f'<rect width="{SVG_W}" height="{SVG_H}" rx="14" fill="#0b1220"/>'
    )
    # Arrow defs
    parts.append(
        '<defs>'
        '<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#64748b"/></marker>'
        '<marker id="arr-active" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#10b981"/></marker>'
        '</defs>'
    )
    # Edges
    for a, b in EDGES:
        ax, ay = _node_center(a)
        bx, by = _node_center(b)
        ax += NODE_W // 2  # exit from right side
        bx -= NODE_W // 2  # enter from left side
        active = state.nodes[a] == "done" and state.nodes[b] in ("running", "done")
        color = "#10b981" if active else "#475569"
        width = 2.5 if active else 1.5
        marker = "url(#arr-active)" if active else "url(#arr)"
        # Use a slight S-curve for non-horizontal edges
        if ay == by:
            d = f"M {ax} {ay} L {bx} {by}"
        else:
            mx = (ax + bx) / 2
            d = f"M {ax} {ay} C {mx} {ay}, {mx} {by}, {bx} {by}"
        parts.append(
            f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="none" '
            f'marker-end="{marker}"/>'
        )
    # Nodes
    for nid in LAYOUT:
        x, y = _node_xy(nid)
        st = state.nodes[nid]
        s = STATE_STYLE[st]
        parts.append(
            f'<g>'
            f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="10" '
            f'fill="{s["fill"]}" stroke="{s["stroke"]}" stroke-width="1.5"/>'
            f'<text x="{x + 12}" y="{y + 22}" fill="{s["text"]}" '
            f'font-size="13" font-weight="600">{s["icon"]} {LABELS[nid]}</text>'
            f'<text x="{x + 12}" y="{y + 44}" fill="{s["text"]}" '
            f'font-size="11" opacity="0.85">{SUBLABELS[nid]}</text>'
            f'</g>'
        )
    parts.append("</svg>")
    return "".join(parts)


def render_markdown(state: FlowState) -> str:
    svg = render_svg(state)
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return (
        "## Pipeline en vivo\n\n"
        f'![pipeline](data:image/svg+xml;base64,{b64})'
    )
