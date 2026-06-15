# GCP Solution: Multi-Agent Architecture Advisor on Cloud Run

Cloud: GCP  
Use case: Multi-agent architecture advisor  
Tags: gcp, vertex-ai, gemini, cloud-run, firestore, cloud-sql, vertex-ai-search, cloud-trace, agent-builder

## Context

This solution is designed for an application where a user describes a software project and multiple agents compare possible cloud architectures.

The application uses Microsoft Agent Framework as the orchestration layer and Gemini or OpenAI as the LLM provider.

GCP is used for deployment, storage, persistence, search and observability.

## Recommended GCP resources

| Layer | GCP resource | Purpose |
|---|---|---|
| Agent orchestration | Microsoft Agent Framework | Orchestrates the multi-agent workflow |
| LLM provider | Vertex AI (Gemini 1.5 Pro / Gemini 1.5 Flash) or OpenAI API | Generates architecture recommendations |
| Agent platform | Vertex AI Agent Builder | Optional managed agent runtime with grounding and tool use |
| Backend/API | Cloud Run | Runs the FastAPI backend as a managed container |
| Storage | Cloud Storage | Stores generated Markdown reports and artifacts |
| Database (document) | Firestore | Stores project metadata and conversation history |
| Database (relational) | Cloud SQL PostgreSQL | Stores users, architecture decision records and structured data |
| Search and RAG | Vertex AI Search | Provides managed RAG with grounded retrieval over knowledge base documents |
| Embeddings | Vertex AI Embeddings (text-embedding-004) | Generates vector embeddings for retrieval |
| Secrets | Secret Manager | Stores API keys, database credentials and application secrets |
| Logs and metrics | Cloud Logging and Cloud Monitoring | Stores application logs, metrics and alerts |
| Tracing | Cloud Trace | Provides distributed tracing across services |
| Frontend delivery | Cloud CDN with Cloud Load Balancing | Serves frontend assets globally |
| TLS certificates | Certificate Manager | Manages HTTPS certificates |
| CI/CD | Cloud Build or GitHub Actions | Builds and deploys the application |

## Architecture

The recommended GCP architecture is:

1. A user submits a project idea through a frontend or notebook.
2. A FastAPI backend running on Cloud Run receives the request.
3. The backend runs the Microsoft Agent Framework workflow.
4. Vertex AI Gemini 1.5 Pro is used as the model provider for reasoning tasks.
5. Vertex AI Gemini 1.5 Flash is used for lighter tasks like summarization and classification.
6. Vertex AI Search provides grounded retrieval over the knowledge base.
7. Generated architecture reports are stored in Cloud Storage.
8. Project metadata and conversation state are stored in Firestore.
9. Structured data like users and architecture decisions are stored in Cloud SQL PostgreSQL.
10. Secrets are stored in Secret Manager.
11. Logs and metrics are sent to Cloud Logging and Cloud Monitoring.
12. Distributed traces are captured with Cloud Trace.

## Vertex AI Agent Builder

Vertex AI Agent Builder provides a managed agent runtime that can be used as an alternative or complement to Microsoft Agent Framework.

Capabilities:
- Managed agent with tool use and function calling.
- Grounding with Google Search and Vertex AI Search.
- Extensions for calling external APIs.
- Data stores for structured and unstructured knowledge.
- Conversation management and session state.

This can be used for simpler agent workflows or as individual tool-using agents within the broader multi-agent system.

## Gemini model options

| Model | Use case | Context window |
|---|---|---|
| Gemini 1.5 Pro | Complex reasoning, architecture analysis, report generation | 2M tokens |
| Gemini 1.5 Flash | Classification, summarization, lightweight tasks | 1M tokens |
| Gemini 1.5 Flash-8B | High-volume low-latency tasks | 1M tokens |

All models support multimodal input (text, images, video, audio) and are accessible through the Vertex AI API.

## MVP recommendation

For the first MVP, use:

- Microsoft Agent Framework.
- Vertex AI Gemini 1.5 Flash (low cost, fast).
- FastAPI running locally or on Cloud Run.
- Cloud Storage for report artifacts.
- Secret Manager for API keys.
- Cloud Logging for observability.

Avoid Cloud SQL and Vertex AI Search until the system needs structured persistence and managed RAG.

## Scalable version

For a scalable GCP version, add:

- Cloud Run with multiple services for backend and agent workers.
- Cloud SQL PostgreSQL for structured persistence.
- Vertex AI Search for managed RAG over the knowledge base.
- Firestore for conversation state and session management.
- Cloud Trace for distributed tracing across agents.
- Vertex AI Agent Builder for managed agent capabilities.
- Cloud CDN for global frontend delivery.
- Pub/Sub for asynchronous communication between agents.

## Observability

| Tool | Purpose |
|---|---|
| Cloud Logging | Structured logs from Cloud Run, Cloud Functions and all GCP services |
| Cloud Monitoring | Metrics, dashboards and alerting |
| Cloud Trace | Distributed tracing across service boundaries |
| Error Reporting | Automatic error grouping and notification |

Cloud Trace integrates with OpenTelemetry, making it compatible with existing instrumentation.

## Pros

- Strong AI/ML platform with Vertex AI and Gemini models.
- Gemini 1.5 Pro offers a 2M token context window.
- Cloud Run provides cost-effective container deployment with scale-to-zero.
- Vertex AI Search offers managed RAG without custom vector store management.
- Good observability with Cloud Trace and Cloud Logging.
- Firestore provides flexible document storage for agent state.

## Cons

- Vertex AI Agent Builder is newer and less mature than some AWS or Azure equivalents.
- Cloud SQL requires Cloud SQL Auth Proxy setup for secure connections.
- GCP networking and IAM can be complex for teams new to the platform.
- Fewer pre-built agent templates compared to Azure AI Foundry.
- Microsoft Agent Framework is not native to GCP, requiring some integration effort.

## Best suited for

This architecture is best suited for teams already using GCP, projects that want to leverage Gemini models, or applications expected to use Vertex AI Search for managed RAG and grounded retrieval.
