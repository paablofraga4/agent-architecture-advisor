from __future__ import annotations

from typing import List

from .config import RERANKER_ENABLED, RERANKER_MODEL_NAME, RERANKER_TOP_K
from .schemas import RetrievedContext

_reranker_model = None


def get_reranker_model():
    global _reranker_model
    if _reranker_model is None:
        from sentence_transformers import CrossEncoder
        _reranker_model = CrossEncoder(RERANKER_MODEL_NAME)
    return _reranker_model


def rerank_contexts(
    query: str,
    contexts: List[RetrievedContext],
    top_k: int = RERANKER_TOP_K,
) -> List[RetrievedContext]:
    if not RERANKER_ENABLED or not contexts:
        return contexts

    model = get_reranker_model()
    pairs = [(query, ctx.chunk_text) for ctx in contexts]
    scores = model.predict(pairs)

    for ctx, score in zip(contexts, scores):
        ctx.rerank_score = float(score)

    ranked = sorted(contexts, key=lambda c: c.rerank_score or 0.0, reverse=True)
    return ranked[:top_k]
