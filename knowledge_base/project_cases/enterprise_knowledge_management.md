# Project Case: Enterprise Knowledge Management System

## Problem

A consulting firm with over 10,000 employees needed a centralized system to search and query knowledge scattered across SharePoint, Confluence and Microsoft Teams. Consultants spent excessive time searching for prior deliverables, templates and internal expertise.

## Business context

Institutional knowledge was siloed across multiple platforms. New consultants had no efficient way to find relevant past work. Senior consultants answered the same questions repeatedly. The firm estimated significant billable hours were lost to internal knowledge discovery.

## Requirements

- Ingest documents from SharePoint, Confluence and Microsoft Teams.
- Process documents of varying formats including PDF, Word, PowerPoint and HTML.
- Support both keyword and semantic search.
- Provide a conversational Q&A interface over the knowledge base.
- Enrich documents with metadata such as practice area, client industry and document type.
- Incorporate user feedback to improve search relevance.
- Support deployment on Azure or AWS.

## Constraints

- The system must respect existing document access permissions.
- Ingestion must handle incremental updates without full reprocessing.
- Search results must be traceable to source documents.
- The system must scale to millions of document chunks.
- Client-confidential documents must be handled according to data classification rules.

## Selected architecture

A multi-source ingestion pipeline with hybrid search and conversational Q&A was selected.

The architecture separates:
- source connectors and ingestion,
- document processing and chunking,
- metadata enrichment,
- hybrid search index,
- conversational Q&A layer,
- feedback collection.

## Components used

### Component: Document processing service

Role:
Extracts text and structure from documents of various formats.

Azure version: Azure Document Intelligence.
AWS version: Amazon Textract.

Why it was selected:
Enterprise documents come in many formats. A managed extraction service handles format variation without custom parsers.

Alternatives considered:
Open-source libraries like Apache Tika were considered but required more maintenance for production-grade extraction.

Trade-offs:
Managed services have per-page costs that scale with document volume.

### Component: Hybrid search index

Role:
Stores document chunks with both vector embeddings and keyword indexes for hybrid retrieval.

Azure version: Azure AI Search with semantic ranking.
AWS version: Amazon OpenSearch Service with vector and BM25 search.

Why it was selected:
Hybrid search combines the precision of keyword matching with the recall of semantic search, which is important when users search with both exact terms and natural language.

Alternatives considered:
Vector-only search was considered but missed exact-match queries for project codes and client names.

Trade-offs:
Hybrid search requires maintaining two index types and tuning the balance between them.

### Component: Language model for Q&A

Role:
Generates conversational answers grounded in retrieved document chunks.

Azure version: Azure OpenAI Service.
AWS version: Amazon Bedrock.

Why it was selected:
Consultants preferred asking questions in natural language rather than constructing search queries.

Trade-offs:
LLM-generated answers must cite sources to maintain trust. Grounding enforcement adds prompt complexity.

### Component: Metadata enrichment pipeline

Role:
Classifies documents by practice area, industry, document type and other taxonomy dimensions.

Why it was selected:
Metadata-based filtering dramatically improves search precision in large knowledge bases.

Trade-offs:
Enrichment adds processing time and requires maintaining a taxonomy.

## Why this architecture was selected

The combination of multi-source ingestion, hybrid search and conversational Q&A was selected because the knowledge discovery problem required both structured filtering and natural language understanding. No single search modality could serve all user needs.

## Alternatives considered

### Enterprise search appliance

Why it was considered:
Turnkey solution with minimal development.

Why it was not selected:
Lacked semantic search and conversational Q&A capabilities.

### Manual knowledge curation

Why it was considered:
High quality when done well.

Why it was not selected:
Does not scale to the volume of documents produced by 10,000 employees.

## Outcome

Consultants reported finding relevant prior work in minutes instead of hours. The conversational Q&A interface became the primary entry point for knowledge discovery.

## Lessons learned

- Chunking strategy made or broke retrieval quality. Chunks that were too large diluted relevance. Chunks that were too small lost context. Overlapping chunks with 10-20% overlap produced the best results.
- Metadata enrichment was essential. Without practice area and document type filters, the search index returned too many loosely related results.
- A user feedback loop improved relevance over time. Thumbs up and thumbs down signals were used to fine-tune ranking and identify gaps in the knowledge base.
- Incremental ingestion was harder than expected. Detecting document updates and deletions across three source systems required careful connector design.

## Reuse this pattern when

- Knowledge is scattered across multiple enterprise platforms.
- Users need both structured search and conversational Q&A.
- The document corpus is large and diverse in format.
- Metadata-based filtering is important for precision.

## Do not reuse this pattern when

- All knowledge is already in a single well-organized system.
- The document corpus is small enough for manual curation.
- Users only need keyword search and do not need conversational answers.
