# Service: Azure Functions

**Provider:** azure
**Document type:** service_reference
**Category:** compute
**Tags:** serverless, event_driven, functions
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview)
- [limits](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)
- [pricing](https://azure.microsoft.com/en-us/pricing/details/functions/)

## Overview

Note


# What is Azure Functions?


Azure Functions is a serverless solution that allows you to build robust apps while using less code, and with less infrastructure and lower costs. Instead of worrying about deploying and maintaining servers, you can use the cloud infrastructure to provide all the up-to-date resources needed to keep your applications running.

You focus on the code that matters most to you, in the most productive language for you, and Azure Functions handles the rest. For a list of supported languages, see [Supported languages in Azure Functions](supported-languages).

## Scenarios

Functions provides a comprehensive set of event-driven [triggers and bindings](functions-triggers-bindings) that connect your functions to other services without having to write extra code.

The following list includes common integrated scenarios that use Functions.

| If you want to... | then... |
| --- | --- |
| [Process file uploads](functions-scenarios#process-file-uploads) | Run code when a file is uploaded or changed in blob storage. |
| [Process data in real time](functions-scenarios#real-time-stream-and-event-processing) | Capture and transform data from event and IoT source streams on the way to storage. |
| [Run AI inference](functions-scenarios#machine-learning-and-ai) | Pull text from a queue and present it to various AI services for analysis and classification. |
| [Run scheduled task](functions-scenarios#run-scheduled-tasks) | Execute data clean-up code on predefined timed intervals. |
| [Build a scalable web API](functions-scenarios#build-a-scalable-web-api) | Implement a set of REST endpoints for your web applications using HTTP triggers. |
| [Build a serverless workflow](functions-scenarios#build-a-serverless-workflow) | Create an event-driven workflow from a series of functions using Durable Functions. |
| [Respond to database changes](functions-scenarios#respond-to-database-changes) | Run custom logic when a document is created or updated in a database. |
| [Create reliable message systems](functions-scenarios#create-reliable-message-systems) | Process message queues using Azure Queue Storage, Service Bus, or Event Hubs. |

These scenarios allow you to build event-driven systems using modern architectural patterns. For more information, see [Azure Functions scenarios](functions-scenarios).

## Development lifecycle

Functions supports you through every stage of app development:

1.

## Key Features

# What is Azure Functions?


Azure Functions is a serverless solution that allows you to build robust apps while using less code, and with less infrastructure and lower costs. Instead of worrying about deploying and maintaining servers, you can use the cloud infrastructure to provide all the up-to-date resources needed to keep your applications running.

You focus on the code that matters most to you, in the most productive language for you, and Azure Functions handles the rest. For a list of supported languages, see [Supported languages in Azure Functions](supported-languages).

## Scenarios

Functions provides a comprehensive set of event-driven [triggers and bindings](functions-triggers-bindings) that connect your functions to other services without having to write extra code.

The following list includes common integrated scenarios that use Functions.

| If you want to... | then... |
| --- | --- |
| [Process file uploads](functions-scenarios#process-file-uploads) | Run code when a file is uploaded or changed in blob storage. |
| [Process data in real time](functions-scenarios#real-time-stream-and-event-processing) | Capture and transform data from event and IoT source streams on the way to storage. |
| [Run AI inference](functions-scenarios#machine-learning-and-ai) | Pull text from a queue and present it to various AI services for analysis and classification. |
| [Run scheduled task](functions-scenarios#run-scheduled-tasks) | Execute data clean-up code on predefined timed intervals. |
| [Build a scalable web API](functions-scenarios#build-a-scalable-web-api) | Implement a set of REST endpoints for your web applications using HTTP triggers. |
| [Build a serverless workflow](functions-scenarios#build-a-serverless-workflow) | Create an event-driven workflow from a series of functions using Durable Functions. |
| [Respond to database changes](functions-scenarios#respond-to-database-changes) | Run custom logic when a document is created or updated in a database. |
| [Create reliable message systems](functions-scenarios#create-reliable-message-systems) | Process message queues using Azure Queue Storage, Service Bus, or Event Hubs. |

These scenarios allow you to build event-driven systems using modern architectural patterns. For more information, see [Azure Functions scenarios](functions-scenarios).

## Development lifecycle

Functions supports you through every stage of app development:

1. **Code** in [C#, Java, JavaScript, PowerShell, Python, or Go](supported-languages), or use [custom handlers](functions-custom-handlers) for languages like Rust.
2. **Develop and debug** locally with [Visual Studio, Visual Studio Code, Maven, and other tools](functions-develop-local).
3. **Deploy** to Azure using [CLI, CI/CD pipelines, or your IDE](functions-deployment-technologies).
4.

## Limits and Quotas

*Source: [https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)*

Note


# Azure Functions hosting options


When you create a function app in Azure, you must choose a hosting option for your app. Azure provides you with these hosting options for your function code:

| Hosting option | Service | Availability | Container support |
| --- | --- | --- | --- |
| **[Flex Consumption plan](flex-consumption-plan)** | Azure Functions | Generally available (GA) | None |
| **[Premium plan](functions-premium-plan)** | Azure Functions | GA | Linux |
| **[Dedicated plan](dedicated-plan)** | Azure Functions | GA | Linux |
| **[Container Apps](../container-apps/functions-overview)** | Azure Container Apps | GA | Linux |
| **[Consumption plan](consumption-plan)** (legacy) | Azure Functions | Windows - GA Linux - Retired | None |

Important

The Consumption plan is a legacy hosting plan. For new serverless function apps, use the [Flex Consumption plan](flex-consumption-plan). For existing Consumption plan apps, [migrate to the Flex Consumption plan](migration/migrate-plan-consumption-to-flex).

The Azure App Service infrastructure on both Linux and Windows virtual machines facilitates the Azure Functions hosting options. The hosting option you choose dictates the following behaviors:

* How your function app is scaled.
* The resources available to each function app instance.
* Support for advanced functionality, such as Azure Virtual Network connectivity.
* Support for Linux containers.

The plan you choose also impacts the costs for running your function code. For more information, see [Billing](#billing).

This article provides a detailed comparison between the various hosting options. To learn more about running and managing your function code in Linux containers, see [Linux container support in Azure Functions](container-concepts).

## Overview of plans

The following table summarizes the benefits of the various options for Azure functions hosting.

| Option | Benefits |
| --- | --- |
| **[Flex Consumption plan](flex-consumption-plan)** | Experience fast horizontal scaling, with flexible compute options, virtual network integration, and serverless pay-as-you-go billing.  In the Flex Consumption plan, function instances dynamically scale out (up to 1,000) based on configured per-instance concurrency, incoming events, and per-function workloads for optimal efficiency.  Consider the Flex Consumption plan when:  â You need a serverless host for your function code, paying only for on-demand executions. â You require virtual network connectivity for secure access to Azure resources. â Your workloads are variable and can go from no activity to demanding rapid, event-driven scaling. â You want to customize compute with memory sizes (512 MB, 2,048 MB, or 4,096 MB) and reduce cold starts via one or more pre-provisioned (always-ready) instances.

## Pricing

*Source: [https://azure.microsoft.com/en-us/pricing/details/functions/](https://azure.microsoft.com/en-us/pricing/details/functions/)*

# Azure Functions pricing

* [Request a pricing quote](/en-us/contact/pricing/)
* [Try Azure for free](/en-us/free/)

## Execute event-driven serverless code functions with an end-to-end development experience

Azure Functions provide a serverless development experience supporting a robust set of event triggers and data bindings.

## Explore pricing options

* ### Pay as you go

  Pay for compute capacity by the second, with no long-term commitments or upfront payments. Increase or decrease consumption on demand.

  [Learn more](/en-us/pricing/purchase-options/pay-as-you-go/)
* ### Azure savings plan for compute

  Save money across select compute services globally by committing to spend a fixed hourly amount for 1 or 3 years, unlocking lower prices until you reach your hourly commitment. Suited for dynamic workloads while accommodating for planned or unplanned changes.

  [Learn more](/en-us/pricing/offers/savings-plan-compute/)

Apply filters to customize pricing options to your needs.

Prices are estimates only and are not intended as actual price quotes. Actual pricing may vary depending on the type of agreement entered with Microsoft, date of purchase, and the currency exchange rate. Prices are calculated based on US dollars and converted using London closing spot rates that are captured in the two business days prior to the last business day of the previous month end. If the two business days prior to the end of the month fall on a bank holiday in major markets, the rate setting day is generally the day immediately preceding the two business days. This rate applies to all transactions during the upcoming month. Sign in to the [Azure pricing calculator](/en-us/pricing/calculator/) to see pricing based on your current program/offer with Microsoft. Contact an [Azure sales specialist](/en-us/contact/pricing/) for more information on pricing or to request a price quote.
