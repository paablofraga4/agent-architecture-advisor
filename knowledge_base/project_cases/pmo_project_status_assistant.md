# Project Case: PMO Project Status Assistant

## Problem

The PMO team needed to consolidate project updates from multiple documents and produce consistent status summaries for steering meetings.

## Business context

Project managers and PMO analysts were spending too much time collecting data manually from reports, meeting notes and trackers. The objective was to reduce reporting latency and improve consistency.

## Requirements

- Ingest project reports and status documents.
- Extract milestones, risks, blockers and progress indicators.
- Provide grounded answers with source evidence.
- Support multi-agent review for quality control.
- Expose outputs through an internal assistant UI.

## Constraints

- Responses must be grounded in retrieved project documents.
- Sensitive project data must stay within controlled enterprise environments.
- The architecture should allow fast iteration for PMO teams.

## Selected architecture

A grounded RAG assistant with a multi-agent review stage was selected.

## Components used

### Component: Document storage

Role:
Stores project status artifacts and supporting documents.

Why it was selected:
Provides a single source of truth for retrieval and traceability.

Alternatives considered:
Keeping files in disconnected team folders.

Trade-offs:
Requires metadata discipline for better retrieval quality.

### Component: Retrieval and vector index

Role:
Finds relevant status evidence from project documents.

Why it was selected:
PMO questions require contextual retrieval across many documents.

Alternatives considered:
Keyword-only search.

Trade-offs:
Semantic retrieval improves recall but requires embedding and index maintenance.

### Component: Multi-agent review

Role:
Validates and refines generated responses before delivery.

Why it was selected:
Reduces hallucinations and improves response structure for executives.

Alternatives considered:
Single-agent response generation.

Trade-offs:
Adds latency and orchestration complexity.

## Why this architecture was selected

The chosen architecture balances speed and trust: retrieval grounds the answers and multi-agent review improves quality for decision-making contexts.

## Alternatives considered

### Manual PMO reporting pipeline

Why it was considered:
Already in place.

Why it was not selected:
High effort, low scalability and inconsistent output quality.

### Single-agent assistant without retrieval

Why it was considered:
Simple to implement.

Why it was not selected:
Insufficient evidence traceability and higher hallucination risk.

## Outcome

The PMO team obtained faster status synthesis with grounded evidence and more consistent reporting artifacts.

## Lessons learned

For PMO assistants, retrieval quality and citation discipline are as important as model quality.

## Reuse this pattern when

- You need evidence-based project summaries.
- Documents are heterogeneous and frequently updated.
- Stakeholders require auditable answers.

## Do not reuse this pattern when

- Data is already structured in a single system of record.
- No evidence traceability is required.
- Real-time low-latency responses are the only priority.
