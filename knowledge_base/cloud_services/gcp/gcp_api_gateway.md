# Service: API Gateway

**Provider:** gcp
**Document type:** service_reference
**Category:** networking
**Tags:** api_gateway, rest, openapi
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://cloud.google.com/api-gateway/docs/about-api-gateway)
- [pricing](https://cloud.google.com/api-gateway/pricing)

## Overview

Send feedback


Stay organized with collections

Save and categorize content based on your preferences.


# About API Gateway

Web-based services today provide a huge variety of functionality, meaning everything from map, weather, and image services, to games, auctions, and many other service types. Service providers have many options for how to implement, deploy, and manage their services. For example, one service might be developed in Java or .NET, while another uses Node.js.

Backend implementations can also vary for a single service provider. A service provider might have legacy services implemented using one architecture, and new services implemented using a completely different architecture.

Regardless of implementation, web-based services all require a way to make the services available to app developers. Often these services are exposed as a set of HTTP endpoints. Depending on the service, the endpoint might also return data, formatted as XML or JSON, to the client app.

## About Google Cloud services

When developing your services on the Google Cloud, you have many options for how you implement the services, such as [Cloud Run functions](/functions/docs), [Cloud Run](/run/docs), and [App Engine standard environment](/appengine/docs). The flexibility of Google Cloud means you choose the correct backend architecture for your service requirements.

App developers are the customers of backend services. App developers consume your services to implement apps for mobile devices or tablets, through apps running in a browser, or through any other type of app that can make a service request.

Exposing services publicly over the web can be challenging. To be successful, a service provider must:

* Authenticate access to the service
* Secure data transport between clients and the service
* Protect the service from malicious attacks
* Scale the service as usage increases or decreases
* Provide the backend operations team with a way to monitor and track service usage
* Track usage to provide accurate billing information

Also, if your services use different interfaces and protocols, then accessing these services can be a challenge to app developers.

## Key Features

## What is an API?

An API is an interface that makes it possible for one application to consume capabilities or data from another application. By defining stable and well-documented entry points, APIs enable developers to access and reuse application logic built by other developers.

For example, the following table describes an example of a REST API that could return information about a book:

| Property | Value | Description |
| --- | --- | --- |
| **URL** | https://www.mybooksapi.com/books/info | Return the title, author, and publishing date of a book based on its International Standard Book Number (ISBN). |
| **HTTP Verb** | GET | Make a GET request to the API. |
| **Query param** | `isbn` | Pass the ISBN number of the book, meaning the book's ID. |
| **Response data** | ``` {   "title" : "book_title",   "author" : "author_name",   "published" : "publish_date" } ``` | JSON object containing book details. |
| **Response code** | 200 | Request successful. |

The following provides an example of a curl request that might be used to get information about a book with the
specified ISBN number:

```
curl -X GET https://www.mybooksapi.com/books/info?isbn=0385504217
```

Because this service has a well-defined API, including a description of data formats and HTTP response codes, the app developer does not need to know anything about the underlying implementation of the backend service.

Since applications that consume APIs are sensitive to changes, APIs also imply a contract between API providers and API consumers. The contract assures that over time the API will change in a predictable manner. For example, the book API might be updated to add additional query parameters, such as `title` or `author`, or change the response JSON to add additional information about the book.

### Define an API

You define an API deployed on API Gateway as an OpenAPI 2.0 spec.
The key components of an API definition include:

* The URL, or entry point, of the backend service
* The data format of any data passed on a request to the API
* The data format of any data returned by the service in the response from the API
* The authentication mechanism used to control access to the service

After you define your API, use the [gcloud](/sdk/gcloud/reference) command line interface to upload it to an API config on Google Cloud:

### Deploy an API config on API Gateway

To create your API, you deploy the API config on API Gateway.
Use the `gcloud` command to deploy the API config:

After the API config is deployed, your clients can make REST calls to the API.

### Manage an API

Once deployed and running, you can monitor API activity, such as usage metrics and logs. When a client makes a request to your API, API Gateway logs information about the request and response. API Gateway also tracks latency, traffic, and errors.

Over time, you might want to update a deployed API to add new capabilities, improve performance, or to fix issues with the API.

## Pricing

*Source: [https://cloud.google.com/api-gateway/pricing](https://cloud.google.com/api-gateway/pricing)*

Page Contents
API Gateway pricing
Per call pricing
API Gateway charges by its calls to
Service Control
. Each API call processed by API Gateway is reported as a tracked operation by the Service Control API and is listed as a line item for Service Control on your bill.
The price for API Gateway depends on the number of calls to your API, as described in the following table:
API calls per month per billing account
Cost per million API calls
0-2M
$0.00
2M-1B
$3.00
1B+
$1.50
If you pay in a currency other than USD, the prices listed in your currency on
Cloud Platform SKUs
apply.
Data Transfer pricing
Data transfer into Google Cloud is free.
General network usage applies to data that exits Google. The API Gateway uses Premium Tier data transfer out to the Internet, with prices shown below. Data transfer prices are consistent with Google Cloud Network Pricing - Premium Tier.
Prices are per GB per month.
Source and destination of traffic
Price (USD)
North America to North America
0 gibibyte to 10,240 gibibyte
$0.105 / 1 gibibyte, per 1 month / account
10,240 gibibyte to 153,600 gibibyte
$0.08 / 1 gibibyte, per 1 month / account
153,600 gibibyte and above
$0.06 / 1 gibibyte, per 1 month / account
Europe to Europe
0 gibibyte to 10,240 gibibyte
$0.105 / 1 gibibyte, per 1 month / account
10,240 gibibyte to 153,600 gibibyte
$0.08 / 1 gibibyte, per 1 month / account
153,600 gibibyte and above
$0.06 / 1 gibibyte, per 1 month / account
Asia Pacific to Asia Pacific
0 gibibyte to 10,240 gibibyte
$0.12 / 1 gibibyte, per 1 month / account
10,240 gibibyte to 153,600 gibibyte
$0.085 / 1 gibibyte, per 1 month / account
153,600 gibibyte and above
$0.08 / 1 gibibyte, per 1 month / account
South America to South America
0 gibibyte to 10,240 gibibyte
$0.12 / 1 gibibyte, per 1 month / account
10,240 gibibyte to 153,600 gibibyte
$0.085 / 1 gibibyte, per 1 month / account
153,600 gibibyte and above
$0.08 / 1 gibibyte, per 1 month / account
Oceania to Oceania
0 gibibyte to 10,240 gibibyte
$0.12 / 1 gibibyte, per 1 month / account
10,240 gibibyte to 153,600 gibibyte
$0.085 / 1 gibibyte, per 1 month / account
153,600 gibibyte and above
$0.08 / 1 gibibyte, per 1 month / account
Intercontinental (excluding Oceania and China)
0 gibibyte to 10,240 gibibyte
$0.12 / 1 gibibyte, per 1 month / account
10,240 gibibyte to 153,600 gibibyte
$0.085 / 1 gibibyte, per 1 month / account
153,600 gibibyte and above
$0.08 / 1 gibibyte, per 1 month / account
Intercontinental to/from Oceania
0 gibibyte to 10,240 gibibyte
$0.19 / 1 gibibyte, per 1 month / account
10,240 gibibyte to 153,600 gibibyte
$0.16 / 1 gibibyte, per 1 month / account
153,600 gibibyte and above
$0.15 / 1 gibibyte, per 1 month / account
Any traffic to China
0 gibibyte to 10,240 gibibyte
$0.19 / 1 gibibyte, per 1 month / account
10,240 gibibyte to 153,600 gibibyte
$0.16 / 1 gibibyte, per 1 month / account
153,600 gibibyte and above
$0.15 / 1 gibibyte, per 1 month / account
What's next
Read the
API Gateway documentation
.
