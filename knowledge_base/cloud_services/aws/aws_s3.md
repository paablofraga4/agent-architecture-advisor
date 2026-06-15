# Service: Amazon S3

**Provider:** aws
**Document type:** service_reference
**Category:** storage
**Tags:** object_storage, documents, data_lake
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [limits](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html)
- [pricing](https://aws.amazon.com/s3/pricing/)

## Overview

# What is Amazon S3?

Amazon Simple Storage Service (Amazon S3) is an object storage service that offers industry-leading scalability,
data availability, security, and performance. Customers of all sizes and industries can use
Amazon S3 to store and protect any amount of data for a range of use cases, such as data lakes,
websites, mobile applications, backup and restore, archive, enterprise applications, IoT
devices, and big data analytics. Amazon S3 provides management features so that you can optimize,
organize, and configure access to your data to meet your specific business, organizational,
and compliance requirements.

###### Note

For more information about using the Amazon S3 Express One Zone storage class with directory buckets, see [S3 Express One Zone](./directory-bucket-high-performance.html#s3-express-one-zone) and [Working with directory buckets](./directory-buckets-overview.html).

###### Topics

* [Features of Amazon S3](#S3Features)
* [How Amazon S3 works](#CoreConcepts)
* [Amazon S3 data consistency model](#ConsistencyModel)
* [Related services](#RelatedAmazonWebServices)
* [Accessing Amazon S3](#API)
* [Paying for Amazon S3](#PayingforStorage)
* [PCI DSS compliance](#pci-dss-compliance)

## Features of Amazon S3

### Storage classes

Amazon S3 offers a range of storage classes designed for different use cases. For
example, you can store mission-critical production data in S3 Standard or S3 Express One Zone for frequent
access, save costs by storing infrequently accessed data in S3 Standard-IA or
S3 One Zone-IA, and archive data at the lowest costs in S3 Glacier Instant Retrieval,
S3 Glacier Flexible Retrieval, and S3 Glacier Deep Archive.

Amazon S3 Express One Zone is a high-performance, single-zone Amazon S3 storage class that is purpose-built
to deliver consistent, single-digit millisecond data access for your most
latency-sensitive applications. S3 Express One Zone is the lowest latency cloud object
storage class available today, with data access
speeds
up to 10x faster and with request costs
50
percent lower than S3 Standard. S3 Express One Zone is the first S3 storage class where you can select a single Availability Zone with
the option to co-locate your object storage with your compute resources, which provides the highest possible access speed.
Additionally, to further increase access speed and support hundreds of thousands of
requests per second, data is stored in a new bucket type: an
Amazon S3 directory bucket.

## Key Features

# What is Amazon S3?

Amazon Simple Storage Service (Amazon S3) is an object storage service that offers industry-leading scalability,
data availability, security, and performance. Customers of all sizes and industries can use
Amazon S3 to store and protect any amount of data for a range of use cases, such as data lakes,
websites, mobile applications, backup and restore, archive, enterprise applications, IoT
devices, and big data analytics. Amazon S3 provides management features so that you can optimize,
organize, and configure access to your data to meet your specific business, organizational,
and compliance requirements.

###### Note

For more information about using the Amazon S3 Express One Zone storage class with directory buckets, see [S3 Express One Zone](./directory-bucket-high-performance.html#s3-express-one-zone) and [Working with directory buckets](./directory-buckets-overview.html).

###### Topics

* [Features of Amazon S3](#S3Features)
* [How Amazon S3 works](#CoreConcepts)
* [Amazon S3 data consistency model](#ConsistencyModel)
* [Related services](#RelatedAmazonWebServices)
* [Accessing Amazon S3](#API)
* [Paying for Amazon S3](#PayingforStorage)
* [PCI DSS compliance](#pci-dss-compliance)

## Features of Amazon S3

### Storage classes

Amazon S3 offers a range of storage classes designed for different use cases. For
example, you can store mission-critical production data in S3 Standard or S3 Express One Zone for frequent
access, save costs by storing infrequently accessed data in S3 Standard-IA or
S3 One Zone-IA, and archive data at the lowest costs in S3 Glacier Instant Retrieval,
S3 Glacier Flexible Retrieval, and S3 Glacier Deep Archive.

Amazon S3 Express One Zone is a high-performance, single-zone Amazon S3 storage class that is purpose-built
to deliver consistent, single-digit millisecond data access for your most
latency-sensitive applications. S3 Express One Zone is the lowest latency cloud object
storage class available today, with data access
speeds
up to 10x faster and with request costs
50
percent lower than S3 Standard. S3 Express One Zone is the first S3 storage class where you can select a single Availability Zone with
the option to co-locate your object storage with your compute resources, which provides the highest possible access speed.
Additionally, to further increase access speed and support hundreds of thousands of
requests per second, data is stored in a new bucket type: an
Amazon S3 directory bucket. For more information, see [S3 Express One Zone](./directory-bucket-high-performance.html#s3-express-one-zone) and [Working with directory buckets](./directory-buckets-overview.html).

You can store data with changing or unknown access patterns in
S3 Intelligent-Tiering, which optimizes storage costs by automatically moving your
data between four access tiers when your access patterns change.

## Limits and Quotas

*Source: [https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html)*

# Amazon S3 multipart upload limits

Multipart upload allows you to upload a single object as a set of parts. Each part is a
contiguous portion of the object's data. After all parts of your object are uploaded, Amazon S3
assembles these parts and creates the object. In general, when your object size reaches 100
MB, you should consider using multipart uploads instead of uploading the object in a single
operation. For more information about multipart uploads, see [Uploading and copying objects using multipart upload in Amazon S3](./mpuoverview.html).

The following table provides multipart upload core specifications. These include maximum
object size, maximum number of parts, maximum part size, and more. There is no minimum size
limit on the last part of your multipart upload.

| Item | Specification |
| --- | --- |
| Maximum object size | 48.8 TiB |
| Maximum number of parts per upload | 10,000 |
| Part numbers | 1 to 10,000 (inclusive) |
| Part size | 5 MiB to 5 GiB. There is no minimum size limit on the last part of your multipart upload. |
| Maximum number of parts returned for a list parts request | 1000 |
| Maximum number of multipart uploads returned in a list multipart uploads request | 1000 |

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Upload an object through multipart upload and
verify its data integrity

Making conditional requests

## Pricing

*Source: [https://aws.amazon.com/s3/pricing/](https://aws.amazon.com/s3/pricing/)*

Amazon S3

* [Overview](/s3/?nc=sn&loc=1)
* Features
* Storage classes
* [Pricing](/s3/pricing/?nc=sn&loc=4)
* [Security](/s3/security/?nc=sn&loc=5)
* More

# Amazon S3

Object storage built to retrieve any amount of data from anywhere

[Sign up](https://signin.aws.amazon.com/signup?request_type=register)

[Connect with a specialist](https://pages.awscloud.com/global-ln-gc-600-contact-us-interest.html?trk=f48b8823-f88e-482e-8331-ff2c7db318e1&sc_channel=el&refid=de3518c5-eb66-4ef5-ab94-ec69c34b86df)

Pay only for what you use. There is no minimum charge. Amazon S3 cost components are storage pricing, request and data retrieval pricing, data transfer and transfer acceleration pricing, data management and insights feature pricing, replication pricing, and transform and query feature pricing.

* Storage & requests
* Files
* Tables
* Vectors
* Data transfer
* Security & buckets
* Management & insights
* Replication
* Transform & query

* Storage & requests
* Storage pricing

  You pay for storing objects in your S3 buckets. The rate you’re charged depends on your objects' size, how long you stored the objects during the month, and the storage class—S3 Standard, S3 Intelligent-Tiering, S3 Standard-Infrequent Access, S3 One Zone-Infrequent Access, S3 Express One Zone, S3 Glacier Instant Retrieval, S3 Glacier Flexible Retrieval (Formerly S3 Glacier), and S3 Glacier Deep Archive. You pay a monthly monitoring and automation charge per object stored in the S3 Intelligent-Tiering storage class to monitor access patterns and move objects between access tiers. In S3 Intelligent-Tiering there are no retrieval charges, and no additional tiering charges apply when objects are moved between access tiers.

  There are per-request ingest charges when using PUT, COPY, or lifecycle rules to move data into any S3 storage class. Consider the ingest or transition cost before moving objects into any storage class. Estimate your costs using the [AWS Pricing Calculator](https://calculator.aws/). To find the best S3 storage class for your workload, learn more [here](/s3/storage-classes/).

  Please note that we list Storage Requests and Data Retrievals Pricing below the Storage Pricing table.

  \* S3 Intelligent-Tiering can store objects smaller than 128 KB, but auto-tiering has a minimum eligible object size of 128 KB. These smaller objects will not be monitored and will always be charged at the Frequent Access tier rates, with no monitoring and automation charge. For each object archived to the Archive Access tier or Deep Archive Access tier in S3 Intelligent-Tiering, Amazon S3 uses 8 KB of storage for the name of the object and other metadata (billed at S3 Standard storage rates) and 32 KB of storage for index and related metadata (billed at S3 Glacier Flexible Retrieval and S3 Glacier Deep Archive storage rates).

  \*\* S3 Standard-IA and S3 One Zone-IA storage have a minimum billable object size of 128 KB.
