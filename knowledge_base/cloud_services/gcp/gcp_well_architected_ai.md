# Google Cloud Well-Architected guidance for AI workloads

**Provider:** gcp
**Document type:** service_reference
**Category:** guidance
**Tags:** well_architected, ai, rag, security, reliability, cost, vertex

Senior-level decision guidance for AI/RAG systems on Google Cloud. Pair with the specific
service reference docs when selecting components.

## Recommended building blocks
- **Vertex AI** for managed LLM/embeddings (Gemini) and the RAG Engine / grounding APIs.
- **Vertex AI Vector Search** (formerly Matching Engine) for high-scale vector retrieval;
  combine with keyword search for hybrid recall.
- **Cloud Run** for the stateless orchestrator/API (scales to zero); **Cloud Functions** /
  Eventarc + Pub/Sub for event-driven ingestion.
- **Firestore** for low-latency state; **Cloud SQL** / AlloyDB for relational.
- **Cloud Storage** for documents and artifacts with lifecycle/Autoclass tiering.
- **Document AI** for OCR/extraction from scanned PDFs.

## Reliability
- Cloud Run is regional and multi-zone by default; use multi-region for DR per RTO.
- Vertex AI enforces per-region quotas (requests/min, tokens) — request increases early and
  add retry/backoff. Pub/Sub decouples ingestion spikes.

## Security & compliance
- VPC Service Controls + Private Service Connect to keep Vertex/Storage traffic private and
  build a data-exfiltration perimeter.
- CMEK (customer-managed keys) in Cloud KMS; service accounts with least privilege/Workload Identity.
- Data residency: pin to an EU region; Cloud Audit Logs; DLP API for PII discovery/redaction.

## Cost
- Cost drivers: Vertex tokens, Vector Search node hours, Cloud Run vCPU-seconds, storage +
  network egress. Cloud Run scale-to-zero is ideal for spiky/low traffic; commit (CUDs) for baseline.
- Cache embeddings and frequent answers.

## Operations
- Terraform for IaC; Cloud Monitoring + Cloud Trace for golden signals plus token/cost metrics.
- Define SLOs; alert on error-budget burn.
