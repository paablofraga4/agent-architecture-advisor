# Service: Azure API Management

**Provider:** azure
**Document type:** service_reference
**Category:** networking
**Tags:** api_gateway, rate_limiting, authentication
**Last updated:** 2026-06-10
**Sources:**
- [overview](https://learn.microsoft.com/en-us/azure/api-management/api-management-key-concepts)
- [limits](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#api-management-limits)
- [pricing](https://azure.microsoft.com/en-us/pricing/details/api-management/)

## Overview

Note


# What is Azure API Management?


**APPLIES TO: All API Management tiers**

This article provides an overview of common scenarios and key components of Azure API Management. Azure API Management is a hybrid, multicloud management platform for APIs across all environments. As a platform-as-a-service, API Management supports the complete API lifecycle.

Tip

If you're already familiar with API Management and ready to start, see these resources:

* [Features and service tiers](api-management-features)
* [Create an API Management instance](get-started-create-service-instance)
* [Import and publish an API](import-and-publish)
* [API Management policies](api-management-howto-policies)

## Scenarios

APIs enable digital experiences, simplify application integration, underpin new digital products, and make data and services reusable and universally accessible. âWith the proliferation and increasing dependency on APIs, organizations need to manage them as first-class assets throughout their lifecycle.â

Azure API Management helps organizations meet these challenges:

* Provide a comprehensive API platform for different stakeholders and teams to produce and manage APIs
* Abstract backend architecture diversity and complexity from API consumers
* Securely expose services hosted on and outside of Azure as APIs
* Protect, accelerate, and observe APIs
* Enable API discovery and consumption by internal and external users

Common scenarios include:

* **Unlocking legacy assets** - APIs are used to abstract and modernize legacy backends and make them accessible from new cloud services and modern applications. APIs allow innovation without the risk, cost, and delays of migration.
* **API-centric app integration** - APIs are easily consumable, standards-based, and self-describing mechanisms for exposing and accessing data, applications, and processes. They simplify and reduce the cost of app integration.
* **Multi-channel user experiences** - APIs are frequently used to enable user experiences such as web, mobile, wearable, or Internet of Things applications. Reuse APIs to accelerate development and ROI.
* **B2B integration** - APIs exposed to partners and customers lower the barrier to integrate business processes and exchange data between business entities. APIs eliminate the overhead inherent in point-to-point integration.

## Key Features

# What is Azure API Management?


**APPLIES TO: All API Management tiers**

This article provides an overview of common scenarios and key components of Azure API Management. Azure API Management is a hybrid, multicloud management platform for APIs across all environments. As a platform-as-a-service, API Management supports the complete API lifecycle.

Tip

If you're already familiar with API Management and ready to start, see these resources:

* [Features and service tiers](api-management-features)
* [Create an API Management instance](get-started-create-service-instance)
* [Import and publish an API](import-and-publish)
* [API Management policies](api-management-howto-policies)

## Scenarios

APIs enable digital experiences, simplify application integration, underpin new digital products, and make data and services reusable and universally accessible. âWith the proliferation and increasing dependency on APIs, organizations need to manage them as first-class assets throughout their lifecycle.â

Azure API Management helps organizations meet these challenges:

* Provide a comprehensive API platform for different stakeholders and teams to produce and manage APIs
* Abstract backend architecture diversity and complexity from API consumers
* Securely expose services hosted on and outside of Azure as APIs
* Protect, accelerate, and observe APIs
* Enable API discovery and consumption by internal and external users

Common scenarios include:

* **Unlocking legacy assets** - APIs are used to abstract and modernize legacy backends and make them accessible from new cloud services and modern applications. APIs allow innovation without the risk, cost, and delays of migration.
* **API-centric app integration** - APIs are easily consumable, standards-based, and self-describing mechanisms for exposing and accessing data, applications, and processes. They simplify and reduce the cost of app integration.
* **Multi-channel user experiences** - APIs are frequently used to enable user experiences such as web, mobile, wearable, or Internet of Things applications. Reuse APIs to accelerate development and ROI.
* **B2B integration** - APIs exposed to partners and customers lower the barrier to integrate business processes and exchange data between business entities. APIs eliminate the overhead inherent in point-to-point integration. Especially with self-service discovery and onboarding enabled, APIs are the primary tools for scaling B2B integration.

Tip

Visit [aka.ms/apimlove](https://aka.ms/apimlove) for a library of useful resources, including videos, blogs, and customer stories about using Azure API Management.

## API Management components

Azure API Management is made up of an API *gateway*, a *management plane*, and a *developer portal*, with features designed for different audiences in the API ecosystem. These components are Azure-hosted and fully managed by default.

## Limits and Quotas

*Source: [https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#api-management-limits](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#api-management-limits)*

Note


# Azure subscription and service limits, quotas, and constraints


This document lists some of the most common Microsoft Azure limits, which are also sometimes called quotas.

* To learn more about Azure pricing, see the [Azure pricing](https://azure.microsoft.com/pricing/) overview and details page.
* The Azure pricing page provides details for specific services; for example, [Windows Virtual Machines](https://azure.microsoft.com/pricing/details/virtual-machines/Windows/).
* You can also use the Azure [pricing calculator](https://azure.microsoft.com/pricing/calculator/) to estimate your costs.
* See [What is Microsoft Billing?](../../cost-management-billing/cost-management-billing-overview) for tips to help manage your costs.

## How to manage limits

Note

Some services have adjustable limits.

When the limit can be adjusted, the tables include **Default limit** and **Maximum limit** headers. The limit can be raised above the default limit but not above the maximum limit. Some services with adjustable limits use different headers with information about adjusting the limit.

When a service doesn't have adjustable limits, the following tables use the header **Limit** without any additional information about adjusting the limit. In those cases, the default and the maximum limits are the same.

If you want to raise the limit or quota above the default limit, [open an online customer support request at no charge](../templates/error-resource-quota#solution).

The terms *soft limit* and *hard limit* are often used informally to describe the current, adjustable limit (soft limit) and the maximum limit (hard limit). If a limit isn't adjustable, there won't be a soft limit but only a hard limit.

[Free Azure trial subscriptions](https://azure.microsoft.com/pricing/offers/ms-azr-0044p?cid=msft_learn) aren't eligible for limit or quota increases. If you have this type of subscription, you can upgrade to a [Pay-as-you-go](https://azure.microsoft.com/pricing/offers/ms-azr-0003p?cid=msft_learn) one. For more information, see [Upgrade your Azure account](../../cost-management-billing/manage/upgrade-azure-subscription) and the overviews for [Try Azure for free or pay as you go](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

Some limits are managed at a regional level.

## Pricing

*Source: [https://azure.microsoft.com/en-us/pricing/details/api-management/](https://azure.microsoft.com/en-us/pricing/details/api-management/)*

# API Management pricing

* [Request a pricing quote](/en-us/contact/pricing/)
* [Try Azure for free](/en-us/free/)

## Publish APIs to developers, partners, and employees securely and at scale

Azure API Management allows organizations to publish APIs hosted on Azure, on-premises, and in other clouds more securely, reliably, and at scale. Use API Management to drive API consumption among internal teams, partners, and developers while benefiting from business and log analytics available in the admin portal. This service helps provide the tools your organization needs for end-to-end API management—everything from provisioning user roles, creating usage plans and quotas, applying policies for transforming payloads, throttling, analytics, monitoring, and alerts.

## Explore pricing options

Apply filters to customize pricing options to your needs.

Prices are estimates only and are not intended as actual price quotes. Actual pricing may vary depending on the type of agreement entered with Microsoft, date of purchase, and the currency exchange rate. Prices are calculated based on US dollars and converted using London closing spot rates that are captured in the two business days prior to the last business day of the previous month end. If the two business days prior to the end of the month fall on a bank holiday in major markets, the rate setting day is generally the day immediately preceding the two business days. This rate applies to all transactions during the upcoming month. Sign in to the [Azure pricing calculator](/en-us/pricing/calculator/) to see pricing based on your current program/offer with Microsoft. Contact an [Azure sales specialist](/en-us/contact/pricing/) for more information on pricing or to request a price quote.
