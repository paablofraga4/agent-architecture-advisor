# Project Case: Remittance PDF Extraction to BI

## Problem

The project required analyzing PDF remittance files from different banks and different remittance types. The system needed to extract structured fields from the PDFs, validate the extracted information and prepare the data for downstream BI dashboards.

## Business context

Business users needed visibility over payment and remittance data. Manual extraction from bank PDFs was slow, error-prone and difficult to scale across banks and document formats.

The output needed to support analytical reporting and dashboarding.

## Requirements

- Ingest PDF files from different banks.
- Support multiple PDF layouts and remittance types.
- Extract structured fields from semi-structured documents.
- Normalize extracted data.
- Validate extracted data before reporting.
- Store structured output for analytics.
- Feed a BI dashboard.
- Support cloud deployment in Azure or AWS.

## Constraints

- The system must support different document formats.
- The extracted data must be reliable enough for reporting.
- The architecture should separate document extraction from analytics.
- The solution should be extensible to new banks and new PDF templates.

## Selected architecture

A document processing pipeline was selected.

The architecture separates:
- raw document storage,
- document extraction,
- validation and normalization,
- structured data storage,
- BI consumption.

## Components used

### Component: Object storage

Role:
Stores the original PDF remittance files.

Why it was selected:
Object storage is suitable for raw unstructured documents and can act as the source of truth for uploaded files.

Alternatives considered:
Local folders were considered for early experimentation but are not suitable for production cloud deployment.

Trade-offs:
Object storage requires an additional processing and indexing layer because it does not extract or analyze document contents by itself.

### Component: Document extraction service

Role:
Extracts structured fields from PDF remittance files.

Why it was selected:
The project required extraction from semi-structured PDF documents with different layouts.

Alternatives considered:
Manual extraction was not selected because it is slow and error-prone.
Pure text parsing was not selected because PDF formats can vary significantly.

Trade-offs:
Document extraction quality must be validated, especially when templates differ across banks.

### Component: Validation and normalization layer

Role:
Validates extracted fields and converts them into a consistent schema.

Why it was selected:
BI reporting requires consistent and trusted structured data.

Alternatives considered:
Sending raw extracted data directly to BI was not selected because it would create quality and consistency problems.

Trade-offs:
This layer adds complexity but improves trust in the reporting output.

### Component: Structured database

Role:
Stores normalized extraction results for analysis.

Why it was selected:
BI dashboards need structured and queryable data.

Alternatives considered:
Keeping results only as JSON files was considered but would make analytical querying harder.

Trade-offs:
A database requires schema design and data quality controls.

### Component: BI dashboard

Role:
Displays extracted and validated remittance data to business users.

Why it was selected:
The project goal included analysis and reporting, not only extraction.

Alternatives considered:
Static reports were considered less flexible than dashboards.

Trade-offs:
BI dashboards depend on clean and modeled data.

## Why this architecture was selected

This architecture was selected because the problem was not only document extraction. The real need was an end-to-end pipeline from raw PDF ingestion to reliable analytical reporting.

Separating storage, extraction, validation, structured persistence and BI consumption makes the system easier to evolve when new banks, new document types or new validation rules are added.

## Alternatives considered

### Fully manual process

Why it was considered:
It already existed or required little technical setup.

Why it was not selected:
It was slow, repetitive, error-prone and difficult to scale.

### Direct PDF-to-dashboard process

Why it was considered:
It looked simpler at first.

Why it was not selected:
It skipped validation and normalization, which are necessary for trusted reporting.

### Local-only script

Why it was considered:
It is useful for initial experimentation.

Why it was not selected:
The user wanted the solution to be hosted in Azure or AWS from the beginning.

## Outcome

The architecture enables automated document ingestion, structured extraction, validation and BI reporting.

## Lessons learned

For document-to-BI use cases, extraction quality and data normalization are as important as the cloud deployment choice.

## Reuse this pattern when

- The input is semi-structured documents.
- The output must feed analytics or dashboards.
- The system must support multiple document formats.
- Validation is required before reporting.

## Do not reuse this pattern when

- The input data is already structured.
- There is no need for analytics.
- Manual processing is acceptable.
- The document formats are too unstable and require human review for every file.
