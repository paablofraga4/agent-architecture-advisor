# Decision Record: Bedrock Knowledge Bases for AWS RAG

## Problem

The project required a managed Retrieval-Augmented Generation layer for an AWS-native document assistant. Users needed to ask questions over private documents stored in Amazon S3.

## Context

The organization was already using AWS. Documents were expected to be stored in Amazon S3. The solution needed managed ingestion, embeddings, retrieval and integration with foundation models available through Amazon Bedrock.

## Requirements

- Store private documents in Amazon S3.
- Ingest documents into a retrieval system.
- Generate embeddings.
- Retrieve relevant document chunks.
- Connect retrieval with foundation models.
- Use AWS-native security and IAM.
- Reduce custom infrastructure.
- Support enterprise RAG workflows.

## Decision

Bedrock Knowledge Bases was selected as the managed RAG layer.

## Why this decision was made

Bedrock Knowledge Bases was chosen because it provides an AWS-native managed RAG capability. It can connect documents from Amazon S3, create embeddings, store vectors in a supported vector store and retrieve relevant context for foundation models available through Amazon Bedrock.

## Alternatives considered

### Amazon OpenSearch Service

Amazon OpenSearch Service was considered because it can store vectors and support search workloads. It was not selected as the primary MVP option because Bedrock Knowledge Bases provides a more managed RAG abstraction.

### Qdrant

Qdrant was considered for local prototyping and open-source vector search. It was not selected for the AWS-native managed version because the target architecture prioritized AWS-managed services.

### Custom Lambda-based RAG pipeline

A custom pipeline using Lambda was considered. It was not selected as the main approach because it would require more custom orchestration, monitoring and maintenance.

## Trade-offs

### Pros

- AWS-native managed RAG capability.
- Integrates with Amazon S3.
- Integrates with Amazon Bedrock.
- Reduces custom RAG infrastructure.
- Fits AWS enterprise environments.
- Uses AWS IAM and security model.

### Cons

- AWS-specific.
- Less portable than open-source RAG.
- Less flexible than a fully custom retrieval pipeline.
- Pricing depends on model usage, storage and retrieval infrastructure.

## When to use this decision

Use Bedrock Knowledge Bases when:
- The organization already uses AWS.
- Documents are stored in Amazon S3.
- The solution needs a managed RAG layer.
- The system should integrate with Amazon Bedrock.
- The team wants to reduce custom infrastructure.

## When not to use this decision

Avoid Bedrock Knowledge Bases when:
- The MVP must run fully locally.
- The solution must remain cloud-agnostic.
- The team needs full control over retrieval internals.
- The organization is not using AWS.