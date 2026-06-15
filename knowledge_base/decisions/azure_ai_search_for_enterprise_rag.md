# Decision Record: Azure AI Search for Enterprise RAG

## Problem

The project required a retrieval layer for an enterprise Retrieval-Augmented Generation system. Users needed to ask questions over private documents stored by project, department, document type and date.

## Context

The organization was already using Azure. Documents were expected to be stored in Azure Blob Storage. The solution needed managed infrastructure, semantic retrieval, keyword retrieval, vector search, metadata filtering and integration with Azure OpenAI.

## Requirements

- Store searchable document chunks.
- Support semantic retrieval.
- Support keyword retrieval.
- Support vector search.
- Support hybrid search.
- Support metadata filtering.
- Integrate with Azure Blob Storage.
- Integrate with Azure OpenAI.
- Reduce operational overhead.
- Fit an Azure-native enterprise architecture.

## Decision

Azure AI Search was selected as the retrieval layer.

## Why this decision was made

Azure AI Search was chosen because it provides a managed retrieval service within the Azure ecosystem. It supports keyword search, vector search, hybrid search, semantic ranking and metadata filtering. These capabilities made it suitable for enterprise RAG systems that need to retrieve grounded context from private documents.

## Alternatives considered

### Qdrant

Qdrant was considered because it is open-source, portable and strong for local vector search. It was not selected for the enterprise Azure deployment because the preferred target architecture was Azure-native and managed.

### PostgreSQL with pgvector

PostgreSQL with pgvector was considered for simpler deployments. It was not selected because the project required stronger retrieval capabilities, hybrid search and more advanced search features.

### Pinecone

Pinecone was considered as a managed vector database. It was not selected because it introduced an additional external vendor outside the Azure ecosystem.

## Trade-offs

### Pros

- Managed retrieval service.
- Azure-native integration.
- Supports keyword search.
- Supports vector search.
- Supports hybrid search.
- Supports metadata filtering.
- Suitable for enterprise RAG systems.
- Reduces operational overhead.

### Cons

- Azure-specific.
- Requires an Azure subscription.
- Can increase cost at scale.
- Less portable than open-source alternatives.

## When to use this decision

Use Azure AI Search when:
- The organization already uses Azure.
- The solution needs managed retrieval.
- The system needs hybrid search.
- The system needs metadata filtering.
- The architecture should integrate with Azure Blob Storage.
- The architecture should integrate with Azure OpenAI.
- Operational overhead should be reduced.

## When not to use this decision

Avoid Azure AI Search when:
- The MVP must run fully locally.
- The solution must remain cloud-agnostic.
- The budget must be close to zero.
- Simple vector similarity search is enough.
- The organization is not using Azure.