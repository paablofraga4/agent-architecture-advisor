"""Render the final AgentArenaResult as a structured executive report."""
from __future__ import annotations

from .schemas import AgentArenaResult


def _pick_winner(result: AgentArenaResult) -> str:
    """Prefer the structured verdict; fall back to text heuristic only if missing."""
    if result.verdict is not None:
        return result.verdict.winner.upper()
    text = (result.final_comparison or "").lower()
    for cloud in ("azure", "aws", "gcp"):
        if f"recomendamos {cloud}" in text or f"recommend {cloud}" in text or f"ganador: {cloud}" in text:
            return cloud.upper()
    final = (result.final_architecture_proposal or "")[:300].lower()
    for cloud in ("azure", "aws", "gcp"):
        if cloud in final:
            return cloud.upper()
    return "—"


def _render_confidence_banner(result: AgentArenaResult) -> str:
    """Show an explicit notice when the judge wasn't confident about the winner."""
    v = result.verdict
    if v is None or v.confidence == "clear":
        return ""

    winner = v.winner.upper()
    runners = [p.upper() for p in v.runners_up_within_gap if p != v.winner]
    runners_str = " · ".join(runners) if runners else "el resto"

    if v.confidence == "tie":
        title = "⚖️ Empate técnico entre proveedores"
        body = (
            f"Las propuestas de **{winner}** y **{runners_str}** son funcionalmente "
            f"equivalentes para este proyecto (diferencia de {v.score_gap} pts sobre 100). "
            f"La arquitectura mostrada abajo es la de **{winner}** por convención, "
            f"pero cualquiera de las otras es igual de defendible."
        )
    else:  # close_tie
        title = "⚠️ Ganador no concluyente"
        body = (
            f"**{winner}** lidera por solo {v.score_gap} pts sobre **{runners_str}**. "
            f"Mostramos la arquitectura de {winner} pero la decisión final debería "
            f"considerar restricciones no técnicas (contratos existentes, skills internos, "
            f"acuerdos comerciales con el proveedor)."
        )

    reason = v.reasoning_summary.strip()
    return (
        f"> **{title}**\n>\n"
        f"> {body}\n>\n"
        f"> *Razonamiento del juez:* {reason}\n\n"
    )


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

    if result.verdict is not None:
        v = result.verdict
        label = {"clear": "✅ Claro", "close_tie": "⚠️ Marginal", "tie": "⚖️ Empate"}[v.confidence]
        runners = ", ".join(p.upper() for p in v.runners_up_within_gap if p != v.winner)
        confidence_row = (
            f"| Confianza del juez | {label} · gap {v.score_gap}/100"
            + (f" · empata con {runners}" if runners else "")
            + " |\n"
        )
    else:
        confidence_row = "| Confianza del juez | (no disponible — verdict no parseado) |\n"

    banner = _render_confidence_banner(result)
    return f"""# Informe de Arquitectura

{banner}> **Proyecto:** {planner.project_summary}
> **Tipo:** {planner.project_type}
> **Cloud recomendado:** **{winner}**

| Métrica | Valor |
|---|---|
| Capacidades requeridas | {caps} |
| Restricciones clave | {constraints} |
| Contextos recuperados | Azure {len(pack.azure_contexts)} · AWS {len(pack.aws_contexts)} · GCP {len(pack.gcp_contexts)} · Neutral {len(pack.neutral_contexts)} |
| Citas totales en propuestas | {citations} |
| Reescrituras por validación | {sum(result.rewrite_counts.values()) if result.rewrite_counts else 0} |
{confidence_row}"""


def fetch_architecture_image(diagram_src: str) -> tuple[bytes, str] | None:
    """Render D2 via kroki.io. Returns (svg_bytes, mime) or None on failure.
    The diagram agent now emits D2, which renders much cleaner than Mermaid.
    """
    if not diagram_src:
        return None
    import urllib.request
    try:
        req = urllib.request.Request(
            "https://kroki.io/d2/svg",
            data=diagram_src.encode("utf-8"),
            headers={
                "Content-Type": "text/plain",
                "User-Agent": "agent-architecture-advisor-mvp/1.0",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read(), "image/svg+xml"
    except Exception as exc:
        print(f"[WARN] kroki D2 render failed: {exc}")
        return None


# Text fallback only used if kroki fails.
def render_architecture_section(result: AgentArenaResult) -> str:
    if not result.mermaid_diagram:
        return ""
    return (
        "## Arquitectura propuesta\n\n"
        f"```\n{result.mermaid_diagram}\n```\n"
    )


def render_full_report(result: AgentArenaResult) -> str:
    parts = [
        render_report_header(result),
        render_architecture_section(result),
        "## Propuesta detallada\n\n" + (result.final_architecture_proposal or ""),
    ]
    return "\n\n".join(p for p in parts if p)
