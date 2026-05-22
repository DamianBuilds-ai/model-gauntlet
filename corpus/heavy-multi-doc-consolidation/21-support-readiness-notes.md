# Helios Support Readiness Notes

Author: Bea (Support lead)
Status: in progress

## Support model at GA

- Free tier: community support only (doc 05).
- Team tier: email support.
- Business tier: priority support.

## Readiness items

- Support needs final docs on the connector setup (doc 03) and the billing/upgrade flow
  (doc 04). The upgrade flow is blocked on the pricing model (per-seat doc 26 vs
  usage-based doc 39), so support cannot finalize the billing FAQ yet.
- Support needs to know the Free-tier row cap to answer "why am I blocked" tickets. That
  number is contested (10,000 doc 05 vs 25,000 doc 26, RISK-4), so the FAQ has a
  placeholder.
- Support needs the data-retention answer for deletion questions; 90 days (doc 28) vs
  180 days (doc 11) is unresolved (RISK-9).

## Staffing

Support staffing assumes the GA date. Since the GA date moved from September 15 to
October 6 (doc 18), support has rescheduled its readiness milestones to the October 6
date. (Support is one of the few docs that already reflects the new date.)

## Escalation

Engineering escalations go to whoever owns Helios on-call post-launch - which is itself
contested (Platform team doc 11 vs new Helios team doc 35, RISK-10). Support has flagged
that it does not currently know who to escalate to after GA.
