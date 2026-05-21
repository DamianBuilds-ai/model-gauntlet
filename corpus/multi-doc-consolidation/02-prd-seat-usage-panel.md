# PRD - Seat Usage Panel

Synthetic corpus doc 2 of 15. Product requirements for the first of the three v1
panels described in 01-project-charter.md.

## Overview

The Seat Usage panel shows a customer how many seats they have provisioned vs how
many are actively used (logged in within the last 30 days). This is the panel most
directly tied to the upsell goal in the charter: customers near their seat cap are
the ones GTM wants to nudge.

## Requirements

- Show provisioned seats, active seats (30-day), and percent utilisation.
- A visual band that turns amber at 80 percent utilisation and red at 95 percent.
- A 90-day sparkline of active-seat trend.

## Data dependency

This panel reads from the new aggregation service (see 06-data-pipeline-notes.md).
It does NOT query the production billing database directly - that was ruled out on
load grounds. The aggregation service must be live before this panel can ship. This
is a hard upstream dependency.

## Owner

Panel owner: Priya (design lead) for the UI, Marcus's team for the data wiring.

## Open question

GTM (Sam) wants a "request more seats" call to action button in the amber/red state
that opens a sales conversation. Eng flagged this is borderline a write action and
v1 is read-only per the charter. Unresolved - tracked in 09-meeting-summary.md.
