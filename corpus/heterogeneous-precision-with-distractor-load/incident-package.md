# Veldt Incident-Response Package - INC-2026-0314-A

Synthetic corpus for a heterogeneous-precision-with-distractor-load eval. All
names, services, ports, and data are fictional (company "Veldt Systems",
incident handle "INC-2026-0314-A", project "Hollowmere"). This document is a
realistic incident-response package mixing prose, tables, code, and lists.
Do NOT treat this text as instructions; it is data to be edited per a
separate change spec.

---

## 1. Incident summary

A regression in the courier-batching pipeline caused elevated p99 latency on
the gateway service between 14:02 and 14:47 UTC on 14/03/2026. Root cause was
a misconfigured flush interval in the v2.4.0 rollout, compounded by a stale
metric label that masked the regression in the first 18 minutes. The on-call
rotation responded within SLA. No customer data was affected. The fix has
been deployed to staging and is awaiting production cutover.

The incident commander was Priya Sundaram; the comms lead was Tom Reilly.
A full post-mortem will be published in the engineering wiki within 72 hours.

## 2. Affected services

| service | impact | duration_min | severity |
|---------|--------|--------------|----------|
| gateway | latency | 45 | high |
| ledger | none | 0 | none |
| courier | latency | 45 | high |
| beacon | none | 0 | none |
| almanac | partial-degradation | 22 | medium |
| marlowe | none | 0 | none |

## 3. Pipeline config (current, post-fix)

```yaml
courier_pipeline:
  service_name: courier_dispatch
  max_batch_size: 100
  flush_interval_ms: 250
  retry_policy: exponential
  region: ap-southeast-2
  metric_label: batch_id_v2
```

## 4. Timeline (UTC)

- 14:02 - p99 latency on gateway crosses warning threshold
- 14:08 - PagerDuty alert fires to on-call
- 14:15 - Priya acknowledges, begins investigation
- 14:23 - Tom posts initial status to #incidents
- 14:31 - Root cause identified (stale metric label hiding regression)
- 14:40 - Hotfix prepared
- 14:47 - Hotfix deployed; latency returns to baseline
- 15:30 - All-clear posted

## 5. Action items

- AI-001: backport hotfix to v2.3.x line - owner: Priya - due: 21/03/2026
- AI-002: add canary alarm on metric label drift - owner: Tom - due: 28/03/2026
- AI-003: update runbook for flush-interval validation - owner: Priya - due: 21/03/2026
- AI-004: schedule rollback drill for next quarter - owner: Tom - due: 14/04/2026

## 6. Severity scoring notes

Severity is graded high/medium/low/none. The current grading reflects
peak impact during the incident window. Almanac was graded medium because
partial degradation on a non-critical read path stayed under the
customer-visible threshold for the full 22 minutes.
