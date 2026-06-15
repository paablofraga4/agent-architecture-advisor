from __future__ import annotations

from .llm import call_llm_async, _run_coroutine_in_new_thread


DIAGRAM_SYSTEM_PROMPT = """You are a technical diagram generator. You produce D2 (https://d2lang.com) diagram code from architecture proposals.

OUTPUT FORMAT:
Return ONLY valid D2 code inside a ```d2 code block. No prose, no markdown headings.

D2 SYNTAX RULES:
1. First line: `direction: right`
2. Group components into containers by layer. Use these container names if applicable:
   ingestion, processing, ai, storage, serving, observability
   Example:
     ai: AI / Agents {
       openai: Azure OpenAI {shape: cloud}
       agent: Agent Framework {shape: hexagon}
     }
3. Component shape by kind:
   - users / external clients: {shape: person}
   - APIs / gateways: {shape: hexagon}
   - compute / functions / agents: {shape: cloud}
   - databases / vector stores: {shape: cylinder}
   - queues / streams: {shape: queue}
   - storage / blobs: {shape: page}
4. Edges show data flow. Label them when non-obvious:  api -> openai: completion
5. Color nodes by cloud provider with style.fill:
   - Azure (Azure/Microsoft services):  {style.fill: "#0078D4"; style.stroke: "#005A9E"; style.font-color: "#ffffff"}
   - AWS    (Amazon/AWS services):      {style.fill: "#FF9900"; style.stroke: "#CC7A00"; style.font-color: "#1a1a1a"}
   - GCP    (Google/GCP services):      {style.fill: "#4285F4"; style.stroke: "#1A73E8"; style.font-color: "#ffffff"}
   - Neutral (third-party, on-prem):    {style.fill: "#374151"; style.stroke: "#1f2937"; style.font-color: "#ffffff"}
6. Keep it readable: max 20 nodes, short labels (no more than 4 words).
7. No `classDef`, no Mermaid syntax. This is D2.

EXAMPLE (target style — do NOT copy the components, only the shape of the syntax):

```d2
direction: right

ingestion: Ingestion {
  user: User {shape: person}
}

ai: AI {
  openai: Azure OpenAI {shape: cloud; style.fill: "#0078D4"; style.stroke: "#005A9E"; style.font-color: "#ffffff"}
}

storage: Storage {
  search: Azure AI Search {shape: cylinder; style.fill: "#0078D4"; style.stroke: "#005A9E"; style.font-color: "#ffffff"}
}

ingestion.user -> ai.openai: query
ai.openai -> storage.search: retrieve
```
"""


def build_diagram_prompt(final_proposal: str, user_idea: str) -> str:
    return f"""{DIAGRAM_SYSTEM_PROMPT}

USER PROJECT:
{user_idea}

FINAL ARCHITECTURE PROPOSAL:
{final_proposal}

Generate a D2 diagram of this architecture following all the rules above.
"""


def extract_d2_code(llm_output: str) -> str:
    import re
    match = re.search(r"```d2\s*\n(.*?)```", llm_output, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Fallback: maybe model emitted mermaid by mistake — strip the fence anyway
    match = re.search(r"```(?:mermaid)?\s*\n(.*?)```", llm_output, re.DOTALL)
    if match:
        return match.group(1).strip()
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
    return extract_d2_code(raw)


def generate_diagram(
    final_proposal: str,
    user_idea: str,
    model: str = "gpt-4o-mini",
) -> str:
    return _run_coroutine_in_new_thread(
        generate_diagram_async(final_proposal, user_idea, model)
    )
