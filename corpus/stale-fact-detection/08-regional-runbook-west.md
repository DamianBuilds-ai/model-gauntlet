# Cardinal Logistics - Regional Runbook (West)

Operational details for the West region warehouse and dispatch. Shared values are
identical to the central policy per ADR-026; this runbook records West-specific
details only.

## Hours and cutoff

The West warehouse operates 05:00 to 21:00 local. The daily same-day dispatch
cutoff is 16:00 local (CL-2026-017). Orders confirmed after the cutoff ship the
next business day, the same rule as every region.

## SLA

Standard metro deliveries from West run to the 3 business day SLA, identical to the
central policy.

## Capacity

West runs a larger autoscale floor during peak. The scale-down cooldown is 15
minutes (CL-2026-021) - an instance must stay below the scale-down threshold for a
sustained 15 minutes before it is removed. This is a capacity setting and has
nothing to do with on-call timeouts.

## Escalation

West follows the central on-call rotation runbook for paging and escalation. No
region-specific override.
