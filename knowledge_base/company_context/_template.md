# Company Context: [Company Name]

**Document type:** company_context

## Organization

- **Industry:** [e.g. financial services, healthcare, retail]
- **Size:** [employees, revenue range]
- **Engineering team:** [size, seniority distribution]
- **Cloud maturity:** [early | intermediate | advanced]

## Cloud Strategy

- **Primary cloud:** [azure | aws | gcp]
- **Secondary cloud:** [if any]
- **Multi-cloud policy:** [yes/no, why]
- **Cloud spend:** [monthly range]

## Existing Infrastructure

<!-- What's already deployed. The advisor uses this to avoid recommending
     things that conflict with existing investments. -->

- **Identity:** [Azure AD, AWS IAM, Google Workspace, Okta, etc.]
- **Networking:** [VPN, ExpressRoute, Direct Connect, etc.]
- **CI/CD:** [GitHub Actions, Azure DevOps, Jenkins, etc.]
- **Monitoring:** [Datadog, CloudWatch, Azure Monitor, etc.]
- **Databases in use:** [PostgreSQL, MongoDB, DynamoDB, etc.]

## Compliance Requirements

- **Regulations:** [GDPR, HIPAA, SOC2, PCI-DSS, etc.]
- **Data residency:** [required regions]
- **Encryption requirements:** [at rest, in transit, customer-managed keys]
- **Audit requirements:** [logging, retention periods]

## Team Skills

<!-- What the team knows well vs what requires ramp-up -->

- **Strong in:** [e.g. Python, Azure Functions, PostgreSQL]
- **Learning:** [e.g. Kubernetes, Terraform, React]
- **No experience:** [e.g. GCP, ML/AI ops]

## Architecture Principles

<!-- Company-specific principles that override generic best practices -->

- [e.g. "Prefer serverless over containers for new projects"]
- [e.g. "All data must stay in EU regions"]
- [e.g. "Use managed services — no self-hosted databases"]

## Known Constraints

- [e.g. "Enterprise agreement with Azure — 30% discount on compute"]
- [e.g. "Security team requires private endpoints for all services"]
- [e.g. "Budget approval needed for services >$500/month"]

## Preferred Vendors / Services

<!-- Services the company has already evaluated and prefers -->

- [e.g. "Auth0 for authentication (company-wide contract)"]
- [e.g. "Datadog for monitoring (already deployed)"]
