# Helios Infra Deployment - Regions Plan

Author: Theo (Platform engineering)
Status: proposed

## Regions at GA

This deployment plan provisions Helios in TWO regions at GA: US and EU. The EU region is
included at GA to serve the EU residency requirement raised in customer research (doc 07,
interview 5) and assumed by the GTM plan (doc 30).

NOTE: the charter (doc 01) commits to US-ONLY at GA, with EU as a post-GA expansion. The
platform engineering notes (doc 11) also assume US-only at GA. THIS doc plans US + EU at
GA. So the regions-at-GA question is in conflict: charter doc 01 and platform notes doc 11
say US-only; this infra doc 23 and the GTM plan doc 30 say US + EU. UNRECONCILED (risk
register doc 12, RISK-13).

## EU specifics

If EU ships at GA, EU customer data stays in the EU region (residency), which interacts
with the data-retention policy (90 days doc 28 vs 180 days doc 11) and the privacy
posture (doc 28). EU residency makes the retention decision more urgent.

## Note

The decision on regions at GA is above this doc's authority; this is the infra TEAM's
recommendation (US + EU) which the steering group has not ratified against the charter's
US-only commitment.
