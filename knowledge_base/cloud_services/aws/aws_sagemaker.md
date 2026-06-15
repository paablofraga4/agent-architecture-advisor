# Service: Amazon SageMaker

**Provider:** aws
**Document type:** service_reference
**Category:** ai
**Tags:** ml, training, inference, endpoints
**Last updated:** 2026-06-10
**Sources:**
- [overview](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
- [limits](https://docs.aws.amazon.com/general/latest/gr/sagemaker.html)
- [pricing](https://aws.amazon.com/sagemaker/pricing/)

## Overview

# What is Amazon SageMaker AI?

Amazon SageMaker AI is a fully managed machine learning (ML) service. With SageMaker AI, data scientists and
developers can quickly and confidently build, train, and deploy ML models into a
production-ready hosted environment. It provides a UI experience for running ML workflows that
makes SageMaker AI ML tools available across multiple integrated development environments (IDEs).

With SageMaker AI, you can store and share your data without having to build and manage your own
servers. This gives you or your organizations more time to collaboratively build and develop
your ML workflow, and do it sooner. SageMaker AI provides managed ML algorithms to run efficiently
against extremely large data in a distributed environment. With built-in support for
bring-your-own-algorithms and frameworks, SageMaker AI offers flexible distributed training options that
adjust to your specific workflows. Within a few steps, you can deploy a model into a secure and
scalable environment from the SageMaker AI console.

###### Topics

* [Amazon SageMaker AI rename](#whatis-rename)
* [Amazon SageMaker and Amazon SageMaker AI](#whatis-rename-unified)
* [Pricing for Amazon SageMaker AI](#whatis-pricing)
* [Recommendations for a first-time user of Amazon SageMaker AI](./first-time-user.html)
* [Overview of machine learning with Amazon SageMaker AI](./how-it-works-mlconcepts.html)
* [Amazon SageMaker AI Features](./whatis-features.html)

## Amazon SageMaker AI rename

On December 03, 2024, Amazon SageMaker was renamed to Amazon SageMaker AI.

## Key Features

# What is Amazon SageMaker AI?

Amazon SageMaker AI is a fully managed machine learning (ML) service. With SageMaker AI, data scientists and
developers can quickly and confidently build, train, and deploy ML models into a
production-ready hosted environment. It provides a UI experience for running ML workflows that
makes SageMaker AI ML tools available across multiple integrated development environments (IDEs).

With SageMaker AI, you can store and share your data without having to build and manage your own
servers. This gives you or your organizations more time to collaboratively build and develop
your ML workflow, and do it sooner. SageMaker AI provides managed ML algorithms to run efficiently
against extremely large data in a distributed environment. With built-in support for
bring-your-own-algorithms and frameworks, SageMaker AI offers flexible distributed training options that
adjust to your specific workflows. Within a few steps, you can deploy a model into a secure and
scalable environment from the SageMaker AI console.

###### Topics

* [Amazon SageMaker AI rename](#whatis-rename)
* [Amazon SageMaker and Amazon SageMaker AI](#whatis-rename-unified)
* [Pricing for Amazon SageMaker AI](#whatis-pricing)
* [Recommendations for a first-time user of Amazon SageMaker AI](./first-time-user.html)
* [Overview of machine learning with Amazon SageMaker AI](./how-it-works-mlconcepts.html)
* [Amazon SageMaker AI Features](./whatis-features.html)

## Amazon SageMaker AI rename

On December 03, 2024, Amazon SageMaker was renamed to Amazon SageMaker AI. This name change does not apply to
any of the existing Amazon SageMaker features.

### Legacy namespaces remain the same

The `sagemaker` API namespaces, along with the following related namespaces,
remain unchanged for backward compatibility purposes.

* AWS CLI commands
* [Managed policies](https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol.html) containing `AmazonSageMaker` prefixes
* [Service
  endpoints](https://docs.aws.amazon.com/general/latest/gr/sagemaker.html) containing `sagemaker`
* [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SageMaker.html) resources containing `AWS::SageMaker` prefixes
* Service-linked role containing `AWSServiceRoleForSageMaker`
* Console URLs containing `sagemaker`
* Documentation URLs containing `sagemaker`

## Amazon SageMaker and Amazon SageMaker AI

On December 03, 2024, Amazon released the next generation of Amazon SageMaker.

Amazon SageMaker is a unified platform for data, analytics, and AI.

## Limits and Quotas

*Source: [https://docs.aws.amazon.com/general/latest/gr/sagemaker.html](https://docs.aws.amazon.com/general/latest/gr/sagemaker.html)*

# Amazon SageMaker AI endpoints and quotas

To connect programmatically to an AWS service, you use an endpoint. AWS services offer the following endpoint types
in some or all of the AWS Regions that the service supports: IPv4 endpoints, dual-stack endpoints, and FIPS endpoints.
Some services provide global endpoints. For more information, see [AWS service endpoints](./rande.html).

Service quotas, also referred to as limits, are the maximum number of service resources or operations for your AWS account.
For more information, see [AWS service quotas](./aws_service_limits.html).

The following are the service endpoints and service quotas for this service.

## Service Endpoints

The following table provides a list of Region-specific endpoints that Amazon SageMaker AI supports for
training and deploying models. This include creating and managing notebook instances,
training jobs, model, endpoint configurations, and endpoints.

| Region Name | Region | Endpoint | Protocol |
| --- | --- | --- | --- |
| US East (Ohio) | us-east-2 | api.sagemaker.us-east-2.amazonaws.com  api-fips.sagemaker.us-east-2.api.aws  api-fips.sagemaker.us-east-2.amazonaws.com  api.sagemaker.us-east-2.api.aws | HTTPS  HTTPS  HTTPS  HTTPS |
| US East (N. Virginia) | us-east-1 | api.sagemaker.us-east-1.amazonaws.com  api-fips.sagemaker.us-east-1.api.aws  api-fips.sagemaker.us-east-1.amazonaws.com  api.sagemaker.us-east-1.api.aws | HTTPS  HTTPS  HTTPS  HTTPS |
| US West (N. California) | us-west-1 | api.sagemaker.us-west-1.amazonaws.com  api-fips.sagemaker.us-west-1.api.aws  api-fips.sagemaker.us-west-1.amazonaws.com  api.sagemaker.us-west-1.api.aws | HTTPS  HTTPS  HTTPS  HTTPS |
| US West (Oregon) | us-west-2 | api.sagemaker.us-west-2.amazonaws.com  api-fips.sagemaker.us-west-2.api.aws  api-fips.sagemaker.us-west-2.amazonaws.com  api.sagemaker.us-west-2.api.aws | HTTPS  HTTPS  HTTPS  HTTPS |
| Africa (Cape Town) | af-south-1 | api.sagemaker.af-south-1.amazonaws.com  api.sagemaker.af-south-1.api.aws | HTTPS  HTTPS |
| Asia Pacific (Hong Kong) | ap-east-1 | api.sagemaker.ap-east-1.amazonaws.com  api.sagemaker.ap-east-1.api.aws | HTTPS  HTTPS |
| Asia Pacific (Hyderabad) | ap-south-2 | api.sagemaker.ap-south-2.amazonaws.com  api.sagemaker.ap-south-2.api.aws | HTTPS  HTTPS |
| Asia Pacific (Jakarta) | ap-southeast-3 | api.sagemaker.ap-southeast-3.amazonaws.com  api.sagemaker.ap-southeast-3.api.aws | HTTPS  HTTPS |
| Asia Pacific (Malaysia) | ap-southeast-5 | api.sagemaker.ap-southeast-5.amazonaws.com  api.sagemaker.ap-southeast-5.api.aws | HTTPS  HTTPS |
| Asia Pacific (Melbourne) | ap-southeast-4 | api.sagemaker.ap-southeast-4.amazonaws.com  api.sagemaker.ap-southeast-4.api.aws | HTTPS  HTTPS |
| Asia Pacific (Mumbai) | ap-south-1 | api.sagemaker.ap-south-1.amazonaws.com  api.sagemaker.ap-south-1.api.aws | HTTPS  HTTPS |
| Asia Pacific (New Zealand) | ap-southeast-6 | api.sagemaker.ap-southeast-6.amazonaws.com  api.sagemaker.ap-southeast-6.api.aws | HTTPS  HTTPS |

## Pricing

*Source: [https://aws.amazon.com/sagemaker/pricing/](https://aws.amazon.com/sagemaker/pricing/)*

Amazon SageMaker

* [Overview](/sagemaker/?nc=sn&loc=1)
* [AI](/sagemaker/ai/)
* Unified Studio
* [Catalog](/sagemaker/catalog/)
* [Customers](/sagemaker/customers/)
* More

# Amazon SageMaker pricing

[Get started for free](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html?pg=sagemakerprice&cta=herobtn&target=_blank)

[Request a pricing quote](/contact-us/sales-support/?pg=sagemakerprice&cta=herobtn&target=_blank)

## Pricing overview

Collaborate and build faster using familiar AWS tools for model development, generative AI application development, data processing, and SQL analytics, accelerated by Amazon Q Developer. Gain unified access to all your data whether it’s stored in data lakes, data warehouses, or federated data sources, with governance built-in to meet your enterprise security needs. When using Amazon SageMaker, AWS will charge you the pricing for each AWS service that you use. The pricing for each key capability of SageMaker is summarized below.

## Amazon SageMaker Unified Studio

SageMaker Unified Studio is a single data and AI development environment that provides an integrated experience to use all your data and tools for analytics and AI. SageMaker Unified Studio uses Amazon SageMaker Catalog, built on Amazon DataZone, for end-to-end governance and access control through entities such as domains, projects, and assets. You will be charged for your usage of SageMaker Catalog. SageMaker Unified Studio also provides fully managed notebooks with a built-in AI agent for data analysis by default, which support SQL, Python and natural language interactions all within a single environment. In addition, each AWS service that you use through the SageMaker Unified Studio is subject to its own individual pricing. This includes AWS storage and compute services, as well as any third-party services, like Git providers.

To accurately estimate your costs, review the individual pricing for the various AWS services available within SageMaker Unified Studio below. For detailed pricing information, consult the official AWS pricing pages for each AWS service you plan to use.

### **Quick setup option**

AWS offers a [quick setup option](https://docs.aws.amazon.com/sagemaker-unified-studio/latest/adminguide/create-domain-sagemaker-unified-studio-quick.html) to help you get started creating an AWS IAM Identity Center (IdC)-based domain. There is an additional charge for any networking resources that AWS sets up on your behalf if you choose the quick setup option for IdC-based domain creation, and exact costs depend on account configuration. Delete any unused resources to avoid unnecessary costs.
