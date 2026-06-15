import pytest
from agent_arena.validators import (
    extract_cited_context_ids,
    validate_citations_typed,
    ids_from_text,
)


class TestExtractCitedContextIds:
    def test_extracts_single_id(self):
        assert extract_cited_context_ids("See [CTX-0001] for details") == {"CTX-0001"}

    def test_extracts_multiple_ids(self):
        text = "Based on [CTX-0001] and [CTX-0042], we recommend..."
        assert extract_cited_context_ids(text) == {"CTX-0001", "CTX-0042"}

    def test_empty_string(self):
        assert extract_cited_context_ids("") == set()

    def test_none_input(self):
        assert extract_cited_context_ids(None) == set()

    def test_no_citations(self):
        assert extract_cited_context_ids("No citations here") == set()

    def test_deduplicates(self):
        text = "[CTX-0001] and again [CTX-0001]"
        assert extract_cited_context_ids(text) == {"CTX-0001"}

    def test_inline_without_brackets(self):
        assert extract_cited_context_ids("Evidence CTX-0005 shows...") == {"CTX-0005"}


class TestValidateCitationsTyped:
    def test_valid_citations(self):
        result = validate_citations_typed(
            proposal="Component A [CTX-0001], Component B [CTX-0002]",
            valid_context_ids={"CTX-0001", "CTX-0002", "CTX-0003"},
        )
        assert result.valid is True
        assert result.has_citations is True
        assert result.invalid_ids == []

    def test_invalid_citation(self):
        result = validate_citations_typed(
            proposal="Component A [CTX-0001], Component B [CTX-9999]",
            valid_context_ids={"CTX-0001", "CTX-0002"},
        )
        assert result.valid is False
        assert "CTX-9999" in result.invalid_ids

    def test_no_citations_is_invalid(self):
        result = validate_citations_typed(
            proposal="No citations at all",
            valid_context_ids={"CTX-0001"},
        )
        assert result.valid is False
        assert result.has_citations is False


class TestIdsFromText:
    def test_returns_sorted_unique(self):
        text = "[CTX-0003] [CTX-0001] [CTX-0003] [CTX-0002]"
        assert ids_from_text(text) == ["CTX-0001", "CTX-0002", "CTX-0003"]

    def test_empty(self):
        assert ids_from_text("") == []
