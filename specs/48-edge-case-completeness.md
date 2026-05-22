---
task_category: edge-case-completeness
prompt_under_test: |
  You are given the complete behavioural specification of ONE function from a
  fictional billing platform called "Cardinal". Read both files in
  corpus/edge-case-completeness/:
    - spec.md - the authoritative specification of
      allocate_cents(total_cents, weights), which splits an integer amount of
      money (in cents) across a list of weighted buckets, distributing the
      indivisible remainder by a deterministic largest-remainder rule.
    - reference_impl.py - a reference implementation that matches the spec exactly.
      Use it to confirm behaviour on any case you are unsure about.

  Produce a COMPLETE enumeration of the EDGE CASES this function must handle.
  Miss nothing. For EACH edge case:
    1. State the input condition precisely (what about total_cents and/or weights
       triggers it).
    2. State the REQUIRED behaviour per the spec (the exact return value, or that
       it raises ValueError - and for value cases give the concrete result on a
       small representative input).
    3. Note in a few words WHY it is an edge case (what makes it non-trivial or
       easy to get wrong).

  Rules:
    - Enumerate edge cases, not the happy path alone. The even-split case
      (allocate_cents(100, [1, 1]) -> [50, 50]) is the trivial baseline; the edge
      cases are the boundary and degenerate inputs and the subtle consequences of
      the rounding and remainder rules.
    - Be exhaustive about the SUBTLE, non-obvious edge cases that follow from the
      spec, not just the obvious empty-list / zero-total ones.
    - Do NOT invent edge cases the spec does not create. If you claim the function
      must handle a condition, it must follow from spec.md (and agree with
      reference_impl.py). Asserting a behaviour the spec does not define, or
      claiming the function handles a case differently than it actually does, is a
      correctness error - a confidently-wrong edge case (one with the wrong
      required behaviour) is WORSE than a missed one, because an engineer writing
      tests from your list will encode a wrong expectation.
    - Ground every edge case in the spec. Where helpful, give the concrete
      input/output (it must match reference_impl.py).
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/edge-case-completeness/
corpus_intent: |
  HEAVY consistency / variance battery (5 runs per model = 15-variant pool,
  model-only, effort inert per the methodology). The headline scored signal is
  WITHIN-FAMILY SPREAD: does a model surface the FULL edge-case set - including the
  subtle, non-obvious ones - on EVERY one of its 5 runs, or only on some.
  Run-to-run reliability on the subtle edge cases - not a per-run ceiling - is the
  separator. The hypothesis (carried from the batch-3 consistency read): the
  stronger model lists the subtle edge cases (the negative-total multi-leftover
  case, the largest-remainder tiebreak, the zero-weight-stays-zero rule, the
  empty-vs-zero-total split, the all-zero-weights split) across all 5 runs, while a
  cheaper model gets the obvious ones every time but DROPS one or more subtle cases
  on its floor runs (or asserts a wrong required behaviour for one). Aggregate per
  model as mean weighted total across the 5 runs AND report the spread (max minus
  min) plus the hit-rate on the SUBTLE edge cases specifically (how many of the 5
  runs caught the designated subtle items with no wrong-behaviour assertions). Flag
  any model whose 5 runs diverge by more than 0.5 weighted total, or whose subtle
  -case hit-rate is below 5/5, as the consistency finding. Corpus: a 3-file
  specification (README + spec.md + reference_impl.py) of one billing function for
  the fictional "Cardinal" platform, with a verified reference implementation.
corpus_delivered: TBD
corpus_match: TBD
notes: |
  HEAVY EDGE-CASE-COMPLETENESS PROBE (enumerate-all-including-subtle consistency).
  One complex but fully-specified function (an integer money allocator with a
  largest-remainder rule) whose required edge-case set includes several subtle,
  non-obvious cases. On a good run, any model lists the obvious empty-list and
  zero-total cases; the hypothesis is that the SUBTLE cases (negative total with
  more than one leftover cent, the remainder tiebreak, zero-weight buckets, the
  empty-vs-nonzero-total raise, the all-zero-weight split) are dropped
  INCONSISTENTLY by cheaper models - present on some of their 5 runs and absent on
  others. The 5-runs-per-model design measures that run-to-run spread directly. Run
  the full 15-variant model-only pool (Haiku x5, Sonnet x5, Opus x5; effort treated
  as inert). Within-family SPREAD is the scored headline.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong edge
  case is worse than a missed one. A model that asserts "negative total_cents
  raises ValueError" (it does NOT - the spec mandates floor toward negative
  infinity and distributes leftover cents) has put a wrong expectation on a test
  list an engineer will encode, breaking a correct function. Reward exact recall of
  the full edge-case set AND correct required-behaviour for each. Penalise the
  wrong-behaviour assertion hardest. The reference implementation is verified
  against all worked examples and a 20,000-case fuzz, so every required behaviour
  below is objective.

  ANSWER KEY (for the scoring Architect). Every item below is verifiable against
  spec.md and reference_impl.py (which was run against all worked examples and a
  20k fuzz with zero invariant violations). There are 11 edge-case entries; they
  split into OBVIOUS (every model should get these) and SUBTLE (the separators).

  OBVIOUS edge cases (E1-E4; weak models still get these):
    E1. Empty weights list + total_cents == 0 -> returns [] (empty list). Edge
        because there is nothing to distribute yet the sum-equals-total invariant
        must still hold (trivially).
    E2. Empty weights list + total_cents != 0 -> raises ValueError. Edge because
        there is no bucket to receive a non-zero amount, so the invariant cannot
        be satisfied.
    E3. total_cents == 0 with non-empty positive weights -> returns all zeros (e.g.
        allocate_cents(0, [5, 5]) -> [0, 0]). Edge: zero is a boundary value.
    E4. Amount divides evenly (R == 0), e.g. allocate_cents(100, [1, 1]) ->
        [50, 50]. The remainder branch does nothing; the no-leftover boundary.

  SUBTLE edge cases (E5-E11; THE SEPARATORS - cheaper models drop these run-to-run
  or assert wrong behaviour):
    E5. All weights are zero (W == 0) with a NON-EMPTY list:
        - total_cents == 0 -> returns n zeros (e.g. allocate_cents(0, [0, 0, 0])
          -> [0, 0, 0]).
        - total_cents != 0 -> raises ValueError (no proportional basis).
        Subtle because it is distinct from the empty-list case AND splits on the
        total being zero or not. A model that conflates this with E1/E2, or that
        tries to divide by W == 0, is wrong.
    E6. A NEGATIVE weight anywhere -> raises ValueError. Subtle because the spec
        allows negative total_cents but NOT negative weights; easy to assume both
        signs are symmetric.
    E7. NEGATIVE total_cents (a credit/refund to split), e.g.
        allocate_cents(-100, [1, 1, 1]) -> [-33, -33, -34]. The base is floored
        TOWARD NEGATIVE INFINITY (-100*1//3 = -34 each, sum -102), leaving R = 2
        leftover cents that are added to the two largest-remainder buckets (indices
        0 and 1), moving them toward zero. THE canonical subtle case: (a) negative
        amounts are valid (NOT a ValueError), (b) flooring is toward negative
        infinity not toward zero, and (c) there can be MORE THAN ONE leftover cent.
        A model that says negative raises, or that truncates toward zero, or that
        assumes R is always 0 or 1, is confidently wrong here.
    E8. Largest-remainder distribution when R > 0: the R leftover cents go to the R
        buckets with the LARGEST fractional remainders, e.g.
        allocate_cents(5, [3, 1]) -> [4, 1] (bucket 0's 0.75 remainder beats bucket
        1's 0.25). Subtle because a naive "give the leftover to the first/last
        bucket" is wrong; it must be the largest remainder.
    E9. TIEBREAK on equal remainders: when remainders are equal, the LOWER INDEX
        gets the extra cent first, e.g. allocate_cents(100, [1, 1, 1]) ->
        [34, 33, 33] (all remainders equal; bucket 0 wins), and
        allocate_cents(7, [1, 1, 1, 1]) -> [2, 2, 2, 1] (R = 3, the three
        lowest-index buckets get the extra cents). Subtle: determinism depends on a
        stable index-ascending tiebreak; without it the result is ambiguous.
    E10. ZERO-WEIGHT bucket among positive ones always receives exactly 0, e.g.
        allocate_cents(100, [2, 0, 1]) -> [67, 0, 33]; the zero-weight bucket has
        remainder 0 and never gets a leftover cent (R < n_pos guarantees leftover
        cents land on positive-weight buckets). Subtle: a model might give the
        zero-weight bucket a stray remainder cent, or skip it and misalign the
        output length/order.
    E11. SINGLE bucket with positive weight -> receives the entire total, e.g.
        allocate_cents(99, [7]) -> [99] (and allocate_cents(-99, [7]) -> [-99]).
        Subtle boundary: n == 1 means all of total goes to one bucket regardless of
        the weight's magnitude; R is whatever flooring leaves (0 here) and the lone
        bucket absorbs it.

  INVARIANTS a strong answer also names (not separate edge cases but the property
  the edge cases protect): len(result) == len(weights); sum(result) ==
  total_cents EXACTLY for every non-raising input; result entries are integers; a
  zero-weight bucket gets 0; output order matches input order; deterministic.

  WRONG-BEHAVIOUR TRAPS (a model that asserts any of these has a confidently-wrong
  entry - the heaviest penalty, worse than omitting an edge case):
    TRAP-A. "Negative total_cents raises ValueError." FALSE - negative totals are
        valid and split per E7. This is the single most likely confidently-wrong
        assertion.
    TRAP-B. "Flooring truncates toward zero." FALSE - the spec mandates floor
        toward NEGATIVE INFINITY (Python //), which differs from truncation for
        negative amounts and changes the result.
    TRAP-C. "The remainder R is always 0 or 1." FALSE - R can be up to n_pos - 1
        (e.g. E7 has R = 2; allocate_cents(7, [1,1,1,1]) has R = 3).
    TRAP-D. "Leftover cents go to the first (or last) bucket." FALSE - they go to
        the largest-remainder buckets, tiebroken by lowest index (E8/E9).
    TRAP-E. "A non-empty all-zero-weights list always raises" OR "always returns
        zeros." FALSE - it depends on whether total_cents is zero (E5); only the
        non-zero-total case raises.
    TRAP-F. "Weights may be negative / negative weights are clamped." FALSE -
        negative weights raise ValueError (E6).

  Scoring guidance:
    - Completeness (weight 2.0) = of the 11 edge-case entries, how many are
      present with the correct condition. Count DROPPED edge cases explicitly. The
      SUBTLE entries (E5-E11) are the strongest signal; dropping E7 (negative
      total) or E9 (tiebreak) is the canonical forgetting-under-load miss.
    - Correctness (hard-fail eligible, weight 3.0) = is the REQUIRED BEHAVIOUR
      stated for each edge case actually correct per the spec / reference impl. A
      list dominated by wrong required-behaviours (especially any TRAP assertion)
      fails Correctness for that run.
    - Hallucination (hard-fail eligible, weight 2.5) = inventing an edge case the
      spec does not create, or asserting a behaviour the function does not have
      (the six TRAPS are the canonical confidently-wrong entries). Citing a
      behaviour that contradicts reference_impl.py is a hallucination.
    - Reasoning quality (weight 2.5) = did the run reason from the rounding and
      remainder RULES (floor toward negative infinity, R can exceed 1,
      largest-remainder + index tiebreak) to DERIVE the subtle cases, rather than
      listing only the surface empty/zero cases. This is where the separation is
      hypothesised to show.
    - Discipline (decision task, weight 1.25) = did the run stay grounded in the
      spec (every claimed edge case follows from spec.md) rather than padding with
      generic "what if the input is huge / what about thread safety" non-edge
      cases that the spec does not create.
    - Source transparency (weight 1.0) = ties each edge case to the spec rule or a
      concrete reference-impl input/output.
    - Format adherence (weight 1.5) = the output envelope plus a clean per-edge
      -case structure (condition, required behaviour, why).

    THE HEADLINE METRIC IS WITHIN-FAMILY SPREAD across the 5 runs per model: the
    hit-rate on the SUBTLE edge cases E5-E11 (how many of the 5 runs caught them
    with no wrong-behaviour assertions) and the weighted-total spread (max minus
    min). A model that catches the subtle set 5/5 with tight spread is consistent;
    a model that goes 3/5 on E7 or swings between correct and a TRAP assertion is
    the inconsistent profile this eval is built to expose. Voice match does not
    apply.
---

# Spec 48 - edge-case-completeness (enumerate-all-including-subtle consistency probe)

A HEAVY consistency battery. ONE fully-specified function from the fictional
"Cardinal" billing platform - `allocate_cents(total_cents, weights)`, an integer
money allocator with a largest-remainder distribution rule - has a required
edge-case set of eleven entries. Four are obvious (empty list, zero total, even
split); seven are subtle and follow from the rounding and remainder rules
(negative total with floor-toward-negative-infinity and multiple leftover cents,
the largest-remainder distribution, the index-ascending tiebreak,
zero-weight-stays-zero, the all-zero-weight split, negative-weight raise, the
single-bucket boundary). The task is to enumerate ALL of them with the correct
required behaviour for each, grounded in the spec - without inventing edge cases or
asserting a wrong behaviour.

The corpus (`corpus/edge-case-completeness/`) is three files: a README, `spec.md`
(the authoritative behavioural contract), and `reference_impl.py` (a reference
implementation verified against every worked example and a 20,000-case fuzz with
zero invariant violations - so the answer key is objective). Six wrong-behaviour
traps are documented (the most likely being "negative total raises" - it does not;
it splits via floor toward negative infinity), because a confidently-wrong required
behaviour is the heaviest penalty: an engineer writing tests from the list encodes
the wrong expectation and breaks a correct function.

This is run at `variant_pool: 15` (5 runs per model, model-only, effort inert). The
scored headline is WITHIN-FAMILY SPREAD: per model, the hit-rate on the SUBTLE
edge cases across the 5 runs (caught with no wrong-behaviour assertions) and the
weighted-total spread. Run-to-run reliability on the subtle cases - whether a model
surfaces them EVERY run or only on its good runs - is the separator, per the
batch-3 consistency read. Correctness-first applies: a confidently-wrong edge case
is penalised harder than a missed one. Standard four-phase `/eval-pit` flow against
the frozen `rubric/rubric.md`.
