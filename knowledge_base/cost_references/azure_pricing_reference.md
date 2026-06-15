# Azure Pricing Reference

## Document type

cloud_reference

## Provider

azure

## Purpose

This document provides approximate monthly cost ranges for common Azure AI and data services. Prices are based on publicly available Azure pricing as of 2024-2025 and are intended for estimation purposes during architecture design.

All prices are in USD. Actual costs vary by region, commitment tier and usage patterns.

## Azure OpenAI Service

Pricing is per 1 million tokens, varying by model.

- GPT-4o: ~$2.50 per 1M input tokens, ~$10.00 per 1M output tokens.
- GPT-4o mini: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens.
- GPT-4 Turbo: ~$10.00 per 1M input tokens, ~$30.00 per 1M output tokens.
- text-embedding-ada-002: ~$0.10 per 1M tokens.
- text-embedding-3-small: ~$0.02 per 1M tokens.

Provisioned throughput units (PTUs) are available for predictable high-volume workloads at fixed monthly rates.

## Azure AI Search

- Free tier: shared resources, limited to 50MB storage.
- Basic tier: ~$75/month, 2GB storage, up to 3 replicas.
- Standard S1: ~$250/month per search unit, 25GB per partition.
- Standard S2: ~$1,000/month per search unit, 100GB per partition.
- Semantic ranker add-on: ~$250/month per search unit.

Search units are the product of replicas and partitions.

## Azure Container Apps

- Consumption plan: $0 when idle (scale to zero).
- vCPU: ~$0.000024 per vCPU-second.
- Memory: ~$0.000003 per GiB-second.
- Typical active workload: ~$30-150/month depending on traffic.

## Azure Blob Storage

- Hot tier: ~$0.018 per GB/month.
- Cool tier: ~$0.01 per GB/month.
- Archive tier: ~$0.002 per GB/month.
- Read operations (hot): ~$0.004 per 10,000 operations.
- Write operations (hot): ~$0.05 per 10,000 operations.

## Azure Cosmos DB

- Serverless: ~$0.25 per 1 million request units (RUs).
- Provisioned throughput: starts at ~$24/month for 400 RU/s.
- Storage: ~$0.25 per GB/month.
- Autoscale provisioned: adjusts between 10% and 100% of max RU/s.

Serverless is cost-effective for intermittent workloads. Provisioned is better for sustained throughput.

## Azure Document Intelligence

- Read model: ~$1.00 per 1,000 pages.
- Prebuilt models (invoice, receipt): ~$10.00 per 1,000 pages.
- Custom models: ~$15.00 per 1,000 pages.
- Free tier: 500 pages/month.

## Azure Functions

- Consumption plan: first 1 million executions free per month.
- Beyond free tier: ~$0.20 per 1 million executions.
- Compute: ~$0.000016 per GB-second.
- Premium plan: from ~$0.173/hour per vCPU for pre-warmed instances.

## Azure Logic Apps

- Consumption: ~$0.000025 per action execution.
- Standard: from ~$0.16/hour for single-tenant hosting.

## Azure API Management

- Consumption tier: ~$3.50 per 1 million calls.
- Developer tier: ~$50/month.
- Basic tier: ~$150/month.
- Standard tier: ~$700/month.

## Example scenario

A typical RAG application serving 1,000 users per day with moderate query volume:

- Azure OpenAI (GPT-4o mini, ~500K input + 200K output tokens/day): ~$5-10/month.
- Azure AI Search (Basic tier, 1 unit): ~$75/month.
- Azure Container Apps (moderate traffic): ~$40-80/month.
- Azure Blob Storage (10GB documents): ~$1/month.
- Azure Cosmos DB (serverless, conversation history): ~$10-30/month.

Estimated total: ~$130-200/month for a basic RAG application.

For a production deployment with higher availability (Standard search, multiple replicas, GPT-4o): ~$400-800/month.

## Notes

- Prices are approximate and subject to change.
- Reserved capacity and enterprise agreements can reduce costs by 20-40%.
- Egress charges apply for data leaving Azure regions.
- Development and testing environments can use lower tiers to reduce costs.
