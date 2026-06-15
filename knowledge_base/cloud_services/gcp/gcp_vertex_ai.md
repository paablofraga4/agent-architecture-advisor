# Service: Vertex AI

**Provider:** gcp
**Document type:** service_reference
**Category:** ai
**Tags:** llm, gemini, ml, agents, search
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform)
- [quotas](https://cloud.google.com/vertex-ai/docs/quotas)
- [pricing](https://cloud.google.com/vertex-ai/pricing)
- [gemini](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models)

## Overview

Send feedback

# Introduction to machine learning on Gemini Enterprise Agent Platform Stay organized with collections Save and categorize content based on your preferences.


Gemini Enterprise Agent Platform provides a comprehensive suite of tools to help you build,
train, and manage machine learning (ML) models at scale. Whether you are using
AutoML for a fast path to high-quality models or creating custom
models with popular frameworks like TensorFlow and PyTorch, Agent Platform
operationalizes the entire ML lifecycle.

## Data preparation

Before you can train a model, you need to prepare your data. Agent Platform
provides managed datasets to simplify this process.

Managed datasets allow you to provide source data for training models. They are
required for AutoML and optional for custom training. You can
create datasets for different data types, including image and tabular data.

For more information, see [Overview of creating managed datasets on Gemini Enterprise Agent Platform](/gemini-enterprise-agent-platform/machine-learning/datasets/overview).

## Model training

Agent Platform provides a managed training service that helps you operationalize
large-scale model training.

You can run training applications based on any ML framework on Google Cloud
infrastructure. Agent Platform also offers integrated support for popular
frameworks like PyTorch, TensorFlow, scikit-learn, and XGBoost.

Key benefits of serverless training include:

* **Fully managed compute infrastructure**: Train models without provisioning or
  managing servers.
* **High performance**: Optimized training jobs that can provide faster
  performance.
* **Distributed training**: Support for multi-node distributed training to
  reduce time and cost.
* **Hyperparameter optimization**: Automatically discover optimal values for your
  model.

For more information, see [serverless training overview](/gemini-enterprise-agent-platform/machine-learning/training/overview).

## Model management

After training your model, you can manage it in the Model Registry.

The Model Registry is a central repository where you can manage the lifecycle of
your ML models.

## Limits and Quotas

*Source: [https://cloud.google.com/vertex-ai/docs/quotas](https://cloud.google.com/vertex-ai/docs/quotas)*

Send feedback

# Gemini Enterprise Agent Platform quotas and limits Stay organized with collections Save and categorize content based on your preferences.


Google Cloud uses quotas to help ensure fairness and reduce
spikes in resource use and availability. A quota restricts how much of a
Google Cloud resource your Google Cloud project can use. Quotas
apply to a range of resource types, including hardware, software, and network
components. For example, quotas can restrict the number of API calls to a
service, the number of load balancers used concurrently by your project, or the
number of projects that you can create. Quotas protect the community of
Google Cloud users by preventing the overloading of services. Quotas also
help you to manage your own Google Cloud resources.

The Cloud Quotas system does the following:

* Monitors your consumption of Google Cloud products and services
* Restricts your consumption of those resources
* Provides a way to
  [request changes to the quota value](/docs/quotas/help/request_increase)
  and [automate quota adjustments](/docs/quotas/quota-adjuster)

In most cases, when you attempt to consume more of a resource than its quota
allows, the system blocks access to the resource, and the task that
you're trying to perform fails.

Quotas generally apply at the Google Cloud project
level. Your use of a resource in one project doesn't affect
your available quota in another project. Within a Google Cloud project, quotas
are shared across all applications and IP addresses.

For more information, see the
[Cloud Quotas overview](/docs/quotas/overview).

There are also *limits* on Gemini Enterprise Agent Platform resources. These limits are
unrelated to the quota system. Limits can't be changed.

## Rate quotas

The following quotas apply to Gemini Enterprise Agent Platform requests for a given
project and supported region. For example, in a single project, you can have up
to 30,000 online inference requests per minute in one region and another 30,000
online inference requests per minute in another supported region.

For the quotas of Gemini models, see [Generative AI on Gemini Enterprise Agent Platform
quotas and system limits](/gemini-enterprise-agent-platform/models/quotas).
For information about the quota of OpenMaaS and 3P MaaS models, see
[Gemini Enterprise Agent Platform managed models for
MaaS](/gemini-enterprise-agent-platform/models/model-garden/explore-models).

## Pricing

*Source: [https://cloud.google.com/vertex-ai/pricing](https://cloud.google.com/vertex-ai/pricing)*

Page Contents
Agent Platform pricing
Prices are listed in US Dollars (USD). If you pay in a currency other than USD, the prices listed in your currency on
Cloud Platform SKUs
apply.
Agent Platform pricing compared to legacy product pricing
The costs for Agent Platform remain the same as they are for the legacy AI Platform and AutoML products that Agent Platform supersedes, with the following exceptions:
Legacy Agent Platform Inference and AutoML Tables predictions supported lower-cost, lower-performance machine types that aren't supported for Agent Platform Inference and AutoML tabular.
Legacy Agent Platform Inference supported
scale-to-zero
, which isn't supported for Agent Platform Inference.
Agent Platform also offers more ways to optimize costs, such as the following:
Optimized TensorFlow runtime
.
Support for
co-hosting models
.
No minimum usage duration for Training and Prediction. Instead, usage is charged in 30 second increments.
Pricing for Generative AI on Agent Platform
For Generative AI on Agent Platform pricing information, see
Pricing for Generative AI on Agent Platform
.
Pricing for AutoML models
For Agent Platform AutoML models, you pay for three main activities:
Training the model
Deploying the model to an endpoint
Using the model to make predictions
Agent Platform uses predefined machine configurations for Agent Platform AutoML models, and the hourly rate for these activities reflects the resource usage.
The time required to train your model depends on the size and complexity of your training data. Models must be deployed before they can provide online predictions or online explanations.
You pay for each model deployed to an endpoint, even if no prediction is made. You must undeploy your model to stop incurring further charges. Models that are not deployed or have failed to deploy are not charged.
You pay only for compute hours used; if training fails for any reason other than a user-initiated cancellation, you are not billed for the time. You are charged for training time if you cancel the operation.
Select a model type below for pricing information.
Image data
Hourly
Hourly
Monthly
Monthly
Operation
Price (classification) (USD)
Price (object detection) (USD)
Training
$3.465 / 1 hour
$3.465 / 1 hour
Training (Edge on-device model)
$18.00 / 1 hour
$18.00 / 1 hour
Deployment and online prediction
$1.375 / 1 hour
$2.002 / 1 hour
Batch prediction
$2.222 / 1 hour
$2.222 / 1 hour
Tabular data
Hourly
Hourly
Monthly
Monthly
Operation
Price per node hour for classification/regression
Price for forecasting
Training
$21.252 / 1 hour
Refer to
Forecasting on Agent Platform
Inference
Same price as
inference for custom-trained models
.
Agent Platform performs batch inference using 40 n1-highmem-8 machines.
Refer to
Forecasting on Agent Platform
Inference charges for Vertex Explainable AI
Compute associated with Vertex Explainable AI is charged at same rate as inference.

## Gemini

*Source: [https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models)*

Send feedback

# Google models Stay organized with collections Save and categorize content based on your preferences.


## Featured Gemini models

3.5 Flash

Designed to deliver strong agentic capabilities (near-Pro level) at substantial speed and value.

* Pro-level coding proficiency and parallel agentic execution
* Features a 1 million token context window
* Near-Pro intelligence at Flash-tier cost and speed

3.1 Flash-Lite

Our most cost-efficient model, optimized for low latency use cases for high-volume, cost-sensitive LLM traffic

* Optimized for low latency and high-volume traffic
* Improved response quality and instruction following
* Improved audio input quality for ASR tasks

3.1 Flash Image
🍌

Turn ideas into production-ready assets

* Generate high-quality images
* Capable of turn-based conversational editing
* Capable of multi-image fusion and character consistency for advanced creative workflows

## Generally available Gemini models

🍌
[Gemini 3.1 Flash Image](/gemini-enterprise-agent-platform/models/gemini/3-1-flash-image)
Turn ideas into production-ready assets. Features conversational editing, multi-image fusion, and character consistency for advanced creative workflows.

🍌
[Gemini 3 Pro Image](/gemini-enterprise-agent-platform/models/gemini/3-pro-image)
High-fidelity image generation with reasoning-enhanced composition.
