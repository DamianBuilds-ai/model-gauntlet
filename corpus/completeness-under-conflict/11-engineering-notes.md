# Engineering Notes - Globex Insight Build

Author: Theo (platform/eng lead).

## Ownership

- The Globex Insight dashboard delivery is owned by Theo's platform team end to end -
  Theo's team owns the dashboard build and its delivery.

  (Note: the activity-panel PRD names Dana as the dashboard owner. Product-owner vs
  delivery-owner may be the intent, but as written the two docs both claim dashboard
  ownership and this is unreconciled.)

## Architecture

- Serving store fronted by a cache layer for read bursts.
- A separate read replica handles heavy analytical reads.

  (The cache layer and the read replica are distinct components; this matches the
  data-pipeline notes.)

## Build status

- Pipeline ingestion: in progress.
- Panels: usage scaffolded, billing and activity not started.
- Auth: blocked on the method decision.

## Dependencies

- Blocked on the auth method decision before wiring sign-in.
- Endpoint tagging (RISK-5) needed before the usage panel is complete.
