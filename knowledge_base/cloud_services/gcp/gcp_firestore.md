# Service: Firestore

**Provider:** gcp
**Document type:** service_reference
**Category:** database
**Tags:** nosql, document, realtime, serverless
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://cloud.google.com/firestore/docs/overview)
- [limits](https://cloud.google.com/firestore/quotas)
- [pricing](https://cloud.google.com/firestore/pricing)

## Overview

Page Contents
Google named a Leader in the 2025 Gartner® Magic Quadrant™ for Cloud Database Management Systems.
Learn more.
Firestore
Enterprise-grade document database with MongoDB compatibility
Build AI, web, and mobile applications with a fully managed, serverless document database that provides virtually unlimited scalability and industry-leading availability.
Try Firestore free
Deploy a dynamic website
New customers get $300 in free credits to spend on Firestore. All customers get 50,000 reads, 20,000 writes, 20,000 deletes, and 1 GB storage free per day, not charged against your credits.
Product highlights
Firestore with MongoDB compatibility
Serverless with up to 99.999% availability SLA
Single-digit milliseconds, read latency performance
Firestore in a minute video
1:49
Features
MongoDB compatibility
Use a familiar MongoDB wire-compatible API on Firestore's serverless database service. You can now use your existing MongoDB application code, drivers, and integrations, in addition to the open-source ecosystem of MongoDB integrations, to quickly build applications for common use cases.
Learn more
.
Real-time synchronization
Develop rich applications utilizing advanced pipeline query capabilities, including full-text search, geospatial, and robust offline data handling. Built-in real-time sync facilitates offline-first or collaborative app development for mobile, web, and wearables. Power workloads in media, gaming, content management, messaging, location-based services, retail, hospitality, and business apps.
Learn more
.
Serverless
Focus on your application development using a fully managed, serverless document database that effortlessly scales up or down to meet any demand, with no manual sharding, maintenance windows, or administrative downtime. Enjoy multi-region replication with strong consistency, ACID-compliant multi-document transactions and virtually unlimited scalability without worrying about managing the underlying database infrastructure.
Gen AI ready
Turn simple text prompts into live, Firestore-backed applications in seconds with our
Google AI Studio
integration. Use
remote MCP
support to securely connect your favorite AI agents and developer tools directly to Firestore. Easily build generative AI applications with Firestore
vector search
,
LangChain
, and
LlamaIndex
integrations.

## Limits and Quotas

*Source: [https://cloud.google.com/firestore/quotas](https://cloud.google.com/firestore/quotas)*

Send feedback


Stay organized with collections

Save and categorize content based on your preferences.


# Quotas and limits

This page identifies the request quotas and limits for Firestore.

## Free Tier usage

Firestore offers a free tier that lets you get started with
Firestore at no cost. The free tier amounts are listed in the following
table.

Free tier amounts are applied daily and reset at midnight Pacific time.

The free tier applies to only one Firestore database per project.
The first database that is created in a project without a free tier database
will get the free tier. If the database with the free tier applied is deleted,
the next database created will receive the free tier.

### Standard edition

| Free tier | Quota |
| --- | --- |
| Stored data | 1 GiB |
| Document reads | 50,000 per day |
| Document writes | 20,000 per day |
| Document deletes | 20,000 per day |
| Outbound data transfer | 10 GiB per month |

### Enterprise edition

| Free tier | Quota |
| --- | --- |
| Stored data | 1 GiB |
| Read units | 50,000 per day |
| Real-time update units | 50,000 per day |
| Write units | 40,000 per day |
| Outbound data transfer | 10 GiB per month |

The following operations and features don't include free usage.
You must [enable billing](/billing/docs/how-to/modify-project) to use these features:

* Managed deletes (TTL)
* PITR data
* Backup data
* Restore operations
* Clone operations

## Limits

The following tables show the limits that apply to
Firestore. These are hard limits unless otherwise noted.

### Databases

### Standard edition

| Limit | Details |
| --- | --- |
| Maximum number of databases per project | 100  You can [contact support](/support-hub) to request an increase to this limit. |
| Maximum number of [customer-managed encryption keys (CMEK) databases](/firestore/docs/cmek) per project | 0  By default the quota is 0 because this feature is behind an allowlist. You can request to increase the quota by filling in [the CMEK access request form](https://docs.google.com/forms/d/e/1FAIpQLSfKs8wJf4IXu1NizvfyU2vT59JDbdPvkehMVZ2ab5l_aDLIIA/viewform?resourcekey=0-O15dlRFvA0JIDmh6VFUEcA). |

### Enterprise edition

| Limit | Details |
| --- | --- |
| Maximum number of databases per project | 100  You can [contact support](/support-hub) to request an increase to this limit. |
| Maximum number of [customer-managed encryption keys (CMEK) databases](/firestore/docs/cmek) per project | 0  By default the quota is 0 because this feature is behind an allowlist. You can request to increase the quota by filling in [the CMEK access request form](https://docs.google.com/forms/d/e/1FAIpQLSfKs8wJf4IXu1NizvfyU2vT59JDbdPvkehMVZ2ab5l_aDLIIA/viewform?resourcekey=0-O15dlRFvA0JIDmh6VFUEcA).

## Pricing

*Source: [https://cloud.google.com/firestore/pricing](https://cloud.google.com/firestore/pricing)*

Page Contents
Firestore pricing
This document explains pricing details for Firestore Standard edition. For Enterprise edition pricing, see
Firestore Enterprise edition pricing
.
If you pay in a currency other than USD, the prices listed in your currency on
Cloud Platform SKUs
apply.
16:23
Pricing overview
When you use Firestore, you are charged for the following:
The number of documents you read, write, and delete
.
The number of index entries read to satisfy a query
.
See more details about index reads
.
The amount of storage that your database uses
, including overhead for metadata and indexes.
The amount of network bandwidth that you use
.
Storage and bandwidth usage are calculated in gibibytes (GiB), where 1 GiB = 2
30
bytes. All charges accrue daily.
The following sections provide details about how you are charged for your Firestore usage.
Free quota
Firestore offers free quota that lets you get started at no cost. The free quota amounts are listed below. If you need more quota, you must
enable billing for your Google Cloud project
.
Quotas are applied daily and reset around midnight Pacific time.
Firestore allows exactly one free database per project.
Free tier
Quota
Stored data
1 GiB
Document reads
50,000 per day
Document writes
20,000 per day
Document deletes
20,000 per day
Outbound data transfer
10 GiB per month
The following operations and features do not include free usage. You must enable billing to use these features:
TTL deletes
PITR data
Backup data
Restore operations
Clone operations
For more information about how these features are billed, see
Storage pricing
.
Pricing by location
The following table lists pricing for reads, writes, deletes, and storage for each Firestore location:
Iowa (us-central1)
Johannesburg (africa-south1)
Taiwan (asia-east1)
Hong Kong (asia-east2)
Tokyo (asia-northeast1)
Osaka (asia-northeast2)
Seoul (asia-northeast3)
Mumbai (asia-south1)
Delhi (asia-south2)
Singapore (asia-southeast1)
Jakarta (asia-southeast2)
Bangkok (asia-southeast3)
Sydney (australia-southeast1)
Melbourne (australia-southeast2)
Europe 3 (eur3)
Warsaw (europe-central2)
Finland (europe-north1)
Stockholm (europe-north2)
Madrid (europe-southwest1)
Belgium (europe-west1)
Berlin (europe-west10)
Turin (europe-west12)
London (europe-west2)
Frankfurt (europe-west3)
Netherlands (europe-west4)
Galaxy Frankfurt (europe-west5)
Zurich (europe-west6)
Milan (europe-west8)
Paris (europe-west9)
Doha (me-central1)
Dammam (me-central2)
Tel Aviv (me-west1)
North America 5 (nam5)
North America 7 (nam7)
Montreal (northamerica-northeast1)
Toronto (northamerica-northeast2)
Mexico (northamerica-south1)
Sao Paulo (southamerica-east1)
Santiago (southamerica-west1)
Iowa (us-central1)
South Carolina (us-east1)
Northern Virginia (us-east4)
Columbus (us-east5)
Dallas (us-south1)
Oregon (us-west1)
Los Angeles (us-west2)
Salt Lake City (us-west3)
Las Vegas (us-west4)
Phoenix (us-west8)
Show discount options
Hourly
Hourly
Monthly
Monthly
Free quota per day
Default
*
