from __future__ import annotations

from typing import Literal
import re

from .schemas import CitationValidation, ContextPack


def get_valid_context_ids_typed(
    context_pack: ContextPack,
    agent: Literal["azure", "aws", "gcp", "all"],
) -> set[str]:
    if agent == "azure":
        contexts = context_pack.azure_contexts + context_pack.neutral_contexts
    elif agent == "aws":
        contexts = context_pack.aws_contexts + context_pack.neutral_contexts
    elif agent == "gcp":
        contexts = context_pack.gcp_contexts + context_pack.neutral_contexts
    else:
        contexts = (
            context_pack.azure_contexts
            + context_pack.aws_contexts
            + context_pack.gcp_contexts
            + context_pack.neutral_contexts
        )

    return {ctx.context_id for ctx in contexts}


def extract_cited_context_ids(text: str) -> set[str]:
    return set(re.findall(r"CTX-\d{4}", text or ""))


def validate_citations_typed(
    proposal: str,
    valid_context_ids: set[str],
) -> CitationValidation:
    cited_ids = extract_cited_context_ids(proposal)
    invalid_ids = cited_ids - valid_context_ids
    has_citations = len(cited_ids) > 0

    return CitationValidation(
        cited_ids=sorted(cited_ids),
        invalid_ids=sorted(invalid_ids),
        has_citations=has_citations,
        valid=len(invalid_ids) == 0 and has_citations,
    )


def ids_from_text(text: str) -> list[str]:
    return sorted(set(re.findall(r"CTX-\d{4}", text or "")))


def ctx_map_from_result(res):
    all_ctx = (
        list(res.context_pack.azure_contexts)
        + list(res.context_pack.aws_contexts)
        + list(res.context_pack.gcp_contexts)
        + list(res.context_pack.neutral_contexts)
    )
    return {ctx.context_id: ctx for ctx in all_ctx}


def format_evidence_trace(res) -> str:
    ctx_map = ctx_map_from_result(res)
    sections = []

    proposals = [
        ("Azure proposal", res.azure_proposal),
        ("AWS proposal", res.aws_proposal),
    ]
    if res.gcp_proposal:
        proposals.append(("GCP proposal", res.gcp_proposal))
    proposals.append(("Final architecture proposal", res.final_architecture_proposal))

    for label, text in proposals:
        ids = ids_from_text(text)
        lines = [f"## {label}: {len(ids)} citas"]
        if not ids:
            lines.append("- Sin citas explicitas")
        for cid in ids:
            ctx = ctx_map.get(cid)
            if ctx is None:
                lines.append(f"- {cid} | NO_ENCONTRADO_EN_CONTEXTO")
            else:
                lines.append(
                    f"- {cid} | provider={ctx.provider} | doc_type={ctx.document_type} | source={ctx.source_file} | section={ctx.section_path}"
                )
        sections.append("\n".join(lines))

    return "\n\n".join(sections)
