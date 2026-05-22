# PRD - Helios Dashboard Builder

Author: Lena (Product, dashboard surface)
Status: in progress

## Summary

The dashboard builder is the core surface of Helios. Users drag fields onto a canvas,
pick a visualization, and the builder renders a live chart against their connected
data. This PRD covers the builder only; the connectors are specified separately in
doc 03 and the billing surface in doc 04.

## Key requirements

- A user can build a dashboard with up to 20 widgets.
- Widgets refresh on a schedule the user picks (5 minutes, 15 minutes, hourly, daily).
- Dashboards can be shared read-only with other users in the same account.
- The builder must render the first widget within 2 seconds on a typical dataset
  (the performance bar agreed with the Platform team in doc 11).

## Dependencies

- The builder reads from the aggregation service described in the data-pipeline notes
  (doc 09). The aggregation service is the shared upstream for both the builder and
  the connectors; if it slips, the builder slips.
- The builder's sharing feature depends on the auth/identity decision (docs 09 and 15
  disagree on the auth method; this PRD assumes whatever auth ships, sharing is scoped
  to same-account users).

## Open question

Mobile rendering of dashboards is requested by sales (doc 31) but mobile scope is
contested (see doc 06 and the meeting summary doc 18). This PRD does not commit to
mobile; it defers to the scope decision.
