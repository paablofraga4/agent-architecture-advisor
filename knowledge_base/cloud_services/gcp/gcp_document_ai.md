# Service: Document AI

**Provider:** gcp
**Document type:** service_reference
**Category:** ai
**Tags:** ocr, document_extraction, forms
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://cloud.google.com/document-ai/docs/overview)
- [quotas](https://cloud.google.com/document-ai/quotas)
- [pricing](https://cloud.google.com/document-ai/pricing)

## Overview

Send feedback

# Document AI overview Stay organized with collections Save and categorize content based on your preferences.


This document is a guide to the fundamental concepts of using Document AI.
You should read this page before proceeding to any other documentation or quickstarts.

## Automate document processing workflows

Businesses all over the world rely heavily on documents to store and convey information.
This information often needs to be digitized for it to become useful. However,
this is usually accomplished through time-intensive, manual processes.

For example:

* Digitizing books for e-readers.
* Processing medical intake forms at doctor's offices.
* Parsing receipts and invoices for expense report validation.
* Authenticating identity based on ID cards.
* Extracting income information from tax forms for approving loans.
* Understanding contracts for key business agreement terms.

Each of these workflows involve getting the raw text from documents, then
extracting specific text from that which corresponds to the data needed (the fields or entities).
However, each document type has a different structure and layout, and the pattern of fields
vary depending on the specific use case.

## Document AI components

Document AI is a [document processing and understanding](https://en.wikipedia.org/wiki/Document_processing)
platform that takes unstructured data from documents and transforms it into
structured data (specific fields, suitable for a database), making it easier to understand, analyze, and consume.

Document AI is built on top of products within Vertex AI with generative AI to help you
create scalable, end-to-end, cloud-based document processing applications without specialized machine learning expertise.

Using Document AI, you can:

* **Digitize documents** using OCR to get text, layout, and various add ons such as image
  quality detection (for readability) and deskewing (fully automatic).
* **Extract** text and layout information, from document files and normalize entities.
* **Identify key-value pairs (kvp)** in structured forms and regular tables. For example: `Name: Jill Smith` is a kvp.
* **Classify** document types to drive downstream processes such as extraction and storage.
* **Split** and classify documents by type.

## Limits and Quotas

*Source: [https://cloud.google.com/document-ai/quotas](https://cloud.google.com/document-ai/quotas)*

Send feedback

# Quotas Stay organized with collections Save and categorize content based on your preferences.


This document lists the quotas and system limits that apply to
Document AI.

* *Quotas* have default values, but you can typically request
  adjustments.
* *System limits* are fixed values that can't be changed.

Google Cloud uses quotas to help ensure fairness and reduce
spikes in resource use and availability. A quota restricts how much of a
Google Cloud resource your Google Cloud project can use. Quotas
apply to a range of resource types, including hardware, software, and network
components. For example, quotas can restrict the number of API calls to a
service, the number of load balancers used concurrently by your project, or the
number of projects that you can create. Quotas protect the community of
Google Cloud users by preventing the overloading of services. Quotas also
help you to manage your own Google Cloud resources.

The Cloud Quotas system does the following:

* Monitors your consumption of Google Cloud products and services
* Restricts your consumption of those resources
* Provides a way to
  [request changes to the quota value](/docs/quotas/help/request_increase)
  and [automate quota adjustments](/docs/quotas/quota-adjuster)

In most cases, when you attempt to consume more of a resource than its quota
allows, the system blocks access to the resource, and the task that
you're trying to perform fails.

Quotas generally apply at the Google Cloud project
level. Your use of a resource in one project doesn't affect
your available quota in another project. Within a Google Cloud project, quotas
are shared across all applications and IP addresses.

For more information, see the
[Cloud Quotas overview](/docs/quotas/overview).

To increase available capacity for your projects, read about [capacity
reservation requests](/document-ai/capacity-reservation).

## Online service tiers

Document AI supports two service tiers and associated quotas for online
process requests to Generative AI-powered processor versions: provisioned
and best effort tiers.

Provisioned tier quota provides 120 pages per minute for base processor versions,
such as custom extractor v1.4 and v1.5, and 30 pages per minute for base processor
versions like custom extractor v1.5 Pro.

Best effort tier quota provides 120 for base processor versions like custom extractor
v1.4 and v1.5, 60 for Pro processor versions such as custom extractor v1.5 Pro,
and is only used once the provisioned quota has been exhausted.

## Pricing

*Source: [https://cloud.google.com/document-ai/pricing](https://cloud.google.com/document-ai/pricing)*

Send feedback


Stay organized with collections

Save and categorize content based on your preferences.


# Document AI pricing

This document explains Document AI pricing details.

Document AI is a solution and intended to be used with
other Google Cloud products. You might need to review the pricing
for [Cloud Vision](/vision/pricing),
[Cloud Natural Language API](/natural-language/pricing), or
[Vertex AI](/vertex-ai/pricing#automl_models).
You are not billed for failed requests (`4xx` or `5xx` response codes).

If you pay in a currency other than USD, the prices listed in your currency on
[Cloud Platform SKUs](https://cloud.google.com/skus/)
apply.

## Digitize text

| Processor | 1 - 5,000,000 pages/month  [5](#footnote5) | 5,000,001+ pages/month |
| --- | --- | --- |
| Enterprise Document OCR Processor | $1.50 per 1,000 pages | $0.60 per 1,000 pages |
| OCR add ons [2](#footnote1) | $6 per 1,000 pages | $6 per 1,000 pages |

## Extract structures and entities from documents

| Processor | 1 - 1,000,000 pages/month | 1,000,001+ pages/month |
| --- | --- | --- |
| Custom extractor [1](#footnote1) | $30 per 1,000 pages | $20 per 1,000 pages |
| Form Parser | $30 per 1,000 pages | $20 per 1,000 pages |
| Layout Parser (Includes initial chunking) | $10 per 1,000 pages | $10 per 1,000 pages |

## Break documents into chunks

| Processor | Price |
| --- | --- |
| Re-chunking parsed documents | $0.02 per 1,000 pages |

If you pay in a currency other than USD, the prices listed in your currency on
[Cloud Platform SKUs](https://cloud.google.com/skus/)
apply.

### Pricing examples

#### Example 1

You sent 100 pages to Form Parser in your monthly billing cycle.
