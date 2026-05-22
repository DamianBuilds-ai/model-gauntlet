# PRD - Usage Panel (Globex Insight)

Owner: Dana (product).

## Purpose

The usage panel shows each customer their consumption over time: API calls, seats
used, and feature adoption.

## Audience / scale

- The dashboard will be available to all REGISTERED customer accounts. We currently
  have about 4,000 registered accounts.
- (Note: "registered accounts" is a different metric from "monthly active accounts" -
  see the customer-research notes for the active figure.)

## Data sources

- Consumption events from the data pipeline.
- Seat counts from the billing system.

## Dependencies

- Depends on the data pipeline (see data-pipeline notes).
- Depends on the dashboard authentication being in place.

## Open items

- Final panel layout pending design review.
