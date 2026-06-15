import pytest
from agent_arena.schemas import (
    PlannerOutput,
    RetrievalQueries,
    RetrievedContext,
    CostEstimate,
    CostComparison,
    ClarificationRequest,
    ContextPack,
    BusinessContext,
    DEFAULT_BUSINESS_CONTEXT,
)


class TestPlannerOutput:
    def test_ensure_list_from_none(self):
        po = PlannerOutput(
            project_summary="test",
            project_type="test",
            required_capabilities=None,
            retrieval_queries=RetrievalQueries(azure=["q"], aws=["q"], gcp=["q"], neutral=["q"]),
        )
        assert po.required_capabilities == []

    def test_ensure_list_from_string(self):
        po = PlannerOutput(
            project_summary="test",
            project_type="test",
            required_capabilities="single_cap",
            retrieval_queries=RetrievalQueries(azure=["q"], aws=["q"], gcp=["q"], neutral=["q"]),
        )
        assert po.required_capabilities == ["single_cap"]


class TestRetrievalQueries:
    def test_gcp_field_exists(self):
        rq = RetrievalQueries(azure=["a"], aws=["b"], gcp=["c"], neutral=["d"])
        assert rq.gcp == ["c"]

    def test_gcp_defaults_empty(self):
        rq = RetrievalQueries(azure=["a"], aws=["b"], neutral=["d"])
        assert rq.gcp == []


class TestRetrievedContext:
    def test_rerank_score_optional(self):
        ctx = RetrievedContext(
            context_id="CTX-0001",
            provider="azure",
            document_type="cloud_reference",
            source_file="test.md",
            section_path="root > test",
            chunk_text="some text",
        )
        assert ctx.rerank_score is None

    def test_rerank_score_set(self):
        ctx = RetrievedContext(
            context_id="CTX-0001",
            provider="gcp",
            document_type="cloud_reference",
            source_file="test.md",
            section_path="root > test",
            chunk_text="some text",
            rerank_score=0.95,
        )
        assert ctx.rerank_score == 0.95


class TestCostEstimate:
    def test_basic(self):
        est = CostEstimate(
            provider="azure",
            mvp_monthly_low=50,
            mvp_monthly_high=150,
            production_monthly_low=300,
            production_monthly_high=800,
        )
        assert est.provider == "azure"


class TestCostComparison:
    def test_from_dict(self):
        data = {
            "estimates": [
                {
                    "provider": "azure",
                    "mvp_monthly_low": 50,
                    "mvp_monthly_high": 150,
                    "production_monthly_low": 300,
                    "production_monthly_high": 800,
                    "key_cost_drivers": ["OpenAI"],
                    "optimization_tips": ["Use mini model"],
                }
            ],
            "summary": "Azure is cheapest",
            "cheapest_mvp": "azure",
            "cheapest_production": "azure",
        }
        cc = CostComparison.model_validate(data)
        assert len(cc.estimates) == 1
        assert cc.cheapest_mvp == "azure"


class TestBusinessContext:
    def test_default_includes_gcp(self):
        assert "gcp" in DEFAULT_BUSINESS_CONTEXT.preferred_clouds
