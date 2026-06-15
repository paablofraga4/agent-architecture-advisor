# Capacity planning & NFR heuristics for cloud AI systems

**Provider:** neutral
**Document type:** architecture_pattern
**Tags:** sizing, capacity, nfr, latency, throughput, cost, slo

Heuristics a senior engineer uses to turn vague requirements into numbers. Always label
outputs as estimates and state the assumptions.

## Translating "scale" into numbers
- Ask for or assume: daily active users, requests per user per day, peak-to-average ratio.
- Peak RPS ≈ (DAU × req/user/day × peak_factor) / 86,400. Peak factor 3–10× for business apps.
- Concurrency ≈ peak RPS × avg request seconds (Little's Law). 50 RPS × 2 s = ~100 in flight.

## Availability math
- 99.9% ≈ 43 min/month down; 99.95% ≈ 22 min; 99.99% ≈ 4.4 min.
- Serial dependencies multiply: two 99.9% services in series ≈ 99.8% combined.
- Each extra nine roughly multiplies cost and operational complexity — justify it.

## Latency budgeting
- p99 end-to-end = sum of each hop's p99 plus queueing. Build a budget table per hop.
- Network round trips and cross-region calls add tens of ms each; keep the hot path in-region.
- For LLMs, time-to-first-token matters more than total time — stream.

## Storage & data
- Hot vs warm vs cold tiers: match access pattern to storage class to cut cost.
- Index/replica overhead is typically 1.5–3× raw data size.
- Cross-region egress and inter-AZ traffic are billed — colocate chatty components.

## Compute sizing
- Serverless when duty cycle < ~40% or traffic is spiky; provisioned when steady & high.
- Autoscale on a leading signal (queue depth, concurrency) not lagging CPU.
- Headroom: target ~60–70% utilization at peak so autoscaling has time to react.

## Cost levers, cheapest first
1. Cache (responses, embeddings) and dedupe work.
2. Right-size instances / pick the correct SKU and tier.
3. Move spiky load to consumption pricing.
4. Commit (reservations / savings plans) only for proven steady baseline.
