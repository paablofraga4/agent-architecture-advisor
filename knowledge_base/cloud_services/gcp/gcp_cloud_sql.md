# Service: Cloud SQL

**Provider:** gcp
**Document type:** service_reference
**Category:** database
**Tags:** sql, postgresql, mysql, relational
**Last updated:** 2026-06-10
**Sources:**
- [overview](https://cloud.google.com/sql/docs/introduction)
- [quotas](https://cloud.google.com/sql/docs/quotas)
- [pricing](https://cloud.google.com/sql/pricing)

## Overview

Send feedback

# Cloud SQL overview Stay organized with collections Save and categorize content based on your preferences.


Cloud SQL is a fully managed relational database service for MySQL,
PostgreSQL, and SQL Server. This frees you from database administration tasks so
that you have more time to manage your data.

This page discusses basic concepts and terminology for Cloud SQL, which
provides SQL data storage for Google Cloud. For a more in-depth
explanation of key concepts, see the [key terms](/sql/docs/key-terms)
and [features](/sql/docs/features) pages. For information about how
Cloud SQL databases compare with one another, see
[Cloud SQL feature support by database
engine](/sql/docs/feature_support).

## Use cases for Cloud SQL

Cloud SQL provides a cloud-based alternative to local MySQL, PostgreSQL,
and SQL Server databases. You should use Cloud SQL if you want to spend
less time managing your database and more time using it.

Many applications running on Compute Engine, App Engine and other
services in Google Cloud use Cloud SQL for database storage.

## What Cloud SQL provides

Cloud SQL offers many services so you don't have to build and maintain
them yourself. You can focus on your data and let Cloud SQL handle the
following operations:

* [Backups](/sql/docs/mysql/backup-recovery/backups)
* [High availability and failover](/sql/docs/mysql/high-availability)
* [Network connectivity](/sql/docs/mysql/connect-overview)
* [Export and import](/sql/docs/mysql/import-export)
* [Maintenance and updates](/sql/docs/mysql/maintenance)
* [Monitoring](/sql/docs/mysql/monitor-instance)
* [Logging](/sql/docs/mysql/logging)

## What is a Cloud SQL instance?

Each Cloud SQL instance is powered by a virtual machine (VM) running on a
host Google Cloud server. Each VM operates the database program, such as
MySQL Server, PostgreSQL, or SQL Server, and service agents that provide
supporting services, such as logging and monitoring. The high
availability option also provides a standby VM in another zone with a
configuration that's identical to the primary VM.

The database is stored on a scalable, durable network storage device called a
`persistent disk` that attaches to the VM.

## Key Features

## What is a Cloud SQL instance?

Each Cloud SQL instance is powered by a virtual machine (VM) running on a
host Google Cloud server. Each VM operates the database program, such as
MySQL Server, PostgreSQL, or SQL Server, and service agents that provide
supporting services, such as logging and monitoring. The high
availability option also provides a standby VM in another zone with a
configuration that's identical to the primary VM.

The database is stored on a scalable, durable network storage device called a
`persistent disk` that attaches to the VM. A static IP address sits in front
of each VM to help make sure that the IP address an application connects to
persists throughout the lifetime of the Cloud SQL instance.

Cloud SQL instance overview:

## Limits and Quotas

*Source: [https://cloud.google.com/sql/docs/quotas](https://cloud.google.com/sql/docs/quotas)*

Send feedback

# Quotas and limits Stay organized with collections Save and categorize content based on your preferences.


This page provides information about the Cloud SQL quotas and limits.
Quotas are applied per-project; limits are applied to the instance or to the
project, depending on the limit.

## Quotas

A *quota* restricts how much of a Google Cloud resource your Google Cloud project can use. Cloud SQL is an example of this type of resource.

For Cloud SQL, quotas are part of a system that do the following:

* Monitor your use or consumption of Cloud SQL instances
* Restrict your consumption of these instances for reasons including ensuring fairness and reducing spikes in usage
* Maintain configurations that enforce prescribed restrictions automatically
* Provide a means to make or request changes to the quota

When a quota is exceeded, in most cases, the system blocks access to the relevant instance immediately, and the task that you're trying to perform fails. Quotas apply to each Google Cloud project and are shared across all instances that use that project.

### Permissions to check and increase your quotas

To check and increase your quotas, you need the following permissions:

* `serviceusage.quotas.get:` check your quotas
* `serviceusage.quotas.update:` increase your quotas

By default, these permissions are included in the [basic IAM roles](/iam/docs/roles-overview#basic) of Editor and Owner and in the
predefined [Quota Administrator](/iam/docs/roles-permissions/servicemanagement) role. If you need additional permissions, then contact your quota administrator.

### Check your quotas

To check the current quotas for resources in your project, go to
the [Quotas](https://console.cloud.google.com/iam-admin/quotas) page in the
Google Cloud console and filter for **Cloud SQL Admin API**. These quotas apply only to
API calls; they don't include database queries.

### Increase your quotas

As your use of Google Cloud expands over time, your quotas can increase
accordingly. If you expect a notable upcoming increase in usage, then
make your request a few days in advance to ensure your quotas are adequately
sized.

There's no charge for requesting a quota increase. Your costs
increase only if you use more resources.

To increase your quotas, follow these steps:

1. In the Google Cloud console, go to the **Quotas** page.

   [Go to the Quotas page](https://console.cloud.google.com/iam-admin/quotas)
2. Filter for the **Cloud SQL Admin API** service.

   If you don't see this service, then [enable the Cloud SQL Admin API](/sql/docs/mysql/admin-api#enable_the_api).
3. Select the checkboxes next to the quotas that you want to change, and then click **Edit quotas**.
4. For each quota that you selected, in the **New limit** field, enter the
   value for the desired limit.
5. In the **Reason description** field, enter a reason for your request of a
   quota increase, and then click **Done**.
6. Click **Next**.
7.

## Pricing

*Source: [https://cloud.google.com/sql/pricing](https://cloud.google.com/sql/pricing)*

Page Contents
Cloud SQL pricing
You can create an account to evaluate how Cloud SQL performs in real-world scenarios. New customers also get $300 in free credits to spend on Cloud SQL to run, test, and deploy workloads. You won't be charged until you upgrade.
Sign up to
try Cloud SQL for free
.
This page contains information about pricing for Cloud SQL.
Cloud SQL offers
two editions
, Enterprise and Enterprise Plus. These editions provide different levels of availability, performance and data protection. The pricing for the vCPUs and memory for each edition varies. Cloud SQL Enterprise edition and Cloud SQL Enterprise Plus edition are supported by Cloud SQL for MySQL, Cloud SQL for PostgreSQL, and Cloud SQL for SQL Server.
Pricing for Cloud SQL depends on your instance type:
MySQL and PostgreSQL
SQL Server
MySQL and PostgreSQL pricing
Cloud SQL pricing is composed of the following charges:
CPU and memory pricing
Storage and networking pricing
Instance pricing
Cloud DNS pricing
Extended support pricing
CPU and memory pricing
For dedicated-core instances, you choose the number of CPUs and the amount of memory you want, up to 96 CPUs and 624 GiB of memory for Enterprise edition and up to 128 CPUs and 864 GiB of memory for Enterprise Plus edition. For Cloud SQL Enterprise Plus edition for SQL Server instances, you can also choose from performance-optimized machines (up to 128 CPUs and 864 GiB of memory) and memory-optimized machines (up to 16 CPUs and 512 GiB of memory). Pricing for CPUs and memory depends on the region where your instance is located. Select your region in the dropdown on the pricing table.
Read replicas and failover replicas are charged at the same rate as stand-alone instances.
HA
prices are applied for instances configured for high availability, also called regional instances.
Learn more about high availability
.
Cloud SQL also offers committed use discounts (CUDs) that provide deeply discounted prices in exchange for your commitment to continuously use database instances in a particular region for a one- or three-year term. In the pricing tables on this page, the prices for CUDs are listed as commitments.
