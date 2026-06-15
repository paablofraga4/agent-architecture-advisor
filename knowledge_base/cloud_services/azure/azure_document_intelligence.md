# Service: Azure AI Document Intelligence

**Provider:** azure
**Document type:** service_reference
**Category:** ai
**Tags:** ocr, document_extraction, forms, invoices
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview)
- [limits](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/service-limits)
- [pricing](https://azure.microsoft.com/en-us/pricing/details/ai-document-intelligence/)

## Overview

Note


# What is Azure Document Intelligence in Foundry Tools?


**This content applies to:**  **v4.0 (GA)** | **Prior versions:**  [**v3.1 (GA)**](?view=doc-intel-3.1.0&preserve-view=tru)  [**v3.0 (retiring)**](?view=doc-intel-3.0.0&preserve-view=tru)  [**v2.1 (retiring)**](?view=doc-intel-2.1.0&preserve-view=tru)

**This content applies to:**  **v3.1 (GA)** | **Latest version:**  [**v4.0 (GA)**](?view=doc-intel-4.0.0&preserve-view=true) | **Prior versions:**  [**v3.0**](?view=doc-intel-3.0.0&preserve-view=true)  [**v2.1**](?view=doc-intel-2.1.0&preserve-view=true)

**This content applies to:**  **v3.0 (retiring)** | **Latest versions:**  [**v4.0 (GA)**](?view=doc-intel-4.0.0&preserve-view=true)  [**v3.1**](?view=doc-intel-3.1.0&preserve-view=true) | **Previous version:**  [v2.1 (retiring)](?view=doc-intel-2.1.0&preserve-view=true)

**This content applies to:**  **v2.1** | **Latest version:**  [**v4.0 (GA)**](?view=doc-intel-4.0.0&preserve-view=tru)

Azure Document Intelligence in Foundry Tools is a cloud-based [Foundry Tools](../?view=doc-intel-4.0.0) service that you can use to build intelligent document processing solutions. Massive amounts of data, spanning various data types, are stored in forms and documents. You can use Azure Document Intelligence to effectively manage the speed at which data is collected and processed. Azure Document Intelligence is key to improved operations, informed data-driven decisions, and enlightened innovation. For information on region access, see [Product availability by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table).

Important

* **Document Intelligence REST API v2.1** reaches end of support on **September 15, 2027**.
* **Document Intelligence REST API 2022-08-31 v3.0** reaches end of support on **March 30, 2029**.
* To avoid production disruption, migrate now to **Azure Document Intelligence 2024-11-30 v4.0**. For more information, see [**Document Intelligence migration guide**](versioning/migration-guide-overview?view=doc-intel-4.0.0).

Azure Document Intelligence in Foundry Tools is a cloud-based [Foundry Tools](../?view=doc-intel-4.0.0) service that you can use to build intelligent document processing solutions. Massive amounts of data, spanning various data types, are stored in forms and documents. You can use Azure Document Intelligence to effectively manage the speed at which data is collected and processed.

## Key Features

# What is Azure Document Intelligence in Foundry Tools?


**This content applies to:**  **v4.0 (GA)** | **Prior versions:**  [**v3.1 (GA)**](?view=doc-intel-3.1.0&preserve-view=tru)  [**v3.0 (retiring)**](?view=doc-intel-3.0.0&preserve-view=tru)  [**v2.1 (retiring)**](?view=doc-intel-2.1.0&preserve-view=tru)

**This content applies to:**  **v3.1 (GA)** | **Latest version:**  [**v4.0 (GA)**](?view=doc-intel-4.0.0&preserve-view=true) | **Prior versions:**  [**v3.0**](?view=doc-intel-3.0.0&preserve-view=true)  [**v2.1**](?view=doc-intel-2.1.0&preserve-view=true)

**This content applies to:**  **v3.0 (retiring)** | **Latest versions:**  [**v4.0 (GA)**](?view=doc-intel-4.0.0&preserve-view=true)  [**v3.1**](?view=doc-intel-3.1.0&preserve-view=true) | **Previous version:**  [v2.1 (retiring)](?view=doc-intel-2.1.0&preserve-view=true)

**This content applies to:**  **v2.1** | **Latest version:**  [**v4.0 (GA)**](?view=doc-intel-4.0.0&preserve-view=tru)

Azure Document Intelligence in Foundry Tools is a cloud-based [Foundry Tools](../?view=doc-intel-4.0.0) service that you can use to build intelligent document processing solutions. Massive amounts of data, spanning various data types, are stored in forms and documents. You can use Azure Document Intelligence to effectively manage the speed at which data is collected and processed. Azure Document Intelligence is key to improved operations, informed data-driven decisions, and enlightened innovation. For information on region access, see [Product availability by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table).

Important

* **Document Intelligence REST API v2.1** reaches end of support on **September 15, 2027**.
* **Document Intelligence REST API 2022-08-31 v3.0** reaches end of support on **March 30, 2029**.
* To avoid production disruption, migrate now to **Azure Document Intelligence 2024-11-30 v4.0**. For more information, see [**Document Intelligence migration guide**](versioning/migration-guide-overview?view=doc-intel-4.0.0).

Azure Document Intelligence in Foundry Tools is a cloud-based [Foundry Tools](../?view=doc-intel-4.0.0) service that you can use to build intelligent document processing solutions. Massive amounts of data, spanning various data types, are stored in forms and documents. You can use Azure Document Intelligence to effectively manage the speed at which data is collected and processed. Azure Document Intelligence is key to improved operations, informed data-driven decisions, and enlightened innovation.

## Limits and Quotas

*Source: [https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/service-limits](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/service-limits)*

Note


# Service quotas and limits


**This content applies to:** **v4.0 (GA)** | **Prior versions:**  [**v3.1 (GA)**](?view=doc-intel-3.1.0&preserve-view=tru)  [**v3.0 (retiring)**](?view=doc-intel-3.0.0&preserve-view=tru)

**This content applies to:**  **v2.1** | **Latest version:**  [**v4.0 (GA)**](?view=doc-intel-4.0.0&preserve-view=tru)

This article contains both a quick reference and detailed description of Azure Document Intelligence in Foundry Tools Quotas and Limits for all [pricing tiers](https://azure.microsoft.com/pricing/details/form-recognizer/). It also contains some best practices to avoid request throttling.

## Model usage

| Document types supported | Read | Layout | Prebuilt models | Custom models | Add-on capabilities |
| --- | --- | --- | --- | --- | --- |
| PDF | âï¸ | âï¸ | âï¸ | âï¸ | âï¸ |
| Images: `JPEG/JPG`, `PNG`, `BMP`, `TIFF`, `HEIF` | âï¸ | âï¸ | âï¸ | âï¸ | âï¸ |
| Microsoft Office: `DOCX`, `PPTX`, `XLS` | âï¸ | âï¸ | âï¸ | âï¸ | âï¸ |

âï¸ = supported
âï¸ = Not supported

For Document Intelligence v4.0 `2024-11-30` (GA) supports page and line features with the following restrictions:

* Angle, width/height, and unit aren't supported.
* For each object detected, bounding polygon or bounding regions aren't supported.
* The `lines` object isn't supported.

| Document types supported | Read | Layout | Prebuilt models | Custom models |
| --- | --- | --- | --- | --- |
| PDF | âï¸ | âï¸ | âï¸ | âï¸ |
| Images: `JPEG/JPG`, `PNG`, `BMP`, `TIFF`, `HEIF` | âï¸ | âï¸ | âï¸ | âï¸ |
| Microsoft Office: `DOCX`, `PPTX`, `XLS` | âï¸ | âï¸ | âï¸ | âï¸ |

âï¸ = supported
âï¸ = Not supported

## Billing

Document Intelligence billing is calculated monthly based on the model type and the number of pages analyzed. You can find usage metrics on the metrics dashboard in the Azure portal. The dashboard displays the number of pages that Azure Document Intelligence processes. You can check the estimated cost spent on the resource by using the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/). For detailed instructions, see [Check usage and estimate cost](how-to-guides/estimate-cost?view=doc-intel-4.0.0). Here are some details:

* When you submit a document for analysis, the service analyzes all pages unless you specify a page range by using the `pages` parameter in your request. When the service analyzes Microsoft Excel and PowerPoint documents through the read, OCR, or layout model, it counts each Excel worksheet and PowerPoint slide as one page.
* When the service analyzes PDF and TIFF files, it counts each page in the PDF file or each image in the TIFF file as one page with no maximum character limits.
* When the service analyzes Microsoft Word and HTML files that the read and layout models support, it counts pages in blocks of 3,000 characters each.

## Pricing

*Source: [https://azure.microsoft.com/en-us/pricing/details/ai-document-intelligence/](https://azure.microsoft.com/en-us/pricing/details/ai-document-intelligence/)*

# Azure Document Intelligence in Foundry Tools pricing

* [Request a pricing quote](/en-us/contact/pricing/)
* [Try Azure for free](/en-us/free/)

## Accelerate information extraction from documents

Document Intelligence uses AI to extract fields, text and data from your documents and forms. It ingests content from forms and documents, applies machine learning technology to identify keys, associated values and tables, and then outputs structured data that includes the relationships within the original file. With Document Intelligence you can extract information quickly, accurately, and tailored to your specific content, without heavy manual intervention or extensive data science expertise.

## Explore pricing options

Apply filters to customize pricing options to your needs.

Prices are estimates only and are not intended as actual price quotes. Actual pricing may vary depending on the type of agreement entered with Microsoft, date of purchase, and the currency exchange rate. Prices are calculated based on US dollars and converted using London closing spot rates that are captured in the two business days prior to the last business day of the previous month end. If the two business days prior to the end of the month fall on a bank holiday in major markets, the rate setting day is generally the day immediately preceding the two business days. This rate applies to all transactions during the upcoming month. Sign in to the [Azure pricing calculator](/en-us/pricing/calculator/) to see pricing based on your current program/offer with Microsoft. Contact an [Azure sales specialist](/en-us/contact/pricing/) for more information on pricing or to request a price quote.
