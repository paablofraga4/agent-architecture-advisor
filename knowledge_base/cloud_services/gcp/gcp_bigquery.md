# Service: BigQuery

**Provider:** gcp
**Document type:** service_reference
**Category:** analytics
**Tags:** analytics, data_warehouse, sql, vector_search
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://cloud.google.com/bigquery/docs/introduction)
- [quotas](https://cloud.google.com/bigquery/quotas)
- [pricing](https://cloud.google.com/bigquery/pricing)
- [vector_search](https://cloud.google.com/bigquery/docs/vector-search-intro)

## Overview

Send feedback


Stay organized with collections

Save and categorize content based on your preferences.


# BigQuery overview

BigQuery is a fully managed, AI-ready data platform that helps
you manage and analyze your data with built-in features like machine learning,
search, geospatial analysis, and business intelligence.
BigQuery's serverless architecture lets you use languages like
SQL and Python to answer your organization's biggest questions with zero
infrastructure management.

BigQuery provides a uniform way to work with both structured and
unstructured data and supports open table formats like Apache Iceberg,
Delta, and Apache Hudi. BigQuery
streaming supports continuous data ingestion and analysis while
BigQuery's scalable, distributed analysis engine lets you query
terabytes in seconds and petabytes in minutes.

BigQuery offers built-in governance capabilities that let you discover and
curate data, and manage metadata and data quality. Through features like
semantic search and data lineage, you can find and validate relevant data for
analysis. You can share data and AI assets across your organization with the
benefits of access control. These features are powered by
Knowledge Catalog, which is a unified, intelligent governance solution for data
and AI assets in Google Cloud.

BigQuery's architecture consists of two parts: a storage layer that
ingests, stores, and optimizes data and a compute layer that provides analytics
capabilities. These compute and storage layers efficiently operate
independently of each other thanks to Google's petabit-scale network that
enables the necessary communication between them.

Legacy databases usually have to share resources between read and write
operations and analytical operations. This can result in resource conflicts and
can slow queries while data is written to or read from storage.
Shared resource pools can become further strained when resources are
required for database management tasks such as assigning or revoking
permissions. BigQuery's separation of compute and storage layers
lets each layer dynamically allocate resources without impacting the performance
or availability of the other.

This separation principle lets BigQuery innovate faster because
storage and compute improvements can be deployed independently, without downtime
or negative impact on system performance.

## Key Features

## Gemini in BigQuery features

Gemini in BigQuery is part
of the [Gemini for Google Cloud](/gemini/docs/overview) product suite
which provides AI-powered assistance to help you work with your
data.

Gemini in BigQuery provides AI assistance to help
you do the following:

* **Explore and understand your data with data insights**. Data insights offers an automated,
  intuitive way to uncover patterns and perform statistical analysis by using insightful queries
  that are generated from the metadata of your tables. This feature is especially helpful in
  addressing the cold-start challenges of early data exploration. For more information, see
  [Generate data insights in BigQuery](/bigquery/docs/data-insights).
* **Discover, transform, query, and visualize data with BigQuery data canvas**. You can use
  natural language with Gemini in BigQuery, to find, join, and
  query table assets, visualize results, and seamlessly collaborate with others throughout the
  entire process. For more information, see [Analyze with
  data canvas](/bigquery/docs/data-canvas).
* **Get assisted SQL and Python data analysis**. You can use Gemini in
  BigQuery to generate or suggest code in either SQL or Python, and to explain
  an existing SQL query. You can also use natural language queries to begin data analysis. To
  learn how to generate, complete, and summarize code, see the following documentation:
  + SQL code assist
    - [Use the SQL generation tool](/bigquery/docs/write-sql-gemini#use_the_sql_generation_tool)
    - [Prompt to generate SQL queries](/bigquery/docs/write-sql-gemini#chat)
    - [Generate SQL queries with Gemini Cloud Assist](/bigquery/docs/write-sql-gemini#chat)
      ([Preview](https://cloud.google.com/products#product-launch-stages))
    - [Convert comments to SQL](/bigquery/docs/write-sql-gemini#natural_language)
      ([Preview](https://cloud.google.com/products#product-launch-stages))
    - [Complete a SQL query](/bigquery/docs/write-sql-gemini#complete_a_sql_query)
      ([Preview](https://cloud.google.com/products#product-launch-stages))
    - [Explain a SQL query](/bigquery/docs/write-sql-gemini#explain_a_sql_query)
  + Python code assist
    - [Generate Python code with the code generation tool](/bigquery/docs/write-sql-gemini#generate_python_code)
    - [Generate Python code with Gemini Cloud Assist](/bigquery/docs/write-sql-gemini#chat-python)
      ([Preview](https://cloud.google.com/products#product-launch-stages))
    - [Python code completion](/bigquery/docs/write-sql-gemini#complete_python_code)
    - [Generate BigQuery DataFrames Python code](/bigquery/docs/write-sql-gemini#dataframe)
      ([Preview](https://cloud.google.com/products#product-launch-stages))* **Prepare data for analysis**. Data preparation in BigQuery gives you context
    aware, AI-generated transformation recommendations to cleanse data for analysis.

## Limits and Quotas

*Source: [https://cloud.google.com/bigquery/quotas](https://cloud.google.com/bigquery/quotas)*

Send feedback


Stay organized with collections

Save and categorize content based on your preferences.


# Quotas and limits

This document lists the quotas and system limits that apply to
BigQuery.

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

There are also *system limits* on BigQuery resources.
System limits can't be changed.

Some error messages specify quotas or limits that you can increase, while other
error messages specify quotas or limits that you can't increase. Reaching a hard
limit means that you need to implement temporary or permanent workarounds or
best practices for your workload. Doing so is a best practice, even for quotas
or limits that can be increased. For details about both types of errors, see
[Troubleshoot quota and limit errors](/bigquery/docs/troubleshoot-quotas).

By default, BigQuery
quotas and limits apply on a [per-project](/bigquery/docs/projects) basis.
Quotas and limits that apply on a different basis are indicated as
such; for example, the maximum number of columns *per table*, or the maximum
number of concurrent API requests *per user*.
Specific policies vary depending on resource availability, user profile,
Service Usage history, and other factors, and are subject to change without
notice.

### Quota replenishment

Daily quotas are replenished at regular intervals throughout the day,
reflecting their intent to guide rate limiting behaviors.

## Pricing

*Source: [https://cloud.google.com/bigquery/pricing](https://cloud.google.com/bigquery/pricing)*

Page Contents
BigQuery pricing
BigQuery is a serverless data analytics platform. You don't need to provision individual instances or virtual machines to use BigQuery. Instead, BigQuery automatically allocates computing resources as you need them. You can also reserve compute capacity ahead of time in the form of slots, which represent virtual CPUs. The pricing structure of BigQuery reflects this design.
Overview of BigQuery pricing
BigQuery pricing has two main components:
Compute pricing
is the cost to process queries, including SQL queries, user-defined functions, scripts, and certain data manipulation language (DML) and data definition language (DDL) statements.
Storage pricing
is the cost to store data that you load into BigQuery.
BigQuery charges for other operations, including using
BigQuery Omni
,
BigQuery ML
,
BI Engine
, and streaming
reads
and
writes
.
In addition, BigQuery has
free operations
and a
free usage tier
.
Every project that you create has a billing account attached to it. Any charges incurred by BigQuery jobs run in the project are billed to the attached billing account. BigQuery storage charges are also billed to the attached billing account. You can view BigQuery costs and trends by using the Cloud Billing reports page in the Google Cloud console.
Key Point:
Pricing models apply to accounts, not individual projects, unless otherwise specified.
Compute pricing models
BigQuery offers a choice of two compute pricing models for running queries:
On-demand pricing
(per TiB). With this pricing model, you are charged for the number of bytes processed by each query. The first 1 TiB of query data processed per month is free.
Capacity pricing
(per slot-hour). With this pricing model, you are charged for compute capacity used to run queries, measured in slots (virtual CPUs) over time. This model takes advantage of
BigQuery editions
. You can use the BigQuery autoscaler or purchase slot commitments, which are dedicated capacity that is always available for your workloads, at a lower price.
For more information about which pricing to choose for your workloads, see
Workload management using Reservations
.
Gemini in BigQuery pricing
See
Gemini in BigQuery Pricing Overview
for information about pricing for Gemini in BigQuery.
On-demand compute pricing
By default, queries are billed using the on-demand (per TiB) pricing model, where you pay for the data scanned by your queries.
With on-demand pricing, you will generally have access to up to 2,000 concurrent slots, shared among all queries in a single project. Periodically, BigQuery will temporarily burst beyond this limit to accelerate smaller queries.

## Vector Search

*Source: [https://cloud.google.com/bigquery/docs/vector-search-intro](https://cloud.google.com/bigquery/docs/vector-search-intro)*

Send feedback


Stay organized with collections

Save and categorize content based on your preferences.


# Introduction to embeddings and vector search

This document provides an overview of embeddings and vector search in
BigQuery. Vector search is a technique to compare similar objects using embeddings, and it
is used to power Google products, including Google Search,
YouTube, and Google Play. You can use vector search to perform
searches at scale. When you use [vector indexes](/bigquery/docs/vector-index)
with vector search, you can take advantage of foundational technologies like
inverted file indexing (IVF) and the
[ScaNN algorithm](https://research.google/blog/announcing-scann-efficient-vector-similarity-search/).

Vector search is built on embeddings. Embeddings are high-dimensional numerical
vectors that represent a given entity, like a piece of text or an audio file.
Machine learning (ML) models use embeddings to encode semantics about such
entities to make it easier to reason about and compare them. For example, a
common operation in clustering, classification, and recommendation models is to
measure the distance between vectors in an
[embedding space](https://en.wikipedia.org/wiki/Latent_space) to find items
that are most semantically similar.

This concept of semantic similarity and distance in an embedding space is
visually demonstrated when you consider how different items might be plotted.
For example, terms like *cat*, *dog*, and *lion*, which all represent types of
animals, are grouped close together in this space due to their shared semantic
characteristics. Similarly, terms like *car*, *truck*, and the more generic term
*vehicle* would form another cluster. This is shown in the following image:

You can see that the animal and vehicle clusters are positioned far apart
from each other.
