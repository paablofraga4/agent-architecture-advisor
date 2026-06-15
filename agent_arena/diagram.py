from __future__ import annotations

from .llm import call_llm_async, _run_coroutine_in_new_thread


DIAGRAM_SYSTEM_PROMPT = """You are a technical diagram generator. You produce Mermaid diagram code from architecture proposals.

STRICT RULES:
1. Output ONLY valid Mermaid code inside a ```mermaid code block.
2. Use flowchart TD (top-down) layout.
3. Include all major components mentioned in the proposal.
4. Group components by layer (ingestion, processing, storage, serving, observability).
5. Use subgraph blocks for logical grouping.
6. Use clear, short labels.
7. Show data flow direction with arrows.
8. Do not include explanatory text outside the mermaid block.
9. Keep it readable — max 25 nodes.
10. Use appropriate shapes: databases as cylinders [(...)], services as rounded rectangles(...), queues as stadium-shaped ([...]).
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
