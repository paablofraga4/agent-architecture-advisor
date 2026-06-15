# Service: Azure AI Search

**Provider:** azure
**Document type:** service_reference
**Category:** search
**Tags:** search, vector, hybrid, rag, semantic_ranking
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search)
- [limits](https://learn.microsoft.com/en-us/azure/search/search-limits-quotas-capacity)
- [pricing](https://azure.microsoft.com/en-us/pricing/details/search/)
- [vector_search](https://learn.microsoft.com/en-us/azure/search/vector-search-overview)

## Overview

Note


# What is Azure AI Search?


Azure AI Search is a fully managed, cloud-hosted service that connects your data to AI. The service unifies access to enterprise and web content so agents and LLMs can use context, chat history, and multi-source signals to produce reliable, grounded answers.

Azure AI Search is available in two pricing models:

* **Dedicated**: Provisioned capacity with fixed pricing. You select a service tier and you're billed per hour based on Search Units (SUs). Best for steady, predictable, high-utilization workloads.
* **Serverless (Preview)**: Consumption-based pricing measured by Compute Units per hour (CU/hr) and per-GB/month for indexed storage. Best for infrequent, bursty, or highly variable workloads.

Important

The Serverless Developer tier is currently in preview. This preview is provided without a service-level agreement and isn't recommended for production workloads. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Billing for the Serverless Developer tier isn't yet enabled during the preview. Estimated costs for your usage are available in the Azure portal and telemetry, but that usage won't appear on your Azure bill during this initial period. Microsoft will provide at least 30 days notice before billing begins. The deferral of billing during this preview is temporary. Serverless Developer is a paid tier and you'll be responsible for any charges accrued once billing begins.

The Serverless Developer tier doesn't support migration to or from other pricing tiers and some features available on other tiers aren't supported during Public Preview. Service limits, supported features, and pricing details may change before general availability.

The preview is currently only available in West Central US, Switzerland North, and Japan East.

Common use cases include *classic search* and retrieval-augmented generation (RAG) using *agentic retrieval*, where the service orchestrates query planning, retrieval, and response construction.

## Key Features

# What is Azure AI Search?


Azure AI Search is a fully managed, cloud-hosted service that connects your data to AI. The service unifies access to enterprise and web content so agents and LLMs can use context, chat history, and multi-source signals to produce reliable, grounded answers.

Azure AI Search is available in two pricing models:

* **Dedicated**: Provisioned capacity with fixed pricing. You select a service tier and you're billed per hour based on Search Units (SUs). Best for steady, predictable, high-utilization workloads.
* **Serverless (Preview)**: Consumption-based pricing measured by Compute Units per hour (CU/hr) and per-GB/month for indexed storage. Best for infrequent, bursty, or highly variable workloads.

Important

The Serverless Developer tier is currently in preview. This preview is provided without a service-level agreement and isn't recommended for production workloads. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Billing for the Serverless Developer tier isn't yet enabled during the preview. Estimated costs for your usage are available in the Azure portal and telemetry, but that usage won't appear on your Azure bill during this initial period. Microsoft will provide at least 30 days notice before billing begins. The deferral of billing during this preview is temporary. Serverless Developer is a paid tier and you'll be responsible for any charges accrued once billing begins.

The Serverless Developer tier doesn't support migration to or from other pricing tiers and some features available on other tiers aren't supported during Public Preview. Service limits, supported features, and pricing details may change before general availability.

The preview is currently only available in West Central US, Switzerland North, and Japan East.

Common use cases include *classic search* and retrieval-augmented generation (RAG) using *agentic retrieval*, where the service orchestrates query planning, retrieval, and response construction.

## Limits and Quotas

*Source: [https://learn.microsoft.com/en-us/azure/search/search-limits-quotas-capacity](https://learn.microsoft.com/en-us/azure/search/search-limits-quotas-capacity)*

Note


# Service limits in Azure AI Search


Maximum limits on storage, workloads, and quantities of indexes and other objects depend on the pricing model of your Azure AI Search service.

Azure AI Search supports two pricing models, each with associated service tiers. The tier you select impacts the service limits outlined in this guidance.

* **Dedicated**: Fixed pricing measured by Search Units (SUs). Service tier options include: Basic, Standard (S1-S3, including S3 HD), Storage Optimized (L1-L2), and a Free tier with limited search service capabilities.
* **Serverless (Preview)**: Consumption-based pricing measured by Compute Units per hour (CU/hr) and per-GB/month for indexed storage. The current preview tier is: Serverless Developer. Limits are defined by per-index caps, per-service object counts, and Serverless throttling behavior.

Important

The Serverless Developer tier is currently in preview. This preview is provided without a service-level agreement and isn't recommended for production workloads. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Billing for the Serverless Developer tier isn't yet enabled during the preview. Estimated costs for your usage are available in the Azure portal and telemetry, but that usage won't appear on your Azure bill during this initial period. Microsoft will provide at least 30 days notice before billing begins. The deferral of billing during this preview is temporary. Serverless Developer is a paid tier and you'll be responsible for any charges accrued once billing begins.

The Serverless Developer tier doesn't support migration to or from other pricing tiers and some features available on other tiers aren't supported during Public Preview. Service limits, supported features, and pricing details may change before general availability.

The preview is currently only available in West Central US, Switzerland North, and Japan East.

To learn more, see [Choose a pricing model and service tier](search-sku-tier).

## Subscription limits

You can create multiple *billable* search services (Basic and higher), up to the maximum number of services allowed at each tier, per region. For example, you can create up to 16 services at the Basic tier and another 16 services at the S1 tier within the same subscription and region. You can then create an additional 16 Basic services in another region for a combined total of 32 Basic services under the same subscription. For more information about service tiers, see [Choose a pricing model and service tier](/en-us/azure/search/search-sku-tier).

You can raise maximum service limits by request.

## Pricing

*Source: [https://azure.microsoft.com/en-us/pricing/details/search/](https://azure.microsoft.com/en-us/pricing/details/search/)*

1. [Home](/en-us/)
2. [Azure pricing](/en-us/pricing/)
3. Foundry IQ pricing

# Foundry IQ pricing

* [Request a pricing quote](/en-us/contact/pricing/)
* [Try Azure for free](/en-us/free/)

## Enable your agents to unlock knowledge from anywhere

Foundry IQ (Azure AI Search) provides a context engineering platform for Microsoft's intelligence layer, unlocking knowledge for your agents, wherever it lives. Foundry IQ automatically handles how agents connect to, process and action enterprise information. With built-in enterprise security and agentic retrieval, agents deliver better results from the right context.
Foundry IQ knowledge bases require a subscription and a standard agentic retrieval plan. Foundry IQ agentic retrieval activity is billed under "Azure AI Search".

## Explore pricing options

Apply filters to customize pricing options for your needs. “N/A” indicates pricing is not supported in the selected region.

Prices are estimates only and are not intended as actual price quotes. Actual pricing may vary depending on the type of agreement entered with Microsoft, date of purchase, and the currency exchange rate. Prices are calculated based on US dollars and converted using London closing spot rates that are captured in the two business days prior to the last business day of the previous month end. If the two business days prior to the end of the month fall on a bank holiday in major markets, the rate setting day is generally the day immediately preceding the two business days. This rate applies to all transactions during the upcoming month. Sign in to the [Azure pricing calculator](/en-us/pricing/calculator/) to see pricing based on your current program/offer with Microsoft. Contact an [Azure sales specialist](/en-us/contact/pricing/) for more information on pricing or to request a price quote.

## Vector Search

*Source: [https://learn.microsoft.com/en-us/azure/search/vector-search-overview](https://learn.microsoft.com/en-us/azure/search/vector-search-overview)*

Note


# Vector search in Azure AI Search


Vector search is an information retrieval approach that supports indexing and querying over numeric representations of content. Because the content is numeric rather than plain text, matching is based on vectors that are most similar to the query vector. This approach enables matching across:

* Semantic or conceptual likeness. For example, "dog" and "canine" are conceptually similar but linguistically distinct.
* Multilingual content, such as "dog" in English and "hund" in German.
* Multiple content types, such as "dog" in plain text and an image of a dog.

This article provides an overview of vector search in Azure AI Search, including supported scenarios, availability, and integration with other Azure services.

Tip

Want to get started right away? Follow these steps:

1. [Provide embeddings](vector-search-how-to-generate-embeddings) for your index or [generate embeddings](vector-search-integrated-vectorization) in an indexer pipeline.
2. [Create a vector index](vector-search-how-to-create-index).
3. [Run vector queries](vector-search-how-to-query).

## What scenarios can vector search support?

Vector search supports the following scenarios:

* **Similarity search**. Encode text using embedding models or open-source models, such as OpenAI embeddings or SBERT, respectively. You then retrieve documents using queries that are also encoded as vectors.
* **[Hybrid search](hybrid-search-overview)**. Azure AI Search defines hybrid search as the execution of vector search and [keyword search](search-lucene-query-architecture) in the same request. Vector support is implemented at the field level. If an index contains vector and nonvector fields, you can write a query that targets both. The queries execute in parallel, and the results are merged into a single response and ranked accordingly.
* **[Multimodal search](multimodal-search-overview)**.
