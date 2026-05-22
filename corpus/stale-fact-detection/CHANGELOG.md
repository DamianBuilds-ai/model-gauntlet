# Cardinal Logistics - Platform Changelog

The authoritative chronological record of operational and platform changes. Each
entry has an id, a date, and a description. The most recent entries are at the
bottom. When a value changes, the change is recorded here; downstream documents
are expected to be updated to match.

---

## CL-2026-003 (2026-01-09)

Standard delivery SLA confirmed at 3 business days for the metro service tier. No
change from the prior policy; logged for the record during the policy review.

## CL-2026-009 (2026-02-02)

API rate limit raised from 300 requests per minute to 600 requests per minute per
API key, after capacity testing showed headroom. All clients and internal services
updated. The config reference and onboarding guide were updated to 600 in the same
release.

## CL-2026-011 (2026-02-21)

Hot-log retention set to 15 days in the logging pipeline (previously ad hoc). The
security policy and config reference both record 15 days.

## CL-2026-014 (2026-03-18)

On-call acknowledgement timeout reduced from 15 minutes to 10 minutes following the
2026-03-14 missed-page incident, where a 15-minute window let a Sev-2 sit
unacknowledged too long before rolling to the secondary. The shorter 10-minute
window is now the standard escalation timeout for all rotations. See ADR-031.

## CL-2026-017 (2026-04-02)

Warehouse daily cutoff time standardised at 16:00 local across all regions for
same-day dispatch. Regional runbooks and onboarding updated.

## CL-2026-021 (2026-04-30)

Autoscale scale-down cooldown set to 15 minutes (the period a service must remain
below the scale-down threshold before an instance is removed). Unrelated to the
on-call escalation timeout; recorded here to avoid confusion with other 15-minute
windows.
