"""Render the final AgentArenaResult as a structured executive report."""
from __future__ import annotations

from .schemas import AgentArenaResult


def _pick_winner(result: AgentArenaResult) -> str:
    """Heuristic: look at final comparison text for a verdict line."""
    text = (result.final_comparison or "").lower()
    for cloud in ("azure", "aws", "gcp"):
        if f"recomendamos {cloud}" in text or f"recommend {cloud}" in text or f"ganador: {cloud}" in text:
            return cloud.upper()
    # Fallback: first cloud mentioned in final_architecture title
    final = (result.final_architecture_proposal or "")[:300].lower()
    for cloud in ("azure", "aws", "gcp"):
        if cloud in final:
            return cloud.upper()
    return "—"


def render_report_header(result: AgentArenaResult) -> str:
    pack = result.context_pack
    planner = pack.planner_output
    winner = _pick_winner(result)

    caps = ", ".join(planner.required_capabilities[:5]) or "—"
    constraints = ", ".join(
        (planner.explicit_constraints + planner.inferred_constraints)[:5]
    ) or "—"

    citations = (
        len(result.azure_validation.cited_ids)
        + len(result.aws_validation.cited_ids)
        + (len(result.gcp_validation.cited_ids) if result.gcp_validation else 0)
    )

    return f"""# Informe de Arquitectura

> **Proyecto:** {planner.project_summary}
> **Tipo:** {planner.project_type}
> **Cloud recomendado:** **{winner}**

| Métrica | Valor |
|---|---|
| Capacidades requeridas | {caps} |
| Restricciones clave | {constraints} |
| Contextos recuperados | Azure {len(pack.azure_contexts)} · AWS {len(pack.aws_contexts)} · GCP {len(pack.gcp_contexts)} · Neutral {len(pack.neutral_contexts)} |
| Citas totales en propuestas | {citations} |
| Reescrituras por validación | {sum(result.rewrite_counts.values()) if result.rewrite_counts else 0} |
"""


def _kroki_url(mermaid_src: str, fmt: str = "png") -> str:
    """Render Mermaid via kroki.io as an inline image URL."""
    import base64, zlib
    compressed = zlib.compress(mermaid_src.encode("utf-8"), 9)
    encoded = base64.urlsafe_b64encode(compressed).decode("ascii")
    return f"https://kroki.io/mermaid/{fmt}/{encoded}"


def fetch_architecture_png(mermaid_src: str) -> bytes | None:
    """Render Mermaid to PNG via kroki.io. Returns PNG bytes or None on failure.
    Uses POST with raw source to avoid User-Agent and URL-length issues.
    """
    if not mermaid_src:
        return None
    import urllib.request
    try:
        req = urllib.request.Request(
            "https://kroki.io/mermaid/png",
            data=mermaid_src.encode("utf-8"),
            headers={
                "Content-Type": "text/plain",
                "User-Agent": "agent-architecture-advisor-mvp/1.0",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except Exception as exc:
        print(f"[WARN] kroki render failed: {exc}")
        return None


# Kept for backwards-compat / fallback rendering only.
def render_architecture_section(result: AgentArenaResult) -> str:
    if not result.mermaid_diagram:
        return ""
    return (
        "## Arquitectura propuesta\n\n"
        f"```mermaid\n{result.mermaid_diagram}\n```\n"
    )


def render_full_report(result: AgentArenaResult) -> str:
    parts = [
        render_report_header(result),
        render_architecture_section(result),
        "## Propuesta detallada\n\n" + (result.final_architecture_proposal or ""),
    ]
    return "\n\n".join(p for p in parts if p)
