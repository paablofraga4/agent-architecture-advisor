import pytest
from agent_arena.cost_estimator import parse_cost_response, format_cost_comparison
from agent_arena.schemas import CostComparison, CostEstimate


class TestParseCostResponse:
    def test_valid_json(self):
        raw = '''{
            "estimates": [
                {
                    "provider": "azure",
                    "mvp_monthly_low": 50,
                    "mvp_monthly_high": 150,
                    "production_monthly_low": 300,
                    "production_monthly_high": 800,
                    "key_cost_drivers": ["OpenAI tokens"],
                    "optimization_tips": ["Use mini model"]
                }
            ],
            "summary": "Azure is cost-effective",
            "cheapest_mvp": "azure",
            "cheapest_production": "azure"
        }'''
        result = parse_cost_response(raw)
        assert isinstance(result, CostComparison)
        assert len(result.estimates) == 1

    def test_json_with_surrounding_text(self):
        raw = 'Here is the estimate:\n{"estimates": [], "summary": "test", "cheapest_mvp": "aws", "cheapest_production": "aws"}\nDone.'
        result = parse_cost_response(raw)
        assert result.cheapest_mvp == "aws"


class TestFormatCostComparison:
    def test_format_output(self):
        cc = CostComparison(
            estimates=[
                CostEstimate(
                    provider="azure",
                    mvp_monthly_low=50,
                    mvp_monthly_high=150,
                    production_monthly_low=300,
                    production_monthly_high=800,
                    key_cost_drivers=["OpenAI"],
                    optimization_tips=["Use mini"],
                ),
            ],
            summary="Azure is cheapest",
            cheapest_mvp="azure",
            cheapest_production="azure",
        )
        text = format_cost_comparison(cc)
        assert "AZURE" in text
        assert "$50" in text
        assert "$800" in text
