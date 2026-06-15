# Decision Record: Qdrant for Local RAG MVP

## Problem

The project needed a local retrieval layer for a RAG prototype without using paid cloud resources.

## Context

The first version of the system was intended to run locally in notebooks. The goal was to validate document ingestion, chunking, embeddings, retrieval and agent grounding before moving to Azure or AWS.

## Requirements

- Run locally.
- Avoid cloud cost.
- Store vector embeddings.
- Support semantic similarity search.
- Support metadata filtering.
- Be easy to start with Docker.
- Be portable.
- Allow experimentation before cloud deployment.

## Decision

Qdrant was selected as the local vector database for the MVP.

## Why this decision was made

Qdrant was chosen because it is open-source, runs locally with Docker, supports vector search and supports metadata filtering. It allows the project to validate the RAG architecture without paying for managed cloud services.

## Alternatives considered

### Azure AI Search

Azure AI Search was considered for the Azure enterprise version. It was not selected for the local MVP because it requires Azure resources and an active subscription.

### Bedrock Knowledge Bases

Bedrock Knowledge Bases was considered for the AWS enterprise version. It was not selected for the local MVP because it requires AWS resources.

### PostgreSQL with pgvector

PostgreSQL with pgvector was considered. It was not selected for the first MVP because Qdrant provides a simpler vector-search-focused setup for experimentation.

## Trade-offs

### Pros

- Runs locally.
- No cloud cost.
- Open-source.
- Supports vector search.
- Supports metadata filtering.
- Easy to run with Docker.
- Good for MVP experimentation.

### Cons

- Not a fully managed cloud service.
- Requires self-management.
- Does not provide the same enterprise search features as Azure AI Search or OpenSearch.
- Production deployment requires additional operational planning.

## When to use this decision

Use Qdrant when:
- The system is in MVP stage.
- Local development is required.
- Cost must be avoided.
- The goal is to validate retrieval quality.
- The team wants portability.

## When not to use this decision

Avoid Qdrant when:
- The organization requires a fully managed cloud-native search service.
- The architecture must be entirely Azure-native.
- The architecture must be entirely AWS-native.
- The team does not want to manage vector infrastructure.