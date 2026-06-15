# Service: Amazon API Gateway

**Provider:** aws
**Document type:** service_reference
**Category:** networking
**Tags:** api_gateway, rest, websocket
**Last updated:** 2026-06-10
**Sources:**
- [overview](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
- [limits](https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html)
- [pricing](https://aws.amazon.com/api-gateway/pricing/)

## Overview

# What is Amazon API Gateway?

Amazon API Gateway is an AWS service for creating, publishing, maintaining, monitoring, and
securing REST, HTTP, and WebSocket APIs at any scale. API developers can create APIs that
access AWS or other web services, as well as data stored in the [AWS Cloud](https://aws.amazon.com/what-is-cloud-computing/). As an API Gateway
API developer, you can create APIs for use in your own client applications. Or you can make
your APIs available to third-party app developers. For more information, see [Who uses API Gateway?](./api-gateway-overview-developer-experience.html#apigateway-who-uses-api-gateway).

API Gateway creates RESTful APIs that:

* Are HTTP-based.
* Enable stateless client-server communication.
* Implement standard HTTP methods such as GET, POST, PUT, PATCH, and DELETE.

For more information about API Gateway REST APIs and HTTP APIs, see [Choose between REST APIs and HTTP APIs](./http-api-vs-rest.html), [API Gateway HTTP APIs](./http-api.html), [Use API Gateway to create REST APIs](./api-gateway-overview-developer-experience.html#api-gateway-overview-rest), and [Develop REST APIs in API Gateway](./rest-api-develop.html).

API Gateway creates WebSocket APIs that:

* Adhere to the [WebSocket](https://datatracker.ietf.org/doc/html/rfc6455)
  protocol, which enables stateful, full-duplex communication between client and
  server.
* Route incoming messages based on message content.

For more information about API Gateway WebSocket APIs, see [Use API Gateway to create WebSocket APIs](./api-gateway-overview-developer-experience.html#api-gateway-overview-websocket) and [Overview of WebSocket APIs in API Gateway](./apigateway-websocket-api-overview.html).

###### Topics

* [Architecture of API Gateway](#api-gateway-overview-aws-backbone)
* [Features of API Gateway](#api-gateway-overview-features)
* [API Gateway use cases](./api-gateway-overview-developer-experience.html)
* [Accessing API Gateway](#introduction-accessing-apigateway)
* [Part of AWS serverless infrastructure](#api-gateway-overview-a-serverless-pillar)
* [How to get started with Amazon API Gateway](#welcome-how-to-get-started)
* [Amazon API Gateway concepts](./api-gateway-basic-concept.html)
* [Choose between REST APIs and HTTP APIs](./http-api-vs-rest.html)
* [Get started with the REST API console](./getting-started-rest-new-console.html)

## Architecture of API Gateway

The following diagram shows API Gateway architecture.


## Key Features

# What is Amazon API Gateway?

Amazon API Gateway is an AWS service for creating, publishing, maintaining, monitoring, and
securing REST, HTTP, and WebSocket APIs at any scale. API developers can create APIs that
access AWS or other web services, as well as data stored in the [AWS Cloud](https://aws.amazon.com/what-is-cloud-computing/). As an API Gateway
API developer, you can create APIs for use in your own client applications. Or you can make
your APIs available to third-party app developers. For more information, see [Who uses API Gateway?](./api-gateway-overview-developer-experience.html#apigateway-who-uses-api-gateway).

API Gateway creates RESTful APIs that:

* Are HTTP-based.
* Enable stateless client-server communication.
* Implement standard HTTP methods such as GET, POST, PUT, PATCH, and DELETE.

For more information about API Gateway REST APIs and HTTP APIs, see [Choose between REST APIs and HTTP APIs](./http-api-vs-rest.html), [API Gateway HTTP APIs](./http-api.html), [Use API Gateway to create REST APIs](./api-gateway-overview-developer-experience.html#api-gateway-overview-rest), and [Develop REST APIs in API Gateway](./rest-api-develop.html).

API Gateway creates WebSocket APIs that:

* Adhere to the [WebSocket](https://datatracker.ietf.org/doc/html/rfc6455)
  protocol, which enables stateful, full-duplex communication between client and
  server.
* Route incoming messages based on message content.

For more information about API Gateway WebSocket APIs, see [Use API Gateway to create WebSocket APIs](./api-gateway-overview-developer-experience.html#api-gateway-overview-websocket) and [Overview of WebSocket APIs in API Gateway](./apigateway-websocket-api-overview.html).

###### Topics

* [Architecture of API Gateway](#api-gateway-overview-aws-backbone)
* [Features of API Gateway](#api-gateway-overview-features)
* [API Gateway use cases](./api-gateway-overview-developer-experience.html)
* [Accessing API Gateway](#introduction-accessing-apigateway)
* [Part of AWS serverless infrastructure](#api-gateway-overview-a-serverless-pillar)
* [How to get started with Amazon API Gateway](#welcome-how-to-get-started)
* [Amazon API Gateway concepts](./api-gateway-basic-concept.html)
* [Choose between REST APIs and HTTP APIs](./http-api-vs-rest.html)
* [Get started with the REST API console](./getting-started-rest-new-console.html)

## Architecture of API Gateway

The following diagram shows API Gateway architecture.

This diagram illustrates how the APIs you build in Amazon API Gateway provide you or your
developer customers with an integrated and consistent developer experience for building
AWS serverless applications. API Gateway handles all the tasks involved in accepting and
processing up to hundreds of thousands of concurrent API calls.

## Limits and Quotas

*Source: [https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html](https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html)*

# Amazon API Gateway quotas

The following quotas apply for all Amazon API Gateway API types.

## API Gateway account-level quotas, per Region

The following quotas apply per account, per Region in Amazon API Gateway.

| Resource or operation | Default quota | Can be increased |
| --- | --- | --- |
| Throttle quota per account, per Region across HTTP APIs, REST APIs, WebSocket APIs, and WebSocket callback APIs | 10,000 requests per second (RPS) with an additional burst capacity provided by the [token bucket algorithm](https://en.wikipedia.org/wiki/Token_bucket), using a maximum bucket capacity of 5,000 requests. \* Note  The burst quota is determined by the API Gateway service team based on the overall RPS quota for the account in the Region. It is not a quota that a customer can control or request changes to. | [Yes](https://console.aws.amazon.com/servicequotas/home/services/apigateway/quotas/L-8A5B8E43) |
| Throttle quota without access control per account per Region for a portal | 250,000 requests per second | No |
| Throttle quota with access control per account per Region for a portal | 10,000 requests per second | No |

\* For the following Regions, the default throttle quota is 2500 RPS and the default burst quota is 1250 RPS:
Africa (Cape Town), Europe (Milan), Asia Pacific (Jakarta), Middle East (UAE), Asia Pacific (Hyderabad),
Asia Pacific (Melbourne), Europe (Spain), Europe (Zurich), Israel (Tel Aviv),
Canada West (Calgary), Asia Pacific (Malaysia), Asia Pacific (Thailand), and Mexico (Central).

## API Gateway quotas for creating, deploying and managing an API

The following fixed quotas apply to creating, deploying, and managing an API in API Gateway,
using the AWS CLI, the API Gateway console, or the API Gateway REST API and its SDKs.

## Pricing

*Source: [https://aws.amazon.com/api-gateway/pricing/](https://aws.amazon.com/api-gateway/pricing/)*

Amazon API Gateway

* [Overview](/api-gateway/)
* [Features](/api-gateway/features/)
* [Pricing](/api-gateway/pricing/)
* [Getting Started](/api-gateway/getting-started/)
* [Resources](/api-gateway/resources/)
* More

# Amazon API Gateway pricing

[Get started for free](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html?pg=apigateprice&cta=herobtn)

[Request a pricing quote](/contact-us/sales-support/?pg=apigateprice&cta=herobtn)


With Amazon API Gateway, you only pay when your APIs are in use. There are no minimum fees or upfront commitments. For HTTP APIs and REST APIs, you pay only for the API calls you receive and the amount of data transferred out. There are no data transfer out charges for Private APIs.

Starting July 15, 2025, new AWS customers will receive up to $200 in AWS Free Tier credits, which can be applied towards eligible AWS services, including Amazon API Gateway. At account sign-up, you can choose between a free plan and a paid plan. The free plan will be available for 6 months after account creation. If you upgrade to a paid plan, any remaining Free Tier credit balance will automatically apply to your AWS bills. All Free Tier credits must be used within 12 months of your account creation date. To learn more about the AWS Free Tier program, refer to [AWS Free Tier website](/free/) and [AWS Free Tier documentation](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier.html).

## Free Tier

The Amazon API Gateway free tier includes **one million API calls** received for REST APIs, **one million API calls** received for HTTP APIs, and **one million messages** and **750,000 connection minutes** for WebSocket APIs per month for **up to 12 months**. If you exceed this number of calls per month, you will be charged the API Gateway usage rates.

Starting July 15, 2025, new AWS customers will receive up to $200 in AWS Free Tier credits, which can be applied towards eligible AWS services, including Amazon API Gateway. At account sign-up, you can choose between a free plan and a paid plan. The free plan will be available for 6 months after account creation. If you upgrade to a paid plan, any remaining Free Tier credit balance will automatically apply to your AWS bills. All Free Tier credits must be used within 12 months of your account creation date. To learn more about the AWS Free Tier program, refer to [AWS Free Tier website](/free/) and [AWS Free Tier documentation](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier.html).

1M REST API CALLS RECEIVED | 1M HTTP API CALLS RECEIVED | 1M MESSAGES | 750,000 CONNECTION MINUTES

*per month*

These free tier offers are only available to new AWS customers, and are available for 12 months following your AWS sign-up date.
