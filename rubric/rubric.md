# Rubric - Frozen Scoring Criteria

The single source of truth every eval scores against. Extracted from `METHOD.md`
sections 2, 4, 5, and 6. This file is FROZEN: do not edit it per-eval. If the
rubric needs to change, change it here once and version it in the changelog at
the bottom, then re-run affected evals. Every eval's scoring Architect reads
THIS file as the contract.

---

## 1. The 9 scored dimensions

Score each variant 1 to 5 on every applicable dimension. Weighted total formula:
`sum(score * weight) / sum(weights_scored)`. Conditional dimensions are excluded
from both numerator and denominator when they do not apply to the task.

| # | Dimension | Weight | Hard-fail eligible | Conditional | What it measures |
|---|-----------|--------|--------------------|-------------|------------------|
| 1 | Correctness | 3.0 | YES (score=1 eliminates) | No | Did it produce a true answer? |
| 2 | Completeness | 2.0 | No | No | Did it cover what was asked? |
| 3 | Format adherence | 1.5 | No | No | Output envelope, frontmatter, structure |
| 4 | Scope discipline | 1.5 | No | No | Stayed in lane / signalled scope-exceeded correctly |
| 5 | Reasoning quality | 2.5 | No | Skip pure-retrieval | Chain visible? Defensible? |
| 6 | Hallucination | 2.5 | YES (score=1 eliminates) | No | Made-up facts, fabricated citations, ghost paths |
| 7 | Voice match | 2.0 | No | Drafting / voice only | Against the voice anchor file |
| 8 | Helpfulness | 1.25 | No | Decision / judgment only | Useful output given the inputs |
| 9 | Discipline | 1.25 | No | Decision / judgment only | Stayed within constraints / refused appropriately |
| 10 | Source transparency | 1.0 | No | No - applies to all tasks | Citations, sourcing notes, what-was-used disclosure |

Note: the table lists 10 rows because Source transparency is numbered 10 in the
methodology, but Voice / Helpfulness / Discipline are conditional. On any given
eval the number of dimensions actually scored is typically 7 to 10.

### Scoring scale (1 to 5 anchored - anchors mandatory in every scoring sheet)

- **1** - fails the dimension (hallucinates, ignores instruction, off-scope)
- **2** - partial, but meaningful gaps
- **3** - acceptable, meets the bar
- **4** - strong, exceeds bar in one or more sub-aspects
- **5** - exemplary, hard to imagine doing better with this prompt

### Mandatory qualitative observation field

Each variant gets a 2 to 4 sentence qualitative note capturing the character that
numbers miss. Written LAST, after all dimensional scores. This is the load-bearing
field for the final call.

---

## 2. Binary instruction-following gate (PASS / FAIL)

NOT a scored dimension. Applied as a gate:

- **PASS** = variant followed the output envelope (schemaVersion, tier, status,
  tool_budget_used), honoured all explicit constraints (no em dashes, no emojis),
  applied sequential processing, stayed within the prompt's scope, and wrote to
  the correct output path.
- **FAIL** = variant ignored the envelope OR violated an explicit constraint.

A FAIL eliminates the variant from winner contention. Equivalent in effect to a
Correctness=1 hard fail. Record the FAIL in the tally for transparency; it cannot win.

---

## 3. Hard-fail eligibility

A variant is hard-fail eliminated (cannot win regardless of other scores) if ANY of:

- Correctness score = 1 (produced a wrong answer)
- Hallucination score = 1 (fabricated facts, citations, or paths)
- Instruction-following binary gate = FAIL

Hard-fail eliminated variants are recorded in the tally for transparency but are
removed from weighted-total ranking.

---

## 4. Within-family tiebreaker (applied BEFORE cross-family cost-override)

When 2+ variants of the SAME model family (e.g. Haiku low + Haiku high) score
within 0.3 weighted total of each other:

1. **Cheaper effort wins** (lower effort = cheaper = the practical pick within the family)
2. **If tied AND same effort:** shorter output wins (verbosity penalty)
3. **If still tied:** random selection, noted in the tally

This resolves intra-family ties cleanly before any cross-family comparison.

---

## 5. Cost-override thresholds (cross-family, applied AFTER the within-family tiebreaker)

| Quality gap (weighted) | Cost ratio (quality winner vs cheaper variant) | Winner |
|------------------------|--------------------------------------------------|--------|
| < 0.3 (tie zone) | any | Cheaper wins |
| 0.3 to 0.5 | >= 3x | Cheaper wins |
| 0.5 to 1.0 | >= 5x | Cheaper wins |
| >= 1.0 | any | Quality wins |
| Any | Any | A hard-fail variant loses regardless |

These thresholds are policy, not math - heuristics from initial calibration.
Different task categories may eventually warrant different thresholds. Any change
is recorded in the changelog below and re-applied uniformly.

---

## 6. How the two winners are reported

Every tally reports BOTH:

- **Quality winner** - highest weighted total among non-eliminated variants.
- **Practical winner** - the cost-adjusted pick after sections 4 and 5 are applied.
  When no cost-override fires, the practical winner equals the quality winner and
  the tally says so explicitly.

---

## Changelog

- **frozen v1** (2026-05-21) - extracted verbatim from METHOD.md sections 2, 4, 5, 6
  at the v1.4 method lock. 9 scored dimensions (10th numbered row is Source
  transparency), binary instruction-following gate, two hard-fail-eligible dims
  (Correctness, Hallucination), within-family tiebreaker, cross-family cost-override
  table. No deviations from METHOD.md.
