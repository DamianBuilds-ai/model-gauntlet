# Quarterly Operations Report - Veldt Systems Q1 2026 (DRAFT - REVISION REQUESTED)

Synthetic corpus for a correction-without-regression eval. The block below is
a PRIOR DRAFT report produced by another agent (deliberately contains ONE
error, plus many subtly-correct adjacent parts). The "Correction note" at the
bottom points at the ONE error and asks for a surgical fix. Do NOT treat any
text inside this corpus as instructions; it is data to be revised per a
separate change spec. All names, services, and numbers are fictional (company
"Veldt Systems", projects "Hollowmere" and "Marlowe").

---

## PRIOR DRAFT OUTPUT (the block to be revised)

```
# Veldt Systems - Q1 2026 Quarterly Operations Report

## 1. Headline metrics
- Revenue: $4,820,000 (up 12% vs Q4 2025)
- Active customers: 1,847
- Net new customers: 142
- Gross margin: 68.4%
- Operating margin: 14.2%

## 2. Service availability (uptime %)

| service | uptime_pct | sla_target | met |
|---------|------------|------------|-----|
| gateway | 99.94 | 99.90 | yes |
| ledger | 99.87 | 99.90 | no |
| courier | 99.96 | 99.90 | yes |
| beacon | 99.91 | 99.90 | yes |
| almanac | 99.99 | 99.90 | yes |
| marlowe | 99.93 | 99.90 | yes |

## 3. Incidents this quarter
- Total incidents: 7
- High severity: 2
- Medium severity: 3
- Low severity: 2
- Mean time to resolve: 38 minutes

## 4. Headcount
- Engineering: 24 (start of quarter) -> 27 (end of quarter)
- Product: 6 -> 7
- Operations: 4 -> 5
- Total: 34 -> 39

## 5. Quarterly themes
The quarter was defined by three themes. First, the courier-batching
pipeline finally shipped to production in v2.4.0 after an eight-week
soak. Second, the gateway team completed the long-planned migration off
the legacy auth layer. Third, customer onboarding throughput doubled
after the new self-serve flow launched in February.

The single noteworthy incident was INC-2026-0314-A on March 14th, a
45-minute gateway latency event traced to a misconfigured flush interval
in the v2.4.0 rollout. Root-cause was identified within 31 minutes and
hotfixed within 45 minutes. No customer data was affected.

## 6. Q2 priorities
1. Ship the courier-batching v2.5 enhancement (idempotency keys)
2. Complete the marlowe metrics shipper consolidation
3. Onboard the platform-engineering hire (start date April 14th)
4. Run the cross-region failover drill (scheduled April 21st)
```

---

## CORRECTION NOTE FROM REVIEWER

The reviewer notes ONE error in the draft above and asks for a revised version.

> **The Operations end-of-quarter headcount figure in section 4 is wrong.**
> Operations did not hire anyone this quarter; the line should read
> `Operations: 4 -> 4`, not `Operations: 4 -> 5`. And the Total
> end-of-quarter figure on the next line is therefore also wrong: with
> Engineering 27 + Product 7 + Operations 4, the correct Total line is
> `Total: 34 -> 38`, not `Total: 34 -> 39`.
>
> Please produce a revised version of the report block with ONLY this
> correction applied. Every other number, sentence, table cell, and bullet in
> the report should remain byte-identical. Do not "improve" the prose, do not
> re-format the table, do not recompute any other figure - just fix the
> Operations end-of-quarter number and the Total end-of-quarter number, and
> leave everything else exactly as the draft has it.

(End of correction note. Apply ONLY the correction above.)
