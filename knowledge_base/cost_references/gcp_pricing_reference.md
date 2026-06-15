# GCP Pricing Reference

## Document type

cloud_reference

## Provider

gcp

## Purpose

This document provides approximate monthly cost ranges for common Google Cloud AI and data services. Prices are based on publicly available GCP pricing as of 2024-2025 and are intended for estimation purposes during architecture design.

All prices are in USD. Actual costs vary by region, commitment tier and usage patterns.

## Vertex AI

Pricing varies by model and is typically per 1 million characters or per 1 million tokens.

- Gemini 1.5 Pro: ~$1.25 per 1M input tokens, ~$5.00 per 1M output tokens.
- Gemini 1.5 Flash: ~$0.075 per 1M input tokens, ~$0.30 per 1M output tokens.
- Gemini 1.0 Pro: ~$0.50 per 1M input tokens, ~$1.50 per 1M output tokens.
- text-embedding-004: ~$0.025 per 1M tokens.
- PaLM 2 (legacy): ~$0.50 per 1M input characters, ~$0.50 per 1M output characters.

Provisioned throughput is available for high-volume workloads.

## Vertex AI Search

- Enterprise edition: ~$4.00 per 1,000 queries.
- Data ingestion: ~$2.50 per 1,000 documents.
- Storage: included in query pricing.
- Blended search (keyword + semantic) is included.

## Cloud Run

- vCPU: ~$0.00002400 per vCPU-second.
- Memory: ~$0.00000250 per GiB-second.
- Requests: ~$0.40 per 1 million requests.
- Scale to zero: no charge when idle.
- Free tier: 2 million requests/month, 360,000 vCPU-seconds, 180,000 GiB-seconds.
- Typical active workload: ~$20-120/month depending on traffic.

## Cloud Storage

- Standard: ~$0.020 per GB/month.
- Nearline: ~$0.010 per GB/month.
- Coldline: ~$0.004 per GB/month.
- Archive: ~$0.0012 per GB/month.
- Class A operations (writes): ~$0.05 per 10,000 operations.
- Class B operations (reads): ~$0.004 per 10,000 operations.

## Firestore

- Document reads: ~$0.06 per 100,000 reads.
- Document writes: ~$0.18 per 100,000 writes.
- Document deletes: ~$0.02 per 100,000 deletes.
- Storage: ~$0.18 per GB/month.
- Free tier: 50,000 reads, 20,000 writes, 20,000 deletes per day.

## Cloud Functions

- Invocations: first 2 million free per month.
- Beyond free tier: ~$0.40 per 1 million invocations.
- Compute: ~$0.0000025 per GHz-second.
- Memory: ~$0.0000025 per GB-second.
- Networking: ~$0.12 per GB egress.

## BigQuery

- On-demand queries: ~$5.00 per TB processed.
- First 1 TB/month free.
- Flat-rate pricing: from ~$2,000/month for 100 slots.
- Storage: ~$0.02 per GB/month (active), ~$0.01 per GB/month (long-term).
- Streaming inserts: ~$0.05 per GB.

## Cloud Workflows

- Internal steps: ~$0.01 per 1,000 steps.
- External steps (HTTP calls): ~$0.025 per 1,000 steps.

## Apigee API Management

- Evaluation: free for limited usage.
- Standard: starts at ~$500/month.
- Enterprise: custom pricing.
- For simpler needs, Cloud Endpoints is free for up to 2 million calls/month.

## Document AI

- General processor: ~$1.50 per 1,000 pages.
- Specialized processors (invoice, receipt): ~$10.00 per 1,000 pages.
- Custom processor: ~$30.00 per 1,000 pages.
- Free tier: 1,000 pages/month for some processors.

## Example scenario

A typical RAG application serving 1,000 users per day with moderate query volume:

- Vertex AI (Gemini 1.5 Flash, ~500K input + 200K output tokens/day): ~$3-6/month.
- Vertex AI Search (~30K queries/month): ~$120/month.
- Cloud Run (moderate traffic): ~$25-60/month.
- Cloud Storage (10GB documents): ~$1/month.
- Firestore (conversation history): ~$5-15/month.

Estimated total: ~$155-200/month for a basic RAG application.

For a production deployment with Gemini 1.5 Pro and higher query volumes: ~$350-700/month.

## Notes

- Prices are approximate and subject to change.
- Committed use discounts can reduce costs by 20-40%.
- Egress charges apply for data leaving GCP regions.
- Free tier benefits are generous for Cloud Run and Cloud Functions, making them cost-effective for low-traffic applications.
- BigQuery free tier of 1 TB/month covers many analytics workloads.
