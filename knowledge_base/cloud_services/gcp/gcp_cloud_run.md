# Service: Cloud Run

**Provider:** gcp
**Document type:** service_reference
**Category:** compute
**Tags:** containers, serverless, deployment
**Last updated:** 2026-06-10
**Sources:**
- [overview](https://cloud.google.com/run/docs/overview/what-is-cloud-run)
- [limits](https://cloud.google.com/run/quotas)
- [pricing](https://cloud.google.com/run/pricing)

## Overview

Send feedback

# What is Cloud Run Stay organized with collections Save and categorize content based on your preferences.


Cloud Run is a fully managed application platform for running your code,
function, or container on top of Google's highly scalable infrastructure.

You can deploy code written in any programming language on Cloud Run if
you can build a container image from it. In fact, building container images is
optional. If you're using Go, Node.js, Python, Java, .NET, Ruby, or a
supported framework you can use the
[source-based deployment](/run/docs/deploying-source-code) option that builds
the container for you, using the best practices for the language you're using.

Google has built Cloud Run to work well together with other services
on Google Cloud, so you can build full-featured applications.

In short, Cloud Run lets developers spend their time writing their
code, and very little time operating, configuring, and scaling their
Cloud Run service. You don't have to create a cluster or manage
infrastructure to be productive with Cloud Run.

## Services, jobs, and worker pools: three ways to run your code

On Cloud Run, your code can run as a
*service*,
*job*, or *worker pool*. All of these resource types are running sandboxed
container instances in the same execution environment and can integrate with
Google Cloud services.

The following table provides a high-level look at the options provided by each
Cloud Run resource type.

| Resource | Description |
| --- | --- |
| Service | Responds to HTTP requests sent to a unique and stable endpoint, using stateless instances that autoscale based on a variety of key metrics, also responds to events and functions. |
| Job | Executes parallelizable tasks that are executed manually, or on a schedule, and run to completion. |
| Worker pool | Handles always-on background workloads such as pull-based workloads, for example, Kafka consumers, Pub/Sub pull queues, or RabbitMQ consumers. |

## Cloud Run services

A Cloud Run service provides you with the infrastructure required to run a reliable HTTPS endpoint.

## Key Features

# What is Cloud Run Stay organized with collections Save and categorize content based on your preferences.


Cloud Run is a fully managed application platform for running your code,
function, or container on top of Google's highly scalable infrastructure.

You can deploy code written in any programming language on Cloud Run if
you can build a container image from it. In fact, building container images is
optional. If you're using Go, Node.js, Python, Java, .NET, Ruby, or a
supported framework you can use the
[source-based deployment](/run/docs/deploying-source-code) option that builds
the container for you, using the best practices for the language you're using.

Google has built Cloud Run to work well together with other services
on Google Cloud, so you can build full-featured applications.

In short, Cloud Run lets developers spend their time writing their
code, and very little time operating, configuring, and scaling their
Cloud Run service. You don't have to create a cluster or manage
infrastructure to be productive with Cloud Run.

## Services, jobs, and worker pools: three ways to run your code

On Cloud Run, your code can run as a
*service*,
*job*, or *worker pool*. All of these resource types are running sandboxed
container instances in the same execution environment and can integrate with
Google Cloud services.

The following table provides a high-level look at the options provided by each
Cloud Run resource type.

| Resource | Description |
| --- | --- |
| Service | Responds to HTTP requests sent to a unique and stable endpoint, using stateless instances that autoscale based on a variety of key metrics, also responds to events and functions. |
| Job | Executes parallelizable tasks that are executed manually, or on a schedule, and run to completion. |
| Worker pool | Handles always-on background workloads such as pull-based workloads, for example, Kafka consumers, Pub/Sub pull queues, or RabbitMQ consumers. |

## Cloud Run services

A Cloud Run service provides you with the infrastructure required to run a reliable HTTPS endpoint. Your responsibility is to make sure your code listens on a TCP port and handles HTTP requests.

The following diagram shows a Cloud Run service running several container instances to handle web requests and events from the client using an HTTPS endpoint.

A standard service includes the following features:

Unique HTTPS endpoint for every service
:   Every Cloud Run service [has an HTTPS endpoint](/run/docs/triggering/https-request) on a unique subdomain of the `*.run.app` domain – and you can configure custom domains as well.

## Limits and Quotas

*Source: [https://cloud.google.com/run/quotas](https://cloud.google.com/run/quotas)*

Send feedback

# Cloud Run Quotas and Limits Stay organized with collections Save and categorize content based on your preferences.


This page contains usage quota and limits that apply when using
Cloud Run.

The number of Cloud Run [resources](/run/docs/resource-model) is limited.
Quotas for Cloud Run encompass API rate limits, which affect
the rate at which you can call the [Cloud Run Admin API](/run/docs/reference/rest).

There is no direct limit for the following:

* The size of container images you can deploy.
* The number of concurrent requests that are served by a
  [Cloud Run service](/run/docs/resource-model#services).

## Resource limits for Cloud Run

To go beyond limits that can be increased, [request a quota increase](/run/quotas#increase).
To go beyond per project limits that cannot be increased, create new resources in a different Google Cloud project or region.

| Resource | Description | Limit | Scope | Can be increased |
| --- | --- | --- | --- | --- |
| Service | Maximum number of services | 1000 | per project and region | Yes |
| Job | Maximum number of jobs | 1000 | per project and region | Yes |
| Worker pool | Maximum number of worker pools | 1000 | per project and region | Yes |
| Job execution | Maximum number of running job executions | 1000 | per project and region | Yes |
| Revision | Number of revisions after which any non-addressable revisions are automatically deleted in historical order | 1000 | per service | No |
| Revision | Maximum number of revisions serving traffic | 4000 | per project and region | Yes |
| Revision tag | Maximum number of [revision tags](/run/docs/rollouts-rollbacks-traffic-migration#tags). When the revision tag limit is exceeded, Cloud Run executes tag cleanup on the service. For the service for which a new tag is being created, tags that don't have a specified traffic percentage are automatically deleted in historical order. | 2000 | per project and region | Yes |
| Job execution | Retention limit for completed job executions. When the number of completed executions for a job reaches this limit, executions are automatically deleted in historical order | 1,000 | per job | No |
| Job execution task1 | Maximum number of [tasks running in parallel](/run/docs/configuring/parallelism#limit) | Depends on selected region and [CPU](/run/docs/configuring/jobs/cpu) and [memory](/run/docs/configuring/jobs/memory-limits) configurations. This limit might be greater in high-capacity regions or lower in recently opened regions. You can view your quota in the [Quotas and system limits](https://console.cloud.google.com/iam-admin/quotas) console page.

## Pricing

*Source: [https://cloud.google.com/run/pricing](https://cloud.google.com/run/pricing)*

Page Contents
Cloud Run pricing
Cloud Run charges you only for the resources you use, rounded up to the nearest 100 millisecond. Your total Cloud Run bill will be the sum of the resource usage in the pricing table after the free tier is applied.
When setting
concurrency
higher than one request at a time, multiple requests can share the allocated CPU and memory of an instance.
Outbound internet data transfer uses the
Premium Network Service Tier
and is charged at
Google Cloud networking pricing
with a free tier of 1GiB free data transfer within North America per month.
Data transfer to Virtual Private Cloud networks is billed as Data transfer from a VM and charged at
Virtual Private Cloud data transfer rates
. Serverless VPC Access connectors also charge for the compute required to run them. See
Serverless VPC Access pricing
.
There is no charge for data transfer to Google Cloud resources in the same region (for example for traffic from one Cloud Run service to another Cloud Run service). There is no charge for data transfer to
Media CDN
,
Cloud CDN
and
Cloud Load Balancing
.
Pricing considerations
When evaluating the pricing of Cloud Run, consider the following:
On-demand and pay per use
: Cloud Run provides on-demand capacity and automatically scales instances. Cloud Run does not require pre-provisioning infrastructure to accommodate for anticipated peak usage. Container instances billed by Cloud Run are used container instances.
Total cost of ownership
: While Cloud Run charges for compute costs, Cloud Run provides more value. For example, Cloud Run offers
zonal redundancy
, requires low operations because
Site Reliability Engineers
do a lot in the background, makes you and your team more productive via its simplicity.
Committed use discounts
: The cost of any continuous use of Cloud Run can be lowered by purchasing
Committed use discounts
. For example, if your Cloud Run service always has one or more active instances, you can lower its cost by committing to at least this amount. Compute flexible committed use discounts apply across GKE, Compute Engine and Cloud Run.
Read more about
cost optimization
.
Pricing calculator
You can use the
Google Cloud pricing calculator
to estimate the cost of using Cloud Run.
Pricing tables
The following pricing tables use the
GiB-second
unit. A GiB-second means for example running a 1 gibibyte instance for 1 second, or running a 256 mebibyte instance for 4 seconds. The same principle applies for the
vCPU-second
unit. CUD refers to
committed use discounts
.
The free tier usage is aggregated across
projects
by
billing account
and resets every month; you are billed only for usage past the free tier. The free tier is applied as a spending based discount using Tier 1 pricing.
Cloud Run pricing depends on the
selected region
.
