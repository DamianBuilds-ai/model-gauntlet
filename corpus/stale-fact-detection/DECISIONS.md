# Cardinal Logistics - Decisions Log (ADRs)

Architecture and operational decision records. Each has an id, a date, a status
(proposed / accepted / rejected / superseded), and the decision. The decisions log
is authoritative for WHY a change was made; the changelog is authoritative for WHEN
a value changed. A decision with status "rejected" did NOT take effect - the prior
state stands.

---

## ADR-026 (2026-02-18) - status: accepted

Adopt regional warehouse runbooks (East and West) as separate documents so each
region can record its own dock and carrier details, with shared values (cutoff,
SLA) kept identical to the central policy.

## ADR-028 (2026-03-05) - status: REJECTED

Proposal: widen the deploy freeze window from the current Friday-12:00-to-Monday-09:00
to a full Thursday-to-Monday freeze, to reduce weekend on-call load. REJECTED after
review - the team judged the wider freeze would bunch too many releases into
mid-week and slow delivery. The freeze window therefore REMAINS Friday 12:00 local
to Monday 09:00 local. No change; the runbook value stands as-is.

## ADR-031 (2026-03-18) - status: accepted

Reduce the on-call acknowledgement timeout from 15 minutes to 10 minutes. Context:
the 2026-03-14 incident saw a Sev-2 page sit for nearly the full 15-minute window
before escalation, delaying response. Decision: the primary on-call now has 10
minutes to acknowledge a page before it rolls to the secondary. This is the
standard escalation timeout for every rotation effective immediately. Recorded in
the changelog as CL-2026-014. All on-call documentation must reflect 10 minutes.

## ADR-033 (2026-04-12) - status: accepted

Standardise the API rate limit headers across all services so every response
carries the remaining-quota header. Does not change the limit itself (600 req/min
per CL-2026-009); concerns header presence only.
