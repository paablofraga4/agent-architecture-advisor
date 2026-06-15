# Decision Record: Cloud Run for Agent Deployment on GCP

## Problem

The project required a managed platform for deploying AI agent backends on Google Cloud Platform.

The system needed to run containerized agent services with minimal operational overhead and cost-efficient scaling.

## Context

The architecture included multiple agentic components that needed to be deployed as HTTP services or background workers. These included retrieval orchestration, agent APIs and report generation services.

The team wanted a GCP-native solution that could scale automatically based on request volume and scale to zero during idle periods.

Provider: GCP.

## Requirements

- Run containerized agent services.
- Autoscale based on incoming requests.
- Scale to zero when idle to reduce costs.
- Support request-based billing.
- Avoid managing clusters or VMs directly.
- Fit a GCP-native architecture.
- Support GPU workloads for inference where needed.

## Decision

Cloud Run was selected as the GCP deployment option for containerized agent services and backend APIs.

## Why this decision was made

Cloud Run was chosen because it provides a fully managed container runtime that autoscales based on request volume, including scaling to zero. This matches the bursty traffic patterns typical of AI agent systems where requests may be infrequent but compute-intensive.

Key factors:
- Request-based billing means the team pays only for actual agent invocations.
- GPU support (Cloud Run GPU) enables running smaller inference models alongside agent logic.
- Native integration with Vertex AI, Cloud Storage and other GCP services simplifies the architecture.
- No cluster management compared to GKE reduces operational burden.
- Concurrency settings allow tuning for agent workloads that may hold connections open during LLM calls.

## Alternatives considered

### GKE (Google Kubernetes Engine)

GKE was considered for full container orchestration. It was not selected because the operational overhead of managing a Kubernetes cluster was not justified for the current workload. GKE remains a valid option if the system needs fine-grained scheduling, custom networking or persistent GPU pools.

### App Engine

App Engine was considered for its simplicity. It was not selected because it provides less control over the container runtime and has stricter constraints on request handling and background processing.

### Compute Engine

Compute Engine was considered for full VM control. It was not selected because managing VMs directly increases operational overhead and does not provide automatic scaling to zero.

## Trade-offs

### Pros

- Autoscales to zero, reducing idle costs.
- Request-based billing fits bursty agent workloads.
- Managed container runtime with no cluster management.
- GPU support for inference workloads.
- Native GCP service integrations.
- Simple deployment model using container images.

### Cons

- Cold starts can add latency on first request after idle periods (typically 1-5 seconds).
- Maximum request timeout of 60 minutes limits very long-running agent pipelines.
- Less control than GKE for complex networking or scheduling requirements.
- Concurrent request handling requires careful tuning for memory-intensive agent workloads.

## When to use this decision

Use Cloud Run when:
- Agent services are deployed on GCP.
- The workload is request-driven with variable traffic.
- Cost efficiency through scale-to-zero is important.
- The team wants to avoid managing infrastructure.
- Individual agent requests complete within 60 minutes.

## When not to use this decision

Avoid Cloud Run when:
- Agent pipelines require more than 60 minutes per execution.
- The workload needs persistent GPU pools with high utilization.
- Complex inter-service networking or service mesh is required.
- The team already operates a GKE cluster with available capacity.
