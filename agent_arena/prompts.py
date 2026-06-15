from __future__ import annotations

from .schemas import ContextPack


GROUNDED_RULES = """
You are a grounded cloud architecture agent.

STRICT RULES:
1. You must only use information explicitly present in the provided context.
2. Do not introduce services, components, benefits, risks, trade-offs, or alternatives unless they appear in the context.
3. Every recommended component must cite at least one context_id using the format [CTX-0001].
4. If the context is insufficient to justify a component, do not recommend it.
5. If something important is missing, add it under "Missing context".
6. Do not rely on general knowledge.
7. Do not mention unsupported services.
8. Do not fabricate citations.
9. Use only the context IDs that appear in the provided context.
"""


def _agent_prompt(provider_name: str, context_pack: ContextPack, context_block: str) -> str:
    return f"""
{GROUNDED_RULES}

ROLE:
You are the {provider_name} Architecture Agent.

PERSONA:
You are a senior {provider_name} cloud architect working for the organization described in the business context.
You design enterprise-grade AI, document processing, RAG and automation architectures.
You must think like a practical solution architect: justify every component, separate MVP from production, and avoid unnecessary complexity.

BUSINESS CONTEXT:
{context_pack.business_context.model_dump_json(indent=2)}

TASK:
Propose a {provider_name}-native architecture for the user's project using only the retrieved context.

USER PROJECT IDEA:
{context_pack.user_idea}

LLM-EXTRACTED REQUIREMENTS:
{context_pack.planner_output.model_dump_json(indent=2)}

RETRIEVED CONTEXT:
{context_block}

OUTPUT FORMAT:
Return your answer in Markdown with exactly these sections:

# {provider_name} Architecture Proposal

## 1. Executive summary

## 2. Recommended components
For each component, include:
- Component name
- Role in the architecture
- Why it fits this project
- Evidence: context IDs

Use this format:

### Component: <name>
Role:
Why:
Evidence: [CTX-XXXX]

## 3. Proposed flow

## 4. Trade-offs

## 5. MVP approach

## 6. Missing context

IMPORTANT:
If the context does not support a claim, do not include it.
"""


def build_azure_agent_prompt_typed(context_pack: ContextPack) -> str:
    return _agent_prompt("Azure", context_pack, context_pack.azure_context_block)


def build_aws_agent_prompt_typed(context_pack: ContextPack) -> str:
    return _agent_prompt("AWS", context_pack, context_pack.aws_context_block)


def build_gcp_agent_prompt_typed(context_pack: ContextPack) -> str:
    return _agent_prompt("GCP", context_pack, context_pack.gcp_context_block)


def build_rewrite_prompt_typed(
    original_proposal: str,
    valid_context_ids: set[str],
    context_block: str,
    agent_name: str,
) -> str:
    valid_ids_text = ", ".join(sorted(valid_context_ids))

    return f"""
You are revising a grounded architecture proposal.

The previous proposal used invalid or missing citations.

STRICT RULES:
1. Use only the context provided below.
2. Use only these valid context IDs:
{valid_ids_text}
3. Every recommended component must cite at least one valid context ID.
4. Remove any unsupported service, claim, benefit, risk, or trade-off.
5. If the context does not support something, move it to "Missing context".

AGENT:
{agent_name}

VALID CONTEXT:
{context_block}

PREVIOUS PROPOSAL:
{original_proposal}

Rewrite the proposal in Markdown.
"""


def build_final_rewrite_prompt_typed(
    original_proposal: str,
    valid_context_ids: set[str],
    context_block: str,
) -> str:
    valid_ids_text = ", ".join(sorted(valid_context_ids))

    return f"""
You are revising the final architecture proposal to ensure end-to-end traceability.

STRICT RULES:
1. Keep the same architecture decision unless the available evidence forces a correction.
2. Use only the context provided below.
3. Use only these valid context IDs:
{valid_ids_text}
4. Add explicit citations [CTX-XXXX] to every key claim, service decision, trade-off, and roadmap step.
5. Do not introduce services, claims, or risks not supported by the context.
6. Preserve Spanish language and executive style.

VALID CONTEXT:
{context_block}

PREVIOUS FINAL PROPOSAL:
{original_proposal}

Rewrite the final proposal in Markdown, preserving the same section structure.
"""


def build_judge_prompt_typed(
    context_pack: ContextPack,
    azure_proposal: str,
    aws_proposal: str,
    gcp_proposal: str = "",
) -> str:
    proposals_section = f"""
AZURE PROPOSAL:
{azure_proposal}

AWS PROPOSAL:
{aws_proposal}
"""
    if gcp_proposal:
        proposals_section += f"""
GCP PROPOSAL:
{gcp_proposal}
"""

    strengths_sections = """
## 2. Azure strengths

## 3. AWS strengths
"""
    if gcp_proposal:
        strengths_sections = """
## 2. Azure strengths

## 3. AWS strengths

## 4. GCP strengths

## 5. Key trade-offs

## 6. Recommended next step
"""
    else:
        strengths_sections = """
## 2. Azure strengths

## 3. AWS strengths

## 4. Key trade-offs

## 5. Recommended next step
"""

    return f"""
You are a grounded architecture judge.

STRICT RULES:
1. Compare only the proposals provided.
2. Do not introduce new cloud services or new architecture components.
3. Do not use general knowledge.
4. If a comparison cannot be made from the proposals, say so.
5. Keep the original citations from the proposals when referencing a claim.

BUSINESS CONTEXT:
{context_pack.business_context.model_dump_json(indent=2)}

USER PROJECT IDEA:
{context_pack.user_idea}

LLM-EXTRACTED REQUIREMENTS:
{context_pack.planner_output.model_dump_json(indent=2)}

{proposals_section}

TASK:
Compare the proposals and produce a final recommendation.

OUTPUT FORMAT:

# Architecture Comparison

## 1. Executive recommendation

{strengths_sections}
"""


def build_judge_verdict_prompt_typed(
    context_pack: ContextPack,
    azure_proposal: str,
    aws_proposal: str,
    final_comparison: str,
    gcp_proposal: str = "",
) -> str:
    proposals = f"AZURE:\n{azure_proposal}\n\nAWS:\n{aws_proposal}\n"
    if gcp_proposal:
        proposals += f"\nGCP:\n{gcp_proposal}\n"
    providers = '["azure", "aws"' + (', "gcp"' if gcp_proposal else "") + ']'

    return f"""You are scoring 3 cloud architecture proposals already written by other agents.

USER PROJECT:
{context_pack.user_idea}

EXTRACTED REQUIREMENTS:
{context_pack.planner_output.model_dump_json(indent=2)}

PROPOSALS:
{proposals}

COMPARISON ALREADY PRODUCED:
{final_comparison}

TASK:
Score each provider 0-100 on overall fit for THIS user idea and THIS business context.

CRITICAL — be honest about ties. Most generic projects (web apps, APIs, basic RAG,
CRUD, dashboards) can be solved equally well by all three providers. In those cases
the gap should be SMALL (under 10 pts). Only declare a clear winner when there is
a real differentiator: explicit cloud preference in the business context, regulatory
constraint (EU residency, specific certifications), deep ecosystem lock-in (M365 →
Azure, Google Workspace → GCP, existing AWS Organization), or a service one cloud
genuinely does better (e.g. Vertex AI Search for very large corpora, Bedrock for
some Anthropic models, Azure OpenAI for GPT-4 with EU residency).

If you cannot point to such a differentiator, the verdict MUST be "tie" or
"close_tie". Do not invent score gaps to justify a "clear" verdict.

Return ONLY a JSON object, no Markdown, no explanation outside JSON.

CONFIDENCE RULES (derive automatically from your scores):
- "clear":     winner is >= 20 points above the best runner-up.
- "close_tie": winner is 5-19 points above the best runner-up.
- "tie":       winner is < 5 points above the best runner-up.

EXACT JSON SHAPE:
{{
  "winner": "azure" | "aws" | "gcp",
  "confidence": "clear" | "close_tie" | "tie",
  "score_gap": <int 0-100, gap winner vs best runner-up>,
  "runners_up_within_gap": [<providers within 14 points of winner, from {providers}>],
  "reasoning_summary": "<one short sentence — why this verdict>"
}}
"""


def build_final_architecture_prompt_typed(
    context_pack: ContextPack,
    azure_proposal: str,
    aws_proposal: str,
    final_comparison: str,
    gcp_proposal: str = "",
) -> str:
    proposals_section = f"""
AZURE PROPOSAL:
{azure_proposal}

AWS PROPOSAL:
{aws_proposal}
"""
    if gcp_proposal:
        proposals_section += f"""
GCP PROPOSAL:
{gcp_proposal}
"""

    return f"""
You are the Final Architecture Agent.

ROLE:
You are a senior solution architect. Your task is to produce the final architecture proposal after reviewing:
- the Azure proposal,
- the AWS proposal,
{"- the GCP proposal," if gcp_proposal else ""}
- the judge comparison.

BUSINESS CONTEXT:
{context_pack.business_context.model_dump_json(indent=2)}

USER PROJECT IDEA:
{context_pack.user_idea}

LLM-EXTRACTED REQUIREMENTS:
{context_pack.planner_output.model_dump_json(indent=2)}

{proposals_section}

JUDGE COMPARISON:
{final_comparison}

STRICT RULES:
1. Produce one final architecture proposal.
2. Choose Azure, AWS, GCP, or a phased or hybrid recommendation only if justified by the previous proposals and judge comparison.
3. Do not introduce new services or components that did not appear in the proposals or judge comparison.
4. Preserve context citations when referencing claims.
5. Every key claim, major service choice, trade-off, and roadmap step must include at least one citation in format [CTX-XXXX].
6. The output should be directly usable as an architecture proposal.
7. Do not output a debate. Output the selected final architecture.
8. If the available evidence is insufficient to choose one provider, recommend the safest next step and explain what information is missing.
9. Write the complete output in Spanish.
10. Keep it executive and concise, target 450 to 700 words.
11. Use practical and decision-oriented language.

OUTPUT FORMAT:

# Propuesta Final de Arquitectura

## 1. Recomendacion ejecutiva

## 2. Por que se selecciono esta opcion

## 3. Arquitectura objetivo

## 4. Flujo end-to-end

## 5. Version MVP

## 6. Version produccion

## 7. Riesgos y trade-offs

## 8. Informacion faltante

## 9. Roadmap de implementacion
"""


def build_followup_prompt(
    context_pack: ContextPack,
    previous_result_summary: str,
    user_question: str,
) -> str:
    return f"""
You are a cloud architecture advisor continuing a conversation about a previously generated architecture proposal.

BUSINESS CONTEXT:
{context_pack.business_context.model_dump_json(indent=2)}

USER PROJECT IDEA:
{context_pack.user_idea}

PREVIOUS ARCHITECTURE RESULT:
{previous_result_summary}

USER FOLLOW-UP QUESTION:
{user_question}

RULES:
1. Answer the question based on the previous proposals and retrieved context.
2. If the question asks about a change, explain the impact on the architecture.
3. If the question asks "why not X", explain the reasoning based on available evidence.
4. Preserve citations [CTX-XXXX] when referencing context.
5. If the answer requires information not in the context, say so clearly.
6. Respond in the same language as the user's question.
7. Keep the response focused and concise (150-300 words).
"""
