# Weighted Requirements Checklist

This is the scoring instrument for the decision. Use it directly: apply the hard gate
first, then compute the weighted score for every platform that PASSES the gate.

## Step 1 - Hard gate (pass/fail, applied BEFORE any weighting)

- EU data residency for ALL functions touching EU customer contact data (per the
  compliance memo, doc 09). A platform that fails this is DISQUALIFIED regardless of
  any weighted score. A roadmap promise does not pass the gate.

Gate result:
- Helmsdesk: PASS (EU residency on Business tier).
- Quillstack: PASS (deploy in an EU region).
- Beaconreach: FAIL (AI/analytics layer processes EU contact data outside the EU
  today; roadmap-only). DISQUALIFIED - do not compute a weighted score for it.

## Step 2 - Weighted dimensions (apply ONLY to gate-passers)

Weights sum to 100. Score each gate-passing platform 1 to 5 on each dimension, then
weighted score = sum(weight_fraction * score). Higher is better.

| Dimension | Weight | Source docs |
|-----------|--------|-------------|
| Operating burden / fit for a team with no platform engineer | 30 | 07, 08, 12, 15 |
| Three-year total cost (fully loaded, incl. people time) | 25 | 07, 13 |
| Peak-season scaling with zero team intervention | 20 | 06, 08, 14 |
| Reliability / measured uptime | 15 | 06 (independent), 03 (vendor claim) |
| Throughput headroom under load | 10 | 05 (stale), 06 (current) |

## Step 3 - Scores (1 to 5 per gate-passer)

Helmsdesk:
- Operating burden: 5 (managed, ~0.05 FTE, vendor runs it).
- Three-year cost: 5 (~63k, cheapest all-in per doc 07).
- Peak scaling: 5 (vendor autoscaling, zero intervention, doc 06/14).
- Reliability: 4 (99.95 percent measured, doc 06).
- Throughput headroom: 3 (current benchmark doc 06 puts it ~1.3x behind Quillstack,
  but absorbs the peak profile via autoscaling).

Quillstack:
- Operating burden: 2 (self-hosted, ~0.4 FTE on a team with no engineer, docs 08/12).
- Three-year cost: 1 (~120k all-in, MOST expensive once people-time counted, doc 07).
- Peak scaling: 2 (manual node additions; documented failure mode in doc 08).
- Reliability: 2 (99.5 percent MEASURED per doc 06, below the 99.99 percent vendor
  claim in doc 03 - use the independent figure).
- Throughput headroom: 5 (leads on raw throughput even on current versions, doc 06;
  the stale doc 05 overstates the lead but the direction holds).

## Step 4 - Compute (weighting math, shown)

Weighted score = (w/100)*score summed.

Helmsdesk = 0.30*5 + 0.25*5 + 0.20*5 + 0.15*4 + 0.10*3
          = 1.50 + 1.25 + 1.00 + 0.60 + 0.30 = 4.65 / 5.

Quillstack = 0.30*2 + 0.25*1 + 0.20*2 + 0.15*2 + 0.10*5
           = 0.60 + 0.25 + 0.40 + 0.30 + 0.50 = 2.05 / 5.

Beaconreach = DISQUALIFIED at the gate; no weighted score.

## Result

Helmsdesk wins at 4.65 vs Quillstack 2.05 among gate-passers. Beaconreach is
disqualified by the EU residency gate. Quillstack's only strength (throughput) carries
the lowest weight and is partly built on a stale benchmark; on the heavily weighted
operating-burden and cost dimensions it loses decisively for a team with no platform
engineer.
