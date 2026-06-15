# Service: Amazon DynamoDB

**Provider:** aws
**Document type:** service_reference
**Category:** database
**Tags:** nosql, key_value, serverless
**Last updated:** 2026-06-10
**Sources:**
- [overview](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [limits](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html)
- [pricing](https://aws.amazon.com/dynamodb/pricing/)

## Overview

# What is Amazon DynamoDB?

Amazon DynamoDB is a serverless, fully managed, distributed NoSQL database with single-digit millisecond performance at any scale.

DynamoDB addresses your needs to overcome scaling and operational complexities of relational
databases. DynamoDB is purpose-built and optimized for operational workloads that require
consistent performance at any scale. For example, DynamoDB delivers consistent single-digit
millisecond performance for a shopping cart use case, whether you have 10 or 100 million
users. [Launched in 2012](https://press.aboutamazon.com/2012/1/amazon-web-services-launches-amazon-dynamodb-a-new-nosql-database-service-designed-for-the-scale-of-the-internet), DynamoDB continues to help you move away from relational
databases while reducing cost and improving performance at scale.

Customers across all sizes, industries, and geographies use DynamoDB to build modern, serverless applications that can start small and scale globally. DynamoDB scales to support tables of virtually any size while
providing consistent single-digit millisecond performance and high availability.

For events, such as [Amazon Prime Day](https://aws.amazon.com/blogs/aws/prime-day-2023-powered-by-aws-all-the-numbers/), DynamoDB
powers multiple high-traffic Amazon properties and systems, including [Alexa](https://alexa.com/), [Amazon.com](https://www.amazon.com/) sites, and all [Amazon fulfillment
centers](https://www.aboutamazon.com/workplace/facilities). For such events, DynamoDB APIs have handled trillions of calls from Amazon
properties and systems. DynamoDB continuously serves hundreds of customers with tables that
have peak traffic of over half a million requests per second. It also serves hundreds of
customers whose table sizes exceed 200 TB, and processes over one billion requests per hour.

###### Topics

* [Characteristics of DynamoDB](#ddb-characteristics)
* [DynamoDB use cases](#ddb-use-cases)
* [Capabilities of DynamoDB](#ddb-capabilities)
* [Service integrations](#ddb-service-integrations)
* [Security](#ddb-intro-security)
* [Resilience](#ddb-intro-resilience)
* [Accessing DynamoDB](#ddb-access)
* [DynamoDB pricing](#ddb-pricing)
* [Getting started with DynamoDB](#ddb-intro-get-started)

## Characteristics of DynamoDB

### Serverless

With DynamoDB, you don't need to provision any servers, or patch, manage, install,
maintain, or operate any software. DynamoDB provides zero downtime maintenance.

## Key Features

# What is Amazon DynamoDB?

Amazon DynamoDB is a serverless, fully managed, distributed NoSQL database with single-digit millisecond performance at any scale.

DynamoDB addresses your needs to overcome scaling and operational complexities of relational
databases. DynamoDB is purpose-built and optimized for operational workloads that require
consistent performance at any scale. For example, DynamoDB delivers consistent single-digit
millisecond performance for a shopping cart use case, whether you have 10 or 100 million
users. [Launched in 2012](https://press.aboutamazon.com/2012/1/amazon-web-services-launches-amazon-dynamodb-a-new-nosql-database-service-designed-for-the-scale-of-the-internet), DynamoDB continues to help you move away from relational
databases while reducing cost and improving performance at scale.

Customers across all sizes, industries, and geographies use DynamoDB to build modern, serverless applications that can start small and scale globally. DynamoDB scales to support tables of virtually any size while
providing consistent single-digit millisecond performance and high availability.

For events, such as [Amazon Prime Day](https://aws.amazon.com/blogs/aws/prime-day-2023-powered-by-aws-all-the-numbers/), DynamoDB
powers multiple high-traffic Amazon properties and systems, including [Alexa](https://alexa.com/), [Amazon.com](https://www.amazon.com/) sites, and all [Amazon fulfillment
centers](https://www.aboutamazon.com/workplace/facilities). For such events, DynamoDB APIs have handled trillions of calls from Amazon
properties and systems. DynamoDB continuously serves hundreds of customers with tables that
have peak traffic of over half a million requests per second. It also serves hundreds of
customers whose table sizes exceed 200 TB, and processes over one billion requests per hour.

###### Topics

* [Characteristics of DynamoDB](#ddb-characteristics)
* [DynamoDB use cases](#ddb-use-cases)
* [Capabilities of DynamoDB](#ddb-capabilities)
* [Service integrations](#ddb-service-integrations)
* [Security](#ddb-intro-security)
* [Resilience](#ddb-intro-resilience)
* [Accessing DynamoDB](#ddb-access)
* [DynamoDB pricing](#ddb-pricing)
* [Getting started with DynamoDB](#ddb-intro-get-started)

## Characteristics of DynamoDB

### Serverless

With DynamoDB, you don't need to provision any servers, or patch, manage, install,
maintain, or operate any software. DynamoDB provides zero downtime maintenance. It has
no versions (major, minor, or patch), and there are no maintenance windows.

DynamoDB's [on-demand capacity mode](./on-demand-capacity-mode.html)
offers pay-as-you-go pricing for read and write requests so you only pay for what
you use. With on-demand, DynamoDB instantly scales up or down your tables to adjust for
capacity and maintains performance with zero administration.

## Limits and Quotas

*Source: [https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html)*

# Quotas in Amazon DynamoDB

This section describes current quotas, formerly referred to as limits, within Amazon DynamoDB.
Each quota applies on a per-Region basis unless otherwise specified.

###### Note

All size measurements in DynamoDB use binary-based units. DynamoDB denotes 1 KB = 1024 bytes, 1 MB = 1024 KB, 1 GB = 1024 MB, 1 TB = 1024 GB.

###### Topics

* [Read/write throughput](#default-limits-throughput-capacity-modes)
* [Reserved Capacity](#reserved-capacity)
* [Tables](#limits-tables)
* [Global tables](#gt-limits-throughput)
* [Secondary indexes](#limits-secondary-indexes)
* [Projected secondary index attributes](#projected-secondary-index-attributes)
* [DynamoDB Streams](#limits-dynamodb-streams)
* [Import from Amazon S3](#import-limits)
* [Table export to Amazon S3](#limits-table-export)
* [Backup and restore](#limits-backup-restore)
* [Contributor Insights](#contributor-insights-quotas)

## Read/write throughput

### Throughput default quotas

AWS places some default quotas on the throughput that your
account can provision and consume within a Region.

The account-level read throughput and account-level write
throughput quotas apply at the account level. These account-level quotas apply to
the sum of the provisioned throughput capacity for all your accountâs tables and
global secondary indexes in a given Region. All the account's available throughput
can be provisioned for a single table or across multiple tables. These quotas only
apply to tables using the provisioned capacity mode.

The table-level read throughput and table-level write throughput
quotas apply differently to tables that use the provisioned capacity mode, and
tables that use the on-demand capacity mode.

For provisioned capacity mode tables and GSIs, the quota is the
maximum amount of read and write capacity units that can be provisioned for any
table or any of its GSIs in the Region. The total of any individual table and all
its GSIs must also remain below the account-level read and write throughput quota.
This is in addition to the requirement that the total of all provisioned tables and
their GSIs must remain below the account-level read and write throughput quota.

For on-demand capacity mode tables and GSIs, the table-level
quota is the maximum read and write capacity units that are available for any table,
or any individual GSI within that table. No account-level read and write throughput
quotas are applied to tables in on-demand mode.

Following are the throughput quotas that apply on your account,
by default.

###### Note

All capacity unit and request unit quotas are measured per second. For
example, a quota of 40,000 read capacity units means 40,000 reads per
second.

###### Note

You can request any number of read capacity units (RCU) or write capacity
units (WCU) for your DynamoDB tables through a service quota increase. The values
listed in the following table represent the initial default quotas.

## Pricing

*Source: [https://aws.amazon.com/dynamodb/pricing/](https://aws.amazon.com/dynamodb/pricing/)*

# Amazon DynamoDB pricing

[Try DynamoDB Free Tier](https://console.aws.amazon.com/dynamodbv2)

[Contact sales support](/contact-us/sales-support/?refid=ft_dynamodb)

Amazon DynamoDB

* [Overview](/dynamodb/)
* Features
* [Pricing](/dynamodb/pricing/)
* [Resources](/dynamodb/resources/)
* [FAQs](/dynamodb/faqs/)
* More

DynamoDB charges for reading, writing, and storing data in tables, along with any optional features you choose to enable.

With two pricing options (on-demand and provisioned) for reads and writes and two pricing options for storage (Standard and Standard - Infrequent Access), you can choose the best pricing option for your workload. Learn more about the different modes and storage classes in the [DynamoDB developer guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/).

* On-demand capacity
* Provisioned capacity

* On-demand capacity
* DynamoDB on-demand mode is a serverless option with pay-per-request pricing and automatic scaling, without the need to plan, provision, or manage capacity. You are billed per read or write request consumed, making it easy to balance costs and performance.

  On-demand mode is recommended in most scenarios including if you:

  + Have new or existing workloads and you do not want to manage capacity
  + Want a serverless database that automatically scales
  + Prefer the ease of paying for only what you use
* Provisioned capacity
* With provisioned capacity, you must specify the number of reads and writes per second you want to provision for your application. You’ll be charged based on the hourly read and write capacity provisioned, and not how much your application has consumed.

  Provisioned capacity may be better if you:

  + Have existing applications with steady and predictable throughput patterns
  + Can forecast capacity requirements

  #### Reserved provisioned capacity

  With DynamoDB reserved provisioned capacity, you can reduce costs of provisioned capacity by committing to a specified level of read and write capacity for a defined period. Reserved provisioned capacity is best suited for workloads with predictable, steady throughput requirements where long-term usage commitments can provide significant savings.

For more information regarding on-demand and provisioned capacity modes, see "How throughput pricing works".

DynamoDB optional features

For billing related questions, see [FAQs](https://aws.amazon.com/dynamodb/faqs/#billing--1pu7u62). For assistance, [request AWS Sales Support](/contact-us/sales-support/?refid=ft_dynamodb) or use the **Ask AWS** chatbot at the bottom of this page and type "Contact AWS Rep".

\* Cold backup storage is supported for on-demand backups that are managed by AWS Backup only.
