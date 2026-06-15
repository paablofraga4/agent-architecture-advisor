# AWS Pricing Reference

## Document type

cloud_reference

## Provider

aws

## Purpose

This document provides approximate monthly cost ranges for common AWS AI and data services. Prices are based on publicly available AWS pricing as of 2024-2025 and are intended for estimation purposes during architecture design.

All prices are in USD. Actual costs vary by region, commitment tier and usage patterns.

## Amazon Bedrock

Pricing is per 1 million tokens (or per 1 million characters for some models), varying by model.

- Claude 3.5 Sonnet: ~$3.00 per 1M input tokens, ~$15.00 per 1M output tokens.
- Claude 3 Haiku: ~$0.25 per 1M input tokens, ~$1.25 per 1M output tokens.
- Amazon Titan Text Express: ~$0.20 per 1M input tokens, ~$0.60 per 1M output tokens.
- Amazon Titan Embeddings: ~$0.02 per 1M input tokens.
- Llama 3 70B: ~$2.65 per 1M input tokens, ~$3.50 per 1M output tokens.

Provisioned throughput is available for predictable high-volume workloads.

## Amazon OpenSearch Service

- Instance pricing varies by type:
  - t3.small.search: ~$0.036/hour (~$26/month).
  - m6g.large.search: ~$0.128/hour (~$92/month).
  - r6g.xlarge.search: ~$0.240/hour (~$173/month).
- Storage: EBS gp3 at ~$0.08/GB/month.
- Serverless: ~$0.24 per OCU-hour (compute), ~$0.024 per GB/month (storage).
- Minimum 2 nodes recommended for production.

## Amazon ECS on Fargate

- vCPU: ~$0.04048 per vCPU-hour (~$29/month per vCPU).
- Memory: ~$0.004445 per GB-hour (~$3.20/month per GB).
- Spot pricing available at up to 70% discount for fault-tolerant workloads.
- No charge when no tasks are running.

## Amazon S3

- Standard: ~$0.023 per GB/month.
- Infrequent Access: ~$0.0125 per GB/month.
- Glacier Instant Retrieval: ~$0.004 per GB/month.
- PUT requests: ~$0.005 per 1,000 requests.
- GET requests: ~$0.0004 per 1,000 requests.

## Amazon DynamoDB

- On-demand capacity:
  - Write: ~$1.25 per 1 million write request units.
  - Read: ~$0.25 per 1 million read request units.
- Provisioned capacity:
  - Write: ~$0.00065 per WCU-hour (~$0.47/month per WCU).
  - Read: ~$0.00013 per RCU-hour (~$0.09/month per RCU).
- Storage: ~$0.25 per GB/month.
- On-demand is cost-effective for unpredictable workloads.

## AWS Lambda

- First 1 million requests free per month.
- Beyond free tier: ~$0.20 per 1 million requests.
- Compute: ~$0.0000166667 per GB-second.
- Free tier includes 400,000 GB-seconds per month.

## Amazon SageMaker

- Real-time inference endpoints:
  - ml.t3.medium: ~$0.05/hour (~$36/month).
  - ml.m5.xlarge: ~$0.23/hour (~$166/month).
  - ml.g4dn.xlarge (GPU): ~$0.526/hour (~$379/month).
- Serverless inference: ~$0.0001 per second of compute.
- Training: billed per instance-hour during training jobs.

## Amazon Textract

- Detect text: ~$1.50 per 1,000 pages.
- Analyze document (forms): ~$50.00 per 1,000 pages.
- Analyze document (tables): ~$15.00 per 1,000 pages.
- Free tier: 1,000 pages/month for first 3 months.

## AWS Step Functions

- Standard workflows: ~$0.025 per 1,000 state transitions.
- Express workflows: ~$0.000001 per request + duration charges.

## Amazon API Gateway

- REST API: ~$3.50 per 1 million API calls.
- HTTP API: ~$1.00 per 1 million API calls.
- WebSocket: ~$1.00 per 1 million messages.

## Example scenario

A typical RAG application serving 1,000 users per day with moderate query volume:

- Amazon Bedrock (Claude 3 Haiku, ~500K input + 200K output tokens/day): ~$6-12/month.
- Amazon OpenSearch (t3.small.search, 2 nodes): ~$52/month.
- ECS Fargate (0.5 vCPU, 1GB, moderate traffic): ~$20-50/month.
- Amazon S3 (10GB documents): ~$1/month.
- Amazon DynamoDB (on-demand, conversation history): ~$5-20/month.

Estimated total: ~$85-135/month for a basic RAG application.

For a production deployment with larger instances and more capable models: ~$300-700/month.

## Notes

- Prices are approximate and subject to change.
- Savings Plans and Reserved Instances can reduce costs by 20-40%.
- Data transfer charges apply for cross-region and internet egress.
- Free tier benefits apply for the first 12 months on many services.
