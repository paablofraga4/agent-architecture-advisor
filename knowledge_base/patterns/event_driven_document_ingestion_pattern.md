# Architecture Pattern: Event-Driven Document Ingestion

## Problem

A system needs to process documents automatically when new files are uploaded.

Manual ingestion is slow, error-prone and does not scale well when documents arrive continuously.

## Context

The system stores raw documents in an object storage layer. New documents must be detected, processed, normalized and indexed into a retrieval system.

This pattern is common in RAG architectures, document assistants and enterprise knowledge systems.

## Requirements

- Detect new uploaded documents.
- Trigger processing automatically.
- Extract or normalize document metadata.
- Extract text from documents.
- Split text into chunks.
- Index chunks into a retrieval system.
- Keep traceability to the original source document.
- Support retries or failure handling.

## Solution

Use an event-driven ingestion pipeline.

The document storage service emits an event when a new file is uploaded. A processing component receives the event and executes the ingestion logic.

## Generic components

### Object storage

Stores the original documents.

Examples:
- Azure Blob Storage.
- Amazon S3.
- Local folder for MVP.

### Event trigger

Detects when a new document is created or uploaded.

Examples:
- Blob upload trigger.
- S3 event.
- Local file watcher for MVP.

### Ingestion processor

Runs the document processing logic.

Responsibilities:
- Read the uploaded document.
- Extract metadata.
- Extract text.
- Normalize content.
- Split text into chunks.
- Send chunks to the retrieval layer.

### Retrieval layer

Stores searchable chunks and metadata.

Examples:
- Qdrant for local MVP.
- Azure AI Search for Azure architecture.
- Bedrock Knowledge Bases or OpenSearch for AWS architecture.

## Typical flow

1. A document is uploaded.
2. An event is generated.
3. The ingestion processor starts.
4. The document is read and validated.
5. Text and metadata are extracted.
6. The content is chunked.
7. Chunks are indexed.
8. The document becomes available for retrieval.

## Pros

- Automates ingestion.
- Reduces manual work.
- Scales better than manual processing.
- Decouples upload from processing.
- Fits RAG and document assistant systems.

## Cons

- Requires event handling.
- Failures must be managed carefully.
- Duplicate processing must be avoided.
- Observability is important.
- Debugging can be harder than a linear script.

## When to use this pattern

Use this pattern when:
- Documents arrive over time.
- Processing should happen automatically.
- The system needs fresh indexed content.
- The architecture includes document storage and retrieval.
- Manual ingestion is not acceptable.

## When not to use this pattern

Avoid this pattern when:
- The document set is static.
- Manual batch ingestion is enough.
- The MVP is only validating retrieval quality.
- Event-driven infrastructure would add unnecessary complexity.