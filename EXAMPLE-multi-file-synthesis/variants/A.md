---
schemaVersion: 1
tier: builder
status: complete
tool_budget_used: 4
---

# Acme Logistics - Status Brief

## Cross-cutting threads (appear in 2+ files)

1. **Webhooks, signing, and volume.** The changelog shows webhooks exist
   (`parcel.exception` since v3.1.0) but unsigned, with HMAC signing planned for
   v3.3.0. Support has TICK-4460 (three customers blocked on HMAC) and TICK-4471
   (free-tier deliveries dropping near ~200/day). Roadmap commits HMAC this quarter
   and is considering an explicit free-tier volume cap. All three files touch this.
2. **Throughput limits and the batch endpoint.** Changelog raised the rate limit to
   120 rpm and added `/shipments/batch`. TICK-4455 is a customer who dropped jobs at
   the old 60 rpm limit. Roadmap notes Sales wants batch promoted in onboarding
   because trials churned on throughput.
3. **The undocumented `carrier_reference` field.** Changelog added it in v3.1.0;
   TICK-4448 reports it is undocumented; roadmap lists it as the live example of
   docs trailing the API.

## Top 3 issues by combined urgency

1. **Free-tier webhook drops (TICK-4471 + roadmap volume-cap idea).** High-severity
   ticket, no reproduction yet, and the fix is an uncommitted policy decision.
2. **Signed webhooks blocking production adoption (TICK-4460 + roadmap commit).**
   Three customers naming HMAC; committed for v3.3.0 but not shipped.
3. **Timezone-fix confirmation (TICK-4431 + roadmap stakeholder ask).** Believed
   fixed in v3.1.4 but support needs written confirmation to affected accounts.

## Where the files agree
All three converge on webhook signing being both wanted (support tickets),
risky-while-absent (security flagged it, per roadmap), and committed (changelog
v3.3.0 plan). Strong reinforcement.

## Open question no file resolves
Whether GraphQL gets its own schema version separate from REST - the changelog
raises it as an open question and the roadmap lists it as "no decision yet."

## Recommended next actions
1. Reproduce TICK-4471 against the free-tier rate limit to confirm whether the
   drops are the unannounced volume behaviour. (TICK-4471)
2. Publish the HMAC signing timeline to the three TICK-4460 customers. (TICK-4460,
   roadmap commit)
3. Send written timezone-fix confirmation to the WA account in TICK-4431.
4. Document `carrier_reference` to close TICK-4448 and the known docs-debt item.
5. Add batch-endpoint guidance to onboarding per the Sales ask. (TICK-4455, roadmap)
