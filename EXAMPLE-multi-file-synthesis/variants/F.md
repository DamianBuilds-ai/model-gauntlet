---
schemaVersion: 1
tier: builder
status: complete
tool_budget_used: 4
---

# Acme Logistics - Status Brief

## Cross-cutting threads

1. **Webhook signing.** The changelog has HMAC planned for v3.3.0, TICK-4460 has
   three customers blocked on it, and the roadmap commits it this quarter and flags
   unsigned payloads as the top security risk. Clear three-file thread.
2. **Throughput and batch.** The 120 rpm limit and `/shipments/batch` from the
   changelog answer the dropped-jobs complaint in TICK-4455, and Sales wants batch
   promoted in onboarding per the roadmap.

## Top 3 issues by combined urgency

1. **HMAC signing** - committed, high demand, security-flagged.
2. **Free-tier webhook drops** - TICK-4471, high severity.
3. **Throughput churn** - TICK-4455 plus the Sales onboarding ask.

## Agreement and open question

- The files agree on webhook signing being the top priority.
- Open question: whether GraphQL is versioned separately from REST (raised in the
  changelog, undecided in the roadmap).

## Recommended next actions

1. Ship HMAC signing per the v3.3.0 commitment.
2. Reproduce the TICK-4471 free-tier drop.
3. Promote the batch endpoint in onboarding.
4. Confirm the timezone fix to the affected account (TICK-4431).
