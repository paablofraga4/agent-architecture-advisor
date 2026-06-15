# Service: Amazon Textract

**Provider:** aws
**Document type:** service_reference
**Category:** ai
**Tags:** ocr, document_extraction, forms, tables
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://docs.aws.amazon.com/textract/latest/dg/what-is.html)
- [limits](https://docs.aws.amazon.com/textract/latest/dg/limits.html)
- [pricing](https://aws.amazon.com/textract/pricing/)

## Overview

# What is Amazon Textract?

Amazon Textract helps you add document text detection and analysis to your applications.
Using Amazon Textract, you can do the following:

* Detect typed and handwritten text in a variety of documents, including financial
  reports, medical records, and tax forms.
* Extract text, forms, and tables from documents with structured data, using the
  Amazon Textract Document Analysis API.
* Specify and extract information from documents using the Queries feature within
  the Amazon Textract Analyze Document API.
* Process invoices and receipts with the AnalyzeExpense API.
* Process ID documents such as drivers licenses and passports issued by U.S.
  government, using the AnalyzeID API.
* Upload and process mortgage loan packages, through automatic routing of the the
  document pages to the appropriate Amazon Textract analysis operations using the Analyze
  Lending workflow. You can retrieve analysis results for each document page or you
  can retrieve summarized results for a set of document pages.
* Use Custom Queries to customize the pretrained Queries feature using
  your data to support your down stream processing needs.

Amazon Textract is based on the same proven, highly scalable, deep-learning technology that
was developed by Amazon's computer vision scientists to analyze billions of images and
videos daily. You don't need any machine learning expertise to use it, as Amazon Textract
includes simple, easy-to-use API operations that can analyze image files and PDF files.
Amazon Textract is always learning from new data, and Amazon is continually adding new
features to the service.

The following are common use cases for using
Amazon Textract:

* **Creating an intelligent search index** â
  Using Amazon Textract you can create libraries of text that is detected in image and PDF
  files.
* **Using intelligent text extraction for natural language
  processing (NLP)** â Amazon Textract provides you with control
  over how text is grouped as an input for NLP applications. It can extract text as
  words and lines. It also groups text by table cells if Amazon Textract document table
  analysis is enabled.
* **Accelerating
  the capture and normalization of data from different
  sources** â Amazon Textract enables text and
  tabular data extraction from a wide variety of documents, such as financial
  documents, research reports, and medical notes.

## Key Features

# What is Amazon Textract?

Amazon Textract helps you add document text detection and analysis to your applications.
Using Amazon Textract, you can do the following:

* Detect typed and handwritten text in a variety of documents, including financial
  reports, medical records, and tax forms.
* Extract text, forms, and tables from documents with structured data, using the
  Amazon Textract Document Analysis API.
* Specify and extract information from documents using the Queries feature within
  the Amazon Textract Analyze Document API.
* Process invoices and receipts with the AnalyzeExpense API.
* Process ID documents such as drivers licenses and passports issued by U.S.
  government, using the AnalyzeID API.
* Upload and process mortgage loan packages, through automatic routing of the the
  document pages to the appropriate Amazon Textract analysis operations using the Analyze
  Lending workflow. You can retrieve analysis results for each document page or you
  can retrieve summarized results for a set of document pages.
* Use Custom Queries to customize the pretrained Queries feature using
  your data to support your down stream processing needs.

Amazon Textract is based on the same proven, highly scalable, deep-learning technology that
was developed by Amazon's computer vision scientists to analyze billions of images and
videos daily. You don't need any machine learning expertise to use it, as Amazon Textract
includes simple, easy-to-use API operations that can analyze image files and PDF files.
Amazon Textract is always learning from new data, and Amazon is continually adding new
features to the service.

The following are common use cases for using
Amazon Textract:

* **Creating an intelligent search index** â
  Using Amazon Textract you can create libraries of text that is detected in image and PDF
  files.
* **Using intelligent text extraction for natural language
  processing (NLP)** â Amazon Textract provides you with control
  over how text is grouped as an input for NLP applications. It can extract text as
  words and lines. It also groups text by table cells if Amazon Textract document table
  analysis is enabled.
* **Accelerating
  the capture and normalization of data from different
  sources** â Amazon Textract enables text and
  tabular data extraction from a wide variety of documents, such as financial
  documents, research reports, and medical notes. With Amazon Textract Analyze Document
  APIs, you can easily and quickly extract unstructured and structured data from your
  documents.
* **Automating data capture from forms** â
  Amazon Textract enables structured data to be extracted from forms.

## Limits and Quotas

*Source: [https://docs.aws.amazon.com/textract/latest/dg/limits.html](https://docs.aws.amazon.com/textract/latest/dg/limits.html)*

# Quotas in Amazon Textract

The following sections provide information about quotas, formerly referred to as limits, when using Amazon Textract. There are two
kinds of quotas. *Set quotas*, which can be viewed in the section [Set Quotas in Amazon Textract](./limits-document.html), cannot be changed. *Default quotas*,
discussed in the section [Default Quotas](./limits-quotas-explained.html), can be viewed or changed via the
[Service quotas console](https://console.aws.amazon.com/servicequotas). You can
also view the current Amazon Textract default quotas on the [Amazon Textract endpoints
and service quotas](https://docs.aws.amazon.com/general/latest/gr/textract.html).

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

API Reference

Set Quotas

## Pricing

*Source: [https://aws.amazon.com/textract/pricing/](https://aws.amazon.com/textract/pricing/)*

Amazon Textract

* [Overview](/textract/)
* Features
* [Pricing](/textract/pricing/)
* [Resources](/textract/resources/)
* [FAQs](/textract/faqs/)
* More

# Amazon Textract pricing

[### AWS Pricing Calculator

Calculate your Amazon Textract and architecture cost in a single estimate.

**Create your custom estimate now »**](https://calculator.aws/#/createCalculator/Textract)

Amazon Textract has five different APIs: Detect Document Text API, Analyze Document API, Analyze Expense API, and Analyze ID API, and Analyze Lending API.

**Detect Document Text API** uses OCR technology to extract text and handwriting from a document.

**Analyze Document API** has four features, Forms, Tables, Queries, and Signatures. You have the flexibility to call any combination of Forms, Tables, Queries, and Signatures together.

* Analyze Document API for Forms extracts data such as key-value pairs (“First Name” and associated value, such as “Jane Smith”). It also uses OCR technology to extract all the text and handwriting from a document.
* Analyze Document API for Tables extracts tabular or table data organized in columns and rows. It also uses OCR technology to extract all the text and handwriting from a document.
* Analyze Document API for Queries provides you the flexibility to specify the information you need from a document (e.g., “What is the customer name?”) and receive that data (e.g., “Jane Doe”) as part of the response. You do not need to worry about the structure of the data in the document or variations in how the data is laid out across different formats and versions of the document. It also uses OCR technology to extract all the text and handwriting from a document.
* Analyze Document API for Custom Queries provides you the ability to call the customized Queries feature for your business-specific documents. You train an adapter using the AWS Console and use the adapter identifier in your Analyze Document API request to use Custom Queries.
* Analyze Document API for Signatures provides the ability to detect handwritten signatures, electronic signatures, and initials on any document or image. It also uses OCR technology to extract all the text and handwriting from a document.

**Analyze ID API** uses machine learning to understand the context of identity documents such as U.S. passports, driver’s licenses, and other IDs. You can automatically extract specific information such as date of expiry and date of birth, as well as intelligently identify and extract implied information such as name and address. Each ID image is considered a page.

**Analyze Lending API** is a specialized mortgage document processing API that automates the classification and extraction of information from a range of mortgage-related application documents. Analyze Lending’s machine learning models have been pre-trained across the diversity of document types that are seen in a typical mortgage application package.
