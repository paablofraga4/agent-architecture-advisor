# Architecture Pattern: LLM Gateway

## Problem

Applications that use multiple LLM providers accumulate provider-specific integration code, making it difficult to switch models, manage costs, implement fallbacks or enforce consistent policies across all LLM calls.

## Context

Modern AI architectures often use models from multiple providers (OpenAI, Anthropic, Google, AWS Bedrock, Azure OpenAI). Each provider has its own API format, authentication, rate limits and pricing. Without a unified abstraction, every service that calls an LLM must handle these differences independently.

This pattern introduces a gateway layer between application code and LLM providers.

## Requirements

- Provide a unified API for calling different LLM providers.
- Support model routing and fallback chains.
- Enable rate limiting and cost tracking.
- Support prompt caching to reduce redundant calls.
- Allow A/B testing across models.
- Provide centralized logging and observability for all LLM calls.

## Solution

Deploy an LLM gateway that sits between application services and LLM providers. All LLM calls route through this gateway, which handles provider-specific translation, policy enforcement and observability.

### Gateway implementation options

#### LiteLLM

Open-source proxy that provides an OpenAI-compatible API for 100+ LLM providers. Supports load balancing, fallbacks, spend tracking and caching. Good starting point for most teams.

#### Custom gateway

A purpose-built service that translates requests to provider-specific APIs. Provides full control over routing logic, caching and policy enforcement. Higher development cost but maximum flexibility.

#### Cloud-native options

- AWS Bedrock provides a unified API for multiple foundation models.
- Azure AI model catalog offers a single endpoint for deployed models.
- These are provider-specific but reduce custom code within that ecosystem.

### Model routing

- Route requests based on task complexity. Use smaller, cheaper models for classification and extraction. Use larger models for complex reasoning.
- Route based on latency requirements. Some providers offer faster inference for specific model sizes.
- Route based on content. Send requests with sensitive data to models deployed in compliant regions.

### Fallback chains

- Define a primary model and one or more fallback models.
- If the primary model returns an error or exceeds latency thresholds, automatically retry with the fallback.
- Example chain: Claude Sonnet (primary) -> GPT-4o (fallback) -> Claude Haiku (emergency fallback).

### Rate limiting and cost tracking

- Enforce per-service and per-user rate limits at the gateway.
- Track token usage and estimated cost per request.
- Set spending alerts and hard limits per service or team.
- Log all requests with model, tokens, latency and cost metadata.

### Prompt caching

- Cache responses for identical prompts with a TTL.
- Use semantic similarity caching for near-duplicate prompts.
- Exclude non-deterministic requests from caching where freshness matters.

### A/B testing

- Split traffic between models to compare quality, latency and cost.
- Log model assignment per request for downstream analysis.
- Use feature flags to control traffic splits.

## Pros

- Unified API simplifies application code.
- Centralized cost tracking and rate limiting.
- Model switching without application changes.
- Improved availability through fallback chains.
- Consistent logging and observability.

## Cons

- Adds a network hop and potential latency.
- Gateway becomes a single point of failure if not deployed with redundancy.
- Prompt caching adds complexity and storage requirements.
- Translation between API formats may lose provider-specific features.

## When to use this pattern

Use this pattern when:
- The system uses models from multiple providers.
- Cost tracking and rate limiting across LLM calls is important.
- The team wants to switch or test models without changing application code.
- Centralized observability for all LLM calls is required.
- Availability requirements justify fallback chains.

## When not to use this pattern

Avoid this pattern when:
- The system uses a single LLM provider and model.
- The overhead of an additional service is not justified.
- The team is in early prototyping and provider flexibility is not yet a concern.
