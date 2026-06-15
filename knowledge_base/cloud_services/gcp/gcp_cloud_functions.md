# Service: Cloud Functions

**Provider:** gcp
**Document type:** service_reference
**Category:** compute
**Tags:** serverless, functions, event_driven
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://cloud.google.com/functions/docs/concepts/overview)
- [limits](https://cloud.google.com/functions/quotas)
- [pricing](https://cloud.google.com/functions/pricing)

## Overview

If you are creating a new function, see the [Console Quickstart](https://cloud.google.com/run/docs/quickstarts/functions/deploy-functions-console) on Cloud Run.

Send feedback


Stay organized with collections

Save and categorize content based on your preferences.


# Functions overview

See the following documentation based on your function version:

* For Cloud Run functions, see
  [Cloud Run documentation](/run/docs/functions-with-run).
  + Learn how to [deploy a Cloud Run function](/run/docs/deploy-functions).
  + If you have existing functions and need to use `gcloud functions` commands
    or the Cloud Functions v2 API for backward compatibility, see
    [Deploy functions created with the v2 API](/run/docs/functions/comparison#v2-deploy).
* For Cloud Run functions (1st gen), see
  [Deploy a function (1st gen)](/functions/1stgendocs/deploy).

For a comparison of the two versions, see
[Compare Cloud Run functions](/run/docs/functions/comparison).


Send feedback

## Limits and Quotas

*Source: [https://cloud.google.com/functions/quotas](https://cloud.google.com/functions/quotas)*

If you are creating a new function, see the [Console Quickstart](https://cloud.google.com/run/docs/quickstarts/functions/deploy-functions-console) on Cloud Run.

Send feedback


Stay organized with collections

Save and categorize content based on your preferences.


# Quotas

This document describes the quota limits for Cloud Run functions.

Quotas for Cloud Run functions encompass 4 areas:

* Resource Limits

  These affect the total amount of resources your functions can consume.
* Time Limits

  These affect how long things can run.
* Rate Limits

  These affect the rate at which you can call the Cloud Run functions API
  to manage your functions.
* Networking Limits

  These affect outbound connection and instance limits.

The different types of limits are described in more detail below.
Differences between limits for Cloud Run functions (1st gen) and
Cloud Run functions (2nd gen) are noted where applicable.

## Resource Limits

Resource limits affect the total amount of resources your functions can consume.
The regional scope is per project, and each project maintains its own limits.

| Quota | Description | Limit (1st gen) | Limit (2nd gen) | Can be increased | Scope |
| --- | --- | --- | --- | --- | --- |
| Number of functions | The total number of functions that can be deployed per region | 1,000 | 1,000 minus the number of Cloud Run services deployed | No | per region |
| Max deployment size | The maximum size of a single function deployment | 100MB (compressed) for sources.  500MB (uncompressed) for sources plus modules. | N/A | No | per function |
| Max uncompressed HTTP request size | Data sent to HTTP Functions in an HTTP request | 10MB | 32MB | No | per invocation |
| Max uncompressed HTTP response size | Data sent from HTTP functions in an HTTP response | 10MB | 10MB for streaming responses.  32MB for non-streaming responses. | No | per invocation |
| Max event size for event-driven functions | Data sent in events to background functions | 10MB | 512KB for Eventarc events.  10MB for legacy events. | No | per event |
| Max function memory | Amount of memory each function instance can use | 8GiB | 32GiB | No | per function |
| Max project memory | Amount of memory, in By, that a project can use. It is measured by the total sum of user-requested memory across function instances over a 1 minute period. | Depends on selected region. This limit might be greater in high-capacity regions or lower in recently opened regions. | N/A | Yes | per project and region |
| Max project CPU | Amount of CPU, in milli vCPU, that a project can use. It is measured by the total sum of user-requested CPU across function instances over a 1 minute period. | Depends on selected region. This limit might be greater in high-capacity regions or lower in recently opened regions.

## Pricing

*Source: [https://cloud.google.com/functions/pricing](https://cloud.google.com/functions/pricing)*

Send feedback


Stay organized with collections

Save and categorize content based on your preferences.


# Cloud Run functions pricing

Depending on which version of Cloud Run functions you are using, see the following pricing pages:

* For Cloud Run functions, see [Cloud Run pricing](https://cloud.google.com/run/pricing).
* For Cloud Run functions (1st gen), see [Cloud Run functions (1st gen) pricing](https://cloud.google.com/functions/pricing-1stgen).

#### Request a custom quote

With Google Cloud's pay-as-you-go pricing, you only pay for the services you
use. Connect with our sales team to get a custom quote for your organization.

[Contact sales](/contact?direct=true)
