# Service: Amazon Bedrock

**Provider:** aws
**Document type:** service_reference
**Category:** ai
**Tags:** llm, foundation_models, agents, rag, knowledge_bases
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html)
- [quotas](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html)
- [pricing](https://aws.amazon.com/bedrock/pricing/)
- [agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)

## Overview

# Overview

Amazon Bedrock is a fully managed service that provides secure, enterprise-grade access to [high-performing foundation models](./models.html) from leading AI companies, enabling you to build and scale generative AI applications.

## Quickstart

Read the [Quickstart](./getting-started.html) to write your first API call using Amazon Bedrock in under five minutes.

Messages API
:   ```
    import anthropic

    client = anthropic.Anthropic()

    response = client.messages.create(
        model="anthropic.claude-opus-4-7",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Can you explain the features of Amazon Bedrock?"}]
    )
    print(response)
    ```

Responses API
:   ```
    from openai import OpenAI

    client = OpenAI()

    response = client.responses.create(
        model="openai.gpt-oss-120b",
        input="Can you explain the features of Amazon Bedrock?"
        )
    print(response)
    ```

Chat Completions API
:   ```
    from openai import OpenAI

    client = OpenAI()

    response = client.chat.completions.create(
        model="openai.gpt-oss-120b",
        messages=[{"role": "user", "content": "Can you explain the features of Amazon Bedrock?"}]
        )
    print(response)
    ```

Converse API
:   ```
    import boto3

    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    response = client.converse(
        modelId='anthropic.claude-opus-4-7',
        messages=[
            {
                'role': 'user',
                'content': [{'text': 'Can you explain the features of Amazon Bedrock?'}]
            }
        ]
    )
    print(response)
    ```

Invoke API
:   ```
    import json
    import boto3

    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    response = client.invoke_model(
        modelId='anthropic.claude-opus-4-7',
        body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'messages': [{ 'role': 'user', 'content': 'Can you explain the features of Amazon Bedrock?'}],
                'max_tokens': 1024
        })
     )
     print(json.loads(response['body'].read()))
    ```

## Supported models

Bedrock supports [100+ foundation models](./models.html) from industry-leading providers, including Amazon, Anthropic, DeepSeek, Moonshot AI, MiniMax, and OpenAI.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **Amazon Nova** | **Claude** | **DeepSeek** | **Kimi** | **MiniMax** | **OpenAI** |


## Limits and Quotas

*Source: [https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html)*

# Quotas for Amazon Bedrock

Your AWS account has default quotas, formerly referred to as limits, for Amazon Bedrock. To view
service quotas for Amazon Bedrock, do one of the following:

* Follow the steps at [Viewing service
  quotas](https://docs.aws.amazon.com/servicequotas/latest/userguide/gs-request-quota.html) and select **Amazon Bedrock** as the service.
* Refer to the [Amazon Bedrock service quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#limits_bedrock) in the AWS General Reference.

Model inference in Amazon Bedrock is controlled by quotas on token usage. Some models use tokens at a higher rate. For more information about these rates and how to optimize your token usage, see [How tokens are counted in Amazon Bedrock](./quotas-token-burndown.html).

Amazon Bedrock offers two inference endpoints â `bedrock-runtime` and `bedrock-mantle` â each with its own per-model quota allocations. Traffic to the two endpoints is tracked against separate quotas, even when calling the same underlying model. For details, see [Quotas for the bedrock-runtime endpoint](./quotas-runtime.html) and [Quotas for the bedrock-mantle endpoint](./quotas-mantle.html).

To maintain the performance of the service and to ensure appropriate usage of Amazon Bedrock, the
default quotas assigned to an account might be updated depending on regional factors,
payment history, fraudulent usage, and/or approval of a [quota increase request](./quotas-increase.html).

###### Topics

* [How tokens are counted in Amazon Bedrock](./quotas-token-burndown.html)
* [Monitor your token usage by counting tokens before running inference](./count-tokens.html)
* [Quotas for the bedrock-runtime endpoint](./quotas-runtime.html)
* [Quotas for the bedrock-mantle endpoint](./quotas-mantle.html)
* [Request an increase for Amazon Bedrock quotas](./quotas-increase.html)

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Code examples

Token counting

## Pricing

*Source: [https://aws.amazon.com/bedrock/pricing/](https://aws.amazon.com/bedrock/pricing/)*

Amazon Bedrock

* [Overview](/bedrock/)
* [Getting Started](/bedrock/getting-started/)
* Capabilities
* Agents
* [Pricing](/bedrock/pricing/)
* More

# Amazon Bedrock pricing

[Get started for free](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html?pg=sagemakerprice&cta=herobtn&target=_blank)

[Request a pricing quote](/contact-us/sales-support/?pg=sagemakerprice&cta=herobtn&target=_blank)

* Model Pricing
* Knowledge Bases
* Guardrails
* Model Evaluation
* Data Automation
* Intelligent Prompt Routing
* Prompt Optimization

* Model Pricing
* ### Model Pricing

  Pricing is dependent on the modality, provider, and model. Please select the model provider to see detailed pricing.

  Amazon Bedrock supports a variety of tiers including Standard, Flex, Priority, and Reserved tiers. [Click to learn more about service tiers](/bedrock/service-tiers/ "Bedrock service tiers").

  Amazon Bedrock offers select foundation models (FMs) from leading AI providers like Anthropic, Meta, Mistral AI, and Amazon for batch inference at a 50% lower price compared to on-demand inference pricing. To learn more about Batch, click [here](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html "batch tier"). Please refer to model list [here](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference-supported.html "model list").

  + AI21 Labs
  + Amazon
  + Anthropic
  + Cohere
  + DeepSeek
  + Google
  + Luma AI
  + Meta
  + MiniMax AI
  + Mistral AI
  + Moonshot AI
  + NVIDIA
  + OpenAI
  + Qwen
  + Stability AI
  + TwelveLabs
  + Writer
  + Z AI
  + Custom Model Import
  + AI21 Labs
  + #### AI21 Labs

    **On-Demand pricing**
  + Amazon
  + - Amazon Nova
    - Amazon Titan
    - Other Amazon
    - Amazon Nova
    - ## Amazon Nova

      ### Pricing for Understanding Models

      #### Global Cross-region Inference

      #### Geo Cross-region inference and in-region

      ### Built-In-Tools

      ### Pricing for Creative Content Generation models

      ### Pricing for Speech Understanding and Generation Models

      ### On-Demand pricing for speech to speech foundation models

      **Note:** \*The text tokens input and output pricing applies to specific use cases such as speech-to-text transcription, tool calls for task completion or knowledge grounding, adding conversation history to the session etc.

      On-demand inference for custom Nova models is priced the same as base Nova inference.

      ### Pricing for Embedding models
    - Amazon Titan
    - ## Amazon Titan
    - Other Amazon
  + Anthropic
  + ## Anthropic

    **On-Demand and Batch pricing**

    **Models with extended access**

    |  |  |  |  |  |  |  |  |  |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Agents

*Source: [https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)*

# Automate tasks in your application using AI agents

Amazon Bedrock Agents offers you the ability to build and configure autonomous agents in your
application. An agent helps your end-users complete actions based on organization data and
user input. Agents orchestrate interactions between foundation models (FMs), data sources,
software applications, and user conversations. In addition, agents automatically call APIs
to take actions and invoke knowledge bases to supplement information for these actions.
By integrating agents, you can accelerate your development effort to deliver generative artificial intelligence (generative AI) applications.

With agents, you can automate tasks for your customers and answer questions for them. For
example, you can create an agent that helps customers process insurance claims or an agent
that helps customers make travel reservations. You don't have to provision capacity, manage
infrastructure, or write custom code. Amazon Bedrock manages prompt engineering, memory, monitoring,
encryption, user permissions, and API invocation.

Agents perform the following tasks:

* Extend foundation models to understand user requests and break down the tasks that
  the agent must perform into smaller steps.
* Collect additional information from a user through natural conversation.
* Take actions to fulfill a customer's request by making API calls to your company
  systems.
* Augment performance and accuracy by querying data sources.

To use an agent, you perform the following steps:

1. (Optional) Create a knowledge base to store your private data in that database. For more information, see [Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases](./knowledge-base.html).
2. Configure an agent for your use case and add at least one of the following components:

   * At least one action group that the agent can perform.
