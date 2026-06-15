# AWS Well-Architected guidance for AI workloads

**Provider:** aws
**Document type:** service_reference
**Category:** guidance
**Tags:** well_architected, ai, rag, security, reliability, cost, bedrock

Senior-level decision guidance for AI/RAG systems on AWS. Pair with the specific service
reference docs when selecting components.

## Recommended building blocks
- **Amazon Bedrock** for managed foundation models (LLM + embeddings) without managing GPUs;
  Bedrock Knowledge Bases for managed RAG, Bedrock Agents for tool use.
- **Amazon OpenSearch Service** (or OpenSearch Serverless) for vector + keyword retrieval.
- **ECS Fargate** or **Lambda** for the orchestrator/API; Lambda + EventBridge/SQS for
  event-driven ingestion.
- **DynamoDB** for low-latency state; **Aurora** for relational.
- **Amazon S3** for documents and artifacts with lifecycle/Intelligent-Tiering.
- **Amazon Textract** for OCR/extraction from scanned PDFs.

## Reliability
- Multi-AZ by default; multi-region for DR per RTO. Use SQS to decouple and absorb spikes.
- Bedrock enforces per-model throughput quotas — request increases and add retry/backoff on
  throttling; consider Provisioned Throughput for steady high volume.

## Security & compliance
- VPC endpoints (PrivateLink) for Bedrock/S3/OpenSearch so traffic stays private.
- KMS customer-managed keys; IAM roles with least privilege, no static keys.
- Data residency: pin to an EU region; CloudTrail for audit; Macie for PII discovery.
- Guardrails for Bedrock to filter PII/unsafe content and reduce prompt-injection blast radius.

## Cost
- Cost drivers: Bedrock tokens, OpenSearch instance/OCU hours, Fargate/Lambda compute,
  S3 storage + inter-AZ/region data transfer. Cache embeddings and frequent answers.
- Lambda for spiky low volume; Fargate/provisioned for steady. Savings Plans for baseline.

## Operations
- CDK/Terraform for IaC; CloudWatch + X-Ray for golden signals plus token/cost metrics.
- Define SLOs; alert on error-budget burn, not raw CPU.
