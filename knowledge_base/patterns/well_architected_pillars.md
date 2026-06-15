# Well-Architected: the five pillars for AI/RAG systems

**Provider:** neutral
**Document type:** architecture_pattern
**Tags:** well_architected, nfr, reliability, security, cost, performance, operations

A senior review of any cloud architecture checks it against five pillars. Use them as
a checklist when proposing or judging a design.

## 1. Reliability
- Define availability targets as numbers: 99.9% = ~43 min/month of downtime; 99.95% = ~22 min.
- Set RPO (max data loss) and RTO (max time to recover) explicitly per data store.
- Design for failure: multi-AZ by default; multi-region only when RTO/compliance demands it.
- Decouple with queues so a downstream outage applies backpressure instead of cascading.
- Idempotency + retries with exponential backoff and jitter on every network call.

## 2. Security
- Encrypt at rest (provider-managed or customer-managed keys/CMK) and in transit (TLS 1.2+).
- Private networking (private endpoints / VPC) so data planes are not exposed publicly.
- Least-privilege identity (managed identities / IAM roles), no long-lived static keys.
- Secrets in a managed vault, never in code or env files committed to git.
- For regulated data: data residency region pinning, audit logging, and PII classification.

## 3. Cost optimization
- Know the cost drivers before quoting: per-token (LLM), per-hour (provisioned), per-GB
  (storage/egress), per-request (serverless). Egress between regions is a silent killer.
- Prefer serverless/consumption for spiky or low-volume workloads; reserved/provisioned
  for steady high-utilization (>~60% duty cycle).
- Cache embeddings and LLM responses; the cheapest token is the one you don't send.
- Right-size first, autoscale second, commit (reservations/savings plans) last.

## 4. Performance efficiency
- Budget latency end-to-end: p99 target = sum of each hop's p99. RAG ≈ retrieval +
  rerank + LLM generation; the LLM call usually dominates (hundreds of ms to seconds).
- Size for peak concurrency (RPS/TPS), not average. Provision replicas to hold p99 under load.
- Use hybrid (vector + keyword) retrieval for recall on exact terms (IDs, article numbers).
- Stream tokens to cut perceived latency on long generations.

## 5. Operational excellence
- Everything as code (IaC), reproducible deploys, no click-ops in production.
- Observability: traces, structured logs, and golden-signal dashboards (latency, errors,
  saturation, traffic). For LLMs add token usage, cost, and grounding/eval metrics.
- Define SLOs and alert on error budget burn, not on raw CPU.
