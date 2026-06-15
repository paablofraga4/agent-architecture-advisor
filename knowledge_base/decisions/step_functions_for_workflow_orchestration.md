# Decision Record: Step Functions for Multi-Step AI Workflow Orchestration on AWS

## Problem

The project required reliable orchestration for multi-step AI agent pipelines on AWS.

The system needed to coordinate sequential and parallel tasks across multiple services with built-in error handling and visibility.

## Context

The architecture included agent pipelines that involved multiple steps: receiving a request, invoking LLMs through Bedrock, retrieving context from knowledge bases, running validation logic and generating final outputs. These steps needed to execute reliably with retries, branching and audit trails.

The team wanted an AWS-native orchestration solution that provides visibility into pipeline execution without building custom workflow management.

Provider: AWS.

## Requirements

- Orchestrate multi-step agent pipelines.
- Support sequential and parallel task execution.
- Provide built-in retry and error handling.
- Integrate with Bedrock, Lambda and other AWS services.
- Offer visual workflow definition and monitoring.
- Maintain an audit trail of pipeline executions.
- Support both synchronous and asynchronous workflows.

## Decision

AWS Step Functions was selected as the orchestration layer for multi-step AI agent pipelines.

## Why this decision was made

Step Functions was chosen because it provides a managed workflow engine with visual definitions, built-in retries and native AWS service integrations. This reduces the custom code needed for pipeline orchestration.

Key factors:
- Visual workflow definitions using Amazon States Language make pipeline logic explicit and reviewable.
- Built-in retry policies, catch blocks and timeout handling reduce custom error management code.
- Native Bedrock integration allows invoking foundation models as workflow steps without Lambda intermediaries.
- Execution history provides a complete audit trail for debugging and compliance.
- Support for parallel branches enables concurrent agent invocations.
- Express Workflows support high-throughput, short-duration pipelines at lower cost.

## Alternatives considered

### Custom orchestration in Lambda

Custom orchestration logic in Lambda functions was considered. It was not selected because it requires building retry logic, state management and error handling from scratch. Custom Lambda orchestration is a valid option for very simple two-step pipelines where Step Functions adds unnecessary complexity.

### Airflow on MWAA (Managed Workflows for Apache Airflow)

MWAA was considered for workflow orchestration. It was not selected because it is optimized for batch data pipelines rather than request-driven agent workflows. MWAA has higher base costs and slower task scheduling. It is a valid option for teams already using Airflow for data engineering.

### EventBridge Pipes

EventBridge Pipes was considered for simple event-driven processing. It was not selected because it supports limited transformation logic and does not provide the branching, parallel execution or complex error handling needed for agent pipelines.

## Trade-offs

### Pros

- Visual workflow definitions.
- Built-in retry and error handling.
- Native Bedrock and AWS service integrations.
- Complete execution audit trail.
- Supports parallel and conditional branching.
- Managed service with no infrastructure to operate.

### Cons

- State payload size limit of 256 KB requires careful data management between steps.
- Amazon States Language has a learning curve.
- Express Workflows have a 5-minute timeout limit.
- Standard Workflows have higher per-transition costs for high-volume pipelines.
- Complex workflows with many states can be difficult to test locally.

## When to use this decision

Use Step Functions when:
- Agent pipelines involve multiple coordinated steps.
- Built-in retry and error handling is important.
- Visual workflow monitoring and audit trails are required.
- The architecture is AWS-native with Bedrock integration.
- The team wants managed orchestration without custom workflow code.

## When not to use this decision

Avoid Step Functions when:
- The pipeline is a simple single-step invocation.
- State payloads exceed 256 KB regularly.
- The team needs sub-second task scheduling latency.
- The orchestration logic is better expressed in application code.
