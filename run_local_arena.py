from agent_arena.arena import run_agent_arena_with_llm_planner_pydantic
from agent_arena.config import DEFAULT_MODEL
from agent_arena.validators import format_evidence_trace
from agent_arena.cost_estimator import format_cost_comparison


user_idea = """
Quiero construir una herramienta de gestión de iniciativas. Esta herramienta debe brindar la posibilidad de dar de alta una iniciativa y poder acompañar todo el proceso de su desarrollo hasta la puesta en producción. La idea es que sirva para gestionar iniciativas de IA. También debe gestionar el buzón del departamento para poder hacer ese seguimineto del desarrollo y de su post-producción.
"""

result = run_agent_arena_with_llm_planner_pydantic(user_idea, model=DEFAULT_MODEL)

print(result.full_report)
print("\n\n" + "=" * 120 + "\n")
print(format_evidence_trace(result))

if result.cost_comparison:
    print("\n\n" + "=" * 120 + "\n")
    print(format_cost_comparison(result.cost_comparison))

if result.mermaid_diagram:
    print("\n\n" + "=" * 120 + "\n")
    print("## Mermaid Diagram\n")
    print(f"```mermaid\n{result.mermaid_diagram}\n```")

if result.rewrite_counts:
    print("\n\n" + "=" * 120 + "\n")
    print("## Rewrite counts")
    for agent, count in result.rewrite_counts.items():
        print(f"  {agent}: {count}")
