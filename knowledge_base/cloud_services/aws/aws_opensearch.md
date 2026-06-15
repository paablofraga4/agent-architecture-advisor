# Service: Amazon OpenSearch Service

**Provider:** aws
**Document type:** service_reference
**Category:** search
**Tags:** search, vector, hybrid, analytics, logs
**Last updated:** 2026-06-10
**Sources:**
- [overview](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html)
- [limits](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html)
- [pricing](https://aws.amazon.com/opensearch-service/pricing/)

## Overview

# What is Amazon OpenSearch Service?

Amazon OpenSearch Service is a managed service that makes it easy to deploy, operate, and scale
OpenSearch clusters in the AWS Cloud. An OpenSearch Service domain is synonymous with an OpenSearch cluster. Domains are clusters with the settings, instance types, instance counts, and storage resources that you specify. Amazon OpenSearch Service supports OpenSearch and legacy
Elasticsearch OSS (up to 7.10, the final open source version of the software). When you
create a domain, you have the option of which search engine to use.

***OpenSearch*** is a
fully open-source search and analytics engine for use cases such as log analytics, real-time
application monitoring, and clickstream analysis. For more information, see the [OpenSearch documentation](https://opensearch.org/docs/).

***Amazon OpenSearch Service*** provisions
all the resources for your OpenSearch cluster and launches it. It also automatically
detects and replaces failed OpenSearch Service nodes, reducing the overhead associated with self-managed
infrastructures. You can scale your cluster with a single API call or a few clicks in the
console.

To get started using OpenSearch Service, you create an OpenSearch Service *domain*,
which is equivalent to an OpenSearch *cluster*. Each EC2 instance in
the cluster acts as one OpenSearch Service node.

You can use the OpenSearch Service console to set up and configure a domain in minutes.

## Key Features

# What is Amazon OpenSearch Service?

Amazon OpenSearch Service is a managed service that makes it easy to deploy, operate, and scale
OpenSearch clusters in the AWS Cloud. An OpenSearch Service domain is synonymous with an OpenSearch cluster. Domains are clusters with the settings, instance types, instance counts, and storage resources that you specify. Amazon OpenSearch Service supports OpenSearch and legacy
Elasticsearch OSS (up to 7.10, the final open source version of the software). When you
create a domain, you have the option of which search engine to use.

***OpenSearch*** is a
fully open-source search and analytics engine for use cases such as log analytics, real-time
application monitoring, and clickstream analysis. For more information, see the [OpenSearch documentation](https://opensearch.org/docs/).

***Amazon OpenSearch Service*** provisions
all the resources for your OpenSearch cluster and launches it. It also automatically
detects and replaces failed OpenSearch Service nodes, reducing the overhead associated with self-managed
infrastructures. You can scale your cluster with a single API call or a few clicks in the
console.

To get started using OpenSearch Service, you create an OpenSearch Service *domain*,
which is equivalent to an OpenSearch *cluster*. Each EC2 instance in
the cluster acts as one OpenSearch Service node.

You can use the OpenSearch Service console to set up and configure a domain in minutes. If you prefer
programmatic access, you can use the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/), the [AWS SDKs](http://aws.amazon.com/code), or [Terraform](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/opensearch_domain).

## Features of Amazon OpenSearch Service

OpenSearch Service includes the following features:

**Scale**

* Numerous configurations of CPU, memory, and storage capacity known as
  *instance types*, including cost-effective Graviton
  instances
* Supports up to 1002 data nodes
* Up to 25 PB of attached storage
* Cost-effective [UltraWarm](./ultrawarm.html) and [cold storage](./cold-storage.html) for read-only data

**Security**

* AWS Identity and Access Management (IAM) access control
* Easy integration with Amazon VPC and VPC security groups
* Encryption of data at rest and node-to-node encryption
* Amazon Cognito, HTTP basic, or SAML authentication for OpenSearch Dashboards
* Index-level, document-level, and field-level security
* Audit logs
* Dashboards multi-tenancy

**Stability**

* Numerous geographical locations for your resources, known as
  *Regions* and *Availability
  Zones*
* Node allocation across two or three Availability Zones in the same AWS
  Region, known as *Multi-AZ*
* Dedicated master nodes to offload cluster management tasks
* Automated snapshots to back up and restore OpenSearch Service domains

**Flexibility**

* SQL support for integration with business intelligence (BI)
  applications
* Custom packages to improve search results


## Limits and Quotas

*Source: [https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html)*

# Amazon OpenSearch Service quotas

Your AWS account has default quotas, formerly referred to as limits, for each AWS
service. Unless otherwise noted, each quota is Region-specific.

To view the quotas for OpenSearch Service domains and instances, Amazon OpenSearch Serverless, and Amazon OpenSearch Ingestion,
see [Amazon OpenSearch Service
quotas](https://docs.aws.amazon.com/general/latest/gr/opensearch-service.html#opensearch-limits) in the *AWS General Reference*.

To view the quotas for OpenSearch Service in the AWS Management Console, open the [Service Quotas console](https://console.aws.amazon.com/servicequotas/home). In the navigation pane, choose
**AWS services** and select **Amazon OpenSearch
Service**. To request a quota increase, see [Requesting a quota
increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html) in the *Service Quotas User Guide*.

###### Note

If you enable egress through your VPC on a VPC domain, reserve additional IP
addresses in each selected subnet for the egress network interfaces that OpenSearch Service creates
in your VPC. For more information, see [Limits and considerations](./vpc-egress.html#vpc-egress-limits).

## Warm node storage quotas

The following table lists the warm node instance types and the maximum amount of storage that each type can use. For OpenSearch Optimized OI2 instances, 80% of the local storage is available as cache, and the maximum addressable warm storage is 5 times the cache storage size.

For example, if an OI2 instance has 468 GB of local storage:

* Cache storage = 375 GB (80% of local storage)
* Maximum addressable warm storage = 1875 GB (5 x 375 GB cache)

| Instance Type | Instance Storage (GB) | Cache Size (GB) | Max Addressable Warm Storage (GB) |
| --- | --- | --- | --- |
| oi2.large.search | 468 | 375 | 1875 |
| oi2.xlarge.search | 937 | 750 | 3750 |
| oi2.2xlarge.search | 1875 | 1500 | 7500 |
| oi2.4xlarge.search | 3750 | 3000 | 15000 |
| oi2.8xlarge.search | 7500 | 6000 | 30000 |

### UltraWarm storage quotas

The following table lists the UltraWarm instance types and the maximum amount of
storage that each type can use. For more information about UltraWarm, see [UltraWarm storage for Amazon OpenSearch Service](./ultrawarm.html).

| Instance type | Maximum storage |
| --- | --- |
| ultrawarm1.medium.search | 1.5 TiB |
| ultrawarm1.large.search | 20 TiB |

## Number of data nodes per AZ

The following table lists the total number of data nodes for AZ deployment is below,
the overall limit signifies the number of data nodes per limit including both the hot
and warm node count.

## Pricing

*Source: [https://aws.amazon.com/opensearch-service/pricing/](https://aws.amazon.com/opensearch-service/pricing/)*

Amazon OpenSearch Service

* [Overview](/opensearch-service/)
* Features
* [Pricing](/opensearch-service/pricing/)
* Getting Started
* Resources
* More

# Amazon OpenSearch Service Pricing

[Request a pricing quote](/contact-us/sales-support/?pg=opensearchprice&cta=herobtn)

## Why Amazon OpenSearch Service?


With Amazon OpenSearch Service, you pay only for what you use with no minimum fee or usage requirement. Amazon OpenSearch Service offers two deployment models:

* For Managed Clusters, you are charged for instance hours, storage, and data transfer. Pricing depends on the instance type and storage tier you choose. For instances, you can use on-demand or Reserved Instance pricing, or save with Database Savings Plans.
* For Serverless, you are charged for compute and storage separately. Compute capacity is measured in OpenSearch Compute Units (OCUs), which correspond to the CPU, memory, and I/O resources required to index data or run queries. Serverless is also covered by Database Savings Plans.

Database Savings Plans applies to both deployment models and offer savings in exchange for a usage commitment (measured in $/hour) over a 1-year term. For more information, see the [Database Savings Plans pricing page](/savingsplans/database-pricing/).


## AWS Pricing Calculator


Calculate your Amazon OpenSearch Service and architecture cost in a single estimate.

[Create your custom estimate now](https://calculator.aws/#/createCalculator/OpenSearchService)


## On-Demand Instance pricing

Except as otherwise noted, our prices are exclusive of applicable taxes and duties, including VAT and applicable sales tax. For customers with a Japanese billing address, use of AWS is subject to Japanese Consumption Tax. [Learn more](/c-tax-faqs/).

## Reserved Instance pricing

With Amazon OpenSearch Service Reserved Instances, you can reserve instances for a one- or three-year term and realize significant savings on usage costs compared to On-Demand instances. Functionally, On-Demand and Reserved Instances are identical. From a billing perspective, however, Reserved Instances can provide significant cost savings.


Reserved Instances have three payment options:

* No Upfront Reserved Instances (NURI) – NURIs offer significant savings compared to On-Demand Instance pricing. You pay nothing upfront, but you commit to pay for the Reserved Instances over the course of a one- or three-year term. One-year NURIs offer a 31% discount and three-year NURIs offer a 48% discount. For T3.medium, one-year NURIs offer a 18% discount and three-year NURIs offer a 28% discount.

* Partial Upfront Reserved Instances (PURI) – PURIs offer higher savings than NURIs. This option requires you to pay a portion of the total cost upfront and pay the remainder of the cost on an hourly basis over the course of the term. One-year PURIs offer a 33% discount and three-year PURIs offer a 50% discount.
