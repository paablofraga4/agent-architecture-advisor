# Project Case: Document Architecture Advisor

## Problem

An internal platform needed to generate architecture proposals for document-centric solutions, comparing Azure and AWS alternatives and explaining trade-offs.

## Business context

Architecture teams needed a reusable advisor that could justify recommendations with explicit evidence from internal knowledge and prior decisions.

## Requirements

- Accept a user project idea in natural language.
- Extract requirements with minimal bias.
- Retrieve cloud references, patterns and decision records.
- Generate Azure and AWS proposals.
- Compare both proposals and produce one final architecture recommendation.

## Constraints

- Recommendations must be grounded in retrieved context.
- No unsupported services should be introduced.
- Output should include practical implementation guidance.

## Selected architecture

A multi-agent architecture advisor with planner, dual provider agents, judge, and final synthesis agent was selected.

## Components used

### Component: Requirement extraction planner

Role:
Transforms user idea into structured requirements and retrieval intents.

Why it was selected:
Provides a deterministic bridge between free text and retrieval strategy.

Alternatives considered:
Direct prompting without planning.

Trade-offs:
Requires strong schema validation and anti-bias prompting.

### Component: Provider-specific proposal agents

Role:
Create Azure and AWS architecture proposals from grounded context.

Why it was selected:
Enables explicit provider comparison with evidence.

Alternatives considered:
Single generic cloud proposal agent.

Trade-offs:
Doubles proposal generation cost and orchestration steps.

### Component: Judge and final synthesis agent

Role:
Compares provider proposals and outputs one final architecture proposal.

Why it was selected:
Separates comparison logic from final recommendation writing.

Alternatives considered:
Returning only side-by-side proposals.

Trade-offs:
Additional stage introduces latency but improves decision usability.

## Why this architecture was selected

The architecture enforces grounded reasoning and provides actionable final recommendations rather than raw debate output.

## Alternatives considered

### Single-pass architecture generation

Why it was considered:
Lower complexity.

Why it was not selected:
Poor transparency on provider trade-offs and weaker decision traceability.

### Human-only architecture review

Why it was considered:
High control.

Why it was not selected:
Lower scalability and slower turnaround.

## Outcome

The system delivers more structured and justifiable architecture proposals with explicit evidence and decision traceability.

## Lessons learned

A final synthesis stage significantly improves stakeholder usability compared to raw agent debate outputs.

## Reuse this pattern when

- You need cloud-provider comparison with evidence.
- Decision traceability is mandatory.
- Architecture proposals must be reusable in delivery projects.

## Do not reuse this pattern when

- Only one cloud provider is in scope.
- A quick informal recommendation is enough.
- Retrieval evidence is unavailable.
