# Azure Well-Architected guidance for AI workloads

**Provider:** azure
**Document type:** service_reference
**Category:** guidance
**Tags:** well_architected, ai, rag, security, reliability, cost, landing_zone

Senior-level decision guidance for AI/RAG systems on Azure. Pair these with the specific
service reference docs when selecting components.

## Recommended building blocks
- **Azure OpenAI Service** for LLM/embeddings with data staying in your tenant/region.
  Use Provisioned Throughput Units (PTUs) for steady high volume, pay-as-you-go for spiky.
- **Azure AI Search** for hybrid (vector + keyword) retrieval with semantic ranking.
- **Azure Container Apps** or **App Service** for the stateless orchestrator/API; Functions
  for event-driven ingestion.
- **Cosmos DB** (low-latency, global) or **Azure SQL** for application/state data.
- **Blob Storage** for documents and artifacts, with lifecycle tiering (hot/cool/archive).

## Reliability
- Deploy across Availability Zones; use paired regions for DR when RTO demands it.
- Azure OpenAI quota is per-region per-model (tokens/min, requests/min) — design within
  TPM/RPM limits and request increases early; add retry/backoff on 429s.

## Security & compliance (banking / regulated)
- Private Endpoints + VNet integration so OpenAI/Search/Storage are not public.
- Customer-managed keys (CMK) in Key Vault; managed identities instead of keys.
- Data residency: pin all services to an EU region; enable diagnostic/audit logs.
- Azure Policy to enforce guardrails; Microsoft Purview for data classification.

## Cost
- Cost drivers: OpenAI tokens, AI Search units/replicas, compute hours, storage + egress.
- PTUs amortize at high steady volume; cache embeddings and frequent answers.

## Operations
- Bicep/Terraform for IaC; Application Insights + Azure Monitor for golden signals plus
  token/cost telemetry. Define SLOs and alert on error-budget burn.
