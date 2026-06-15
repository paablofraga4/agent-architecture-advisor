import pytest
from unittest.mock import patch
from agent_arena.schemas import RetrievedContext
from agent_arena.reranker import rerank_contexts


def _make_ctx(ctx_id, text, score=0.5):
    return RetrievedContext(
        context_id=ctx_id,
        provider="azure",
        document_type="cloud_reference",
        source_file="test.md",
        section_path="root > test",
        chunk_text=text,
        score=score,
    )


class TestRerankerDisabled:
    @patch("agent_arena.reranker.RERANKER_ENABLED", False)
    def test_passthrough_when_disabled(self):
        contexts = [_make_ctx("CTX-0001", "text 1"), _make_ctx("CTX-0002", "text 2")]
        result = rerank_contexts("query", contexts, top_k=2)
        assert len(result) == 2
        assert result[0].context_id == "CTX-0001"

    @patch("agent_arena.reranker.RERANKER_ENABLED", False)
    def test_empty_contexts(self):
        result = rerank_contexts("query", [], top_k=5)
        assert result == []
