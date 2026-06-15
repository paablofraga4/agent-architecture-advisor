# Amazon S3 for Document Storage

## Purpose

Amazon S3 is an object storage service used to store unstructured data such as documents, PDFs, JSON files, logs, images and extracted text.

## When to use this service

Use Amazon S3 when a project requires:
- Storing raw documents.
- Organizing documents by project, customer, department or date.
- Triggering ingestion pipelines when new files arrive.
- Keeping original files before indexing.
- Building an AWS-native RAG architecture.

## Typical usage in RAG architectures

In AWS RAG systems, Amazon S3 commonly acts as the document source layer.

Typical files:
- PDFs.
- Word documents.
- Markdown files.
- JSON exports.
- Technical documents.
- Project updates.
- Meeting notes.

## Role in document ingestion

Amazon S3 can trigger processing workflows when new documents are uploaded.

Typical flow:
1. A document is uploaded to an S3 bucket.
2. An event is emitted.
3. A processing component receives the event.
4. Text and metadata are extracted.
5. The document is indexed into a retrieval system.

## Example organization strategy

Documents can be organized using prefixes such as:

- s3://bucket/projects/{project_id}/documents/{document_type}/{file_name}
- s3://bucket/clients/{client_id}/knowledge/{date}/{file_name}
- s3://bucket/departments/{department}/documents/{file_name}

## Pros

- Scalable object storage.
- Strong AWS-native integration.
- Suitable for raw document storage.
- Can trigger event-driven workflows.
- Common source layer for Bedrock Knowledge Bases.

## Cons

- It is not a semantic retrieval service by itself.
- Requires a retrieval or indexing layer for RAG.
- Metadata and prefix strategy must be designed carefully.
- Search over content requires additional services.

## Best suited for

- Raw document storage.
- AWS-native document ingestion.
- RAG source repositories.
- Event-driven pipelines.
- Bedrock Knowledge Bases input documents.

## Not ideal for

- Direct vector search.
- Direct semantic search.
- Complex relational queries.