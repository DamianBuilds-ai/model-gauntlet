# Ops Postmortem Note - Self-Hosted Support Tool (prior company)

Author: the ops lead, recounting experience running a self-hosted support suite at a
previous employer (a team of similar size to Cardinal). Shared as direct evidence for
the Quillstack operating-burden question.

## What happened

We ran a self-hosted, open-source support platform comparable to Quillstack with no
dedicated platform engineer. For the first few quiet months it was fine. Then:

- A peak-season spike hit and we had NOT pre-scaled. The console slowed to the point
  agents could not work for most of a day while we scrambled to add capacity. Manual
  scaling is only as good as the person remembering to do it ahead of time.
- A version upgrade went sideways and took the instance down for half a day; the
  rollback was not clean because backup verification had quietly lapsed.
- Patching slipped repeatedly because it always lost to higher-priority day-job work.
  We carried known-unpatched components for weeks at a time.

## Costed impact

The two outages plus the chronic patching debt cost us, conservatively, the equivalent
of several weeks of disrupted support over the year - far more than any subscription
saving from going open source. The hidden cost of self-hosting without a platform
engineer is not the infrastructure bill, it is the operating attention you do not have.

## Recommendation from experience

For a small team with no platform engineer, a managed platform is worth the
subscription premium. Do not be seduced by a zero-license figure.
