# PRD - API Call Volume Panel

Synthetic corpus doc 3 of 15. Second of the three v1 panels.

## Overview

The API Call Volume panel shows a customer their API request counts over time,
broken down by endpoint category, with their plan's monthly quota marked. This is
the panel customers ask about most often in the support tickets the charter cites.

## Requirements

- Daily and monthly API call totals.
- Breakdown by endpoint category (read, write, admin).
- The plan quota line overlaid, with projected month-end usage.
- A 90-day history.

## Data dependency

Also reads from the aggregation service (06-data-pipeline-notes.md), same hard
upstream dependency as the Seat Usage panel. Additionally, the endpoint-category
breakdown needs a new tagging step in the ingestion path that does not exist yet -
this is extra scope on top of the base aggregation service and is the single
riskiest data item in the project (see 07-risk-register.md, RISK-2).

## Owner

Panel owner: Marcus's team end to end (data-heavy panel, less design surface).

## Note

The projected month-end usage calc was descoped once already in an earlier review,
then added back when GTM argued it is the strongest upsell trigger. It is currently
IN scope but is the first thing to cut if the timeline slips (decision logged in
09-meeting-summary.md).
