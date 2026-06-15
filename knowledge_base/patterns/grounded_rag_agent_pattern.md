# Architecture Pattern: Grounded RAG Agent

## Problem

An agent may hallucinate services, components, benefits or risks when generating architecture proposals.

For architecture advisory systems, unsupported claims can lead to poor technical decisions.

## Context

The system uses a knowledge base and retrieval layer. Agents should only use retrieved evidence when generating proposals.

This pattern is useful for:
- Architecture advisors.
- Enterprise assistants.
- Compliance-sensitive systems.
- Technical recommendation engines.
- Multi-agent comparison systems.

## Requirements

- Retrieve relevant context before generation.
- Pass context IDs to the agent.
- Require citations for every recommended component.
- Prevent unsupported claims.
- Detect invalid citations.
- Rewrite proposals when evidence is missing or invalid.
- Clearly report missing context.

## Solution

Use a grounded RAG agent pattern.

The agent receives:
- User request.
- Extracted requirements.
- Retrieved context.
- Context IDs.
- Strict grounding rules.
- Output format requirements.

The agent must cite context IDs for each recommendation.

## Context format

Each context block should include:
- Context ID.
- Provider.
- Document type.
- Source file.
- Section path.
- Chunk text.

Example:

[CTX-0001]
Provider: azure
Document type: decision_record
Source: azure_ai_search_for_enterprise_rag.md
Section: Why this decision was made

Text...

## Agent rules

The agent must:
- Use only provided context.
- Cite context IDs.
- Avoid unsupported services.
- Avoid unsupported risks or benefits.
- Say what context is missing when needed.
- Avoid relying on general model knowledge.

## Evidence checker

After the agent generates a proposal, an evidence checker validates:
- Whether context IDs exist.
- Whether the proposal contains citations.
- Whether invalid citations were invented.

If validation fails, the system asks the agent to rewrite the proposal using only valid context IDs.

## Pros

- Reduces hallucination.
- Improves traceability.
- Makes proposals auditable.
- Works well with decision records.
- Helps agents explain why a component is recommended.

## Cons

- Requires good context quality.
- Requires enough knowledge base coverage.
- Can produce incomplete answers if context is missing.
- Requires citation validation logic.
- Strict grounding may reduce creativity.

## When to use this pattern

Use this pattern when:
- Architecture recommendations must be evidence-based.
- The system should avoid invented components.
- The user needs source traceability.
- The agent is used for technical decision support.
- The knowledge base contains decision records and architecture patterns.

## When not to use this pattern

Avoid this pattern when:
- The task is purely creative.
- Source grounding is not important.
- There is no useful knowledge base.
- The user expects broad brainstorming rather than evidence-based recommendations.