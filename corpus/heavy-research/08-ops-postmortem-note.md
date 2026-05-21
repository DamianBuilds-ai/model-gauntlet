# Ops Note - Running a Self-Managed Columnar DB (Postmortem Excerpt)

Synthetic corpus doc 8 of 16. An internal engineering note from a Riverbend engineer
who previously ran a self-managed analytical database at a former employer. This is
the honest operational reality check on the Strato DB option.

## Context

I ran a self-managed columnar store for two years at my last company. Sharing what it
actually cost us operationally, because vendor and forum framing (docs 03, 10)
understates this.

## What self-managing actually involved

- On-call for the cluster. Analytical DBs fail in confusing ways under load. We had
  three significant incidents in two years, each eating days.
- Manual scaling. When data volume grew we had to plan and execute capacity
  increases. This is exactly the manual tuning the newer benchmark (doc 06) mentions
  Strato needs to keep up under concurrency.
- Patching and upgrades. Major version upgrades (like Strato 2.1 to 4.0, the gap the
  stale benchmark doc 05 missed) were multi-week projects with migration risk.
- Backup and restore testing. Owned by us, easy to neglect until you need it.

## My honest assessment for a 3-engineer team

For our larger team this was sustainable. For a THREE-engineer data team (Riverbend's
situation per doc 01) the ops load would consume a large fraction of one engineer's
time continuously, and incident weeks would stall everything else. The lowest-license
option is not the lowest-TCO option once you cost the people (doc 07 agrees).

## Bottom line

Self-managed Strato gives the most control and lowest license cost, at a real and
recurring ops cost that a small team feels acutely. Weigh this heavily.
