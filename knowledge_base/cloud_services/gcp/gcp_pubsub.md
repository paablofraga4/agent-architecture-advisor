# Service: Pub/Sub

**Provider:** gcp
**Document type:** service_reference
**Category:** messaging
**Tags:** messaging, event_driven, streaming
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://cloud.google.com/pubsub/docs/overview)
- [quotas](https://cloud.google.com/pubsub/quotas)
- [pricing](https://cloud.google.com/pubsub/pricing)

## Overview

Send feedback

# What is Pub/Sub? Stay organized with collections Save and categorize content based on your preferences.


Pub/Sub is an asynchronous and scalable messaging service that decouples
services producing messages from services processing those messages.

Pub/Sub allows services to communicate asynchronously, with
latencies typically on the order of 100 milliseconds.

Pub/Sub is used for streaming analytics and data integration
pipelines to load and distribute data. It's equally effective as a
messaging-oriented middleware for service integration or as a queue to parallelize tasks.

Pub/Sub lets you create systems of event producers and consumers,
called **publishers** and **subscribers**. Publishers communicate with
subscribers asynchronously by broadcasting events, rather than by
synchronous remote procedure calls (RPCs).

Publishers send events to the Pub/Sub service, without regard to
how or when these events are to be processed. Pub/Sub then
delivers events to all the services that react to them. In systems communicating
through RPCs, publishers must wait for subscribers to receive the data. However,
the asynchronous integration in Pub/Sub increases the flexibility
and robustness of the overall system.

To get started with Pub/Sub, check out the
[Quickstart using Google Cloud console](/pubsub/docs/create-topic-console).
For a more comprehensive introduction, see
[Building a Pub/Sub messaging system](/pubsub/docs/quickstart-py-mac).

## Common use cases

* **Ingesting user interaction and server events.** To use user
  interaction events from end-user apps or server events from your system,
  you might forward them to Pub/Sub. You can then use a
  stream processing tool, such as Dataflow, which delivers
  the events to databases. Examples of such databases are
  BigQuery, Bigtable, and Cloud Storage.
  Pub/Sub lets you gather events from many clients
  simultaneously.
* **Real-time event distribution.** Events, raw or processed, may
  be made available to multiple applications across your team and organization
  for real- time processing. Pub/Sub supports an "enterprise
  event bus" and event-driven application design patterns.
  Pub/Sub lets you integrate with many systems that export
  events to Pub/Sub.
* **Replicating data among databases.** Pub/Sub
  is commonly used to distribute change events from databases.

## Key Features

# What is Pub/Sub? Stay organized with collections Save and categorize content based on your preferences.


Pub/Sub is an asynchronous and scalable messaging service that decouples
services producing messages from services processing those messages.

Pub/Sub allows services to communicate asynchronously, with
latencies typically on the order of 100 milliseconds.

Pub/Sub is used for streaming analytics and data integration
pipelines to load and distribute data. It's equally effective as a
messaging-oriented middleware for service integration or as a queue to parallelize tasks.

Pub/Sub lets you create systems of event producers and consumers,
called **publishers** and **subscribers**. Publishers communicate with
subscribers asynchronously by broadcasting events, rather than by
synchronous remote procedure calls (RPCs).

Publishers send events to the Pub/Sub service, without regard to
how or when these events are to be processed. Pub/Sub then
delivers events to all the services that react to them. In systems communicating
through RPCs, publishers must wait for subscribers to receive the data. However,
the asynchronous integration in Pub/Sub increases the flexibility
and robustness of the overall system.

To get started with Pub/Sub, check out the
[Quickstart using Google Cloud console](/pubsub/docs/create-topic-console).
For a more comprehensive introduction, see
[Building a Pub/Sub messaging system](/pubsub/docs/quickstart-py-mac).

## Common use cases

* **Ingesting user interaction and server events.** To use user
  interaction events from end-user apps or server events from your system,
  you might forward them to Pub/Sub. You can then use a
  stream processing tool, such as Dataflow, which delivers
  the events to databases. Examples of such databases are
  BigQuery, Bigtable, and Cloud Storage.
  Pub/Sub lets you gather events from many clients
  simultaneously.
* **Real-time event distribution.** Events, raw or processed, may
  be made available to multiple applications across your team and organization
  for real- time processing. Pub/Sub supports an "enterprise
  event bus" and event-driven application design patterns.
  Pub/Sub lets you integrate with many systems that export
  events to Pub/Sub.
* **Replicating data among databases.** Pub/Sub
  is commonly used to distribute change events from databases. These events
  can be used to construct a view of the database state and state history in
  BigQuery and other data storage systems.
* **Parallel processing and workflows.** You can efficiently
  distribute many tasks among multiple workers by using Pub/Sub
  messages to communicate with the workers.

## Limits and Quotas

*Source: [https://cloud.google.com/pubsub/quotas](https://cloud.google.com/pubsub/quotas)*

Send feedback

# Pub/Sub quotas and limits Stay organized with collections Save and categorize content based on your preferences.


Google Cloud uses quotas to restrict how much of a particular shared Google Cloud resource that you can use. Each quota represents a specific
countable resource, such as API calls to a particular service, the number of
bytes sent to a particular service, or the number of streaming connections used
concurrently by your project.

Many services also have limits that are unrelated to the quota system. These are
fixed constraints, such as maximum message sizes or the number of Pub/Sub resources you can create in a project, which cannot be
increased or decreased.

## View and manage quotas

For a given project, you can use the
[IAM & admin quotas dashboard](https://console.cloud.google.com/iam-admin/quotas?project=_&service=pubsub.googleapis.com)
to view current quota limits and usage. You can also use this dashboard to do the following:

* Reduce your quota limits
* Initiate a process to apply for higher quota limits

For more information about monitoring and alerting on your quota usage, see
[Monitoring](/pubsub/docs/monitoring#quota).

## Quota usage attribution

For push subscriber throughput, quota usage is charged against the project that
contains the push subscription. This is the project that appears in the name of
the subscription.

For all other quotas, usage is charged against the project associated with the
credentials specified in the request. The quota usage is not charged against
the project that contains the requested resource.

For example: If a service account in project A sends a publish request to
publish to a topic in project B, the quota is charged to project A.
In some cases, you might want quota usage to be charged against another
project. You can use the `X-Goog-User-Project` system parameter to
change the project for quota attribution. For more information about `X-Goog-User-Project`,
see [System parameters](/apis/docs/system-parameters#definitions).

You can use gcloud CLI to set the project for quota attribution
for a specific request. The gcloud CLI sends
the `X-Goog-User-Project` request header.

You must have the `roles/serviceusage.serviceUsageConsumer` role
or a custom role with the `serviceusage.services.use` permission on the project
that you are going to use for quota attribution.

The following example shows how to get a list of subscriptions in the project
RESOURCE\_PROJECT while charging the *Administrator
operations* quota against the project QUOTA\_PROJECT. Run
the following command in your Google Cloud CLI terminal:

```
gcloud pubsub subscriptions list --project=
RESOURCE_PROJECT --billing-project=
QUOTA_PROJECT
```

Replace `QUOTA_PROJECT` with the ID of the Google Cloud project against which you want to charge quota.

Note that in Pub/Sub, the billed project is always the one that
contains the resource.

## Pricing

*Source: [https://cloud.google.com/pubsub/pricing](https://cloud.google.com/pubsub/pricing)*

Page Contents
Pub/Sub pricing
The cost of Pub/Sub has three components:
Throughput costs for message publishing and delivery
Data transfer costs associated with throughput that crosses a Google Cloud zone or region boundary
Storage costs associated with retaining messages
Pub/Sub
service charges are based on usage (the number of published, delivered, or stored bytes).
Pub/Sub Lite
throughput and storage charges, by contrast, are based on reserved capacity.
Data transfer charges for both services are based on usage, rather than reserved capacity.
Prerequisites
This document requires that you understand the architecture of Pub/Sub or Pub/Sub Lite and the common terms that are part of each product. For more information, see
Pub/Sub architecture
.
Pricing examples
The following table compares the monthly cost of Pub/Sub and Pub/Sub Lite systems for sample loads in North America. This example assumes a 24-hour message storage period, a 50% resource utilization for Pub/Sub Lite, and a pull or push subscription type for Pub/Sub. Other types of subscriptions might have additional costs.
Publish throughput in MiBps
Number of subscriptions
Zonal Lite topic (USD)
Regional Lite topic (USD)
Pub/Sub (USD)
10
1
$169
$608
$2,000
10
2
$214
$788
$3,000
100
1
$1,688
$6,075
$19,760
100
2
$2,138
$7,875
$29,640
When you compare the cost of Pub/Sub and Pub/Sub Lite, consider the differences in features between the two products. For more information, see
Choosing Pub/Sub or Pub/Sub Lite
.
Pub/Sub service pricing
The pricing details in this section apply only to Pub/Sub and not Pub/Sub Lite. This section includes the following topics:
Throughput costs
Storage costs
Single message transforms costs
Data transfer costs
Cross-project Pub/Sub billing
Filtered messages costs
Throughput costs
Throughput is the total number of bytes written (publish throughput) to a Pub/Sub topic or read (subscribe throughput) from a subscription to a topic over an interval of time.
Every calendar month, the first 10 GiB of throughput identified as the
Message Delivery Basic
SKU for a billing account is free. After that, the price is
$40 per TiB
in all Google Cloud regions. However, if you are using an import topic or an export subscription, read the next sections.
Throughput costs for BigQuery subscriptions
BigQuery subscriptions cost
$50 per TiB
in all Google Cloud regions for reading (subscribe throughput) from a subscription and writing to BigQuery. There are no additional BigQuery data ingestion charges. However, other types of BigQuery charges such as storage and data extraction apply. For more information, see
BigQuery pricing
. The first 10 GiB of BigQuery subscription throughput is not free.
Throughput costs for Cloud Storage subscriptions
Cloud Storage subscriptions cost
$50 per TiB
in all Google Cloud regions for reading (subscribe throughput) from a subscription and writing to Cloud Storage.
