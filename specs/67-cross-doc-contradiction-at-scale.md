---
task_category: cross-doc-contradiction-at-scale
prompt_under_test: |
  You are given a specification set for a fictional order-fulfilment platform called
  "Project Marlowe" at corpus/cross-doc-contradiction-at-scale/marlowe-specs.md. It
  contains 30 short specification documents, each delimited by a "=== DOC NN ==="
  header.

  Your task: surface EVERY genuine contradiction in this spec set - cases where the
  documents, taken together, cannot all be true at once. A contradiction may be direct
  (two docs state opposing facts) OR triangulated (no single pair contradicts, but
  three or more docs combined produce an impossible or unsafe situation).

  For each contradiction you find:
    - name the exact DOC numbers involved,
    - state in one or two sentences what the conflict is,
    - explain why those documents cannot all hold together.

  Read carefully. Some apparent tensions are NOT contradictions (a design choice stated
  in one place and a constraint in another that are compatible). Only report a conflict
  if the documents genuinely cannot coexist. Do not invent a contradiction to pad the
  list.

  Output a markdown list, one entry per contradiction, with the DOC numbers, the
  conflict, and the reasoning. After the list, append the required output envelope
  (schemaVersion, tier, status, tool_budget_used) on separate lines. No em dashes (use
  spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/cross-doc-contradiction-at-scale/
corpus_intent: |
  One file (corpus/cross-doc-contradiction-at-scale/marlowe-specs.md) holding 30 short
  fictional spec docs for "Project Marlowe", an order-fulfilment platform. The doc set
  is internally consistent EXCEPT for one buried, triangulated contradiction that no
  single pair of documents reveals - it only emerges when THREE documents are combined.

  THE BURIED ITEM (the scored discriminator): a triangulated contradiction across
  DOC 07 + DOC 25 + DOC 26.
    - DOC 07 states the reservation hold window is 30 minutes; after expiry the stock is
      released and the order returns to RECEIVED.
    - DOC 25 states Dispatch ASSUMES any RESERVED order still has a live reservation for
      its entire pick, does NOT re-check the reservation, and decrements on-hand at pick
      time on that assumption.
    - DOC 26 states a multi-warehouse pick can take up to 45 minutes normally and up to
      90 minutes during peak surge.
  Combined: a 45-90 minute pick EXCEEDS the 30-minute reservation TTL, so the
  reservation can expire mid-pick (stock released, order returned to RECEIVED per DOC
  07), yet Dispatch (DOC 25) never re-checks and still decrements on-hand against an
  expired/released reservation. The three documents cannot all hold: either the
  reservation TTL must cover the worst-case pick duration, or Dispatch must re-check
  before pick. NO PAIR alone contradicts - 07+25 looks fine if picks are fast, 25+26
  looks fine if reservations never expire, 07+26 looks fine if Dispatch re-checks. Only
  all three together expose the impossibility.

  A weak model either (a) misses it entirely because no two adjacent docs conflict, or
  (b) flags a non-contradiction (e.g. claims DOC 05 cancellation-states and DOC 15
  cancellation-policy conflict, when they are compatible) - a false positive. The
  correct answer names DOC 07, DOC 25, AND DOC 26 together and explains the TTL-vs-pick-
  duration-vs-no-recheck triangle. Catch-rate on this single triangulated item across
  the 5 runs of a family is the load-bearing signal.

  QUALITY PRINCIPLE (correctness-first): there is exactly ONE genuine contradiction in
  the set, and it is triangulated. Surfacing it with the correct three DOC numbers and
  the correct reasoning is full credit. Reporting additional "contradictions" that are
  actually compatible design choices is a precision / hallucination error. Missing the
  triangle is the recall miss.

  ANSWER KEY (for the scoring Architect):
    GENUINE CONTRADICTIONS = exactly 1.
      C1 (triangulated): DOC 07 + DOC 25 + DOC 26. The 30-minute reservation hold
         window (07) can be exceeded by a 45-90 minute pick (26), so a reservation can
         expire mid-pick; but Dispatch never re-checks the reservation before
         decrementing on-hand (25). The three cannot coexist safely - a pick can outlast
         the reservation while Dispatch assumes it cannot. Resolution requires either a
         longer TTL or a Dispatch re-check.
    NON-CONTRADICTIONS that look tempting but are COMPATIBLE (must NOT be reported):
      - DOC 05 (cancel only from RECEIVED/RESERVED) vs DOC 15 (no cancel after
        DISPATCHED): compatible - both restrict cancellation, no conflict.
      - DOC 09 (reservations decrement available immediately) vs DOC 11 (on-hand
        decrements at pick): compatible - two different counters.
      - DOC 22 (backorders bypass reservation TTL) vs DOC 07 (30-min TTL): compatible -
        backorder is an explicit exception.
      - DOC 19 (2s allocation SLA) vs DOC 08 (retry every 5 min): compatible - decision
        latency vs retry cadence are different clocks.
      - DOC 17 burst 400 for 5s vs DOC 17 base 200/s: same doc, intentional, not a
        cross-doc conflict.

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - The reported contradiction names ALL THREE of DOC 07, DOC 25, DOC 26 (or "07",
      "25", "26"). Grep the output for co-occurrence of `07`/`7`, `25`, and `26` in one
      contradiction entry. Missing any one of the three = the triangle is not fully
      caught.
    - The reasoning references the reservation TTL (30 minute / 30-minute / hold window)
      AND the pick duration (45 / 90 / minute) AND the no-re-check / assumption (DOC 25).
      Grep for `30` (minute), `90` or `45`, and `re-check`/`recheck`/`assume`/`expire`.
    - The output reports exactly ONE genuine contradiction. Any entry naming a
      non-contradiction pair from the list above is a false positive (precision error).

  Scoring guidance:
    - Correctness (hard-fail eligible) = the single triangulated contradiction
      identified with the correct three DOC numbers and correct reasoning.
    - Completeness = the triangle fully named (all three docs, not just two).
    - Hallucination (hard-fail eligible) = reporting a compatible design choice as a
      contradiction, or inventing DOC content not present.
    - Discipline = not padding the list; exactly one genuine contradiction reported.
    - Voice match does NOT apply.
notes: |
  Chat A consistency battery (61-70). variant_pool 15 (3 models x N=5). The SCORED
  SIGNAL is WITHIN-FAMILY SPREAD across the 5 runs PLUS per-model buried-item catch-rate:
  did all 5 runs of a family surface the triangulated DOC 07+25+26 contradiction (TTL vs
  pick duration vs no-re-check), or did some runs miss it (no pair conflicts, so it is
  easy to skim past) or pad the list with a compatible-design-choice false positive.
  Peak score on one run is not the question; consistency of catching the one buried
  triangulated item across 5 runs is.

  This is a cross-document contradiction task at scale: 30 short fictional Project
  Marlowe spec docs (corpus/cross-doc-contradiction-at-scale/marlowe-specs.md), all
  internally consistent except one contradiction that no single pair reveals - it
  emerges only when the 30-minute reservation TTL (DOC 07), Dispatch's no-re-check
  assumption (DOC 25), and the up-to-90-minute pick duration (DOC 26) are combined. The
  precision traps are several compatible-looking pairs (cancellation policy, two
  inventory counters, backorder TTL exception) that a weak model may over-report. Answer
  key gives the one genuine triangle, the non-contradiction exclusion set, and
  grep-verifiable invariants. Standard four-phase /eval-pit flow against the frozen
  rubric/rubric.md. Codenames are neutral fictional (Project Marlowe). Voice match does
  not apply.
---

# Spec 67 - cross-doc-contradiction-at-scale

Given 30 short specification documents for a fictional order-fulfilment platform
(Project Marlowe), surface every genuine contradiction - the cases where the documents
cannot all be true at once - while resisting the temptation to flag compatible design
choices as conflicts.

The corpus (`corpus/cross-doc-contradiction-at-scale/marlowe-specs.md`) is internally
consistent except for ONE buried, triangulated contradiction. No single pair of
documents conflicts. The conflict emerges only when three are combined: DOC 07 fixes the
reservation hold window at 30 minutes (after which stock is released and the order
returns to RECEIVED); DOC 25 states Dispatch assumes the reservation stays live for the
whole pick and never re-checks before decrementing on-hand; DOC 26 states a pick can run
45 to 90 minutes. A 90-minute pick outlasts a 30-minute reservation, so the reservation
can expire mid-pick while Dispatch blindly decrements on-hand against a released
reservation. The three cannot coexist; the resolution is either a longer TTL or a
Dispatch re-check.

The correct answer names DOC 07, DOC 25, and DOC 26 together with that reasoning. The
failure modes are missing it (no adjacent pair conflicts, so it is easy to skim past) or
padding the list with a compatible-but-tempting pair (cancellation policy, the two
inventory counters, the backorder TTL exception) as a false positive.

This is a Chat A consistency-battery eval. Standard four-phase `/eval-pit` flow against
the frozen `rubric/rubric.md`. The scored signal is within-family SPREAD across the 5
runs plus per-model catch-rate on the single buried triangulated contradiction, not peak
score on one lucky run. The variant pool is 15 (3 models x N=5, effort inert per the
methodology). The answer key in `corpus_intent` gives the one genuine triangle, the
non-contradiction exclusion set, and grep-verifiable invariants for the scoring
Architect. Codenames are neutral fictional (Project Marlowe). Voice match does not apply.
