# Decision Record: Vertex AI Search for RAG on GCP

## Problem

The project required a managed retrieval solution for building grounded AI applications on Google Cloud Platform.

The system needed to ingest, index and retrieve information from both structured and unstructured data sources to support RAG workflows.

## Context

The architecture included RAG-based agents that needed access to enterprise knowledge bases. Documents included PDFs, web pages, structured databases and internal wikis.

The team needed a retrieval layer that integrated natively with Vertex AI for grounding LLM responses with relevant source material.

Provider: GCP.

## Requirements

- Support unstructured document ingestion (PDFs, HTML, text).
- Support structured data sources.
- Provide semantic and keyword search capabilities.
- Integrate with Vertex AI models for grounding.
- Handle chunking and embedding automatically.
- Provide relevance tuning and ranking controls.
- Managed service with minimal operational overhead.

## Decision

Vertex AI Search was selected as the GCP retrieval layer for RAG-based agent architectures.

## Why this decision was made

Vertex AI Search was chosen because it provides end-to-end managed retrieval that integrates directly with the Vertex AI platform. This reduces the number of components the team needs to manage independently.

Key factors:
- Native grounding API allows LLM responses to cite retrieved sources directly.
- Automatic document processing handles chunking, embedding and indexing without custom pipelines.
- Supports multiple data store types including unstructured documents, structured data and website content.
- Built-in ranking and relevance tuning reduces the need for custom retrieval logic.
- Integrates with Vertex AI Agents and Gemini models through the grounding API.

## Alternatives considered

### Pinecone on GCP

Pinecone was considered as a managed vector database. It was not selected because it requires a separate embedding pipeline and does not integrate natively with Vertex AI grounding. Pinecone remains a valid option for teams that need more control over the embedding and retrieval process.

### Self-hosted Qdrant on GKE

Self-hosted Qdrant on GKE was considered for full control over the vector search layer. It was not selected because it increases operational overhead with cluster management, scaling and backup responsibilities. Qdrant on GKE is a valid option for teams that need custom similarity metrics or want to avoid vendor lock-in.

## Trade-offs

### Pros

- Fully managed retrieval pipeline.
- Native integration with Vertex AI and Gemini grounding.
- Supports unstructured, structured and website data stores.
- Automatic chunking and embedding.
- Built-in relevance tuning and ranking.
- Reduces custom pipeline code.

### Cons

- Less flexible than self-managed vector databases for custom retrieval strategies.
- Vendor lock-in to GCP ecosystem.
- Limited control over chunking strategies and embedding models compared to custom pipelines.
- Pricing can be opaque for high-volume retrieval workloads.
- Newer service with evolving feature set.

## When to use this decision

Use Vertex AI Search when:
- The architecture is GCP-native.
- The team wants managed document ingestion and retrieval.
- Grounding LLM responses with source citations is required.
- The data includes a mix of structured and unstructured sources.
- Reducing custom retrieval pipeline code is a priority.

## When not to use this decision

Avoid Vertex AI Search when:
- The team needs full control over embedding models and chunking strategies.
- The architecture must remain cloud-agnostic.
- The retrieval workload requires custom similarity metrics or filtering logic.
- The project is an MVP where a local vector database is sufficient.
