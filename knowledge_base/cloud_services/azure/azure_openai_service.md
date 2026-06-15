# Service: Azure OpenAI Service

**Provider:** azure
**Document type:** service_reference
**Category:** ai
**Tags:** llm, gpt, embeddings, chat, completions
**Last updated:** 2026-06-10
**Sources:**
- [overview](https://learn.microsoft.com/en-us/azure/ai-services/openai/overview)
- [quotas](https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits)
- [pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/)
- [models](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models)

## Overview

Note


# Foundry Models sold by Azure


Microsoft Foundry Models in the model catalog comprise two main categories, namely *Foundry Models sold by Azure* and *Foundry Models from partners and community*.
This article lists a selection of Foundry Models sold by Azure, along with their capabilities, [deployment types](deployment-types), and regions of availability, excluding deprecated and retired models. Foundry Models sold by Azure are also referred to as *Direct from Azure Models* or *Azure Direct Models*.

Models sold by Azure are also hosted by Azure and operated by Azure as part of the Foundry Models service. They include all Azure OpenAI models and specific, [selected models from top providers](models-sold-directly-by-azure?pivots=azure-direct-others). These models are billed through your Azure subscription, covered by Azure service-level agreements, and supported by Microsoft. To see a list of Foundry Models that are supported by the Foundry Agent Service, see [Models supported by Agent Service](../../agents/concepts/limits-quotas-regions), and for a list of Foundry Models from partners, see [Foundry Models from partners and community](models-from-partners).

Tip

Use the tabs at the top of this page to switch between [Azure OpenAI models](models-sold-directly-by-azure?pivots=azure-openai) and [Other model collections](models-sold-directly-by-azure?pivots=azure-direct-others) from providers like Cohere, DeepSeek, Meta, Mistral AI, and xAI.

## Azure OpenAI in Microsoft Foundry models

Azure OpenAI is powered by a diverse set of models with different capabilities and price points.

## Key Features

### Capabilities

| Model ID | Description | Context Window | Max Output Tokens | Training Data (up to) |
| --- | --- | --- | --- | --- |
| `gpt-chat-latest` (2026-05-28) **Preview** | - [Reasoning](../../openai/how-to/reasoning)  - Chat Completions API.   - [Responses API](../../openai/how-to/responses).   - Structured outputs   - Functions, tools, and parallel tool calling. | 128,000   Input: 111,616   Output: 16,384 | 16,384 | August 2025 |
| `gpt-chat-latest` (2026-05-05) **Preview** | - [Reasoning](../../openai/how-to/reasoning)  - Chat Completions API.   - [Responses API](../../openai/how-to/responses).   - Structured outputs   - Functions, tools, and parallel tool calling. | 128,000   Input: 111,616   Output: 16,384 | 16,384 | August 2025 |

Note

You might also see this model referred to by OpenAI as GPT-5.5 Instant or in the OpenAI API as `chat-latest`. In Microsoft Foundry, the product name for this release is `gpt-chat-latest`. The model continues to follow the existing [Preview lifecycle](../../openai/concepts/model-retirements) and standard notice periods. The team is also evaluating ways to simplify how customers access continuously updated models over time, but current behavior remains unchanged as that work continues.

## Limits and Quotas

*Source: [https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits](https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits)*

Note


# Azure OpenAI in Microsoft Foundry Models quotas and limits


This article contains a quick reference and a detailed description of the quotas and limits for Azure OpenAI.

## Scope of quota

Quotas and limits aren't enforced at the tenant level. Instead, the highest level of quota restrictions is scoped at the Azure subscription level.

## Regional quota allocation

Tokens per minute (TPM) and requests per minute (RPM) limits are defined *per region*, *per subscription*, and *per model or deployment type*.

For example, if the `gpt-4.1` Global Standard model is listed with a quota of *5 million TPM* and *5,000 RPM*, then *each region* where that [model or deployment type is available](../foundry-models/concepts/models-sold-directly-by-azure) has its own dedicated quota pool of that amount for *each* of your Azure subscriptions. Within a single Azure subscription, it's possible to use a larger quantity of total TPM and RPM quota for a given model and deployment type, as long as you have resources and model deployments spread across multiple regions.

## Quota tiers

We are introducingâ¯Quota Tiers to improve the Foundry Models experience and reduce friction asâ¯workloadsâ¯scale. Quotasâ¯willâ¯now increase automatically with usage, helping avoid rateâ¯limitâ¯errorsâ¯while also creating a fairer environment for allâ¯users. Seven tiersâ¯will beâ¯madeâ¯available:â¯Free Tierâ¯andâ¯Tiers 1â¯throughâ¯6â¯-â¯withâ¯Tier 6 offering the highest quotas.â¯A customerâsâ¯initialâ¯assigned tierâ¯isâ¯based onâ¯their currentâ¯usageâ¯of that modelâ¯andâ¯their currentâ¯relationshipâ¯withâ¯Microsoft, such as Enterpriseâ¯Agreementâ¯(EAâ¯orâ¯MCA-E)â¯status.â¯

### Whatâs changing for me?

Previously, Foundry offered only Default and Enterprise quota levels for pay as you go offer type, with a large gap betweenâ¯eachâ¯levelâ¯and aâ¯longerâ¯process to request increases. With Quota Tiers, all users are assigned a tier with quotas equal to or higher than theirâ¯previousâ¯levels. Any previously approved quota increases areâ¯retainedâ¯and will not be reduced.

## Pricing

*Source: [https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/)*

# Azure OpenAI pricing

* [Request a pricing quote](/en-us/contact/pricing/)
* [Try Azure for free](/en-us/free/)

## Azure OpenAI Service pricing overview

Azure OpenAI Service delivers enterprise-ready generative AI featuring powerful models from OpenAI, enabling organizations to innovate with text, audio, and vision capabilities. Beyond the cutting-edge models, companies choose Azure OpenAI Service for built-in data privacy, regional/area/global flexibility, and seamless integration into the Azure ecosystem including Fabric, Cosmos DB and Azure AI Search. Companies of all sizes can confidently scale AI solutions to enhance customer experience, automate workflows, and unlock creative potential, driving measurable impact and competitive differentiation.

To help customers in the journey, we offer pricing and cost management solutions to meet your needs. including:

* **Standard (On-Demand):** Pay-as-you-go for input and output tokens.
* **Provisioned (PTUs):** [Allocate throughput](https://docs.microsoft.com/en-us/azure/ai-services/openai/concepts/provisioned-throughput) with predictable costs, with monthly and annual reservations available to reduce overall spend.
* **Batch API:** Language models are also now available in the [Batch API for global deployments and three regions](https://aka.ms/aoai-batch-how-to), that returns completions within 24 hours for a 50% discount on Global Standard Pricing.

You can choose from the following deployment types for Standard and Provisioned, which enable greater flexibility and control of pricing and performance. This flexibility helps when there is increasingly more restrictive data processing boundaries and need for increased throughput and lower price.

* **Global Deployment** – Global SKU
* **Data Zone Deployment** – Geographic based (EU or US)
* **Regional Deployment** – Local Region (up to 27 regions)

## Explore pricing options

Apply filters to customize pricing options to your needs.

Prices are estimates only and are not intended as actual price quotes. Actual pricing may vary depending on the type of agreement entered with Microsoft, date of purchase, and the currency exchange rate. Prices are calculated based on US dollars and converted using London closing spot rates that are captured in the two business days prior to the last business day of the previous month end. If the two business days prior to the end of the month fall on a bank holiday in major markets, the rate setting day is generally the day immediately preceding the two business days. This rate applies to all transactions during the upcoming month. Sign in to the [Azure pricing calculator](/en-us/pricing/calculator/) to see pricing based on your current program/offer with Microsoft. Contact an [Azure sales specialist](/en-us/contact/pricing/) for more information on pricing or to request a price quote.

## Models

*Source: [https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models)*

Note


# Foundry Models sold by Azure


Microsoft Foundry Models in the model catalog comprise two main categories, namely *Foundry Models sold by Azure* and *Foundry Models from partners and community*.
This article lists a selection of Foundry Models sold by Azure, along with their capabilities, [deployment types](deployment-types), and regions of availability, excluding deprecated and retired models. Foundry Models sold by Azure are also referred to as *Direct from Azure Models* or *Azure Direct Models*.

Models sold by Azure are also hosted by Azure and operated by Azure as part of the Foundry Models service. They include all Azure OpenAI models and specific, [selected models from top providers](models-sold-directly-by-azure?pivots=azure-direct-others). These models are billed through your Azure subscription, covered by Azure service-level agreements, and supported by Microsoft. To see a list of Foundry Models that are supported by the Foundry Agent Service, see [Models supported by Agent Service](../../agents/concepts/limits-quotas-regions), and for a list of Foundry Models from partners, see [Foundry Models from partners and community](models-from-partners).

Tip

Use the tabs at the top of this page to switch between [Azure OpenAI models](models-sold-directly-by-azure?pivots=azure-openai) and [Other model collections](models-sold-directly-by-azure?pivots=azure-direct-others) from providers like Cohere, DeepSeek, Meta, Mistral AI, and xAI.

## Azure OpenAI in Microsoft Foundry models

Azure OpenAI is powered by a diverse set of models with different capabilities and price points.
