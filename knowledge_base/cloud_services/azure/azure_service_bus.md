# Service: Azure Service Bus

**Provider:** azure
**Document type:** service_reference
**Category:** messaging
**Tags:** messaging, queues, topics, async
**Last updated:** 2026-06-10
**Sources:**
- [overview](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview)
- [limits](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-quotas)
- [pricing](https://azure.microsoft.com/en-us/pricing/details/service-bus/)

## Overview

Note


# What is Azure Service Bus?


Azure Service Bus is a fully managed enterprise message broker with message queues and publish-subscribe topics. Use Service Bus to decouple applications and services from each other. It provides the following benefits:

* Load-balances work across competing workers
* Safely routes and transfers data and control across service and application boundaries
* Coordinates transactional work that requires a high degree of reliability

## Overview

Applications and services transfer data between each other by using **messages**. A message is a container that holds data and is decorated with metadata. The data can be any kind of information, including structured data encoded with common formats such as JSON, XML, Apache Avro, or plain text.

Some common messaging scenarios include:

* **Messaging**. Transfer business data, such as sales or purchase orders, journals, or inventory movements.
* **Decouple applications**. Improve reliability and scalability of applications and services. Producer and consumer don't have to be online or readily available at the same time. The [load is leveled](/en-us/azure/architecture/patterns/queue-based-load-leveling) such that traffic spikes don't overtax a service.
* **Load balancing**. Allow for multiple [competing consumers](/en-us/azure/architecture/patterns/competing-consumers) to read from a queue at the same time, each safely obtaining exclusive ownership to specific messages.
* **Topics and subscriptions**. Enable 1:*n* relationships between [publishers and subscribers](/en-us/azure/architecture/patterns/publisher-subscriber), allowing subscribers to select particular messages from a published message stream.
* **Transactions**. Perform several operations, all in the scope of an atomic transaction. For example, the following operations can be done in the scope of a transaction:

  1. Obtain a message from one queue.
  2. Post results of processing to one or more different queues.
  3. Move the input message from the original queue.

  The results become visible to downstream consumers only upon success, including the successful settlement of input message, allowing for once-only processing semantics. This transaction model is a robust foundation for the [compensating transactions](/en-us/azure/architecture/patterns/compensating-transaction) pattern in the greater solution context.
* **Message sessions**.

## Key Features

# What is Azure Service Bus?


Azure Service Bus is a fully managed enterprise message broker with message queues and publish-subscribe topics. Use Service Bus to decouple applications and services from each other. It provides the following benefits:

* Load-balances work across competing workers
* Safely routes and transfers data and control across service and application boundaries
* Coordinates transactional work that requires a high degree of reliability

## Overview

Applications and services transfer data between each other by using **messages**. A message is a container that holds data and is decorated with metadata. The data can be any kind of information, including structured data encoded with common formats such as JSON, XML, Apache Avro, or plain text.

Some common messaging scenarios include:

* **Messaging**. Transfer business data, such as sales or purchase orders, journals, or inventory movements.
* **Decouple applications**. Improve reliability and scalability of applications and services. Producer and consumer don't have to be online or readily available at the same time. The [load is leveled](/en-us/azure/architecture/patterns/queue-based-load-leveling) such that traffic spikes don't overtax a service.
* **Load balancing**. Allow for multiple [competing consumers](/en-us/azure/architecture/patterns/competing-consumers) to read from a queue at the same time, each safely obtaining exclusive ownership to specific messages.
* **Topics and subscriptions**. Enable 1:*n* relationships between [publishers and subscribers](/en-us/azure/architecture/patterns/publisher-subscriber), allowing subscribers to select particular messages from a published message stream.
* **Transactions**. Perform several operations, all in the scope of an atomic transaction. For example, the following operations can be done in the scope of a transaction:

  1. Obtain a message from one queue.
  2. Post results of processing to one or more different queues.
  3. Move the input message from the original queue.

  The results become visible to downstream consumers only upon success, including the successful settlement of input message, allowing for once-only processing semantics. This transaction model is a robust foundation for the [compensating transactions](/en-us/azure/architecture/patterns/compensating-transaction) pattern in the greater solution context.
* **Message sessions**. Implement high-scale coordination of workflows and multiplexed transfers that require strict message ordering or message deferral.

If you're familiar with other message brokers like Apache ActiveMQ, Service Bus concepts are similar to what you know. As Service Bus is a platform as a service (PaaS) offering, a key difference is that you don't need to worry about the following actions.

## Limits and Quotas

*Source: [https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-quotas](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-quotas)*

Note


# Service Bus quotas


This section lists basic quotas and throttling thresholds in Azure Service Bus messaging.

## Messaging quotas

The following table lists quota information specific to Azure Service Bus messaging. For information about pricing and other quotas for Service Bus, see [Service Bus pricing](https://azure.microsoft.com/pricing/details/service-bus/).

### Common limits for all tiers

The following limits are common across all tiers.

| Quota name | Value | Notes |
| --- | --- | --- |
| Maximum number of namespaces per Azure subscription per region | 1000 (default and maximum) | This limit is based on the `Microsoft.ServiceBus` provider, not based on the tier. Therefore, it's the total number of namespaces across all tiers. Subsequent requests for additional namespaces are rejected. |
| Number of concurrent connections on a namespace | Net Messaging: 1,000.  AMQP: 5,000. | Subsequent requests for additional connections are rejected. REST operations don't count toward concurrent TCP connections. |
| Number of concurrent receive requests on a queue, topic, or subscription entity | 5,000 | Subsequent receive requests are rejected. This quota applies to the combined number of concurrent receive operations across all subscriptions on a topic. |
| Maximum size of any messaging entity path: queue or topic | 260 characters. |  |
| Maximum size of any messaging entity name: namespace, subscription, or subscription rule | 50 characters. |  |
| Maximum size of a message ID | 128 |  |
| Maximum number of session states per messaging entity: queue or subscription | 1,000,000 |  |
| Maximum size of a message session ID | 128 |  |
| Message property size for a queue, topic, or subscription entity | Maximum message property size for each property is 32 KB.  Cumulative size of all properties can't exceed 64 KB. This limit applies to the entire header of the brokered message, which has both user properties and system properties, such as sequence number, label, and message ID.  Maximum number of header properties in property bag: **byte/int.MaxValue**. | The exception `SerializationException` is generated. |
| Number of SQL filters per topic | 2,000 | Subsequent requests for creation of additional filters on the topic are rejected, and the calling code receives an exception. |
| Number of correlation filters per topic | 100,000 | Subsequent requests for creation of additional filters on the topic are rejected, and the calling code receives an exception. |
| Size of SQL filters or actions | Maximum length of filter condition string: 1,024 (1 K).  Maximum length of rule action string: 1,024 (1 K).  Maximum number of expressions per rule action: 32. | Subsequent requests for creation of additional filters are rejected, and the calling code receives an exception. |
| Number of shared access authorization rules per namespace, queue, or topic | Maximum number of rules per entity type: 12.

## Pricing

*Source: [https://azure.microsoft.com/en-us/pricing/details/service-bus/](https://azure.microsoft.com/en-us/pricing/details/service-bus/)*

# Service Bus pricing

* [Request a pricing quote](/en-us/contact/pricing/)
* [Try Azure for free](/en-us/free/)

## Connect across private and public cloud environments

Azure Service Bus is a messaging infrastructure that sits between applications allowing them to exchange messages for improved scale and resiliency.

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

US government entities are eligible to purchase Azure Government services from a licensing solution provider with no upfront financial commitment, or directly through a pay-as-you-go online subscription.

[Learn more](/en-us/explore/global-infrastructure/government/)

