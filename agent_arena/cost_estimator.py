from __future__ import annotations

import json
from typing import Optional, Any

from .llm import call_llm_async, _run_coroutine_in_new_thread
from .schemas import CostComparison, CostEstimate, ContextPack


COST_SYSTEM_PROMPT = """You are a cloud cost estimation agent specializing in AI and data architectures.

STRICT RULES:
1. Return ONLY a JSON object — no Markdown, no explanations.
2. Base estimates on the components mentioned in the proposals and the cost reference context.
3. Provide monthly cost RANGES (low-high), not single numbers.
4. Separate MVP costs from production costs.
5. Be conservative — it's better to slightly overestimate than underestimate.
6. List the top 3 cost drivers for each provider.
7. Include 2-3 optimization tips per provider.
8. If cost data is not available in context, use your best estimate and note it.
"""


def build_cost_prompt(
    context_pack: ContextPack,
    azure_proposal: str,
    aws_proposal: str,
    gcp_proposal: str = "",
) -> str:
    providers_section = f"""
AZURE PROPOSAL:
{azure_proposal}

AWS PROPOSAL:
{aws_proposal}
"""
    if gcp_proposal:
        providers_section += f"""
GCP PROPOSAL:
{gcp_proposal}
"""

    providers_list = '["azure", "aws"'
    if gcp_proposal:
        providers_list += ', "gcp"'
    providers_list += ']'

    return f"""{COST_SYSTEM_PROMPT}

USER PROJECT:
{context_pack.user_idea}

REQUIREMENTS:
{context_pack.planner_output.model_dump_json(indent=2)}

{providers_section}

Return a JSON object with this exact structure:
{{
  "estimates": [
    {{
      "provider": "azure",
      "mvp_monthly_low": 50,
      "mvp_monthly_high": 150,
      "production_monthly_low": 300,
      "production_monthly_high": 800,
      "key_cost_drivers": ["Azure OpenAI tokens", "AI Search Standard tier", "Container Apps compute"],
      "optimization_tips": ["Use GPT-4o-mini for non-critical calls", "Start with Basic AI Search tier"]
    }}
  ],
  "summary": "Brief comparison of cost profiles across providers",
  "cheapest_mvp": "provider_name",
  "cheapest_production": "provider_name"
}}

Include estimates for providers: {providers_list}
"""


def _repair_json(text: str) -> str:
    """Try to fix common LLM JSON issues."""
    import re
    # Remove trailing commas before } or ]
    text = re.sub(r",\s*([}\]])", r"\1", text)
    # Remove markdown code fences
    text = re.sub(r"^```(?:json)?\s*\n?", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n?```\s*$", "", text, flags=re.MULTILINE)
    # Replace single quotes with double quotes (crude but covers common cases)
    # Only if there are no double quotes at all in a value context
    return text


def parse_cost_response(raw: str) -> CostComparison:
    import re
    text = raw.strip()
    # Remove markdown fences
    text = re.sub(r"^```(?:json)?\s*\n?", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n?```\s*$", "", text, flags=re.MULTILINE)
    # Extract JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)
    # First attempt
    try:
        data = json.loads(text)
        return CostComparison.model_validate(data)
    except json.JSONDecodeError:
        pass
    # Repair and retry
    repaired = _repair_json(text)
    try:
        data = json.loads(repaired)
        return CostComparison.model_validate(data)
    except json.JSONDecodeError as e:
        # Last resort: try to extract estimates array manually
        raise ValueError(
            f"Failed to parse cost estimation JSON after repair: {e}\n"
            f"Raw output (first 500 chars): {raw[:500]}"
        )


async def estimate_costs_async(
    context_pack: ContextPack,
    azure_proposal: str,
    aws_proposal: str,
    gcp_proposal: str = "",
    model: str = "gpt-4o-mini",
    trace: Any = None,
) -> CostComparison:
    prompt = build_cost_prompt(context_pack, azure_proposal, aws_proposal, gcp_proposal)
    raw = await call_llm_async(
        prompt=prompt,
        model=model,
        trace=trace,
        span_name="cost_estimation",
        metadata={"agent": "cost_estimator"},
        agent_name="cost_estimator_agent",
    )
    return parse_cost_response(raw)


def estimate_costs(
    context_pack: ContextPack,
    azure_proposal: str,
    aws_proposal: str,
    gcp_proposal: str = "",
    model: str = "gpt-4o-mini",
) -> CostComparison:
    return _run_coroutine_in_new_thread(
        estimate_costs_async(context_pack, azure_proposal, aws_proposal, gcp_proposal, model)
    )


def format_cost_comparison(comparison: CostComparison) -> str:
    lines = ["# Estimacion de Costos Mensuales\n"]
    lines.append(f"{comparison.summary}\n")

    for est in comparison.estimates:
        lines.append(f"## {est.provider.upper()}")
        lines.append(f"- **MVP**: ${est.mvp_monthly_low:,.0f} - ${est.mvp_monthly_high:,.0f} /mes")
        lines.append(f"- **Produccion**: ${est.production_monthly_low:,.0f} - ${est.production_monthly_high:,.0f} /mes")
        lines.append(f"- **Drivers de costo**: {', '.join(est.key_cost_drivers)}")
        lines.append(f"- **Tips de optimizacion**: {', '.join(est.optimization_tips)}")
        lines.append("")

    lines.append(f"**MVP mas economico**: {comparison.cheapest_mvp}")
    lines.append(f"**Produccion mas economica**: {comparison.cheapest_production}")
    return "\n".join(lines)
