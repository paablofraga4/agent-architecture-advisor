"""Specialist agents that critique the cloud proposals from 4 orthogonal angles.

Each specialist receives the 3 cloud proposals + business context and returns
a structured set of findings (severity + topic + recommendation). The final
architecture agent consumes these findings to produce a hardened proposal.

This is what makes 'multi-agent' a real debate instead of 3 parallel monologues.
"""
from __future__ import annotations

import asyncio
import json
import re
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field

from .llm import call_llm_async
from .schemas import ContextPack


Severity = Literal["high", "medium", "low"]
SpecialistKind = Literal["security", "finops", "compliance", "data"]


class SpecialistFinding(BaseModel):
    severity: Severity
    topic: str
    applies_to: list[str] = Field(default_factory=list)  # ["azure"], ["aws","gcp"], ["all"]
    issue: str
    recommendation: str


class SpecialistReport(BaseModel):
    agent: SpecialistKind
    overall_concern: str = ""
    findings: list[SpecialistFinding] = Field(default_factory=list)


SPECIALIST_BRIEFS: dict[SpecialistKind, str] = {
    "security": (
        "You are a senior cloud security architect. Audit the proposals for: identity & access "
        "(IAM least-privilege, managed identities vs static keys), secrets management (Key Vault / "
        "Secrets Manager / Secret Manager usage), network perimeter (private endpoints, VPC, "
        "private link), data-at-rest and in-transit encryption, public exposure of services, and "
        "supply chain (managed vs custom images)."
    ),
    "finops": (
        "You are a senior FinOps practitioner. Audit the proposals for total cost of ownership over "
        "3 years (not just monthly MVP), reserved capacity vs on-demand, idle resources, egress costs "
        "between services, choice of provisioned vs serverless tier given the expected scale, and "
        "non-obvious cost drivers (LLM tokens, vector DB storage, log retention)."
    ),
    "compliance": (
        "You are a senior compliance and data-protection officer. Audit the proposals for GDPR "
        "(data residency, DPA, subprocessor list), sector-specific certifications (HIPAA, PCI-DSS, "
        "SOC2, ISO 27001) when relevant to the business context, retention and right-to-erasure, "
        "audit logging requirements, and cross-border data flows."
    ),
    "data": (
        "You are a senior data architect. Audit the proposals for data lineage (can we trace where "
        "every datum came from?), data quality controls, schema evolution, separation of operational "
        "vs analytical stores, governance (catalog, ownership), and reuse of existing data assets "
        "mentioned in the business context."
    ),
}


def _build_specialist_prompt(
    kind: SpecialistKind,
    context_pack: ContextPack,
    azure_proposal: str,
    aws_proposal: str,
    gcp_proposal: str,
) -> str:
    brief = SPECIALIST_BRIEFS[kind]
    proposals = f"AZURE PROPOSAL:\n{azure_proposal}\n\nAWS PROPOSAL:\n{aws_proposal}\n"
    if gcp_proposal:
        proposals += f"\nGCP PROPOSAL:\n{gcp_proposal}\n"

    return f"""{brief}

USER PROJECT:
{context_pack.user_idea}

BUSINESS CONTEXT:
{context_pack.business_context.model_dump_json(indent=2)}

REQUIREMENTS:
{context_pack.planner_output.model_dump_json(indent=2)}

PROPOSALS TO AUDIT:
{proposals}

TASK:
Identify 2-6 concrete issues across the proposals from your perspective ({kind}).
Be SPECIFIC: name services, name the missing control, name the affected proposals.
Do NOT repeat generic textbook advice. If a proposal already handles something well,
do not list it as a finding.

If everything is genuinely fine from your perspective, return an empty findings list
and explain it in overall_concern. Do NOT invent issues.

Return ONLY a JSON object, no Markdown, no prose outside JSON:

{{
  "agent": "{kind}",
  "overall_concern": "<one short sentence — the single most important thing this proposal misses from a {kind} POV, or 'no material concerns' if fine>",
  "findings": [
    {{
      "severity": "high" | "medium" | "low",
      "topic": "<short label, e.g. 'Secrets in environment variables'>",
      "applies_to": ["azure"] or ["aws","gcp"] or ["all"],
      "issue": "<specific problem, naming services>",
      "recommendation": "<specific fix, naming the service to use>"
    }}
  ]
}}
"""


async def run_specialist_async(
    kind: SpecialistKind,
    context_pack: ContextPack,
    azure_proposal: str,
    aws_proposal: str,
    gcp_proposal: str,
    model: str,
    trace: Any = None,
) -> Optional[SpecialistReport]:
    prompt = _build_specialist_prompt(kind, context_pack, azure_proposal, aws_proposal, gcp_proposal)
    raw = await call_llm_async(
        prompt=prompt,
        model=model,
        trace=trace,
        span_name=f"specialist_{kind}",
        metadata={"agent": f"specialist_{kind}"},
        agent_name=f"specialist_{kind}_agent",
    )
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return None
    try:
        return SpecialistReport.model_validate_json(match.group(0))
    except Exception as exc:
        print(f"  [WARN] Specialist {kind} parse failed: {exc}")
        return None


async def run_all_specialists_async(
    context_pack: ContextPack,
    azure_proposal: str,
    aws_proposal: str,
    gcp_proposal: str,
    model: str,
    trace: Any = None,
) -> list[SpecialistReport]:
    kinds: list[SpecialistKind] = ["security", "finops", "compliance", "data"]
    results = await asyncio.gather(*[
        run_specialist_async(k, context_pack, azure_proposal, aws_proposal, gcp_proposal, model, trace)
        for k in kinds
    ], return_exceptions=True)
    out: list[SpecialistReport] = []
    for r in results:
        if isinstance(r, SpecialistReport):
            out.append(r)
    return out


def render_specialist_block_for_final(reports: list[SpecialistReport]) -> str:
    """Compact text block to inject into the final architecture prompt."""
    if not reports:
        return ""
    lines = ["SPECIALIST FINDINGS (incorporate them into the final architecture):"]
    for r in reports:
        lines.append(f"\n## {r.agent.upper()}")
        if r.overall_concern:
            lines.append(f"Overall: {r.overall_concern}")
        for f in r.findings:
            lines.append(
                f"- [{f.severity.upper()}] ({','.join(f.applies_to)}) {f.topic}: "
                f"{f.issue} → {f.recommendation}"
            )
    return "\n".join(lines)


def render_specialist_section_for_report(reports: list[SpecialistReport]) -> str:
    """Markdown section for the final user-facing report."""
    if not reports:
        return ""
    sev_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    lines = ["## Hallazgos de agentes especialistas"]
    for r in reports:
        title = {"security": "🛡️ Seguridad", "finops": "💰 FinOps",
                 "compliance": "⚖️ Compliance", "data": "🗄️ Data"}[r.agent]
        lines.append(f"\n### {title}")
        if r.overall_concern:
            lines.append(f"_{r.overall_concern}_\n")
        if not r.findings:
            lines.append("- Sin hallazgos materiales.")
        for f in r.findings:
            scope = "/".join(p.upper() for p in f.applies_to)
            lines.append(
                f"- {sev_icon[f.severity]} **{f.topic}** _(en {scope})_  \n"
                f"  Problema: {f.issue}  \n"
                f"  Recomendación: {f.recommendation}"
            )
    return "\n".join(lines)
