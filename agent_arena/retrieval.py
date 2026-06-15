from __future__ import annotations

from typing import List
from pydantic import ValidationError
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

from .config import COLLECTION_NAME, EMBEDDING_MODEL_NAME, QDRANT_HOST, QDRANT_PORT
from .schemas import Provider, RetrievedContext
from .reranker import rerank_contexts

_embedding_model = None
_qdrant_client = None


def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _embedding_model


def get_qdrant_client():
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    return _qdrant_client


def build_provider_filter(provider: str | None = None):
    if provider is None:
        return None

    from qdrant_client.models import FieldCondition, Filter, MatchValue

    return Filter(
        must=[
            FieldCondition(
                key="provider",
                match=MatchValue(value=provider),
            )
        ]
    )


def retrieve_contexts(
    query: str,
    provider: str | None = None,
    top_k: int = 5,
) -> list[dict]:
    embedding_model = get_embedding_model()
    client = get_qdrant_client()

    query_vector = embedding_model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).tolist()

    search_filter = build_provider_filter(provider)

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=search_filter,
        limit=top_k,
        with_payload=True,
        with_vectors=False,
    )

    contexts = []
    for point in response.points:
        payload = dict(point.payload)
        payload["score"] = point.score
        contexts.append(payload)

    return contexts


def validate_retrieved_contexts(raw_contexts: List[dict]) -> List[RetrievedContext]:
    contexts = []

    for raw in raw_contexts:
        try:
            contexts.append(RetrievedContext.model_validate(raw))
        except ValidationError as e:
            raise ValueError(
                f"Retrieved context does not match schema:\n{e}\n\nRaw context:\n{raw}"
            ) from e

    return contexts


def retrieve_typed_contexts(
    query: str,
    provider: Provider,
    top_k: int,
    use_reranker: bool = True,
) -> List[RetrievedContext]:
    # Fetch more candidates when reranking so the reranker has room to reorder
    fetch_k = top_k * 2 if use_reranker else top_k
    raw_contexts = retrieve_contexts(
        query=query,
        provider=provider,
        top_k=fetch_k,
    )
    typed = validate_retrieved_contexts(raw_contexts)
    if use_reranker:
        typed = rerank_contexts(query=query, contexts=typed, top_k=top_k)
    return typed


def format_context_block(contexts: list[dict]) -> str:
    blocks = []
    for ctx in contexts:
        block = f"""[{ctx['context_id']}]
Provider: {ctx['provider']}
Document type: {ctx['document_type']}
Source: {ctx['source_file']}
Section: {ctx['section_path']}

{ctx['chunk_text']}"""
        blocks.append(block)
    return "\n\n" + ("\n\n" + "-" * 100 + "\n\n").join(blocks)


def format_context_block_typed(contexts: List[RetrievedContext]) -> str:
    blocks = []

    for ctx in contexts:
        block = f"""[{ctx.context_id}]
Provider: {ctx.provider}
Document type: {ctx.document_type}
Source: {ctx.source_file}
Section: {ctx.section_path}

{ctx.chunk_text}"""
        blocks.append(block)

    return "\n\n" + ("\n\n" + "-" * 100 + "\n\n").join(blocks)


def build_contexts_summary(context_pack) -> str:
    lines = []

    lines.append("## Azure contexts")
    for ctx in context_pack.azure_contexts:
        lines.append(
            f"- {ctx.context_id} | {ctx.provider} | {ctx.document_type} | {ctx.source_file} | {ctx.section_path}"
        )

    lines.append("\n## AWS contexts")
    for ctx in context_pack.aws_contexts:
        lines.append(
            f"- {ctx.context_id} | {ctx.provider} | {ctx.document_type} | {ctx.source_file} | {ctx.section_path}"
        )

    if context_pack.gcp_contexts:
        lines.append("\n## GCP contexts")
        for ctx in context_pack.gcp_contexts:
            lines.append(
                f"- {ctx.context_id} | {ctx.provider} | {ctx.document_type} | {ctx.source_file} | {ctx.section_path}"
            )

    lines.append("\n## Neutral contexts")
    for ctx in context_pack.neutral_contexts:
        lines.append(
            f"- {ctx.context_id} | {ctx.provider} | {ctx.document_type} | {ctx.source_file} | {ctx.section_path}"
        )

    return "\n".join(lines)
