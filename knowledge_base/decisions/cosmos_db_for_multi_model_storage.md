# Decision Record: Cosmos DB for Multi-Model Data on Azure

## Problem

The project required a flexible database for storing metadata, session state and vector embeddings on Azure.

The system needed a single database service that could handle multiple data models and access patterns without running separate database systems.

## Context

The architecture included AI agents that needed to persist conversation sessions, store document metadata, maintain user preferences and perform vector similarity search for retrieval. Each of these workloads had different data model requirements.

The team wanted an Azure-native solution that could consolidate multiple storage concerns into a single managed service.

Provider: Azure.

## Requirements

- Support document-style storage for metadata and sessions.
- Support vector search for embeddings.
- Provide multiple API options for different data models.
- Offer global distribution for multi-region deployments.
- Provide a serverless option for variable workloads.
- Integrate natively with Azure services.
- Handle both transactional and analytical access patterns.

## Decision

Azure Cosmos DB was selected as the multi-model database for Azure-based agent architectures.

## Why this decision was made

Cosmos DB was chosen because it supports multiple data models and APIs within a single managed service. This allows the team to store session data, metadata and vector embeddings without operating separate database systems.

Key factors:
- Multiple API support (NoSQL, MongoDB, PostgreSQL, Cassandra, Gremlin, Table) enables using the right data model for each workload.
- Integrated vector search allows combining metadata queries with similarity search in a single query.
- Global distribution with configurable consistency levels supports multi-region agent deployments.
- Serverless tier provides cost-efficient scaling for variable or bursty workloads.
- Native integration with Azure Functions, Azure AI Services and other Azure components.

## Alternatives considered

### PostgreSQL Flexible Server

PostgreSQL Flexible Server with pgvector was considered for relational storage with vector search. It was not selected because it provides a single data model and does not offer the same global distribution or serverless scaling. PostgreSQL is a valid option for teams that prefer relational schemas and have simpler distribution requirements.

### Azure SQL

Azure SQL was considered for relational storage. It was not selected because it lacks native vector search support and the document-style flexibility needed for session and metadata storage.

### MongoDB Atlas on Azure

MongoDB Atlas was considered for document storage. It was not selected because it runs outside the Azure-native management plane and adds a separate vendor relationship. MongoDB Atlas is a valid option for teams already standardized on MongoDB.

## Trade-offs

### Pros

- Multiple APIs for different data models in a single service.
- Integrated vector search for RAG workloads.
- Global distribution with tunable consistency.
- Serverless tier for cost-efficient variable workloads.
- Azure-native with full platform integration.
- Automatic indexing reduces operational tuning.

### Cons

- Cost at scale can be significant, especially with provisioned throughput.
- Request Unit (RU) model adds complexity to capacity planning and cost estimation.
- Vendor lock-in to Azure Cosmos DB APIs and pricing model.
- Vector search capabilities are newer and less mature than dedicated vector databases.
- Cross-partition queries can be expensive and require careful data modeling.

## When to use this decision

Use Cosmos DB when:
- The architecture needs multiple data models in a single service.
- Vector search, session storage and metadata live in the same platform.
- Global distribution or multi-region deployment is required.
- The workload is variable and benefits from serverless scaling.
- The architecture is Azure-native.

## When not to use this decision

Avoid Cosmos DB when:
- A single relational data model is sufficient.
- The team needs a dedicated high-performance vector database.
- Cost predictability is critical and the RU model adds too much uncertainty.
- The workload is small enough for a simple managed PostgreSQL instance.
