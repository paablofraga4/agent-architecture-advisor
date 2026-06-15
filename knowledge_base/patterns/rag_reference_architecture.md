# Reference architecture: production RAG over enterprise documents

**Provider:** neutral
**Document type:** architecture_pattern
**Tags:** rag, retrieval, vector_search, ingestion, reranking, grounding, llm

A provider-agnostic blueprint for a grounded RAG assistant. Map each box to a managed
service from the target cloud.

## Logical components
1. **Ingestion pipeline**: pull documents → parse (OCR for scanned PDFs) → clean →
   chunk (typically 300–800 tokens, 10–20% overlap) → embed → upsert to the index.
   Run as batch or event-driven on upload. Track a content hash to avoid re-embedding.
2. **Vector index**: stores embeddings + metadata for filtering (tenant, doc type,
   sensitivity). Prefer hybrid (vector + keyword) for exact-term recall.
3. **Retriever + reranker**: fetch top-N (e.g. 20) candidates, optionally rerank with a
   cross-encoder to top-k (e.g. 5). Reranking improves precision at a latency cost.
4. **Orchestrator / agent**: builds the grounded prompt, calls the LLM, enforces
   citations, and can call tools. Keep it stateless behind an API.
5. **LLM**: generation grounded strictly on retrieved context to limit hallucination.
6. **Serving API**: auth, rate limiting, streaming responses, request/trace logging.

## Sizing heuristics
- Vectors ≈ documents × avg chunks/doc. 100k docs × 3 chunks ≈ 300k vectors.
- Index size ≈ vectors × dims × 4 bytes. 300k × 1536 × 4 ≈ ~1.8 GB raw (before overhead).
- Embedding throughput: batch encode; a CPU model does ~10²–10³ chunks/s, GPU far more.
- Latency budget (p99): retrieval ~50–150 ms + rerank ~50–200 ms + LLM ~0.5–3 s.
- Concurrency: size LLM/serving replicas for peak QPS, not average.

## Quality & safety
- Require inline citations to source chunks; reject ungrounded claims.
- Evaluate with a golden Q/A set: groundedness, answer relevance, retrieval hit-rate.
- Add a guardrail for PII and prompt injection on both input and retrieved content.

## Common failure modes
- **Stale index**: ingestion lag → answers miss new documents. Mitigate with event-driven re-index.
- **Low recall on exact terms**: pure vector misses article numbers/IDs → use hybrid search.
- **Context overflow**: too many chunks → truncated prompt; cap k and compress.
- **Cost blowup**: re-embedding unchanged docs and uncached repeat queries.
