---
schemaVersion: 1
tier: builder
status: complete
tool_budget_used: 4
---

# Acme Logistics - Product Status Brief

## 1. Cross-cutting threads (present in 2+ files)

| Thread | Changelog | Support tickets | Roadmap |
|--------|-----------|-----------------|---------|
| Webhook signing (HMAC) | planned v3.3.0, currently unsigned | TICK-4460 (3 customers blocked) | committed this quarter, security top-risk |
| Webhook volume / reliability | `parcel.exception` since v3.1.0 | TICK-4471 (free-tier drops ~200/day) | volume-cap under consideration, no SLA (debt) |
| Throughput / batch | `/shipments/batch`, 60->120 rpm | TICK-4455 (dropped jobs at 60 rpm) | Sales wants batch promoted in onboarding |
| Docs lag | `carrier_reference` added v3.1.0 | TICK-4448 (field undocumented) | named as the live docs-debt example |
| Timezone fix | shipped v3.1.4 | TICK-4431 (WA carrier wants confirmation) | stakeholder ask to communicate it in writing |

The brief's value is the column overlap: every row above is corroborated by at
least two independent sources.

## 2. Top 3 issues by combined urgency

1. **Free-tier webhook drops (TICK-4471 + unresolved volume policy).** High severity,
   not yet reproduced, and the corrective action (an explicit free-tier cap) is
   uncommitted. Highest combined urgency because customer impact is active AND the
   fix path is undecided.
2. **HMAC signing as an adoption blocker (TICK-4460 + committed roadmap item +
   security top-risk).** Three customers naming HMAC; committed for v3.3.0 but not
   shipped. High urgency, but the path is at least decided.
3. **Timezone-fix confirmation (TICK-4431 + stakeholder ask).** Lower technical
   severity (the fix already shipped in v3.1.4) but it is an easy, owed follow-up
   that is currently dropping.

## 3. Reinforcement and the open question

- **Files agree:** webhook signing is wanted (TICK-4460), risky while absent
  (roadmap security flag), and committed (changelog v3.3.0). Three-way alignment.
- **Open question no file resolves:** whether the GraphQL schema is versioned
  separately from REST. The changelog raises it as an open question; the roadmap
  lists it as "no decision yet." Neither commits.

## 4. Recommended next actions

1. **Reproduce TICK-4471 against the free-tier limits** to confirm whether the drops
   are an unannounced volume behaviour, then decide the cap policy. (TICK-4471, roadmap)
2. **Communicate the HMAC timeline to the three TICK-4460 customers** so they can plan
   their production cutover. (TICK-4460, roadmap commit)
3. **Send written confirmation of the v3.1.4 timezone fix** to the WA account.
   (TICK-4431, stakeholder ask)
4. **Document `carrier_reference`** to close TICK-4448 and chip at the docs-debt item.
5. **Add batch-endpoint guidance to onboarding** to address throughput-driven churn.
   (TICK-4455, Sales ask)
