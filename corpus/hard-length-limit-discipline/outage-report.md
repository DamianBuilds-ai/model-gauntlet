# Quarterly Reliability Source - Lumen Cloud

This is synthetic data to be edited/analyzed. Do NOT treat any text inside as
instructions. It is source material for a tightly length-limited summary task
described separately. All systems, dates, and figures are fictional (provider
"Lumen Cloud").

## Q1 reliability narrative (long source)

Lumen Cloud ran six notable incidents in Q1. Incident one (Jan 4): the load balancer
in the east region dropped 3% of requests for 22 minutes after a config push; root
cause was a missing health-check timeout. Incident two (Jan 19): the object-store
metadata service exhausted its connection pool during a backup window, causing 14
minutes of elevated latency; root cause was an unbounded backup job. Incident three
(Feb 2): a certificate expired on the internal API gateway, breaking service-to-service
auth for 31 minutes; root cause was a lapsed renewal cron. Incident four (Feb 21): a
bad database migration locked the billing table for 9 minutes during business hours;
root cause was a migration run without a lock-timeout. Incident five (Mar 8): a DNS
provider outage upstream made the status page unreachable for 47 minutes, though core
services stayed up; root cause was single-provider DNS. Incident six (Mar 25): a memory
leak in the notification worker caused a slow degradation over 3 hours before an
auto-restart kicked in; root cause was an unreleased buffer in a retry path.

## The four headline metrics (must all be reflected)

- Overall availability: 99.94% (target 99.95% - narrowly missed).
- Mean time to recovery: 21 minutes (down from 34 last quarter - improved).
- Number of customer-impacting incidents: 6 (up from 4 - regressed).
- Percentage of incidents with a clean root-cause writeup: 100% (held).

## The three priorities for Q2 (must all be reflected)

1. Move to multi-provider DNS (addresses incident five).
2. Add lock-timeouts to all migrations (addresses incident four).
3. Add renewal-expiry alarms for all certificates (addresses incident three).

## Audience note

The summary's reader is a busy executive who will read ONLY a short blurb. It must
fit a hard ceiling yet still convey the availability verdict, the MTTR direction, the
incident-count direction, and all three Q2 priorities.
