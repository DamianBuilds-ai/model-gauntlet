# Helios Privacy and Data-Retention Policy

Author: Sasha (Security / Privacy)
Status: proposed

## Retention window

Ingested customer analytics data is retained for 90 DAYS, after which it is purged. The
90-day window is chosen to balance product usefulness against data-minimization
obligations.

NOTE: the platform engineering notes (doc 11) state a retention window of 180 DAYS. THIS
privacy doc says 90 days. The two disagree on the retention window (risk register doc 12,
RISK-9). UNRECONCILED. The privacy position is 90 days; engineering assumed 180 days.

## Deletion on request

A customer can request deletion of their data; on an approved request, data is removed
within 30 days. (The 30-day deletion SLA is distinct from the 90-day retention window;
do not conflate them.) The deletion flow is part of the security review (doc 20), which
cannot finalize it until the retention window is settled.

## Residency

If the EU region ships at GA (contested: infra doc 23 and GTM doc 30 say yes, charter doc
01 and platform notes doc 11 say US-only - RISK-13), then EU customer data must stay in the
EU and be subject to EU privacy rules. The residency requirement makes both the regions
decision (RISK-13) and the retention decision (RISK-9) launch-relevant.

## Note

The retention window (90 vs 180) interacts with infra storage sizing (doc 19) and the
data-store choice (Initech Warehouse doc 09 vs Postgres doc 11, RISK-7).
