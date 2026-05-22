# PRD - Billing Panel (Globex Insight)

Owner: Dana (product).

## Purpose

The billing panel shows each customer their current plan, usage-based charges, and
invoice history.

## Data sources

- Invoice records from the billing system.
- Usage-based charge lines computed from consumption events in the data pipeline.

## Dependencies

- Depends on the data pipeline (consumption events).
- Depends on the dashboard authentication.
- Depends on the billing system read access being provisioned.

## Notes

- Invoice history depth shown to customers should match the data retention policy (see
  the compliance memo for the retention period and the activity-panel PRD for the
  retention figure used there - confirm they agree before build).
