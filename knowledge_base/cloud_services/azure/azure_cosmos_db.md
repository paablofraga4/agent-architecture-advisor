# Service: Azure Cosmos DB

**Provider:** azure
**Document type:** service_reference
**Category:** database
**Tags:** nosql, multi_model, global_distribution, vector_search
**Last updated:** 2026-06-10
**Sources:**
- [overview](https://learn.microsoft.com/en-us/azure/cosmos-db/introduction)
- [limits](https://learn.microsoft.com/en-us/azure/cosmos-db/concepts-limits)
- [pricing](https://azure.microsoft.com/en-us/pricing/details/cosmos-db/)
- [vector_search](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/vector-search)

## Overview

Note


# Azure Cosmos DB - Database for the AI Era


> "OpenAI relies on Cosmos DB to dynamically scale their ChatGPT service â one of the fastest-growing consumer apps ever â enabling high reliability and low maintenance."
> â Satya Nadella, Microsoft chairman and chief executive officer

Today's applications are required to be highly responsive and always online. They must respond in real time to large changes in usage at peak hours, store ever increasing volumes of data, and make this data available to users in milliseconds. To achieve low latency and high availability, instances of these applications need to be deployed in datacenters that are close to their users.

The surge of AI-powered applications created another layer of complexity, because many of these applications integrate a multitude of data stores. For example, some organizations built applications that simultaneously connect to MongoDB, Redis, and Gremlin. These databases differ in implementation workflow and operational performances, posing extra complexity for scaling applications.

Azure Cosmos DB simplifies and expedites your application development by being the single database for your operational data needs, from [geo-replicated distributed caching](https://medium.com/@marcodesanctis2/using-azure-cosmos-db-as-your-persistent-geo-replicated-distributed-cache-b381ad80f8a0) to back up to [vector indexing and search](vector-database). It provides the data infrastructure for modern applications like [AI agent](ai-agents), digital commerce, Internet of Things, and booking management. It can accommodate all your operational data models, including document, vector, key-value, graph, and table.

If you're comparing Azure database services to find the right fit for your workload, see [Choose an Azure data service](/en-us/azure/architecture/guide/technology-choices/data-store-overview) in the Azure Architecture Center.

## An AI database providing industry-leading capabilities...

## ...for free

Azure Cosmos DB is a fully managed NoSQL and vector database. It offers single-digit millisecond response times, automatic and instant scalability, along with guaranteed speed at any scale.

## Key Features

## An AI database providing industry-leading capabilities...

## Limits and Quotas

*Source: [https://learn.microsoft.com/en-us/azure/cosmos-db/concepts-limits](https://learn.microsoft.com/en-us/azure/cosmos-db/concepts-limits)*

Note


# Azure Cosmos DB service quotas and default limits


This article explains the default quotas and limits for Azure Cosmos DB resources. It helps you manage operations, storage, and throughput effectively.

## Storage and database operations

After you create an Azure Cosmos DB account under your subscription, you can manage data in your account by [creating databases, containers, and items](resource-model).

### Provisioned throughput

You allocate throughput at the container level or the database level in terms of [request units (RUs) or request units per second (RU/s)](request-units). The following table lists the limits for storage and throughput per container/database. Storage refers to the combined amount of data and index storage.

| Resource | Limit |
| --- | --- |
| Maximum RUs per container ([dedicated throughput provisioned mode](resource-model#azure-cosmos-db-containers)) | 1,000,000 Â¹ |
| Maximum RUs per database ([shared throughput provisioned mode](resource-model#azure-cosmos-db-containers)) | 1,000,000 Â¹ |
| Maximum RUs per partition (logical & physical) | 10,000 |
| Maximum storage across all items per (logical) partition | 20 GB Â² |
| Maximum number of distinct (logical) partition keys | Unlimited |
| Maximum storage per container | Unlimited |
| Maximum attachment size per Account (Attachment feature is being deprecated) | 2 GB |
| Minimum RU/s required per 1 GB | 1 RU/s |

Â¹ Increase Maximum RUs per container or database by [filing an Azure support ticket](create-support-request-quota-increase).

Â² To learn about best practices for managing workloads that have partition keys requiring higher limits for storage or throughput, see [Create a synthetic partition key](synthetic-partition-keys) and [hierarchical partition keys overview](hierarchical-partition-keys). If your workload reaches the logical partition limit of 20 GB in production, the recommended long-term solution is to use [hierarchical partition keys overview](hierarchical-partition-keys) to rearchitect your application. With hierarchical partition keys, you can use up to three levels of keys, allowing you to exceed 20 GB of data for your first level key and avoid this limit. To give you time to rearchitect your application, request a temporary increase in the logical partition key limit for your existing application. [File an Azure support ticket](create-support-request-quota-increase) and select quota type **Temporary increase in container's logical partition key size**. Requesting a temporary increase is intended as a temporary mitigation and not recommended as a long-term solution, as **SLA guarantees are not honored when the limit is increased**. To remove the configuration, file a support ticket and select quota type **Restore containerâs logical partition key size to default (20 GB)**.

## Pricing

*Source: [https://azure.microsoft.com/en-us/pricing/details/cosmos-db/](https://azure.microsoft.com/en-us/pricing/details/cosmos-db/)*

# Azure Cosmos DB pricing

* [Request a pricing quote](/en-us/contact/pricing/)
* [Try Azure for free](/en-us/free/)

## Build or modernize scalable, high-performance apps

Quickly and easily develop apps at any scale with Azure Cosmos DB, a fully managed and serverless distributed database supporting NoSQL and relational workloads. [Get guaranteed speed and availability](/en-us/support/legal/sla/cosmos-db/v1_3/) for NoSQL data, automatic and instant scalability, and support for open source PostgreSQL, MongoDB, and Cassandra. Azure Cosmos DB offers cost-effective pricing models for apps of any size, from dev/test to production.

[Azure AI Advantage: Build high-performance intelligent apps in Azure with a free 90-day Azure Cosmos DB subscription for Azure AI customers.](https://aka.ms/AzureAIAdvantageBlog)

## Explore pricing options

Apply filters to customize pricing options to your needs.

Prices are estimates only and are not intended as actual price quotes. Actual pricing may vary depending on the type of agreement entered with Microsoft, date of purchase, and the currency exchange rate. Prices are calculated based on US dollars and converted using London closing spot rates that are captured in the two business days prior to the last business day of the previous month end. If the two business days prior to the end of the month fall on a bank holiday in major markets, the rate setting day is generally the day immediately preceding the two business days. This rate applies to all transactions during the upcoming month. Sign in to the [Azure pricing calculator](/en-us/pricing/calculator/) to see pricing based on your current program/offer with Microsoft. Contact an [Azure sales specialist](/en-us/contact/pricing/) for more information on pricing or to request a price quote. See [frequently asked questions](/en-us/pricing/) about Azure pricing.

## Vector Search

*Source: [https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/vector-search](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/vector-search)*

Note


# Vector search in Azure Cosmos DB for NoSQL


Azure Cosmos DB for NoSQL now offers efficient vector indexing and search. This feature is designed to handle multi-modal, high-dimensional vectors, enabling efficient and accurate vector search at any scale. You can now store vectors directly in the documents alongside your data. Each document in your database can contain not only traditional schema-free data, but also multi-modal high-dimensional vectors as other properties of the documents. This colocation of data and vectors allows for efficient indexing and searching, as the vectors are stored in the same logical unit as the data they represent. Keeping vectors and data together simplifies data management, AI application architectures, and the efficiency of vector-based operations.

Azure Cosmos DB for NoSQL offers flexibility by letting you choose the vector indexing method:

* A *flat* or k-nearest neighbors exact search (sometimes called brute-force) can provide 100% retrieval recall for smaller, focused vector searches. especially when combined with query filters and partition-keys.
* A quantized flat index that compresses vectors using DiskANN-based quantization methods for better efficiency in the kNN search.
* DiskANN, a suite of state-of-the-art vector indexing algorithms developed by Microsoft Research to power efficient, high accuracy multi-modal vector search at any scale.

To learn more about vector indexing, see [Vector indexes](index-policy#vector-indexes).

Vector search in Azure Cosmos DB can be combined with all other supported Azure Cosmos DB NoSQL query filters and indexes by using `WHERE` clauses.
