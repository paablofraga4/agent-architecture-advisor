# Service: Azure Container Apps

**Provider:** azure
**Document type:** service_reference
**Category:** compute
**Tags:** containers, serverless, microservices, deployment
**Last updated:** 2026-06-10
**Sources:**
- [overview](https://learn.microsoft.com/en-us/azure/container-apps/overview)
- [limits](https://learn.microsoft.com/en-us/azure/container-apps/quotas)
- [pricing](https://azure.microsoft.com/en-us/pricing/details/container-apps/)

## Overview

Note


# Azure Container Apps overview


Azure Container Apps is a serverless platform that allows you to maintain less infrastructure and save costs while running containerized applications. Instead of worrying about server configuration, container orchestration, and deployment details, Container Apps provides all the up-to-date server resources required to keep your applications stable and secure.

Common uses of Azure Container Apps include:

* Deploying API endpoints
* Hosting background processing jobs
* Handling event-driven processing
* Running microservices

Additionally, applications built on Azure Container Apps can dynamically scale based on the following characteristics:

* HTTP traffic
* Event-driven processing
* CPU or memory load
* Any [KEDA-supported scaler](https://keda.sh/docs/2.19/scalers/)

To begin working with Container Apps, select the description that best describes your situation.

|  | Description | Resource |
| --- | --- | --- |
| **I'm new to containers** | Start here if you have yet to build your first container but are curious how containers can serve your development needs. | [Learn more about containers](start-containers) |
| **I'm using serverless containers** | Container Apps provides automatic scaling, reduces operational complexity, and allows you to focus on your application rather than infrastructure.  Start here if you're interested in the management, scalability, and pay-per-use features of cloud computing.

## Key Features

## Features

With Azure Container Apps, you can:

* [**Use the Azure CLI extension, Azure portal or ARM templates**](get-started) to manage your applications.
* [**Enable HTTPS or TCP ingress**](ingress-overview) without having to manage other Azure infrastructure.
* [**Build microservices with Dapr**](microservices) and [access its rich set of APIs](dapr-overview).
* [**Run jobs**](jobs) on-demand, on a schedule, or based on events.
* [**Run Azure Functions**](functions-overview) for [event-driven scenarios](../azure-functions/functions-scenarios) using triggers, bindings, and automatic scaling.
* Add [**Azure Spring Apps**](https://aka.ms/asaonaca) to your Azure Container Apps environment.
* [**Use specialized hardware**](plans) for access to increased compute resources.
* [**Run multiple container revisions**](application-lifecycle-management) and manage the container app's application lifecycle.
* [**Autoscale**](scale-app) your apps based on any KEDA-supported scale trigger. Most applications can scale to zero1.
* [**Split traffic**](revisions) across multiple versions of an application for Blue/Green deployments and A/B testing scenarios.
* [**Use internal ingress and service discovery**](connect-apps) for secure internal-only endpoints with built-in DNS-based service discovery.
* [**Run containers from any registry**](containers), public or private, including Docker Hub and Azure Container Registry (ACR).
* [**Provide an existing virtual network**](vnet-custom) when creating an environment for your container apps.
* [**Securely manage secrets**](manage-secrets) directly in your application.
* [**Monitor logs**](log-monitoring) using Azure Log Analytics.
* [**Generous quotas**](quotas), which can be overridden to increase limits on a per-account basis.

1 Applications that [scale on CPU or memory load](scale-app) can't scale to zero.

## Limits and Quotas

*Source: [https://learn.microsoft.com/en-us/azure/container-apps/quotas](https://learn.microsoft.com/en-us/azure/container-apps/quotas)*

Note


# Quotas for Azure Container Apps


Azure Container Apps assigns different quota types to different scopes. In addition to the subscription scope, quotas also apply to region, environment, and application scopes. All quota requests are initiated using Azure Quota Management System (QMS), which features two options for making quota requests.

| Request type | Description | Use for these scopes... | View request status via |
| --- | --- | --- | --- |
| [Integrated requests](quota-requests#integrated-requests) | Integrated requests are often approved within a few minutes. If your request exceeds a quotas threshold, then a support ticket is generated for a Support Engineer to review the request. Review times can delay approval by up to a few days. | âª region  âª subscription | [Azure portal](#list-usage-portal) |
| [Manual requests](quota-requests#manual-requests) | Manual requests always result in generating a support ticket. Approval is often automated, but some requests can take up to a few days for us to process. | âª environment | [Azure CLI](#list-usage-cli) |

Note

Azure Container Apps is a production grade service designed for at-scale workloads. Making a quota request that escalates to the support team isn't out of the norm, but part of the process of managing resources on behalf of our customers. **Azure Container Apps is an at-scale service. Most all quota change requests are granted with exceptions only in limited circumstances**.

## View current quotas levels

Depending on the quota type, you can view your quota levels via the [Azure portal](https://ms.portal.azure.com/#view/Microsoft_Azure_Capacity/QuotaMenuBlade/%7E/myQuotas) and through the Azure CLI.

When in the portal, select **Azure Container Apps** for the *Provider*.

Quotas change requests made via the manual method aren't available in the portal. Use the following command to view your quotas on a per environment basis.

Before you run the following command, make sure to replace the placeholders surrounded by `<>` with your own values.

```
az containerapp env list-usages \
  --resource-group <RESOURCE_GROUP_NAME> \
  --name <ENVIRONMENT_NAME>
```

## When to request quota

If an environment or subscription reaches a quota limit, it can have unintended consequences which include:

* Scaling restrictions on an app
* Provisioning times out with a failure
* Container Apps environment or workload profile creation failure

Your default quotas depend on factors which include the age and type of your subscription, and service use.

## Pricing

*Source: [https://azure.microsoft.com/en-us/pricing/details/container-apps/](https://azure.microsoft.com/en-us/pricing/details/container-apps/)*

# Azure Container Apps pricing

* [Request a pricing quote](/en-us/contact/pricing/)
* [Try Azure for free](/en-us/free/)

## Build and deploy modern apps and microservices using serverless containers

Azure Container Apps is a fully managed serverless container service that scales dynamically based on HTTP traffic or events.

﻿

## Explore pricing options

* ### Pay as you go

  Pay for compute capacity by the second, with no long-term commitments or upfront payments. Increase or decrease consumption on demand.

  [Learn more](/en-us/pricing/purchase-options/pay-as-you-go/)
* ### Azure savings plan for compute

  Save money across select compute services globally by committing to spend a fixed hourly amount for 1 or 3 years, unlocking lower prices until you reach your hourly commitment. Suited for dynamic workloads while accommodating for planned or unplanned changes.

  [Learn more](/en-us/pricing/offers/savings-plan-compute/)

Apply filters to customize pricing options to your needs.

Prices are estimates only and are not intended as actual price quotes. Actual pricing may vary depending on the type of agreement entered with Microsoft, date of purchase, and the currency exchange rate. Prices are calculated based on US dollars and converted using London closing spot rates that are captured in the two business days prior to the last business day of the previous month end. If the two business days prior to the end of the month fall on a bank holiday in major markets, the rate setting day is generally the day immediately preceding the two business days. This rate applies to all transactions during the upcoming month. Sign in to the [Azure pricing calculator](/en-us/pricing/calculator/) to see pricing based on your current program/offer with Microsoft. Contact an [Azure sales specialist](/en-us/contact/pricing/) for more information on pricing or to request a price quote.
