import json
from pathlib import Path

from agent_arena.audit import (
    new_run_id, compute_kb_hash, compute_prompts_hash,
    build_snapshot, save_snapshot, load_snapshot, verify_snapshot, list_snapshots,
)
from agent_arena.schemas import (
    AgentArenaResult, ContextPack, BusinessContext, PlannerOutput,
    RetrievalQueries, CitationValidation, JudgeVerdict, DEFAULT_BUSINESS_CONTEXT,
)


def _dummy_result():
    pack = ContextPack(
        user_idea="dummy idea",
        business_context=DEFAULT_BUSINESS_CONTEXT,
        planner_output=PlannerOutput(
            project_summary="dummy", project_type="dummy",
            retrieval_queries=RetrievalQueries(),
        ),
        final_queries=RetrievalQueries(),
        azure_contexts=[], aws_contexts=[], gcp_contexts=[], neutral_contexts=[],
        azure_context_block="", aws_context_block="", gcp_context_block="",
    )
    return AgentArenaResult(
        context_pack=pack,
        azure_proposal="a", aws_proposal="b", gcp_proposal="",
        azure_validation=CitationValidation(cited_ids=["CTX-0001"], invalid_ids=[], has_citations=True, valid=True),
        aws_validation=CitationValidation(cited_ids=["CTX-0002"], invalid_ids=[], has_citations=True, valid=True),
        final_comparison="cmp", final_architecture_proposal="final",
        full_report="r",
        verdict=JudgeVerdict(winner="azure", confidence="clear", score_gap=25, runners_up_within_gap=[], reasoning_summary="."),
    )


def test_run_id_is_sortable_and_unique():
    a = new_run_id()
    b = new_run_id()
    assert a != b
    assert len(a) == 24  # YYYYMMDD-HHMMSS-XXXXXXXX = 8+1+6+1+8


def test_kb_and_prompts_hash_are_deterministic():
    assert compute_kb_hash() == compute_kb_hash()
    assert compute_prompts_hash() == compute_prompts_hash()


def test_snapshot_roundtrip_and_signature_verifies():
    run_id = new_run_id()
    rec = build_snapshot(
        run_id=run_id, user_idea="x", model="gpt-4o-mini",
        seed=42, temperature=0.0, started_at=1.0, finished_at=2.5,
        client_id="test_client", result=_dummy_result(),
    )
    path = save_snapshot(rec)
    assert path.exists()
    loaded = load_snapshot(run_id)
    assert verify_snapshot(loaded) is True
    # Tamper detection
    loaded["user_idea"] = "tampered"
    assert verify_snapshot(loaded) is False
    # Cleanup
    path.unlink()


def test_list_snapshots_filters_by_client():
    rec1 = build_snapshot(
        run_id=new_run_id(), user_idea="x", model="m", seed=42, temperature=0.0,
        started_at=1.0, finished_at=2.0, client_id="cli_a", result=_dummy_result(),
    )
    rec2 = build_snapshot(
        run_id=new_run_id(), user_idea="y", model="m", seed=42, temperature=0.0,
        started_at=1.0, finished_at=2.0, client_id="cli_b", result=_dummy_result(),
    )
    p1 = save_snapshot(rec1)
    p2 = save_snapshot(rec2)
    try:
        a = list_snapshots(client_id="cli_a")
        b = list_snapshots(client_id="cli_b")
        assert any(r["run_id"] == rec1["run_id"] for r in a)
        assert all(r["run_id"] != rec1["run_id"] for r in b)
    finally:
        p1.unlink()
        p2.unlink()
