# Support and SLA Comparison

Synthetic corpus doc 15 of 16. A comparison of vendor support and availability
guarantees - an ops-burden tradeoff that interacts with the small-team constraint.

## Support model per option

- **Lumen Cloud:** 24/7 vendor support with a contractual uptime SLA. If the platform
  has an incident, it is the VENDOR's pager, not Riverbend's. For a 3-engineer team
  this offloads availability risk almost entirely.
- **Strato DB:** community support plus optional paid third-party support contracts.
  No vendor uptime SLA - availability is RIVERBEND's responsibility (consistent with
  the postmortem doc 08). The team carries the pager.
- **Beacon Analytics:** business-hours vendor support on the standard plan, 24/7 only
  on the premium plan. Uptime SLA exists but is weaker than Lumen's on the standard
  tier.

## Interaction with team size

This is another lens on the same core tradeoff: the smaller the team, the more
valuable a vendor-carried SLA becomes, because the team cannot absorb being the
last line of defence for availability. Riverbend's 3-engineer constraint (doc 01)
makes Lumen's vendor SLA a meaningful, costable benefit and makes Strato's
self-owned availability a meaningful, costable risk.

## Note

Do not double-count: the ops/people cost in doc 07 already partly reflects this. But
the SLA dimension adds the availability-RISK angle (tail risk of extended downtime),
which the cost model averages rather than captures as variance.
