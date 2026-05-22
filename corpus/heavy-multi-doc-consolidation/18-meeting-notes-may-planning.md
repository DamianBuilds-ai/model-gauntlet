# Helios May Planning Meeting Notes

Date: May (mid-project re-plan)
Attendees: steering group, workstream leads
Author: Devin

## Key decisions (these SUPERSEDE the kickoff doc 13 and charter doc 01 where they differ)

1. GA DATE MOVED. GA is moved from September 15 to October 6. The reason: the
   aggregation-service work (doc 09, RISK-1) and the unresolved auth decision (RISK-5)
   will not both land in time for September 15. October 6 is the new committed GA date.
   This supersedes the September 15 in the charter (doc 01) and the kickoff (doc 13).
   The week-3 status (doc 24) and the GTM plan (doc 30) reflect October 6; the week-1
   (doc 08) and week-2 (doc 17) statuses predate this meeting and still show September
   15.

2. MOBILE MOVED TO FAST-FOLLOW. Mobile dashboard viewing is moved OUT of GA scope to a
   fast-follow after launch. This supersedes the mobile PRD (doc 06), which still treats
   mobile as in-GA-scope. The formal scope doc (doc 37) records mobile as out of GA scope
   per this decision.

## Items explicitly NOT decided at this meeting

- The auth method (SSO vs magic-link) was discussed but NOT decided; it remains open and
  blocking the security review. The meeting noted it as the top risk to the new October 6
  date.
- The pricing model (per-seat vs usage-based) was deferred again to an exec memo (doc 39).
- The analytics data-store conflict (Initech Warehouse vs Postgres) was flagged but not
  resolved.

## Note for consolidation

This is the LATER, governing meeting. Its date (October 6) and its mobile decision
(fast-follow) override the earlier kickoff and charter values. A consolidator should
treat October 6 as the current GA date and call out that the charter/week-1/week-2 docs
carry the stale September 15.
