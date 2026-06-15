# Google Cloud Functions for Event-Driven Document Ingestion

Cloud: GCP  
Use case: Event-driven document processing and ingestion  
Tags: gcp, cloud-functions, serverless, eventarc, pubsub, cloud-storage, event-driven, ingestion

## Purpose

Google Cloud Functions (2nd gen) is a serverless compute service used to run code in response to events without managing servers. The 2nd generation is built on Cloud Run and offers improved concurrency, longer timeouts and Eventarc integration.

## When to use this service

Use Cloud Functions when a project requires:
- Event-driven processing triggered by Cloud Storage uploads.
- Lightweight ingestion tasks for document pipelines.
- Reacting to Pub/Sub messages.
- HTTP-triggered endpoints for webhooks or simple APIs.
- Metadata normalization and validation.
- Triggering indexing workflows in a RAG pipeline.
- Reducing infrastructure management overhead.

## When NOT to use this service

Do not use Cloud Functions when:
- The processing takes longer than 60 minutes.
- The workload requires complex multi-agent orchestration.
- Streaming responses are needed.
- The application needs persistent connections or WebSockets.
- A full containerized backend is more appropriate.
- The workload needs GPU acceleration.

## Cloud Functions 1st gen vs 2nd gen

| Feature | 1st gen | 2nd gen |
|---|---|---|
| Runtime | Functions Framework | Built on Cloud Run |
| Concurrency | 1 request per instance | Up to 1,000 concurrent requests per instance |
| Timeout | 9 minutes (HTTP), 9 minutes (event) | 60 minutes (HTTP), 9 minutes (event) |
| Min instances | Not supported | Supported (reduces cold starts) |
| Eventarc | Not supported | Full Eventarc integration |
| Traffic splitting | Not supported | Supported via Cloud Run revisions |

## Eventarc integration

Cloud Functions 2nd gen uses Eventarc as the unified eventing layer. Eventarc supports:
- Cloud Storage events (object finalize, delete, archive, metadata update).
- Pub/Sub messages.
- Cloud Audit Log events from over 130 GCP services.
- Custom events from applications.
- Firebase events (Authentication, Firestore, Realtime Database).

Eventarc routes events through Pub/Sub under the hood, providing at-least-once delivery.

## Typical usage in RAG architectures

Cloud Functions can be used in the ingestion phase of a RAG architecture.

Typical responsibilities:
- React to Cloud Storage upload events.
- Validate uploaded files by type and size.
- Extract document metadata.
- Start text extraction logic.
- Chunk documents for indexing.
- Send processed content to a vector store or retrieval layer.
- Trigger downstream workflows via Pub/Sub.

## Role in a document assistant architecture

In a document assistant, Cloud Functions connects Cloud Storage with the processing and retrieval pipeline.

Example flow:
1. A PDF is uploaded to a Cloud Storage bucket.
2. Eventarc routes the object.finalize event to a Cloud Function.
3. The function reads the file metadata and validates the document.
4. The function extracts text using Document AI or a library like PyPDF.
5. Extracted text is chunked.
6. Chunks are indexed into Vertex AI Search or a vector database.

## Concurrency model

2nd gen Cloud Functions support up to 1,000 concurrent requests per instance. This means:
- Fewer instances are needed to handle traffic spikes.
- Cost is lower compared to 1st gen for bursty workloads.
- Global variables and in-memory caches are shared across concurrent requests within the same instance.
- Database connection pooling should be configured carefully.

## Cold starts

Cold starts occur when a new instance must be initialized. Mitigation strategies:
- Set a minimum instance count to keep warm instances available.
- Use lighter runtimes (Go, Node.js) for faster startup.
- Minimize dependencies and package size.
- Use lazy initialization for heavy clients.

Typical cold start times:
- Python: 500ms to 3 seconds depending on dependencies.
- Node.js: 200ms to 1 second.
- Go: 100ms to 500ms.
- Java: 2 to 10 seconds without GraalVM native image.

## Pricing

| Item | Details |
|---|---|
| Free tier | 2 million invocations per month, 400,000 GB-seconds, 200,000 GHz-seconds |
| Invocations | $0.40 per million invocations after free tier |
| Compute (memory) | $0.0000025 per GB-second |
| Compute (CPU) | $0.0000100 per GHz-second |
| Networking | Outbound at standard GCP egress rates |

## Integration points

| Integration | Purpose |
|---|---|
| Cloud Storage | Trigger on object events for document ingestion |
| Pub/Sub | Subscribe to topics for asynchronous message processing |
| Eventarc | Unified event routing from GCP and custom sources |
| Document AI | Extract structured text from PDFs and scanned documents |
| Vertex AI Search | Index processed documents for RAG retrieval |
| Firestore | Store processing metadata and status |
| Cloud Logging | Structured logging for debugging and monitoring |
| Secret Manager | Access API keys and credentials securely |

## Pros

- Serverless with no infrastructure management.
- Strong event-driven integration via Eventarc.
- 2nd gen concurrency reduces cost and instance count.
- Generous free tier for low-traffic workloads.
- GCP-native integration with Cloud Storage and Pub/Sub.
- Supports Python, Node.js, Go, Java, .NET and Ruby.

## Cons

- Not ideal for long-running multi-agent processing.
- Cold starts can affect latency for infrequent invocations.
- Debugging distributed event flows can be harder than local scripts.
- 9-minute timeout for event-triggered functions.
- No GPU support.
- Complex pipelines may require Workflows or Cloud Composer for orchestration.

## Best suited for

- Cloud Storage-triggered document ingestion.
- Lightweight document validation and metadata extraction.
- Event-driven RAG ingestion pipelines.
- Serverless GCP-native MVPs.
- Webhook handlers and simple HTTP endpoints.

## Not ideal for

- Long-running agent processes.
- Heavy document processing exceeding timeout limits.
- Complex orchestration without additional workflow services.
- Workloads requiring GPU acceleration.
