# Helios Glossary and Cast

Author: Devin (Program manager)
Status: reference

Reference list of people and terms. Introduces no conflicts; helps a consolidation attribute
positions to the right owners.

## Cast (fictional)

- Lena - Product, dashboard surface and connectors (docs 02, 03, 05, 16).
- Priya - Product, Commerce; pricing and billing surface (docs 04, 26).
- Sol - Product, mobile (doc 06).
- Mara - Research and analytics (docs 07, 27).
- Devin - Program manager; status, scope, risk register, comms (docs 08, 12, 13, 17, 18, 24,
  36, 37, 41, 42, 43).
- Arman - Data platform; aggregation service, data store (docs 09, 25, 32, 38).
- Noor - Design; design system, auth UX, accessibility (docs 10, 15, 29).
- Theo - Platform engineering; architecture, infra, ops/SLA (docs 11, 19, 23, 33).
- Quinn - QA (doc 14).
- Bea - Support (doc 21).
- Raj - Billing platform; claims billing-adapter ownership (doc 22) - DISPUTED vs Dana (doc
  04), RISK-3.
- Dana - named in the billing PRD (doc 04) as the billing-adapter owner - DISPUTED vs Raj's
  team (doc 22), RISK-3. (Dana and Dana-Lee are different people: Dana is engineering, Dana-Lee
  is Legal.)
- Dana-Lee - Legal; accessibility and contract terms (doc 34).
- Kira - Marketing; GTM (doc 30).
- Owen - Sales; beta and pipeline (doc 31).
- Sasha - Security and Privacy; security review and retention policy (docs 20, 28).

## Key contested terms (pointers to the conflicts, not assertions)

- GA date: September 15 (stale, docs 01/08/13/17) vs October 6 (current, docs 18/24/30),
  RISK-2.
- Auth: SSO (doc 09) vs magic-link (doc 15), RISK-5.
- Pricing: per-seat (doc 26) vs usage-based (doc 39), RISK-12.
- Data store: Initech Warehouse (docs 09/25/38) vs Postgres (doc 11), RISK-7.
- Retention: 90 days (doc 28) vs 180 days (doc 11), RISK-9.
- Regions at GA: US-only (docs 01/11) vs US+EU (docs 23/30), RISK-13.
- Free-tier rows: 10,000 (doc 05) vs 25,000 (doc 26), RISK-4.
- SLA: 99.9 percent (docs 01/05) vs 99.5 percent (doc 33), RISK-11.
- Accessibility: A at GA (docs 10/15) vs AA at GA (doc 34), RISK-8.
- Billing-adapter owner: Dana (doc 04) vs Raj's team (doc 22), RISK-3.
- Post-launch on-call: Platform team (docs 11/33) vs new Helios team (doc 35), RISK-10.
- Launch budget: 250k (doc 30) vs 180k (doc 40), RISK-14.
- Mobile at GA: in scope (doc 06) vs fast-follow (docs 18/37), RISK-6.
- Security status: green (doc 24) vs pending/blocked (doc 20), RISK-15.
- Beta count: 12 pre-churn (docs 08/17) vs 8 post-churn (docs 24/31), reconcilable via 4 churn.
