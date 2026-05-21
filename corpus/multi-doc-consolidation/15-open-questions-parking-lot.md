# Open Questions / Parking Lot

Synthetic corpus doc 15 of 15. A loose catch-all of unresolved items and v2
candidates, scraped from various threads. Deliberately a grab-bag.

## Still open (need a decision before launch)

- **Auth method.** SSO (doc 06) or email magic-link (doc 10)? Stated both ways in
  the planning docs. Now blocking the security review from starting (doc 12). No
  named owner for this decision yet. This is the single most cross-cutting open item.
- **Billing adapter owner.** Priya (docs 04, 07) or Marcus's team (doc 11)? Recorded
  inconsistently. Matters because the security review's caching item (doc 12) needs a
  clear owner.
- **Endpoint-tagging assignment (RISK-2).** Still no named engineer. Asked for two
  weeks running (docs 08, 13). Top escalation.
- **Security review slot.** Still not booked (docs 08, 09, 13). Hard gate for the
  billing panel.

## Decided (recorded here for completeness, decisions live in doc 09)

- Seat "request more seats" CTA: ships as a link to the sales form. Read-only safe.
- Projected month-end calc: in scope, first to cut if slip.
- Permissions: deferred to v2, shared view for v1.
- Launch date: moved to June 19 (charter doc 01 still shows the old June 12).

## v2 parking lot

- CSV export (top recurring customer ask, doc 05).
- Granular per-user permissions (Customer D, doc 05).
- Slack limit alerts (Customer F, doc 05).
- Custom report builder (parked from the start, doc 01).

## Note for whoever consolidates this

Three things are stated two different ways across these docs: the launch date, the
billing adapter owner, and the auth method. None of the three should be silently
resolved - each needs to be surfaced as a conflict with both sources named.
