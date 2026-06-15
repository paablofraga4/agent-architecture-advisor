# Project Case: Multi-Tenant SaaS AI Platform

## Problem

A technology company needed to build a multi-tenant SaaS platform that offers AI-powered document processing to small and medium businesses. Each tenant needed isolated data, per-tenant knowledge bases and usage-based billing.

## Business context

SMBs wanted AI document processing capabilities but could not afford dedicated infrastructure or AI expertise. The platform needed to provide a shared infrastructure with strong tenant isolation, predictable costs and a self-service onboarding experience.

## Requirements

- Onboard tenants through self-service with minimal configuration.
- Provide per-tenant document ingestion and knowledge base.
- Share inference infrastructure across tenants to reduce costs.
- Isolate tenant data completely.
- Track usage per tenant for billing purposes.
- Scale to hundreds of tenants with varying workloads.
- Support deployment on Azure or AWS.

## Constraints

- No tenant must be able to access another tenant's data.
- A single noisy tenant must not degrade performance for others.
- Per-tenant cost attribution must be accurate for billing.
- The platform must support tenant-level configuration such as custom prompts and document types.
- Infrastructure costs must scale sub-linearly with tenant count.

## Selected architecture

A shared-infrastructure multi-tenant architecture with logical tenant isolation was selected.

The architecture separates:
- tenant provisioning and configuration,
- per-tenant document storage and indexing,
- shared inference layer with tenant-aware routing,
- usage metering and billing,
- API gateway with tenant authentication.

## Components used

### Component: Container-based application layer

Role:
Hosts the document processing and inference orchestration services.

Azure version: Azure Container Apps.
AWS version: Amazon ECS on Fargate.

Why it was selected:
Serverless containers provide auto-scaling from zero and eliminate the need to manage underlying infrastructure. Per-request scaling aligns costs with actual tenant usage.

Alternatives considered:
Dedicated VMs per tenant were considered but would not scale economically to hundreds of tenants.

Trade-offs:
Cold start latency can affect the first request after idle periods.

### Component: Per-tenant data store

Role:
Stores tenant documents, extracted data and knowledge base content.

Azure version: Azure Cosmos DB with partition keys per tenant.
AWS version: Amazon DynamoDB with tenant-prefixed partition keys.

Why it was selected:
Partition-based isolation in a shared database provides data separation without the overhead of per-tenant database instances.

Alternatives considered:
Separate database instances per tenant were considered but are cost-prohibitive at scale.

Trade-offs:
Partition-based isolation requires careful access control to prevent cross-tenant data leakage. Hot partitions from a single active tenant can affect shared throughput in provisioned mode.

### Component: Shared inference layer

Role:
Routes inference requests to language model endpoints with tenant-aware context.

Azure version: Azure OpenAI Service.
AWS version: Amazon Bedrock.

Why it was selected:
Shared model endpoints avoid the cost of per-tenant model deployments while providing the same capabilities.

Trade-offs:
Rate limits and quotas must be managed across tenants. A single tenant with high usage can exhaust shared capacity.

### Component: API gateway

Role:
Authenticates tenants, enforces rate limits and routes requests to backend services.

Azure version: Azure API Management.
AWS version: Amazon API Gateway.

Why it was selected:
A managed API gateway provides authentication, rate limiting and usage tracking without custom infrastructure.

Trade-offs:
API gateway adds latency per request but is essential for multi-tenant security and metering.

## Why this architecture was selected

Shared infrastructure with logical isolation was selected because per-tenant dedicated infrastructure would not scale economically to the target of hundreds of SMB tenants. The architecture minimizes fixed costs per tenant while maintaining strong data isolation.

## Alternatives considered

### Dedicated infrastructure per tenant

Why it was considered:
Strongest isolation and simplest mental model.

Why it was not selected:
Cost per tenant would be too high for SMB pricing.

### Single-tenant monolith cloned per customer

Why it was considered:
Simple deployment model.

Why it was not selected:
Operational overhead of managing hundreds of independent deployments.

## Outcome

The platform onboarded over 200 tenants in the first year with infrastructure costs growing sub-linearly. Tenant isolation was maintained with zero cross-tenant data incidents.

## Lessons learned

- Noisy neighbor prevention required rate limiting at multiple layers: API gateway, inference routing and database throughput. No single layer was sufficient.
- Per-tenant cost attribution was harder than expected. Shared resources like inference endpoints required usage metering at the request level to allocate costs accurately.
- Data isolation patterns needed to be enforced at the application layer, not just the database layer. Every query and API call had to include tenant context.
- Tenant-specific configuration such as custom prompts and document schemas added complexity to the shared service layer but was essential for product differentiation.

## Reuse this pattern when

- The product serves many tenants with similar workloads.
- Per-tenant infrastructure cost must be minimized.
- Data isolation is a hard requirement.
- Usage-based billing is needed.

## Do not reuse this pattern when

- Each customer requires heavily customized infrastructure.
- The number of tenants is small and dedicated resources are affordable.
- Regulatory requirements mandate physically separate infrastructure per customer.
