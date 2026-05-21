# Industry Analyst Note - Managed vs Self-Managed Analytics

Synthetic corpus doc 11 of 16. A short note from an industry analyst firm. Reasonably
balanced and current; a reliable source on the general tradeoff and on Beacon's BI
flexibility.

## On the managed-vs-self-managed question

The analyst's framing: the right choice is dominated less by raw performance (the
platforms have converged - see current benchmarks) and more by TEAM OPERATING
CAPACITY and total cost of ownership. Small teams systematically underestimate the
ops cost of self-managed analytical databases. This matches Riverbend's postmortem
(doc 08) and cost model (doc 07).

## On the three categories

- Managed consumption warehouses (Lumen-like): best when ops capacity is scarce and
  you can tolerate variable, volume-scaling bills.
- Self-managed columnar (Strato-like): best for teams with real platform-engineering
  depth who want control and lowest license cost and can absorb the ops load.
- Bundled managed analytics with built-in BI (Beacon-like): fastest to value for
  business users, but the built-in BI layer trades flexibility, and such platforms
  often lag dedicated warehouses on heavy interactive latency (consistent with doc 06).

## On Beacon's BI layer specifically

The analyst notes bundled BI layers are great for standard dashboards but power users
hit ceilings on custom modelling. Reasonable for a company whose analytics needs are
mostly standard reporting, limiting for one with sophisticated/custom needs.

## Net

A current, balanced source. Use it to anchor the general framing; pair its conclusions
with the Riverbend-specific cost (doc 07), ops (doc 08), and compliance (doc 09)
constraints.
