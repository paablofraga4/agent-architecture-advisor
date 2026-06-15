# Decision Record: ECS Fargate for Agent Deployment

## Problem

The project required a way to deploy agent services, APIs and orchestration components in an AWS-native architecture.

The system needed to run containers without managing servers directly.

## Context

The architecture included multiple agentic components:
- Requirement planner.
- AWS architecture agent.
- Azure architecture agent.
- Judge agent.
- Retrieval orchestration service.
- Report generation service.

The deployment target needed to support longer-running services and backend APIs.

## Requirements

- Run containerized services.
- Support backend APIs.
- Support long-running agent services.
- Support background workers.
- Avoid managing servers directly.
- Fit an AWS-native architecture.
- Support future scaling.

## Decision

ECS Fargate was selected as the AWS deployment option for containerized agent services and backend APIs.

## Why this decision was made

ECS Fargate was chosen because it allows the system to run containerized services without directly managing servers. It is suitable for APIs, workers and long-running agent orchestration components.

## Alternatives considered

### AWS Lambda

AWS Lambda was considered for event-driven ingestion and lightweight processing. It was not selected as the main agent deployment option because persistent or longer-running agent services fit better in a containerized service model.

### Local notebooks

Local notebooks were used for MVP experimentation. They were not selected for AWS deployment because they are not suitable for production service hosting.

### Self-managed virtual machines

Self-managed servers were not selected because they increase operational overhead and require server management.

## Trade-offs

### Pros

- Managed container execution.
- Suitable for APIs and workers.
- Good for long-running agent services.
- Avoids direct server management.
- AWS-native.
- Useful for production agent orchestration.

### Cons

- AWS-specific.
- Requires containerization.
- More complex than local notebooks.
- May be unnecessary for very small MVPs.

## When to use this decision

Use ECS Fargate when:
- Agents need to run as backend services.
- The system needs containerized deployment.
- The architecture is AWS-native.
- Long-running APIs or workers are required.
- The project has moved beyond local notebooks.

## When not to use this decision

Avoid ECS Fargate when:
- The MVP must stay fully local.
- The workload is only a lightweight upload trigger.
- The system does not need containerized services.
- The team wants the simplest possible prototype.