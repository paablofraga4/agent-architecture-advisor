# Architecture Pattern: Multi-Agent Architecture Advisor

## Problem

A user needs to compare different architecture options for a project.

A single assistant may produce a generic recommendation and may not clearly separate competing alternatives.

## Context

The system receives a project idea and must generate architecture proposals from different perspectives, such as Azure and AWS. Each proposal must be grounded in retrieved context and then compared by a judge.

## Requirements

- Interpret the user project idea.
- Extract architectural requirements.
- Retrieve relevant knowledge.
- Generate separate architecture proposals.
- Keep each proposal grounded in evidence.
- Compare proposals using a judge agent.
- Produce a final recommendation.
- Avoid hallucinated services or unsupported claims.

## Solution

Use a multi-agent architecture advisor.

The system separates responsibilities across specialized agents.

## Agents

### Requirement Planner

Reads the user idea and extracts:
- Project summary.
- Required capabilities.
- Constraints.
- Non-functional requirements.
- Retrieval focus.
- Retrieval queries.

The planner should not propose a final architecture.

### Retrieval Layer

Retrieves context from the knowledge base using provider-specific filters.

Provider-specific retrieval:
- Azure agent receives Azure and neutral context.
- AWS agent receives AWS and neutral context.
- Neutral context includes architecture patterns and local MVP decisions.

### Azure Architecture Agent

Generates an Azure-native proposal using only Azure and neutral context.

It must:
- Cite context IDs.
- Avoid unsupported services.
- Explain missing context when evidence is insufficient.

### AWS Architecture Agent

Generates an AWS-native proposal using only AWS and neutral context.

It must:
- Cite context IDs.
- Avoid unsupported services.
- Explain missing context when evidence is insufficient.

### Judge Agent

Compares the Azure and AWS proposals.

It must:
- Use only the proposals provided.
- Avoid introducing new services.
- Keep citations when referencing claims.
- Recommend the best next step.

## Typical flow

1. User describes a project idea.
2. Requirement Planner extracts structured requirements.
3. Query Builder creates Azure, AWS and neutral retrieval queries.
4. Retriever builds context packs.
5. Azure Agent generates an Azure proposal.
6. AWS Agent generates an AWS proposal.
7. Evidence Checker validates citations.
8. Judge Agent compares both proposals.
9. Final report is produced.

## Pros

- Separates reasoning responsibilities.
- Makes comparison clearer.
- Supports provider-specific proposals.
- Encourages grounded outputs.
- Easier to debug than one large generic agent.

## Cons

- More moving parts.
- Requires context management.
- Requires validation of citations.
- More latency than a single-agent system.
- Planner output must be validated.

## When to use this pattern

Use this pattern when:
- Multiple architecture options must be compared.
- Different cloud providers are being evaluated.
- The user wants structured recommendations.
- Grounded reasoning is important.
- Traceability to sources is required.

## When not to use this pattern

Avoid this pattern when:
- The task is very simple.
- A single known architecture is already selected.
- There is not enough knowledge base content to ground proposals.
- The system does not need comparison.