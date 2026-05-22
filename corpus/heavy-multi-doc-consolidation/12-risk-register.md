# Helios Risk Register

Owner: Devin (Program manager)
Status: living document

This register tracks the open risks and the cross-document conflicts. Each conflict is
given a RISK id. A consolidator should surface every one of these and NOT silently pick
a winner where the source documents disagree.

- RISK-1 (critical): the aggregation service (doc 09) is the shared upstream for BOTH
  the dashboard builder (doc 02) AND the connectors (doc 03). A slip blocks both. This
  is the highest-fanout dependency. Owner: Arman.
- RISK-2 (high): launch date conflict. The charter (doc 01) says September 15. The May
  planning meeting (doc 18) moved GA to October 6, and that later date is carried in the
  week-3 status (doc 24) and the GTM plan (doc 30). The week-1 status (doc 08) still
  cites September 15. UNRECONCILED in the source set - the later meeting date should
  govern but several docs still show the old date.
- RISK-3 (high): billing-adapter owner conflict. The billing PRD (doc 04) says Dana
  owns the billing adapter. The billing-integration notes (doc 22) say Raj's team owns
  it. UNRECONCILED.
- RISK-4 (medium): Free-tier row-cap conflict. The product spec (doc 05) says 10,000
  rows. The pricing doc (doc 26) says 25,000 rows. UNRECONCILED.
- RISK-5 (critical): auth-method conflict. The data-pipeline notes (doc 09) specify SSO
  (SAML). The design notes (doc 15) specify email magic-link. This blocks the security
  review (doc 20) from starting. UNRECONCILED and load-bearing.
- RISK-6 (medium): mobile-at-GA conflict. The mobile PRD (doc 06) says mobile is in GA
  scope. The planning meeting (doc 18) and the scope doc (doc 37) say mobile is a
  fast-follow, out of GA scope. UNRECONCILED.
- RISK-7 (high): analytics data-store conflict. The data-pipeline notes (doc 09) say the
  system of record is the Initech Warehouse. The platform engineering notes (doc 11) say
  Postgres. UNRECONCILED.
- RISK-8 (medium): accessibility-level conflict. Legal (doc 34) requires WCAG 2.1 AA at
  GA. Design (doc 10) plans level A at GA with AA as a fast-follow. UNRECONCILED.
- RISK-9 (medium): retention-window conflict. Privacy (doc 28) says 90 days. Platform
  engineering (doc 11) says 180 days. UNRECONCILED.
- RISK-10 (medium): post-launch on-call ownership conflict. Platform engineering (doc
  11) expects to own Helios on-call. The org doc (doc 35) says a new Helios team owns it.
  UNRECONCILED.
- RISK-11 (low): SLA conflict. The charter (doc 01) and product spec (doc 05) say 99.9
  percent uptime. The ops/SLA doc (doc 33) says 99.5 percent. UNRECONCILED.
- RISK-12 (medium): pricing-model conflict. The pricing doc (doc 26) specifies per-seat
  pricing. The exec memo (doc 39) proposes usage-based pricing and is later. UNRECONCILED
  pending exec decision.
- RISK-13 (low): regions-at-GA conflict. The charter (doc 01) and platform notes (doc 11)
  say US-only at GA. The infra doc (doc 23) and GTM plan (doc 30) say US + EU at GA.
  UNRECONCILED.
- RISK-14 (low): GA marketing-budget conflict. The GTM plan (doc 30) cites a 250k launch
  budget. The finance doc (doc 40) approves 180k. UNRECONCILED.
- RISK-15 (medium): security sign-off STATUS conflict. The security review (doc 20) says
  sign-off is pending and blocked on auth. The week-3 status (doc 24) reports security as
  "complete / green". The status overstates; UNRECONCILED.
