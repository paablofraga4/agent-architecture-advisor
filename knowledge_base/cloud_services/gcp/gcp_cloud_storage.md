# Service: Cloud Storage

**Provider:** gcp
**Document type:** service_reference
**Category:** storage
**Tags:** object_storage, documents, data_lake
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://cloud.google.com/storage/docs/introduction)
- [quotas](https://cloud.google.com/storage/quotas)
- [pricing](https://cloud.google.com/storage/pricing)

## Overview

Send feedback

# Cloud Storage overview Stay organized with collections Save and categorize content based on your preferences.


This page describes Cloud Storage and how it works.

## How Cloud Storage works

Cloud Storage is a scalable and managed storage service offered by
Google Cloud that lets you store data as *objects* in containers called
*buckets*.

All buckets are associated with a *project*, and you group your
projects under an *organization*. After you create a project, you can
[create buckets](/storage/docs/creating-buckets), [upload objects](/storage/docs/uploading-objects) to your buckets, and
[download objects](/storage/docs/downloading-objects) from your buckets. You can also grant permissions to make
your data accessible to principals you specify or
[accessible to everyone on the public internet](/storage/docs/access-control/making-data-public). Directory capabilities
let you utilize Cloud Storage more similarly to a hard
drive or Network Attached Storage (NAS): folders let you organize objects
in a directory structure, and managed folders let you simplify
access control to your objects.

Each project, bucket, object, folder, and managed folder is a *resource* in
Google Cloud, as are things such as [Compute Engine instances](/compute/docs/instances).

## The Google Cloud hierarchy

Here's how the Cloud Storage structure can apply to a real-world case:

* [Organization](/resource-manager/docs/cloud-platform-resource-hierarchy#organizations): Your company, called Example Inc., creates a Google Cloud
  organization called `exampleinc.org`.
* [Project](/storage/docs/projects): Example Inc. is building several applications, and each one is
  associated with a project. Each project has its own set of
  Cloud Storage APIs, as well as other resources.
* [Bucket](/storage/docs/buckets): Each project can contain multiple buckets, which are
  containers to store your objects. For example, you might create a `photos`
  bucket for all the image files your app generates and a separate `videos`
  bucket. Cloud Storage offers different [storage classes](/storage/docs/storage-classes)
  and [locations](/storage/docs/locations) for your buckets, letting you choose the durability and
  availability of your data to suit the needs of your workloads.

  Buckets serve as a primary data foundation in the broader Google Cloud
  ecosystem.

## Limits and Quotas

*Source: [https://cloud.google.com/storage/quotas](https://cloud.google.com/storage/quotas)*

Send feedback

# Quotas & limits Stay organized with collections Save and categorize content based on your preferences.


This page describes quotas and request limits for Cloud Storage. You
can request increases to quotas, but limits cannot be adjusted.

Quotas and limits are subject to change.

## Buckets

| Limit | Value | Notes |
| --- | --- | --- |
| Maximum [bucket name](/storage/docs/buckets#naming) size | 63 characters | If the name contains a dot (.), the limit is 222 characters. |
| Maximum bucket creation and deletion rate per project | Approximately one request every two seconds | Plan on fewer buckets and more objects in most cases. For example, a common design choice is to use one bucket per user of your project. However, if you're designing a system that adds many users per second, then design for many users in one bucket (with appropriate [permissions](/storage/docs/access-control/iam)) so that the bucket creation rate limit doesn't become a bottleneck.  Highly available applications shouldn't depend on bucket creation, deletion, or list operations in the critical path of their application. Bucket names are part of a centralized and global namespace: any dependency on this namespace creates a single point of failure for your application. If a location is temporarily unavailable, the bucket list operation might return only a partial list of buckets. Due to these considerations and the bucket creation/deletion limit, the recommended practice for highly available services on Cloud Storage is to pre-create all the buckets necessary. |
| Maximum bytes of data that can be stored across all the zonal buckets per project, per zone  This limit only applies to buckets that use [Rapid Bucket](/storage/docs/rapid/rapid-bucket). | 1 TB default limit, but might be lower or higher based on your project's billing account history | For more information about zonal buckets, see [Rapid Bucket](/storage/docs/rapid/rapid-bucket). |
| Maximum [bucket restoration](/storage/docs/use-soft-deleted-buckets) rate per project | Approximately one request every two seconds |  |
| Maximum rate of bucket metadata updates per bucket | One update per second | Rapid updates to a single bucket (for example, changing the CORS configuration) might result in throttling errors. |
| Maximum number of principals that can be granted IAM roles per bucket | 1,500 principals for all IAM roles  100 principals for [legacy IAM roles](/storage/docs/access-control/iam#acls) | See [Principal types](/storage/docs/access-control/iam#identities) for more information. |
| Maximum number of [Pub/Sub notification configurations](/storage/docs/pubsub-notifications) per bucket | 100 notification configurations |  |
| Maximum number of concurrent bucket relocations supported from the same location within a project | 5 buckets | See [Bucket relocation](/storage/docs/bucket-relocation/overview) for more information.

## Pricing

*Source: [https://cloud.google.com/storage/pricing](https://cloud.google.com/storage/pricing)*

Page Contents
Cloud Storage pricing
This document discusses pricing for Cloud Storage. For Google Drive, which offers simple online storage for your personal files, see
Google Drive pricing
.
If you pay in a currency other than USD, the prices listed in your currency on
Cloud Platform SKUs
apply.
Overview
Cloud Storage pricing is based on the following components:
Data storage
: the amount of data stored in your buckets. Storage rates vary depending on the storage class of your data and location of your buckets.
Data processing
: the processing done by Cloud Storage, which includes operations charges, any applicable retrieval fees, and inter-region replication.
Network usage
: the amount of data read from or moved between your buckets.
Rapid Cache
: On-demand accelerated read cache for your buckets.
Rapid Bucket
: High performance object storage in a zonal bucket.
Pricing tables
The pricing tables below show what charges apply when using Cloud Storage.
For example scenarios that show usage and charges, see the
Pricing examples page
. For the Google Cloud pricing calculator, see the
Calculator page
.
Data storage
Click on a geographic area to view the at-rest costs for associated
locations
:
Region
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
Zurich (europe-west6)
Milan (europe-west8)
Paris (europe-west9)
Doha (me-central1)
Dammam (me-central2)
Tel Aviv (me-west1)
Montreal (northamerica-northeast1)
Toronto (northamerica-northeast2)
Mexico (northamerica-south1)
Sao Paulo (southamerica-east1)
Santiago (southamerica-west1)
Iowa (us-central1)
South Carolina (us-east1)
Northern Virginia (us-east4)
Columbus (us-east5)
Alabama (us-east7)
Dallas (us-south1)
Oregon (us-west1)
Los Angeles (us-west2)
Salt Lake City (us-west3)
Las Vegas (us-west4)
Phoenix (us-west8)
Hourly
Hourly
Monthly
Monthly
Standard storage
Nearline storage
Coldline storage
Archive storage
Rapid Cache storage
$0.000027397 / 1 gibibyte hour, per 1 month / account
$0.000013699 / 1 gibibyte hour
$0.000005479 / 1 gibibyte hour
$0.000001644 / 1 gibibyte hour
$0.0001233 / 1 gibibyte hour
If you pay in a currency other than USD, the prices listed in your currency on
Cloud Platform SKUs
apply.
Dual-region
Iowa (us-central1)
Taiwan (asia-east1)
Mumbai (asia-south1)
Delhi (asia-south2)
Singapore (asia-southeast1)
Asia 1 (asia1)
Sydney (australia-southeast1)
Melbourne (australia-southeast2)
Europe 4 (eur4)
Europe 5 (eur5)
Europe 7 (eur7)
Europe 8 (eur8)
