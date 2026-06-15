# Architecture Pattern: Observability for AI and LLM Applications

## Problem

AI and LLM-based applications have unique observability challenges. Traditional application monitoring does not capture LLM-specific metrics like token usage, response quality, hallucination rates or multi-step agent trace propagation.

## Context

AI systems involve chains of LLM calls, retrieval steps, tool invocations and agent decisions. Debugging a bad output requires tracing through multiple steps to identify whether the issue was in retrieval, prompt construction, model response or post-processing.

This pattern provides a framework for observability across all layers of an AI architecture.

## Requirements

- Trace requests through multi-step agent chains.
- Log LLM calls with inputs, outputs and metadata.
- Track token usage and costs per request.
- Monitor latency at each step of the pipeline.
- Detect quality issues including hallucinations.
- Support feedback loops for continuous improvement.
- Integrate with existing observability infrastructure.

## Solution

Implement observability at three levels: infrastructure metrics, application traces and AI-specific quality metrics.

### Trace propagation through agent chains

- Assign a unique trace ID to each user request.
- Propagate the trace ID through every agent step, LLM call, retrieval query and tool invocation.
- Use OpenTelemetry for trace propagation to maintain compatibility with existing observability stacks.
- Record parent-child relationships between steps to build a complete execution tree.

### LLM call logging

- Log every LLM call with: model name, provider, prompt (or prompt hash for sensitive data), completion, token counts, latency, temperature and other parameters.
- Store prompts and completions in a separate data store from operational logs due to volume and sensitivity.
- Apply PII redaction before logging if prompts contain user data.

### Token usage tracking

- Track input tokens, output tokens and total tokens per call.
- Aggregate token usage by model, agent, user and time period.
- Calculate estimated cost per request using provider pricing.
- Set alerts for unusual token usage spikes that may indicate prompt injection or infinite loops.

### Latency monitoring

- Measure end-to-end latency for complete agent pipelines.
- Measure per-step latency: retrieval, LLM call, tool execution, post-processing.
- Track P50, P95 and P99 latency percentiles.
- Set latency budgets per step and alert when budgets are exceeded.

### Hallucination detection

- Compare LLM outputs against retrieved source documents for factual grounding.
- Use automated evaluation (LLM-as-judge) to score response faithfulness.
- Track hallucination rates over time as a quality metric.
- Flag responses with low grounding scores for human review.

### Feedback loops

- Collect explicit user feedback (thumbs up/down, ratings).
- Collect implicit signals (follow-up questions, task completion).
- Link feedback to specific trace IDs for root cause analysis.
- Use feedback data to identify patterns in low-quality responses.

### Observability tools

- Langfuse: open-source LLM observability with trace visualization, cost tracking and evaluation.
- LangSmith: LangChain-integrated observability platform with dataset management and testing.
- Phoenix (Arize): open-source tool for LLM trace analysis and evaluation.
- OpenTelemetry: standard for distributed tracing that integrates with cloud-native monitoring.
- Cloud-native options: CloudWatch, Azure Monitor, Google Cloud Monitoring for infrastructure metrics.

### Key metrics to track

- Token usage per model, agent and time period.
- Cost per request and per agent invocation.
- Latency percentiles (P50, P95, P99) per pipeline step.
- Error rates by step and error type.
- Retrieval relevance scores.
- Hallucination rate (automated and human-evaluated).
- User feedback scores.
- Cache hit rates for prompt caching.

## Pros

- Enables debugging of complex multi-step agent failures.
- Provides cost visibility and control.
- Supports continuous quality improvement through feedback.
- Identifies performance bottlenecks in agent pipelines.

## Cons

- Logging LLM inputs and outputs increases storage costs.
- Automated quality evaluation adds latency and LLM costs.
- Sensitive data in prompts requires careful redaction.
- Observability infrastructure itself requires maintenance.

## When to use this pattern

Use this pattern when:
- The system includes multi-step agent pipelines.
- LLM costs need tracking and optimization.
- Response quality monitoring is important.
- The team needs to debug production agent issues.
- The system is moving beyond prototype stage.

## When not to use this pattern

Avoid full observability when:
- The system is a simple single-call prototype.
- The overhead of logging is not justified by the workload scale.
- The team is still iterating on basic functionality.
