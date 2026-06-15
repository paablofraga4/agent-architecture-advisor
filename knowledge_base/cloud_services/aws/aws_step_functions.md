# Service: AWS Step Functions

**Provider:** aws
**Document type:** service_reference
**Category:** integration
**Tags:** workflow, orchestration, state_machine
**Last updated:** 2026-06-10
**Sources:**
- [overview](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [limits](https://docs.aws.amazon.com/step-functions/latest/dg/limits-overview.html)
- [pricing](https://aws.amazon.com/step-functions/pricing/)

## Overview

# What is Step Functions?

###### Managing state and transforming data

Learn about [Passing data between states with variables](./workflow-variables.html) and [Transforming data with JSONata](./transforming-data.html).

With AWS Step Functions, you can create workflows, also called [State machines](./concepts-statemachines.html), to build distributed applications, automate processes, orchestrate
microservices, and create data and machine learning pipelines.

Step Functions is based on *state machines* and *tasks*. In Step Functions, state machines are called *workflows*, which are a series of event-driven steps. Each step in a workflow is called a *state*. For example, a [Task state](./state-task.html) represents a unit of work that another AWS service performs, such as calling another AWS service or API. Instances of running workflows performing tasks are called *executions* in Step Functions.

The work in your state machine tasks can also be done using [Activities](./concepts-activities.html) which are workers that exist outside of Step Functions.

In the Step Functions' console, you can **visualize**, edit, and
debug your applicationâs workflow. You can examine the state of each step in your workflow
to make sure that your application runs in order and as expected.

Depending on your use case, you can have Step Functions call AWS services, such as Lambda, to
perform tasks. You can have Step Functions control AWS services, such as AWS Glue, to create extract,
transform, and load workflows. You also can create long-running, automated workflows for
applications that require human interaction.

For a complete list of AWS Regions where Step Functions is available, see the [AWS
Region Table](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/).

###### Learn how to use Step Functions

Start with the [Getting started tutorial](./getting-started.html) in this guide. For advanced topics and use cases, see the modules in [The Step Functions Workshop](https://catalog.workshops.aws/stepfunctions).

## Standard and Express workflows types

Step Functions has two workflow types:

* **Standard** workflows are ideal for long-running,
  auditable workflows, as they show execution history and visual debugging.

  Standard workflows have **exactly-once** workflow
  execution and can run for up to **one year**.

## Key Features

# What is Step Functions?

###### Managing state and transforming data

Learn about [Passing data between states with variables](./workflow-variables.html) and [Transforming data with JSONata](./transforming-data.html).

With AWS Step Functions, you can create workflows, also called [State machines](./concepts-statemachines.html), to build distributed applications, automate processes, orchestrate
microservices, and create data and machine learning pipelines.

Step Functions is based on *state machines* and *tasks*. In Step Functions, state machines are called *workflows*, which are a series of event-driven steps. Each step in a workflow is called a *state*. For example, a [Task state](./state-task.html) represents a unit of work that another AWS service performs, such as calling another AWS service or API. Instances of running workflows performing tasks are called *executions* in Step Functions.

The work in your state machine tasks can also be done using [Activities](./concepts-activities.html) which are workers that exist outside of Step Functions.

In the Step Functions' console, you can **visualize**, edit, and
debug your applicationâs workflow. You can examine the state of each step in your workflow
to make sure that your application runs in order and as expected.

Depending on your use case, you can have Step Functions call AWS services, such as Lambda, to
perform tasks. You can have Step Functions control AWS services, such as AWS Glue, to create extract,
transform, and load workflows. You also can create long-running, automated workflows for
applications that require human interaction.

For a complete list of AWS Regions where Step Functions is available, see the [AWS
Region Table](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/).

###### Learn how to use Step Functions

Start with the [Getting started tutorial](./getting-started.html) in this guide. For advanced topics and use cases, see the modules in [The Step Functions Workshop](https://catalog.workshops.aws/stepfunctions).

## Standard and Express workflows types

Step Functions has two workflow types:

* **Standard** workflows are ideal for long-running,
  auditable workflows, as they show execution history and visual debugging.

  Standard workflows have **exactly-once** workflow
  execution and can run for up to **one year**.

## Limits and Quotas

*Source: [https://docs.aws.amazon.com/step-functions/latest/dg/limits-overview.html](https://docs.aws.amazon.com/step-functions/latest/dg/limits-overview.html)*

# Step Functions service quotas

AWS Step Functions provide default service quotas for state machine parameters, such as the
number of API actions during a time period or the number of state machines that you
can define. Quotas are designed to prevent misconfigured state machine from
consuming all of the resources of the system, although many do not have hard limits.

To request a service quota increase, you can do one of the following:

* Use the Service Quotas console at <https://console.aws.amazon.com/servicequotas/home>. For information about requesting a quota increase using the Service Quotas console, see [Requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html) in the *Service Quotas User Guide*.
* Use the **Support Center** page in the AWS Management Console to request a quota increase for resources provided by AWS Step Functions on a per-Region basis. For more information, see [AWS service quotas](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html) in the *AWS General Reference*.

###### Important

New AWS accounts have reduced state transition quotas. AWS raises these quotas automatically based on your usage.

###### Note

If a particular stage of your state machine execution or activity execution takes too
long, you can configure a state machine timeout to cause a timeout event.

###### Topics

* [General quotas](#service-limits-general)
* [Quotas related to accounts](#service-limits-accounts)
* [Quotas related to HTTP Task](#service-limits-http-task)
* [Quotas related to state throttling](#service-limits-api-state-throttling)
* [Quotas related to API action throttling](#service-limits-api-action-throttling-general)
* [Quotas related to state machine executions](#service-limits-state-machine-executions)
* [Quotas related to task executions](#service-limits-task-executions)
* [Quotas related to versions and aliases](#quotas-versions-aliases)
* [Restrictions related to tagging](#sfn-limits-tagging)

## General quotas

Names of state machines, executions, and activity tasks must not exceed 80 characters in length. These names must be unique for your account and AWS Region,
and must not contain any of the following:

* Whitespace
* Wildcard characters (`? *`)
* Bracket characters (`< > { } [ ]`)
* Special characters (`` " # % \ ^ | ~ ` $ & , ; : / ``)
* Control characters (`\\u0000` - `\\u001f` or `\\u007f` - `\\u009f`).

Step Functions accepts names for state machines, executions, activities, and labels that contain non-ASCII characters.

## Pricing

*Source: [https://aws.amazon.com/step-functions/pricing/](https://aws.amazon.com/step-functions/pricing/)*

AWS Step Functions

* [Overview](/step-functions/)
* [Features](/step-functions/features/)
* [Pricing](/step-functions/pricing/)
* [Use Cases](/step-functions/use-cases/)
* [Customers](/step-functions/customers/)
* More

# AWS Step Functions Pricing

[Get started for free](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html?pg=stepfuncprice&cta=herobtn)

[Request a pricing quote](/contact-us/sales-support/)

## AWS Step Functions Standard Workflows pricing details

You are charged based on the number of state transitions required to execute your application.

Step Functions counts a **state transition** each time a step of your workflow is executed. You are charged for the total number of state transitions across all your state machines, including retries.

The Step Functions free tier includes **4,000 free state transitions per month**. All charges are metered daily and billed monthly.

Free Tier


4,000 state transitions

*per month*

*The Step Functions Free Tier does not automatically expire at the end of your 12 month AWS Free Tier term, and is available to both existing and new AWS customers indefinitely.*

State Transitions


*With AWS Step Functions, you pay for the number state transitions you use per month. You are charged per state transition above the free tier. See the State Transitions Pricing Table for details. \_*

*If you include retry error handling in any steps of your workflow, each retry will be charged as an additional state transition.*

## AWS Step Functions Standard Workflow State transitions pricing

## AWS Step Functions Express Workflows pricing details

With Step Functions Express Workflows, you pay only for what you use. You are charged based on the number of requests for your workflow and its duration.

Step Functions Express Workflows counts a request each time it starts executing a workflow, and you are charged for the total number of requests across all your workflows. This includes tests from the console.

Duration is calculated from the time your workflow begins executing until it completes or otherwise terminates, rounded up to the nearest 100ms, and the amount of memory used in the execution of your workflow, billed in 64-MB chunks.

Memory consumption is based on the size of a workflow definition, the use of map or parallel states, and the execution (payload) data size. Pricing examples 3 and 4 show examples of estimating memory utilization.

## Additional charges

You may incur additional charges if the operation of your application workflow utilizes other AWS services or transfers data. For example, if your application workflow invokes an AWS Lambda function, you will be billed for each request and for the duration of each Lambda function. To invoke endpoints in private networks, such as in Amazon Virtual Private Clouds (VPC), Step Functions integrates with AWS PrivateLink and Amazon VPC Lattice.
