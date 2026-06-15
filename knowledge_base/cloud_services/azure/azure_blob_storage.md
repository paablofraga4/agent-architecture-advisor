# Service: Azure Blob Storage

**Provider:** azure
**Document type:** service_reference
**Category:** storage
**Tags:** object_storage, documents, blobs
**Last updated:** 2026-06-10
**Sources:**
- [overview](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-overview)
- [limits](https://learn.microsoft.com/en-us/azure/storage/common/scalability-targets-standard-account)
- [pricing](https://azure.microsoft.com/en-us/pricing/details/storage/blobs/)

## Overview

Note


# What is Azure Blob storage?


Azure Blob Storage is Microsoft's object storage solution for the cloud. Blob Storage is optimized for storing massive amounts of unstructured data. Unstructured data is data that doesn't adhere to a particular data model or definition, such as text or binary data.

## About Blob Storage

Blob Storage is designed for:

* Serving images or documents directly to a browser.
* Storing files for distributed access.
* Streaming video and audio.
* Writing to log files.
* Storing data for backup and restore, disaster recovery, and archiving.
* Storing data for analysis by an on-premises or Azure-hosted service.

Users or client applications can access objects in Blob Storage via HTTP or HTTPS from anywhere in the world. You can access objects in Blob Storage through the [Azure Storage REST API](/en-us/rest/api/storageservices/blob-service-rest-api), [Azure PowerShell](/en-us/powershell/module/az.storage), [Azure CLI](/en-us/cli/azure/storage), or an Azure Storage client library. Client libraries are available for different languages, including:

* [.NET](/en-us/dotnet/api/overview/azure/storage)
* [Java](/en-us/java/api/overview/azure/storage)
* [Node.js](https://github.com/Azure/azure-sdk-for-js/tree/master/sdk/storage)
* [Python](storage-quickstart-blobs-python)
* [Go](https://github.com/Azure/azure-sdk-for-go/tree/main/sdk/storage/azblob)

Clients can also securely connect to Blob Storage by using SSH File Transfer Protocol (SFTP) and mount Blob Storage containers by using the Network File System (NFS) 3.0 protocol.

## About Azure Data Lake Storage Gen2

Blob Storage supports Azure Data Lake Storage Gen2, Microsoft's enterprise big data analytics solution for the cloud. Azure Data Lake Storage Gen2 offers a hierarchical file system as well as the advantages of Blob Storage, including:

* Low-cost, tiered storage
* High availability
* Strong consistency
* Disaster recovery capabilities

For more information about Data Lake Storage Gen2, see [Introduction to Azure Data Lake Storage Gen2](data-lake-storage-introduction).

## Next steps

* [Introduction to Azure Blob storage](storage-blobs-introduction)
* [Introduction to Azure Data Lake Storage](data-lake-storage-introduction)


## Additional resources

## Key Features

# What is Azure Blob storage?


Azure Blob Storage is Microsoft's object storage solution for the cloud. Blob Storage is optimized for storing massive amounts of unstructured data. Unstructured data is data that doesn't adhere to a particular data model or definition, such as text or binary data.

## About Blob Storage

Blob Storage is designed for:

* Serving images or documents directly to a browser.
* Storing files for distributed access.
* Streaming video and audio.
* Writing to log files.
* Storing data for backup and restore, disaster recovery, and archiving.
* Storing data for analysis by an on-premises or Azure-hosted service.

Users or client applications can access objects in Blob Storage via HTTP or HTTPS from anywhere in the world. You can access objects in Blob Storage through the [Azure Storage REST API](/en-us/rest/api/storageservices/blob-service-rest-api), [Azure PowerShell](/en-us/powershell/module/az.storage), [Azure CLI](/en-us/cli/azure/storage), or an Azure Storage client library. Client libraries are available for different languages, including:

* [.NET](/en-us/dotnet/api/overview/azure/storage)
* [Java](/en-us/java/api/overview/azure/storage)
* [Node.js](https://github.com/Azure/azure-sdk-for-js/tree/master/sdk/storage)
* [Python](storage-quickstart-blobs-python)
* [Go](https://github.com/Azure/azure-sdk-for-go/tree/main/sdk/storage/azblob)

Clients can also securely connect to Blob Storage by using SSH File Transfer Protocol (SFTP) and mount Blob Storage containers by using the Network File System (NFS) 3.0 protocol.

## About Azure Data Lake Storage Gen2

Blob Storage supports Azure Data Lake Storage Gen2, Microsoft's enterprise big data analytics solution for the cloud. Azure Data Lake Storage Gen2 offers a hierarchical file system as well as the advantages of Blob Storage, including:

* Low-cost, tiered storage
* High availability
* Strong consistency
* Disaster recovery capabilities

For more information about Data Lake Storage Gen2, see [Introduction to Azure Data Lake Storage Gen2](data-lake-storage-introduction).

## Next steps

* [Introduction to Azure Blob storage](storage-blobs-introduction)
* [Introduction to Azure Data Lake Storage](data-lake-storage-introduction)


## Additional resources

## Limits and Quotas

*Source: [https://learn.microsoft.com/en-us/azure/storage/common/scalability-targets-standard-account](https://learn.microsoft.com/en-us/azure/storage/common/scalability-targets-standard-account)*

Note


# Scalability and performance targets for standard storage accounts


This reference details scalability and performance targets for Azure Storage. The scalability and performance targets listed here are high-end targets, but they're achievable. In all cases, the request rate and bandwidth that your storage account achieves depend on the size of objects stored, the access patterns used, and the type of workload your application performs.

Test your service to determine whether its performance meets your requirements. If possible, avoid sudden spikes in the rate of traffic and ensure that traffic is well-distributed across partitions.

When your application reaches the limit of what a partition can handle for your workload, Azure Storage begins to return error code 503 (Server Busy) or error code 500 (Operation Timeout) responses. If 503 errors occur, consider modifying your application to use an exponential backoff policy for retries. The exponential backoff decreases the load on the partition and eases spikes in traffic to that partition.

The service-level agreement (SLA) for Azure Storage accounts is available at [SLA for Storage Accounts](https://azure.microsoft.com/support/legal/sla/storage/v1_5/).

## Scale targets for standard storage accounts and disk access resources

The following table describes default limits for Azure general-purpose v2 (GPv2), general-purpose v1 (GPv1), and Blob Storage accounts.

A few entries in the table also apply to disk access and are explicitly labeled. Disk access is a resource that is exclusively used for importing or exporting managed disks through [private links](/en-us/azure/virtual-machines/disks-restrict-import-export-overview#private-links).

Customers should use a GPv2 storage account, because [GPv1 is being retired](/en-us/azure/storage/common/general-purpose-version-1-account-migration-overview). You can easily upgrade a GPv1 or Blob Storage account to a GPv2 account with no downtime and no need to copy data. For more information, see [Upgrade to a GPv2 storage account](/en-us/azure/storage/common/storage-account-upgrade).

The *ingress* limit refers to all data sent to a storage account or disk access. The *egress* limit refers to all data received from a storage account or disk access.

Note

You can request higher capacity and ingress limits. To request an increase, contact [Azure Support](https://azure.microsoft.com/support/faq/).

| Resource | Limit |
| --- | --- |
| Maximum number of storage accounts with standard endpoints per region per subscription, including standard and premium storage accounts. | 250 by default, 500 by request1 |
| Maximum number of storage accounts with Azure DNS zone endpoints (preview) per region per subscription, including standard and premium storage accounts. | 5,000 (preview) |
| Default maximum storage account capacity.

## Pricing

*Source: [https://azure.microsoft.com/en-us/pricing/details/storage/blobs/](https://azure.microsoft.com/en-us/pricing/details/storage/blobs/)*

# Azure Blob Storage pricing

* [Request a pricing quote](/en-us/contact/pricing/)
* [Try Azure for free](/en-us/free/)

## Massively scalable and secure object storage

Block blob storage is used for streaming and storing documents, videos, pictures, backups, and other unstructured text or binary data.

Total cost of block blob storage depends on:

* Volume of data stored per month.
* Quantity and types of operations performed, along with any data transfer costs.
* Data redundancy option selected.

## Explore pricing options

Apply filters to customize pricing options to your needs.

Prices are estimates only and are not intended as actual price quotes. Actual pricing may vary depending on the type of agreement entered with Microsoft, date of purchase, and the currency exchange rate. Prices are calculated based on US dollars and converted using London closing spot rates that are captured in the two business days prior to the last business day of the previous month end. If the two business days prior to the end of the month fall on a bank holiday in major markets, the rate setting day is generally the day immediately preceding the two business days. This rate applies to all transactions during the upcoming month. Sign in to the [Azure pricing calculator](/en-us/pricing/calculator/) to see pricing based on your current program/offer with Microsoft. Contact an [Azure sales specialist](/en-us/contact/pricing/) for more information on pricing or to request a price quote. See [frequently asked questions](/en-us/pricing/) about Azure pricing.

File Structure

Hierarchical Namespace (NFS v3.0, SFTP Protocol)
Flat Namespace

Redundancy:

LRS
ZRS
GRS
RA GRS
GZRS
RA GZRS

Region:


Central US
East US
East US 2
North Central US
South Central US
West Central US
West US
West US 2
West US 3

UK South
UK West

UAE Central
UAE North

Switzerland North
Switzerland West

Sweden Central
Sweden South

Spain Central

Qatar Central

Poland Central

Norway East
Norway West

New Zealand North

Mexico Central

Malaysia West

Korea Central
Korea South

Japan East
Japan West

Italy North

Israel Central

Indonesia Central

Central India
South India
West India

Germany North
Germany West Central

France Central
France South

North Europe
West Europe

Denmark East

Chile Central

Canada Central
Canada East

Brazil South
Brazil Southeast

Belgium Central

US Gov Arizona
US Gov Texas
US Gov Virginia

Austria East

Australia Central
Australia Central 2
Australia East
Australia Southeast

East Asia
Southeast Asia

South Africa North
South Africa West

Currency:

United States – Dollar ($) USD
Australia – Dollar ($) AUD
Brazil – Real (R$) BRL
Canada – Dollar ($) CAD
Denmark – Krone (kr) DKK
Euro Zone – Euro (€) EUR
India – Rupee (₹) INR
Japan – Yen (¥) JPY
Korea – Won (₩) KRW
New Zealand – Dollar ($) NZD
Norway – Krone (kr) NOK
Russia – Ruble (руб) RUB
Sweden – Krona (kr) SEK
Switzerland – Franc (chf) CHF
Taiwan – Dollar (NT$) TWD
United Kingdom – Pound (£) GBP

