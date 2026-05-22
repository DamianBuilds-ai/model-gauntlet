# Helios Open Questions - Parking Lot

Author: Devin (Program manager)
Status: living list

Loose open questions not yet promoted to the risk register (doc 12). Some are minor; none
introduce a NEW cross-doc conflict beyond what is already tracked, but they record open
threads a consolidation should mention as undecided.

- Should the connector incremental sync cadence be faster than 15 minutes for some sources?
  Interview 2 (doc 07) asked for near-real-time. Currently a fast-follow, undecided.
- Should dashboards allow more than 20 widgets? Interview 1 (doc 07) asked. Undecided;
  current cap is 20 (doc 02).
- What is the exact deletion SLA wording for the contract? Privacy (doc 28) says 30 days to
  honor a deletion request; Legal (doc 34) to confirm contract language. Open.
- Who signs off the final GA go/no-go? The steering group (doc 01), but the criteria include
  the blocked security sign-off (doc 20), so the go/no-go cannot be scheduled until auth
  (RISK-5) is decided. Open.
- Will the EU region (if it ships, RISK-13) need a separate status page / SLA reporting?
  Undecided, depends on the regions outcome.

## Note

The parking lot defers to the risk register (doc 12) for the formal conflicts. It is included
so a consolidation captures the long tail of undecided items, not only the 15 tracked risks.
