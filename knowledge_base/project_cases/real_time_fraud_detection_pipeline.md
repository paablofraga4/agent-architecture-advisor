# Project Case: Real-Time Fraud Detection Pipeline

## Problem

A fintech payment processor needed to detect fraudulent transactions in real time, score each payment event with an ML model and generate alerts for the fraud operations team.

## Business context

Fraud losses were increasing as transaction volume grew. The existing batch-based fraud review process introduced delays of hours, by which time fraudulent transactions had already settled. The company needed sub-second scoring to block or flag suspicious payments before completion.

## Requirements

- Ingest payment events in real time from multiple channels.
- Extract features from transaction data for model scoring.
- Score each transaction with an ML fraud detection model.
- Generate alerts for high-risk transactions.
- Provide a dashboard for fraud analysts.
- Support model versioning and A/B testing.
- Support deployment on Azure or AWS.

## Constraints

- End-to-end latency from event to score must be under 500ms.
- The system must handle peak loads of 10K transactions per second.
- False positive rate must be tunable without redeploying the model.
- Model updates must not cause downtime.
- All scoring decisions must be logged for regulatory audit.

## Selected architecture

A real-time event streaming pipeline with ML scoring was selected.

The architecture separates:
- event ingestion,
- feature extraction,
- model scoring,
- alert generation,
- analytics and dashboarding.

## Components used

### Component: Event streaming

Role:
Ingests payment events in real time and distributes them to downstream consumers.

Azure version: Azure Event Hubs.
AWS version: Amazon Kinesis Data Streams.

Why it was selected:
Managed event streaming provides the throughput and low latency needed for real-time processing.

Alternatives considered:
Direct API calls between services were considered but create tight coupling and do not handle backpressure.

Trade-offs:
Event streaming adds operational complexity but decouples producers from consumers.

### Component: Feature extraction service

Role:
Enriches raw payment events with computed features such as transaction velocity, geolocation anomalies and device fingerprint changes.

Why it was selected:
ML models require engineered features that are not present in raw events.

Trade-offs:
Feature computation adds latency. Features must be kept in sync between training and inference.

### Component: ML model scoring

Role:
Runs the fraud detection model on enriched feature vectors and returns a risk score.

Azure version: Azure ML managed endpoints.
AWS version: Amazon SageMaker real-time endpoints.

Why it was selected:
Managed ML endpoints provide auto-scaling, model versioning and canary deployments.

Alternatives considered:
Embedding the model in the application code was considered but makes model updates harder.

Trade-offs:
Network calls to a model endpoint add latency but enable independent model lifecycle management.

### Component: Alert and decision store

Role:
Stores scoring decisions and generates alerts for high-risk transactions.

Azure version: Azure Cosmos DB.
AWS version: Amazon DynamoDB.

Why it was selected:
Low-latency writes are needed to log every scoring decision for audit.

Trade-offs:
Storage costs grow with transaction volume.

### Component: Analytics dashboard

Role:
Displays fraud trends, alert volumes and model performance metrics.

Azure version: Power BI.
AWS version: Amazon QuickSight.

Why it was selected:
Fraud analysts need visual tools to identify patterns and tune alert thresholds.

Trade-offs:
Dashboards require a data modeling layer between the raw event store and the visualization tool.

## Why this architecture was selected

Real-time streaming was selected because batch processing could not meet the latency requirements. The separation of feature extraction and model scoring allows each component to scale independently and enables model updates without pipeline changes.

## Alternatives considered

### Batch scoring pipeline

Why it was considered:
Simpler to build and operate.

Why it was not selected:
Batch delays of minutes or hours were unacceptable for fraud prevention.

### In-application rule engine

Why it was considered:
Deterministic and fast.

Why it was not selected:
Rules alone could not capture the complex fraud patterns that ML models detect.

## Outcome

The pipeline reduced fraud detection latency from hours to under 500ms. The fraud team could tune alert thresholds without redeploying models, and model A/B testing enabled continuous improvement.

## Lessons learned

- Latency requirements drove the architecture toward serverless and managed streaming. Every additional network hop had to be justified.
- Model versioning was critical. The team needed to roll back models quickly when a new version increased false positives.
- False positive tuning was an ongoing operational task, not a one-time configuration. The threshold needed to be adjustable without code changes.
- Feature consistency between training and inference pipelines was a persistent source of bugs.

## Reuse this pattern when

- Decisions must be made in real time on streaming events.
- ML model scoring is part of the decision pipeline.
- Model updates must happen independently of application deployments.
- Audit logging of every decision is required.

## Do not reuse this pattern when

- Batch processing latency is acceptable.
- Simple rules can handle the detection logic.
- Transaction volume is very low and a monolithic approach is simpler.
