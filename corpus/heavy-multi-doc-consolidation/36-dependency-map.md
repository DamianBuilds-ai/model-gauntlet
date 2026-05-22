# Helios Dependency Map

Author: Devin (Program manager)
Status: reference

A compact map of the cross-document dependency chains. Introduces no new conflicts; it
restates the chains so a consolidation can trace them. The conflicts themselves are in the
risk register (doc 12).

## Critical-path chains

1. Aggregation service (doc 09/25) -> BOTH dashboard builder (doc 02) AND connectors (doc
   03). Highest fanout (RISK-1). A slip here slips the whole GA.
2. Auth decision (SSO doc 09 vs magic-link doc 15, RISK-5) -> security review (doc 20) ->
   GA exit criteria (QA doc 14). Auth is undecided, so the security review is blocked, so a
   hard GA gate is blocked. This is the critical-path conflict.
3. Pricing model (per-seat doc 26 vs usage-based doc 39, RISK-12) -> billing surface (doc
   04) AND billing adapter (doc 22) AND GTM messaging (doc 30) AND analytics instrumentation
   (doc 27). Four things wait on the pricing decision.
4. Free-tier row cap (10,000 doc 05 vs 25,000 doc 26, RISK-4) -> billing surface display
   (doc 04) AND onboarding copy (doc 16) AND support FAQ (doc 21) AND conversion funnel
   (doc 27).
5. Retention window (90 doc 28 vs 180 doc 11, RISK-9) -> infra storage sizing (doc 19) AND
   deletion flow / security review (doc 20) AND EU residency (doc 23/28).
6. Regions at GA (US-only doc 01/11 vs US+EU doc 23/30, RISK-13) -> infra deployment (doc
   23) AND privacy/residency (doc 28) AND GTM markets (doc 30).
7. Data store (Initech Warehouse doc 09 vs Postgres doc 11, RISK-7) -> aggregation service
   query path (doc 25) AND QA integrity tests (doc 14) AND infra storage profile (doc 19).

## Date and status chains

- GA date: kickoff/charter September 15 (doc 01/13) SUPERSEDED by May meeting October 6
  (doc 18), carried into week-3 status (doc 24) and GTM (doc 30); week-1 (doc 08) and week-2
  (doc 17) still show the stale September 15 (RISK-2).
- Security status: week-3 status (doc 24) says green; security review (doc 20) says
  pending/blocked. Doc 20 governs (RISK-15).
