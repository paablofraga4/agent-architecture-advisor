# Service: Azure Logic Apps

**Provider:** azure
**Document type:** service_reference
**Category:** integration
**Tags:** workflow, automation, connectors, low_code
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-overview)
- [limits](https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-limits-and-config)
- [pricing](https://azure.microsoft.com/en-us/pricing/details/logic-apps/)

## Overview

Note


# What is Azure Logic Apps?


Azure Logic Apps is a cloud platform where you can create and run automated workflows in, across, and outside the software ecosystems in your enterprise or organization. This platform greatly reduces or removes the need to write code when your workflows must connect and work with resources from different components, such as services, systems, apps, and data sources.

Azure Logic Apps includes low-code-no-code tools for you to work with legacy, modern, and cutting-edge systems that exist in the cloud, on premises, or in hybrid environments. For example, you use a visual designer along with prebuilt operations to make building workflows as easy as possible. These prebuilt operations act as the building blocks in your workflows by giving you access to various resources and completing common tasks, such as getting data, sending data, and managing data. With Azure Logic Apps, you can build integration solutions that scale and support the business scenarios for your enterprise or organization's needs. You can also build intelligent autonomous and conversational workflows that incorporate AI capabilities by including AI agents and large language models (LLMs).

The following examples describe only a sample of tasks, business processes, and workloads that you can automate with Azure Logic Apps:

* Schedule and send email notifications using Office 365 when a specific event happens, for example, a new file is uploaded.
* Route and process customer orders across on-premises systems and cloud services.
* Move uploaded files from an SFTP or FTP server to Azure Blob Storage.
* Monitor social media activity, analyze the sentiment, and create alerts or tasks for items that need review.

The following example workflow uses conditions and switches to determine the next action. Suppose you have an order system, and your workflow processes incoming orders. You want to manually review orders above a certain cost. Your workflow already has steps that determine the cost from an incoming order.

## Key Features

# What is Azure Logic Apps?


Azure Logic Apps is a cloud platform where you can create and run automated workflows in, across, and outside the software ecosystems in your enterprise or organization. This platform greatly reduces or removes the need to write code when your workflows must connect and work with resources from different components, such as services, systems, apps, and data sources.

Azure Logic Apps includes low-code-no-code tools for you to work with legacy, modern, and cutting-edge systems that exist in the cloud, on premises, or in hybrid environments. For example, you use a visual designer along with prebuilt operations to make building workflows as easy as possible. These prebuilt operations act as the building blocks in your workflows by giving you access to various resources and completing common tasks, such as getting data, sending data, and managing data. With Azure Logic Apps, you can build integration solutions that scale and support the business scenarios for your enterprise or organization's needs. You can also build intelligent autonomous and conversational workflows that incorporate AI capabilities by including AI agents and large language models (LLMs).

The following examples describe only a sample of tasks, business processes, and workloads that you can automate with Azure Logic Apps:

* Schedule and send email notifications using Office 365 when a specific event happens, for example, a new file is uploaded.
* Route and process customer orders across on-premises systems and cloud services.
* Move uploaded files from an SFTP or FTP server to Azure Blob Storage.
* Monitor social media activity, analyze the sentiment, and create alerts or tasks for items that need review.

The following example workflow uses conditions and switches to determine the next action. Suppose you have an order system, and your workflow processes incoming orders. You want to manually review orders above a certain cost. Your workflow already has steps that determine the cost from an incoming order. So, you add a condition that compares each order to your cost threshold, for example:

For more information about the logic behind this workflow, see [How logic apps work](#how-logic-apps-work).

Tip

To learn more, you can ask Azure Copilot these questions:

* *What problems can I solve with Azure Logic Apps?*
* *What benefits does Azure Logic Apps provide?*

To find Azure Copilot, on the [Azure portal](https://portal.azure.com) toolbar, select **Copilot**.

To try creating your first workflow, see [Get started](#get-started).

## Limits and Quotas

*Source: [https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-limits-and-config](https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-limits-and-config)*

Note


# Limits and configuration reference for Azure Logic Apps


Applies to: **Azure Logic Apps (Consumption + Standard)**

Important

For Power Automate, see [Limits and configuration in Power Automate](/en-us/power-automate/limits-and-config).

This reference guide describes the limits and configuration information for Azure Logic Apps and related resources. Based on your scenario, solution requirements, the capabilities that you want, and the environment where you want to run your workflows, you choose whether to create a Consumption logic app workflow that runs in *multitenant* Azure Logic Apps or a Standard logic app workflow that runs in *single-tenant* Azure Logic Apps or an App Service Environment (v3 - Windows plans only).

Note

Many limits are the same across the available environments where Azure Logic Apps runs, but differences are noted where they exist.

The following table briefly summarizes differences between a Consumption logic app and a Standard logic app.

| Hosting option | Benefits | Resource sharing and usage | [Pricing and billing model](/en-us/azure/logic-apps/logic-apps-pricing) | [Limits management](/en-us/azure/logic-apps/logic-apps-limits-and-config) |
| --- | --- | --- | --- | --- |
| **Consumption**   Host environment: Multitenant Azure Logic Apps | - Easiest to get started   - Pay for what you use   - Fully managed | A single logic app resource can have *only one* workflow.   All logic apps *across Microsoft Entra tenants* share the same processing (compute), storage, network, and so on.   **Note**: Regarding data residency and redundancy:   - In workflows or workflow sections that don't interact with agents, the data is replicated in the [paired region](/en-us/azure/reliability/cross-region-replication-azure). For high availability, [geo-redundant storage (GRS)](/en-us/azure/storage/common/storage-redundancy#geo-redundant-storage) is enabled.   - Any agents in a workflow use an Azure OpenAI model that can originate from any region, so data residency isn't guaranteed for data that the model handles. | [Consumption (pay-per-execution)](/en-us/azure/logic-apps/logic-apps-pricing#consumption-pricing) | Azure Logic Apps manages the default values for these limits, but you can change some of these values, if that option exists for a specific limit. |
| **Standard (Workflow Service Plan)**   Host environment:  Single-tenant Azure Logic Apps | - More built-in connectors hosted on the single-tenant runtime for higher throughput and lower costs at scale   - More control and fine-tuning capability around runtime and performance settings   - Integrated support for virtual networks and private endpoints.   - Create your own built-in connectors. | A single logic app resource can have multiple [*stateful* and *stateless*](/en-us/azure//logic-apps/single-tenant-overview-compare#stateful-stateless) workflows.   Workflows *in a single logic app and tenant* share the same processing (compute), storage, network, and so on.

## Pricing

*Source: [https://azure.microsoft.com/en-us/pricing/details/logic-apps/](https://azure.microsoft.com/en-us/pricing/details/logic-apps/)*

# Logic Apps pricing

* [Request a pricing quote](/en-us/contact/pricing/)
* [Try Azure for free](/en-us/free/)

## Automate the access and use of data across clouds

[Azure Logic Apps](/en-us/products/logic-apps/) allows IT professionals and developers to automate business process execution and workflow using an easy-to-use visual designer.

## Explore pricing options

Apply filters to customize pricing options to your needs.

Prices are estimates only and are not intended as actual price quotes. Actual pricing may vary depending on the type of agreement entered with Microsoft, date of purchase, and the currency exchange rate. Prices are calculated based on US dollars and converted using London closing spot rates that are captured in the two business days prior to the last business day of the previous month end. If the two business days prior to the end of the month fall on a bank holiday in major markets, the rate setting day is generally the day immediately preceding the two business days. This rate applies to all transactions during the upcoming month. Sign in to the [Azure pricing calculator](/en-us/pricing/calculator/) to see pricing based on your current program/offer with Microsoft. Contact an [Azure sales specialist](/en-us/contact/pricing/) for more information on pricing or to request a price quote. See [frequently asked questions](/en-us/pricing/) about Azure pricing.

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

Display pricing by:

Hour
Month

US government entities are eligible to purchase Azure Government services from a licensing solution provider with no upfront financial commitment, or directly through a pay-as-you-go online subscription.

[Learn more](/en-us/explore/global-infrastructure/government/)

