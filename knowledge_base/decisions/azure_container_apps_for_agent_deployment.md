# Decision Record: Azure Container Apps for Agent Deployment

## Problem

The project required a way to deploy agent services, backend APIs and orchestration components in an Azure-native architecture.

The system needed to run containerized services without requiring full Kubernetes management.

## Context

The architecture included multiple agentic components:
- Requirement planner.
- Azure architecture agent.
- AWS architecture agent.
- Judge agent.
- Retrieval orchestration service.
- Report generation service.

The team wanted a deployment option suitable for APIs and long-running services while keeping operational overhead lower than managing Kubernetes directly.

## Requirements

- Run containerized services.
- Support backend APIs.
- Support long-running agent services.
- Support background workers.
- Avoid direct Kubernetes management.
- Fit an Azure-native architecture.
- Keep deployment simpler than AKS.
- Support future scaling.

## Decision

Azure Container Apps was selected as the Azure deployment option for containerized agent services and backend APIs.

## Why this decision was made

Azure Container Apps was chosen because it provides a managed container runtime suitable for APIs, microservices, workers and agent orchestration services. It allows the system to run containerized components without managing a full Kubernetes cluster.

## Alternatives considered

### Azure Kubernetes Service

Azure Kubernetes Service was considered because it provides full Kubernetes control. It was not selected for this stage because the project did not require full Kubernetes complexity and the goal was to reduce operational overhead.

### Azure Functions

Azure Functions was considered for lightweight event-driven processing. It was not selected as the main agent deployment option because agents and orchestration services may require longer-running processes than typical short-lived functions.

### Local notebooks

Local notebooks were used for the MVP. They were not selected for cloud deployment because they are not suitable for production API hosting or scalable service execution.

## Trade-offs

### Pros

- Managed container execution.
- Suitable for APIs and agent services.
- Less operational complexity than AKS.
- Good fit for microservice-style architectures.
- Supports containerized deployment.
- Azure-native.

### Cons

- Azure-specific.
- Less control than AKS.
- Requires containerization.
- More complex than local notebooks for MVP.

## When to use this decision

Use Azure Container Apps when:
- The system needs Azure-native container deployment.
- Agents must run as APIs or long-running services.
- The team wants to avoid managing Kubernetes.
- The architecture includes multiple service components.
- The MVP has moved beyond notebooks or local scripts.

## When not to use this decision

Avoid Azure Container Apps when:
- The MVP must remain fully local.
- The workload is a simple short-lived event function.
- Full Kubernetes control is required.
- The team does not want to containerize services.