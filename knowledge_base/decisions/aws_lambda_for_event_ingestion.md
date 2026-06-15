# Decision Record: AWS Lambda for Event-Driven Document Ingestion

## Problem

The project required a way to automatically process documents when they are uploaded to Amazon S3.

The system needed an AWS-native ingestion trigger without managing servers.

## Context

The architecture used Amazon S3 as the raw document storage layer. Documents were uploaded over time and needed to be processed, normalized and indexed into a retrieval system.

The ingestion component needed to react to upload events and execute lightweight processing logic.

## Requirements

- Detect new document uploads.
- Trigger processing from Amazon S3 events.
- Run lightweight ingestion logic.
- Extract or normalize metadata.
- Start downstream document processing.
- Avoid managing servers.
- Fit an AWS-native architecture.

## Decision

AWS Lambda was selected for event-driven document ingestion.

## Why this decision was made

AWS Lambda was chosen because it can run code in response to S3 upload events without requiring server management. It fits lightweight ingestion tasks such as validating files, reading metadata and triggering downstream processing.

## Alternatives considered

### ECS Fargate

ECS Fargate was considered for containerized services and longer-running processes. It was not selected for the upload-triggered ingestion step because Lambda is simpler for event-driven lightweight processing.

### Local ingestion script

A local ingestion script was considered for the MVP. It was not selected for the AWS cloud version because it does not automatically react to S3 upload events.

### Fully manual ingestion

Manual ingestion was not selected because it would be slow, error-prone and difficult to scale.

## Trade-offs

### Pros

- Serverless.
- AWS-native.
- Integrates with S3 events.
- Good for lightweight ingestion.
- Reduces operational overhead.
- No server management required.

### Cons

- Not ideal for long-running processing.
- Execution limits may apply.
- Complex workflows may require additional orchestration.
- Distributed event debugging can be harder than local scripts.

## When to use this decision

Use AWS Lambda when:
- Documents are uploaded to Amazon S3.
- Processing should start automatically.
- The ingestion task is lightweight.
- The architecture should remain serverless.
- Operational overhead should be minimized.

## When not to use this decision

Avoid AWS Lambda when:
- Processing is long-running.
- Agents need to run as persistent services.
- The workflow requires complex orchestration without additional services.
- The MVP must remain fully local.