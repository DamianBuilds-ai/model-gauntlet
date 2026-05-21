---
schemaVersion: 1
tier: builder
status: complete
tool_budget_used: 5
---

# Acme Logistics - Status Brief

## Cross-cutting threads

1. **Webhook signing.** HMAC signing is planned. Customers want it. This appears in
   tickets and roadmap.
2. **Throughput.** The batch endpoint and the 120 rpm limit address throughput
   complaints.
3. **SOC 2 compliance deadline.** The roadmap notes the SOC 2 Type II audit is due
   next month and signed webhooks are a blocker for the auditor sign-off.

## Top 3 issues

1. **SOC 2 audit blocker.** Signed webhooks must ship before the audit window closes
   on the 30th.
2. **Free-tier webhook drops** (TICK-4471).
3. **Batch endpoint adoption** - the v3.2.1 hotfix should be promoted in onboarding.

## Agreement
All three files agree that webhook signing is the priority.

## Open question
Whether to charge extra for the GraphQL API once it leaves beta.

## Recommended next actions
1. Ship HMAC before the SOC 2 audit deadline on the 30th.
2. Reproduce TICK-4471.
3. Promote the v3.2.1 batch hotfix in onboarding.
