# Service: AWS Lambda

**Provider:** aws
**Document type:** service_reference
**Category:** compute
**Tags:** serverless, functions, event_driven
**Last updated:** 2026-06-15
**Sources:**
- [overview](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [limits](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)
- [pricing](https://aws.amazon.com/lambda/pricing/)

## Overview

# What is AWS Lambda?

###### Tip

Join Serverless experts for free hands-on workshops to learn how to build Serverless
applications with best practices. [Click here](https://aws-experience.com/amer/smb/events/series/Get-Hands-On-With-Serverless?trk=188abe3e-9f94-4e84-aefb-398d944ad567%26sc_channel%3Del) to sign up.

AWS Lambda is a compute service that runs code without the need to manage servers. Your code runs, scaling up and down automatically, with pay-per-use pricing.
To get started, see [Create your first function](./getting-started.html).

You can use Lambda for:

* **File processing**: Process files automatically when uploaded to Amazon Simple Storage Service. See [file processing examples](./example-apps.html#examples-apps-file) for details.
* **Long-running workflows:** Use [durable Lambda functions](./durable-functions.html) to build stateful, multi-step workflows that can run for up to one year. Perfect for order processing, approval workflows, human-in-the-loop processes, and complex data pipelines that need to remember their progress.
* **Database operations and integration examples**: Respond to database changes and automate data workflows. See [database examples](./example-apps.html#examples-apps-database) for details.
* **Scheduled and periodic tasks**: Run automated operations on a regular schedule using EventBridge. See [scheduled task examples](./example-apps.html#examples-apps-scheduled) for details.
* **Stream processing**: Process real-time data streams for analytics and monitoring. See [Kinesis Data Streams](./with-kinesis.html) for details.
* **Web applications**: Build scalable web apps that automatically adjust to demand.
* **Mobile backends**: Create secure API backends for mobile and web applications.
* **IoT backends**: Handle web, mobile, IoT, and third-party API requests. See [IoT](./services-iot.html) for details.

For pricing information, see [AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/).

## Functions and durable functions

[Lambda functions](./lambda-functions-chapter.html)
run for up to 15 minutes and are ideal for event-driven tasks like processing API requests, handling
file uploads, or responding to database changes. [Durable functions](./durable-functions.html)
extend this model for workloads that need to run longer and survive interruptions. They can execute for
up to one year, automatically checkpointing their progress so they resume reliably after failures.

## Key Features

# What is AWS Lambda?

###### Tip

Join Serverless experts for free hands-on workshops to learn how to build Serverless
applications with best practices. [Click here](https://aws-experience.com/amer/smb/events/series/Get-Hands-On-With-Serverless?trk=188abe3e-9f94-4e84-aefb-398d944ad567%26sc_channel%3Del) to sign up.

AWS Lambda is a compute service that runs code without the need to manage servers. Your code runs, scaling up and down automatically, with pay-per-use pricing.
To get started, see [Create your first function](./getting-started.html).

You can use Lambda for:

* **File processing**: Process files automatically when uploaded to Amazon Simple Storage Service. See [file processing examples](./example-apps.html#examples-apps-file) for details.
* **Long-running workflows:** Use [durable Lambda functions](./durable-functions.html) to build stateful, multi-step workflows that can run for up to one year. Perfect for order processing, approval workflows, human-in-the-loop processes, and complex data pipelines that need to remember their progress.
* **Database operations and integration examples**: Respond to database changes and automate data workflows. See [database examples](./example-apps.html#examples-apps-database) for details.
* **Scheduled and periodic tasks**: Run automated operations on a regular schedule using EventBridge. See [scheduled task examples](./example-apps.html#examples-apps-scheduled) for details.
* **Stream processing**: Process real-time data streams for analytics and monitoring. See [Kinesis Data Streams](./with-kinesis.html) for details.
* **Web applications**: Build scalable web apps that automatically adjust to demand.
* **Mobile backends**: Create secure API backends for mobile and web applications.
* **IoT backends**: Handle web, mobile, IoT, and third-party API requests. See [IoT](./services-iot.html) for details.

For pricing information, see [AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/).

## Functions and durable functions

[Lambda functions](./lambda-functions-chapter.html)
run for up to 15 minutes and are ideal for event-driven tasks like processing API requests, handling
file uploads, or responding to database changes. [Durable functions](./durable-functions.html)
extend this model for workloads that need to run longer and survive interruptions. They can execute for
up to one year, automatically checkpointing their progress so they resume reliably after failures. Use
durable functions when you need multi-step workflows, human-in-the-loop approvals, or coordination
across services over extended periods.

## How Lambda works

When using Lambda, you are responsible only for your code.

## Limits and Quotas

*Source: [https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)*

# Lambda quotas

###### Important

New AWS accounts have reduced concurrency and memory quotas. AWS raises these quotas automatically based on your usage.

AWS Lambda is designed to scale rapidly to meet demand, allowing your functions to scale up to serve traffic
in your application. Lambda is designed for short-lived compute tasks that do not retain or rely upon state between
invocations. Code can run for up to 15 minutes in a single invocation and a single function can use up to
10,240 MB of memory.

Itâs important to understand the guardrails that are put in place to protect your account and the workloads of
other customers. Service quotas exist in all AWS services and consist of hard limits, which you cannot change,
and soft limits, which you can request increases for. By default, all new accounts are assigned a quota profile
that allows exploration of AWS services.

To see the quotas that apply to your account, navigate to the
[Service Quotas dashboard](https://console.aws.amazon.com/servicequotas/home). Here, you can view
your service quotas, request a quota increase, and view current utilization. From here, you can drill down to a
specific AWS service, such as Lambda:

The following sections list default quotas and limits in Lambda by category.

###### Topics

* [Compute and storage](#compute-and-storage)
* [Function configuration, deployment, and execution](#function-configuration-deployment-and-execution)
* [Lambda API requests](#api-requests)
* [Other services](#quotas-other-services)

## Compute and storage

Lambda sets quotas for the amount of compute and storage resources that you can use to run and store functions.
Quotas for concurrent executions and storage apply per AWS Region. Elastic network interface (ENI) quotas apply
per virtual private cloud (VPC), regardless of Region. The following quotas can be increased from their default
values. For more information, see [Requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html) in the
*Service Quotas User Guide*.

| Resource | Default quota | Can be increased up to |
| --- | --- | --- |
| Concurrent executions | 1,000 | Tens of thousands |
| Storage for uploaded functions (.zip file archives) and layers. Each function version and layer version consumes storage.  For best practices on managing your code storage, see [Monitoring Lambda code storage](https://serverlessland.com/content/service/lambda/guides/aws-lambda-operator-guide/code-storage) in Serverless Land. | 75 GB | Terabytes |
| Storage for functions defined as container images. These images are stored in Amazon ECR. | See [Amazon ECR service quotas](https://docs.aws.amazon.com/AmazonECR/latest/userguide/service-quotas.html). |  |
| [Elastic network interfaces per virtual private cloud (VPC)](./configuration-vpc.html)  Note  This quota is shared with other services, such as Amazon Elastic File System (Amazon EFS).

## Pricing

*Source: [https://aws.amazon.com/lambda/pricing/](https://aws.amazon.com/lambda/pricing/)*

AWS Lambda

* [Overview](/lambda/)
* Features
* [Pricing](/lambda/pricing/)
* [Getting Started](/lambda/getting-started/)
* [Resources](/lambda/resources/)
* More

# AWS Lambda pricing

[Get started for free](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html?pg=lambdaprice&cta=herobtn)

[Request a pricing quote](/contact-us/sales-support/?pg=lambdaprice&cta=herobtn)

## Overview

AWS Lambda is a serverless compute service that lets you run code without provisioning or managing servers. Create workload-aware cluster scaling logic, maintain event integrations, and manage runtimes with ease. With Lambda, you can run code for virtually any type of application or backend service, all with zero administration, and only pay for what you use. You are charged based on the number of requests for your functions and the duration it takes for your code to execute.

Lambda counts a request each time it starts executing in response to an event notification trigger, such as from Amazon Simple Notification Service (SNS) or Amazon EventBridge, or an invoke call, such as from Amazon API Gateway, or via the AWS SDK, including test invokes from the AWS Console.

Duration is calculated from the time your code begins executing until it returns or otherwise terminates, rounded up to the nearest 1 ms\*. The price depends on the amount of memory you allocate to your function. In the AWS Lambda resource model, you choose the amount of memory you want for your function, and are allocated proportional CPU power and other resources. An increase in memory size triggers an equivalent increase in CPU available to your function. To learn more, see the [Function Configuration documentation.](https://docs.aws.amazon.com/lambda/latest/dg/resource-model.html)

You can run your Lambda functions on processors built on either x86 or Arm architectures. AWS Lambda functions running on Graviton2, using an Arm-based processor architecture designed by AWS, deliver up to 34% better price performance compared to functions running on x86 processors. This applies to a variety of serverless workloads, such as web and mobile backends, data, and media processing.

\* Duration charges apply to code that runs in the handler of a function as well as initialization code that is declared outside of the handler. For Lambda functions with [AWS Lambda Extensions](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-extensions-api.html), duration also includes the time it takes for code in the last running extension to finish executing during shutdown phase. For Lambda functions configured with [SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html), duration also includes the time it takes for the runtime to load, any code that runs in a [runtime hook](https://docs.aws.amazon.com/lambda/latest/dg/snapstart-runtime-hooks.html), and the initialization code executed during creation of copies of snapshots created for resilience.
