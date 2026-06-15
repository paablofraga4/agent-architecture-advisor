# Architecture Pattern: Security for AI Applications

## Problem

AI applications introduce security risks that do not exist in traditional software. Prompt injection, PII leakage through LLM outputs, unauthorized access to knowledge bases and adversarial inputs require security controls beyond standard application security.

## Context

AI systems process user inputs that are passed to LLMs, retrieve information from knowledge bases and generate outputs that may be shown to users or used to trigger actions. Each of these stages presents attack surfaces that must be secured.

This pattern covers security controls across the full AI application stack.

## Requirements

- Defend against prompt injection attacks.
- Detect and redact PII in inputs and outputs.
- Filter harmful or inappropriate content.
- Control access to knowledge bases and models.
- Encrypt data at rest and in transit.
- Maintain audit logs for compliance.
- Manage API keys and credentials securely.

## Solution

Apply defense-in-depth security across input handling, model access, data protection and output validation.

### Prompt injection defense

- Validate and sanitize user inputs before including them in prompts.
- Use system prompts that instruct the model to ignore attempts to override instructions.
- Separate user content from system instructions using clear delimiters and structured prompt formats.
- Implement input classifiers that detect injection attempts before they reach the LLM.
- Limit the actions that LLM outputs can trigger. Never allow raw LLM output to execute system commands.
- Use allowlists for tool invocations rather than letting the LLM call arbitrary functions.

### PII detection and redaction

- Scan user inputs for PII (names, emails, phone numbers, addresses, SSNs) before sending to LLM APIs.
- Use dedicated PII detection services (Azure AI Language, AWS Comprehend, Google DLP) or open-source libraries (Presidio).
- Redact or mask PII in logs, traces and stored conversations.
- Apply output scanning to catch PII that the LLM may generate from its training data.

### Content filtering

- Apply input filters to block harmful, illegal or off-topic content before LLM processing.
- Apply output filters to prevent the system from returning harmful or inappropriate responses.
- Use provider-built content filters (Azure Content Safety, Bedrock Guardrails) as a baseline.
- Add custom filters for domain-specific content policies.

### RBAC for knowledge bases

- Implement role-based access control for document collections and data sources.
- Ensure retrieval results respect user permissions. A user should not receive documents they are not authorized to view.
- Apply document-level or collection-level access control in the retrieval layer.
- Map knowledge base permissions to the organization's identity system.

### Encryption

- Encrypt all data at rest using provider-managed or customer-managed keys.
- Enforce TLS for all data in transit, including internal service-to-service communication.
- Use customer-managed keys (CMK) for sensitive knowledge bases to maintain key control.
- Encrypt conversation logs and LLM traces that contain user data.

### Audit logging

- Log all LLM invocations with user identity, timestamp, model used and token counts.
- Log all knowledge base access with user identity and documents retrieved.
- Log administrative actions (model deployment, knowledge base updates, access control changes).
- Retain audit logs according to compliance requirements.
- Make audit logs tamper-resistant using append-only storage.

### Model access control

- Restrict which models and endpoints each service can access.
- Use IAM policies (AWS), managed identities (Azure) or service accounts (GCP) for model access.
- Avoid embedding API keys in application code. Use secret managers (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager).
- Rotate API keys on a regular schedule.

### API key management

- Store all API keys and credentials in a secrets manager, never in code or environment variables.
- Use short-lived tokens where possible.
- Implement key rotation without service downtime.
- Monitor key usage for anomalous patterns.

### Compliance considerations

- GDPR: implement data deletion capabilities, consent management and data processing records for EU user data.
- SOC 2: maintain audit trails, access controls and incident response procedures.
- HIPAA: apply additional encryption and access controls if processing healthcare data.
- Document which data flows through which LLM providers for data processing agreements.

## Pros

- Reduces risk of prompt injection and data leakage.
- Provides compliance evidence through audit logging.
- Protects user data across the full pipeline.
- Establishes consistent security policies across AI components.

## Cons

- Security controls add latency to request processing.
- PII detection may produce false positives that degrade user experience.
- Content filtering requires ongoing tuning to balance safety and utility.
- Compliance requirements increase development and operational effort.

## When to use this pattern

Use this pattern when:
- The AI system processes user-provided inputs.
- The system accesses sensitive or regulated data.
- Compliance requirements (GDPR, SOC 2, HIPAA) apply.
- The system is exposed to external users.
- LLM outputs trigger actions or are shown to end users.

## When not to use this pattern

Avoid full security hardening when:
- The system is an internal prototype with no sensitive data.
- The team is validating basic functionality before production.
- The system does not process user inputs or sensitive information.
