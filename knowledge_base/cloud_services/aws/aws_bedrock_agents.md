# Service: Amazon Bedrock Agents

**Provider:** aws
**Document type:** cloud_reference

## Purpose

Managed service for building AI agents that can plan, reason, and execute multi-step tasks using foundation models. Agents can invoke APIs, query knowledge bases, and orchestrate workflows autonomously.

## Key Features

- **Foundation model choice**: Claude (Anthropic), Titan (Amazon), Llama (Meta), Mistral, Cohere — switch models without code changes.
- **Action groups**: Define tools the agent can call via OpenAPI schemas. The agent decides when and how to use them.
- **Knowledge Bases integration**: Connect to S3-backed vector stores for RAG. Agent automatically retrieves relevant context.
- **Guardrails**: Content filtering, topic denial, PII redaction, and grounding checks applied at inference time.
- **Session management**: Multi-turn conversation state maintained server-side with configurable TTL.
- **Code interpreter**: Optional sandbox for the agent to write and execute Python for data analysis.
- **Prompt management**: Version and A/B test system prompts.

## When to Use

- Building conversational AI agents that need to call external APIs or databases.
- RAG applications where the agent must combine retrieval with reasoning.
- Multi-step workflows where the agent plans and executes a chain of actions.
- When you need managed guardrails for content safety and grounding.

## When NOT to Use

- Simple single-turn Q&A without tool use — direct Bedrock InvokeModel is cheaper.
- Real-time streaming with sub-100ms latency requirements.
- Workloads that require fine-tuned open-source models not available on Bedrock.
- When you need full control over the orchestration loop (use custom code with LangChain or Agent Framework instead).

## Integration Points

- **S3**: Document source for Knowledge Bases.
- **Lambda**: Execute custom logic as action groups.
- **OpenSearch Serverless**: Default vector store for Knowledge Bases.
- **CloudWatch**: Logs and metrics for agent invocations.
- **X-Ray**: Distributed tracing through agent execution steps.
- **Step Functions**: Orchestrate Bedrock Agents as part of larger workflows.
- **IAM**: Fine-grained access control per agent and knowledge base.

## Pricing (US East, as of 2025)

- **Agent invocations**: No additional charge beyond model token costs.
- **Model tokens** (per 1M tokens):
  - Claude 3.5 Sonnet: $3.00 input / $15.00 output
  - Claude 3 Haiku: $0.25 input / $1.25 output
  - Titan Text Express: $0.20 input / $0.60 output
  - Llama 3.1 70B: $2.65 input / $3.50 output
- **Knowledge Bases**: Storage in OpenSearch Serverless from $0.24/hr per OCU (min 2 OCUs).
- **Guardrails**: $0.75 per 1K text units for content filtering, $0.10 for topic denial.

## Typical Monthly Cost

- Small agent (10K invocations/month, Haiku): $15-40/month
- Medium agent (100K invocations, Sonnet + KB): $200-500/month
- Enterprise (1M invocations, Sonnet + KB + Guardrails): $2,000-5,000/month

## Architecture Patterns

- **Single agent + KB**: Conversational RAG with tool use.
- **Multi-agent collaboration**: Supervisor agent delegates to specialist agents (each with own KB and action groups).
- **Human-in-the-loop**: Agent pauses for approval before executing sensitive actions.
