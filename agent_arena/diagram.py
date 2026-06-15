from __future__ import annotations

from .llm import call_llm_async, _run_coroutine_in_new_thread


DIAGRAM_SYSTEM_PROMPT = """You are a technical diagram generator. You produce Mermaid diagram code from architecture proposals.

STRICT RULES:
1. Output ONLY valid Mermaid code inside a ```mermaid code block.
2. Use flowchart TD (top-down) layout.
3. Include all major components mentioned in the proposal.
4. Group components by layer using subgraph blocks: Ingestion, Processing, AI/Agents, Storage, Serving, Observability. Omit layers that don't apply.
5. Use clear, short labels (no more than 4 words per node).
6. Show data flow direction with arrows; use labeled arrows for non-obvious flows: A -->|event| B
7. Do not include explanatory text outside the mermaid block.
8. Keep it readable — max 25 nodes.
9. Use shapes by component kind:
   - databases / vector stores: [(name)]
   - object storage / blobs: [/name/]
   - queues / streams / event buses: ([name])
   - serverless / compute services: (name)
   - LLMs / agents: {{name}}
   - users / external systems: ((name))
10. ALWAYS append these classDef blocks at the end and assign each node to ONE of the provider classes
    based on the cloud service prefix (Azure/Microsoft -> azure, AWS/Amazon -> aws, GCP/Google -> gcp,
    everything else -> neutral):

    classDef azure   fill:#0078D4,stroke:#005A9E,color:#ffffff
    classDef aws     fill:#FF9900,stroke:#CC7A00,color:#1a1a1a
    classDef gcp     fill:#4285F4,stroke:#1A73E8,color:#ffffff
    classDef neutral fill:#374151,stroke:#1f2937,color:#ffffff

    Example assignment line:  class blob,functions,openai azure
"""


def build_diagram_prompt(final_proposal: str, user_idea: str) -> str:
    return f"""{DIAGRAM_SYSTEM_PROMPT}

USER PROJECT:
{user_idea}

FINAL ARCHITECTURE PROPOSAL:
{final_proposal}

Generate a Mermaid flowchart diagram that visualizes this architecture.
Include the selected cloud provider services as node labels.
Group by architectural layer using subgraph blocks.
"""


def extract_mermaid_code(llm_output: str) -> str:
    import re
    match = re.search(r"```mermaid\s*\n(.*?)```", llm_output, re.DOTALL)
    if match:
        return match.group(1).strip()
    if llm_output.strip().startswith("flowchart") or llm_output.strip().startswith("graph"):
        return llm_output.strip()
    return llm_output.strip()


async def generate_diagram_async(
    final_proposal: str,
    user_idea: str,
    model: str = "gpt-4o-mini",
    trace=None,
) -> str:
    prompt = build_diagram_prompt(final_proposal, user_idea)
    raw = await call_llm_async(
        prompt=prompt,
        model=model,
        trace=trace,
        span_name="diagram_generation",
        metadata={"agent": "diagram"},
        agent_name="diagram_generator_agent",
    )
    return extract_mermaid_code(raw)


def generate_diagram(
    final_proposal: str,
    user_idea: str,
    model: str = "gpt-4o-mini",
) -> str:
    return _run_coroutine_in_new_thread(
        generate_diagram_async(final_proposal, user_idea, model)
    )
