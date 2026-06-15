from agent_arena.audit import build_snapshot, save_snapshot, new_run_id
from agent_arena.memory import enrich_business_context_with_memory, load_client_history
from agent_arena.schemas import (
    AgentArenaResult, ContextPack, PlannerOutput, RetrievalQueries,
    CitationValidation, JudgeVerdict, DEFAULT_BUSINESS_CONTEXT,
)


def _make_result(summary: str, winner: str):
    pack = ContextPack(
        user_idea=summary, business_context=DEFAULT_BUSINESS_CONTEXT,
        planner_output=PlannerOutput(project_summary=summary, project_type="t", retrieval_queries=RetrievalQueries()),
        final_queries=RetrievalQueries(),
        azure_contexts=[], aws_contexts=[], gcp_contexts=[], neutral_contexts=[],
        azure_context_block="", aws_context_block="", gcp_context_block="",
    )
    return AgentArenaResult(
        context_pack=pack, azure_proposal="a", aws_proposal="b",
        azure_validation=CitationValidation(cited_ids=[], invalid_ids=[], has_citations=False, valid=False),
        aws_validation=CitationValidation(cited_ids=[], invalid_ids=[], has_citations=False, valid=False),
        final_comparison="", final_architecture_proposal="", full_report="",
        verdict=JudgeVerdict(winner=winner, confidence="clear", score_gap=30, runners_up_within_gap=[], reasoning_summary="."),
    )


def test_memory_injects_previous_decisions_into_business_context_notes():
    client = "mem_test_client"
    # Seed two past snapshots
    paths = []
    for summary, w in [("Project A RAG", "azure"), ("Project B fraud", "aws")]:
        rid = new_run_id()
        rec = build_snapshot(
            run_id=rid, user_idea=summary, model="m", seed=42, temperature=0.0,
            started_at=1.0, finished_at=2.0, client_id=client,
            result=_make_result(summary, w),
        )
        paths.append(save_snapshot(rec))
    try:
        enriched = enrich_business_context_with_memory(DEFAULT_BUSINESS_CONTEXT, client)
        assert "Project A RAG" in enriched.notes
        assert "Project B fraud" in enriched.notes
        assert "AZURE" in enriched.notes
        assert "AWS" in enriched.notes

        history = load_client_history(client)
        assert len(history) == 2
    finally:
        for p in paths:
            p.unlink()


def test_no_memory_returns_original_context():
    out = enrich_business_context_with_memory(DEFAULT_BUSINESS_CONTEXT, None)
    assert out is DEFAULT_BUSINESS_CONTEXT
    out2 = enrich_business_context_with_memory(DEFAULT_BUSINESS_CONTEXT, "no_history_client_xyz")
    assert out2.notes == DEFAULT_BUSINESS_CONTEXT.notes
