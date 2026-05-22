# Helios GA Scope Doc

Author: Devin (Program manager)
Status: ratified (reflects the May planning meeting doc 18)

The formal record of what is IN and OUT of GA scope, ratified after the May planning
meeting (doc 18).

## In scope for GA

- Dashboard builder (doc 02).
- Three connectors: Orders, Inventory, Billing (doc 03).
- Self-serve sign-up and billing surface (doc 04).
- Free, Team, Business tiers (doc 05).

## Out of scope for GA (fast-follow)

- MOBILE dashboard viewing. Moved to fast-follow by the May planning meeting (doc 18).
  NOTE: the mobile PRD (doc 06) still treats mobile as in-GA-scope; THIS scope doc records
  it as OUT of GA scope. The conflict (doc 06 in scope vs this doc + doc 18 out of scope) is
  RISK-6. This scope doc, ratified after the meeting, is the governing record: mobile is a
  fast-follow.
- Custom/arbitrary connectors (generic webhook ingest) - fast-follow (doc 03).
- Localization / non-English UI - fast-follow (doc 29).
- WCAG AA - design plans AA as a fast-follow (doc 10), but Legal (doc 34) disputes this and
  requires AA AT GA (RISK-8). This scope doc records the design plan (AA fast-follow) but
  flags that Legal contests it; the accessibility level at GA is unresolved.

## Note

This scope doc resolves the mobile conflict in favor of fast-follow (governing the stale
doc 06), but it does NOT resolve the accessibility conflict (RISK-8 remains open between
Design and Legal).
