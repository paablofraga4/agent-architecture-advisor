import pytest
import json
from agent_arena.planner import (
    extract_json_string_from_text,
    repair_schema_like_output,
    parse_planner_output,
    build_clarification_check,
)
from agent_arena.schemas import PlannerOutput, RetrievalQueries


class TestExtractJsonStringFromText:
    def test_clean_json(self):
        text = '{"key": "value"}'
        assert extract_json_string_from_text(text) == '{"key": "value"}'

    def test_json_with_markdown(self):
        text = '```json\n{"key": "value"}\n```'
        result = extract_json_string_from_text(text)
        assert '"key"' in result

    def test_json_with_surrounding_text(self):
        text = 'Here is the JSON:\n{"key": "value"}\nEnd.'
        result = extract_json_string_from_text(text)
        assert '"key"' in result

    def test_no_json_raises(self):
        with pytest.raises(ValueError, match="No JSON object found"):
            extract_json_string_from_text("no json here")


class TestRepairSchemaLikeOutput:
    def test_normal_data_untouched(self):
        data = {"project_summary": "test", "project_type": "demo"}
        assert repair_schema_like_output(data) == data

    def test_schema_like_unwrapped(self):
        data = {"properties": {"project_summary": "test", "project_type": "demo"}}
        result = repair_schema_like_output(data)
        assert result == {"project_summary": "test", "project_type": "demo"}


class TestParsePlannerOutput:
    def test_valid_output(self):
        data = {
            "project_summary": "Test project",
            "project_type": "demo",
            "required_capabilities": ["api_layer"],
            "non_functional_requirements": ["low_latency"],
            "explicit_constraints": [],
            "inferred_constraints": [],
            "assumptions": [],
            "explicit_cloud_preferences": ["azure"],
            "missing_information": [],
            "retrieval_focus": ["api"],
            "retrieval_queries": {
                "azure": ["azure query"],
                "aws": ["aws query"],
                "gcp": ["gcp query"],
                "neutral": ["neutral query"],
            },
        }
        result = parse_planner_output(json.dumps(data))
        assert isinstance(result, PlannerOutput)
        assert result.project_summary == "Test project"
        assert result.retrieval_queries.gcp == ["gcp query"]


class TestBuildClarificationCheck:
    def _make_planner(self, missing=None, assumptions=None):
        return PlannerOutput(
            project_summary="test",
            project_type="test",
            missing_information=missing or [],
            assumptions=assumptions or [],
            retrieval_queries=RetrievalQueries(azure=["q"], aws=["q"], gcp=["q"], neutral=["q"]),
        )

    def test_no_issues_proceed(self):
        result = build_clarification_check(self._make_planner())
        assert result.proceed_anyway is True

    def test_few_missing_proceed(self):
        result = build_clarification_check(self._make_planner(missing=["a", "b"]))
        assert result.proceed_anyway is True

    def test_critical_assumption_blocks(self):
        result = build_clarification_check(
            self._make_planner(assumptions=["authentication method is unclear"])
        )
        assert result.proceed_anyway is False
        assert len(result.critical_assumptions) == 1

    def test_many_questions_blocks(self):
        result = build_clarification_check(
            self._make_planner(missing=["a", "b", "c"])
        )
        assert result.proceed_anyway is False
