# Decision Record: OpenSearch for Hybrid Search on AWS

## Problem

The project required a search layer that combines vector similarity search with traditional keyword search on AWS.

The system needed hybrid retrieval to improve result quality for RAG agents that handle both semantic and exact-match queries.

## Context

The architecture included RAG-based agents that needed to retrieve documents using both semantic meaning and keyword precision. Pure vector search missed exact terminology while pure keyword search missed semantically related content.

The team needed an AWS-native solution that supports both search modes in a single service.

Provider: AWS.

## Requirements

- Support vector similarity search (k-NN).
- Support traditional keyword and BM25 search.
- Combine vector and keyword scores in hybrid queries.
- Integrate natively with AWS services.
- Provide monitoring and dashboard capabilities.
- Handle document ingestion and indexing at scale.
- Support metadata filtering alongside search.

## Decision

Amazon OpenSearch Service was selected as the hybrid search layer for AWS-based RAG architectures.

## Why this decision was made

OpenSearch was chosen because it supports both k-NN vector search and traditional BM25 keyword search in a single service. This enables hybrid retrieval strategies without running separate systems.

Key factors:
- The k-NN plugin supports multiple vector similarity algorithms (HNSW, IVF, Faiss).
- Native AWS integration with IAM, VPC, CloudWatch and other services.
- OpenSearch Dashboards provides built-in monitoring and query debugging.
- Hybrid search can be implemented using search pipelines that combine scores from vector and keyword queries.
- Supports metadata filtering, aggregations and complex query logic alongside vector search.

## Alternatives considered

### Pinecone

Pinecone was considered as a managed vector database. It was not selected because it does not provide native keyword search and requires a separate system for BM25 retrieval. Pinecone is a valid option when pure vector search is sufficient.

### Bedrock Knowledge Bases

Bedrock Knowledge Bases was considered for fully managed RAG. It was not selected because it provides less control over the retrieval strategy, ranking and hybrid search configuration. Bedrock Knowledge Bases is a valid option for simpler RAG use cases where managed defaults are acceptable.

### Amazon Kendra

Kendra was considered for enterprise search. It was not selected because it is optimized for enterprise document search rather than custom hybrid vector and keyword retrieval. Kendra is a valid option for document search with built-in connectors.

## Trade-offs

### Pros

- Supports vector and keyword search in a single service.
- k-NN plugin with multiple algorithm options.
- Native AWS integration and IAM-based access control.
- OpenSearch Dashboards for monitoring and debugging.
- Flexible query DSL for complex retrieval logic.
- Supports search pipelines for score normalization and combination.

### Cons

- Operational complexity for cluster sizing, shard management and index tuning.
- Requires more configuration than fully managed alternatives like Bedrock Knowledge Bases.
- Cluster costs are continuous even during low-traffic periods (no scale-to-zero).
- Hybrid search score normalization requires careful tuning.
- Learning curve for OpenSearch query DSL and k-NN configuration.

## When to use this decision

Use OpenSearch when:
- The architecture needs combined vector and keyword search.
- Fine-grained control over retrieval ranking is required.
- The system is AWS-native and needs IAM integration.
- Monitoring and query debugging through dashboards is important.
- The team has experience with Elasticsearch or OpenSearch.

## When not to use this decision

Avoid OpenSearch when:
- Pure vector search is sufficient for the use case.
- The team wants a fully managed RAG solution with no cluster management.
- The workload is small enough for a simpler retrieval approach.
- Cost optimization requires scale-to-zero capabilities.
