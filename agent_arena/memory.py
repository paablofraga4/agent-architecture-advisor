"""Per-client memory of past arena runs.

When the same client returns with a new project, the system injects a
summary of previous decisions into the business_context so the agents
don't contradict themselves across projects for the same client.
"""
from __future__ import annotations

from typing import Optional
from .audit import list_snapshots, load_snapshot
from .schemas import BusinessContext


MAX_HISTORY_ENTRIES = 5  # only show the most recent runs to keep prompt size bounded


def load_client_history(client_id: str) -> list[dict]:
    """Most recent runs first."""
    all_runs = list_snapshots(client_id=client_id)
    all_runs.sort(key=lambda r: r.get("timestamp_utc", ""), reverse=True)
    return all_runs[:MAX_HISTORY_ENTRIES]


def summarize_history_for_prompt(client_id: str) -> str:
    """One short bullet per past run, ready to drop into a prompt."""
    history = load_client_history(client_id)
    if not history:
        return ""

    lines = []
    for h in history:
        winner = (h.get("verdict_winner") or "—").upper()
        conf = h.get("verdict_confidence") or "—"
        summary = h.get("project_summary") or "(sin resumen)"
        lines.append(f"- [{h['run_id']}] {summary} → recomendado: **{winner}** ({conf})")

    return (
        "Decisiones previas para este cliente (no las contradigas sin justificación nueva):\n"
        + "\n".join(lines)
    )


def enrich_business_context_with_memory(
    business_context: BusinessContext,
    client_id: Optional[str],
) -> BusinessContext:
    """Return a copy of business_context with previous decisions appended to notes."""
    if not client_id:
        return business_context

    memo = summarize_history_for_prompt(client_id)
    if not memo:
        return business_context

    enriched = business_context.model_copy(deep=True)
    sep = "\n\n---\n\n" if enriched.notes else ""
    enriched.notes = f"{enriched.notes}{sep}{memo}"
    return enriched
