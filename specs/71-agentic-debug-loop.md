---
task_category: agentic-debug-loop
prompt_under_test: |
  You are given a captured debugging session at
  corpus/agentic-debug-loop/transcript.md. It contains a fictional library
  (widgetkit/discount.py), its test file, and a LOG of a prior agent's iterate-observe
  debugging loop (tool calls plus their outputs). The prior agent thrashed and did NOT
  reach a fix; its final conclusion ("the test file might be stale") is unverified and
  may be wrong.

  Your job is to finish the debugging loop correctly. Reason over the evidence already
  gathered in the log (you do not need to call any tools - all the tool output you need
  is in the transcript). Then produce:

    1. ROOT CAUSE: the single true cause of the failing tests, stated precisely (which
       line, why it produces the observed outputs).
    2. WHY THE PRIOR AGENT WAS WRONG: identify the specific flawed step in its reasoning
       loop.
    3. THE MINIMAL FIX: the smallest possible code change that makes the failing tests
       pass WITHOUT breaking any currently-passing test. Show the exact before/after of
       only the line(s) you change.
    4. VERIFICATION: state what each affected test will return after your fix, confirming
       all 7 tests pass.

  Do NOT rewrite the whole file. Do NOT change the tests. Do NOT change apply_discount
  or bundle_price unless you can prove they are the cause. Apply the smallest correct
  change. No em dashes (use spaced hyphens). No emojis.

  After your answer, append the required output envelope (schemaVersion, tier, status,
  tool_budget_used) as separate lines.
variant_pool: 9
corpus: corpus/agentic-debug-loop/
corpus_intent: |
  One transcript file (corpus/agentic-debug-loop/transcript.md) holding: the source
  module widgetkit/discount.py, its test file, and a captured PRIOR-agent debugging loop
  (6 turns of simulated run_tests / read_file tool calls and their outputs). This is a
  single-shot proxy for an agentic iterate-observe-revise loop: the model reasons over
  an already-captured loop instead of running tools live. The discriminator is whether
  the model forms a correct hypothesis grounded in the evidence and lands the minimal
  fix, versus thrashing or adopting the prior agent's wrong conclusion.

  QUALITY PRINCIPLE (correctness-first). The transcript is internally CONSISTENT: the
  source as written really does produce the failing outputs shown in the log, and the
  docstring/tests really are the intended spec. A model that diagnoses the actual bug
  and proposes the one-line fix is correct. A model that parrots the prior agent's "the
  test file is stale" conclusion, or that proposes changing the tests, or that "fixes"
  apply_discount (which the log already proved correct), is confidently wrong. The
  prior-agent log is a TRAP: it ends on a plausible-but-false conclusion the model must
  reject.

  ANSWER KEY (for the scoring Architect).

    ROOT CAUSE: the bug is the tier guard in tiered_discount. The line reads
    `if qty > 50:` but the documented tiers are `1-9 -> 0%, 10-49 -> 10%, 50+ -> 20%`
    (50 inclusive). Because `qty > 50` is strict, qty == 50 falls through to the
    `elif qty >= 10` branch and gets the 10% tier (90.0) instead of the 20% tier (80.0).
    This off-by-one on the boundary is the SINGLE cause of BOTH failing tests:
      - test_tiered_high: tiered_discount(100, 50) returns 90.0, expected 80.0.
      - test_bundle_total: bundle_price([(100,10),(200,50)]) returns 270.0 (90.0 + 180.0)
        instead of 250.0 (90.0 + 160.0), because the (200, 50) line is mis-tiered at 10%.

    WHY THE PRIOR AGENT WAS WRONG: at turn 5 it correctly traced that `50 > 50` is False
    and the 20% branch is skipped, but then concluded "the test is just wrong / stale"
    instead of recognizing that the strict `>` contradicts the documented `50+` (50
    inclusive) tier. It mis-assigned blame to the test rather than the off-by-one guard.

    THE MINIMAL FIX: change exactly one character on one line:
      BEFORE: `    if qty > 50:`
      AFTER:  `    if qty >= 50:`
    No other line changes. apply_discount and bundle_price are UNCHANGED (the log already
    confirmed apply_discount is correct via test_apply_basic / test_apply_full passing).

    VERIFICATION AFTER FIX (all 7 tests pass):
      test_apply_basic: apply_discount(100,20) == 80.0  PASS
      test_tiered_mid: tiered_discount(100,10) == 90.0  PASS
      test_tiered_high: tiered_discount(100,50) == 80.0 PASS (was 90.0)
      test_bundle_total: bundle_price(...) == 250.0      PASS (was 270.0)
      test_apply_full: apply_discount(100,100) == 0.0    PASS
      test_boundary_qty_nine: tiered_discount(100,9)==100.0 PASS
      (the transcript shows 6 collected names; both the >=50 fix lines resolve cleanly.)

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - The fix names `qty >= 50` (or equivalently "change > to >=" on the tier guard).
      A correct answer contains the string `>= 50` as the fixed guard.
    - The answer identifies tiered_discount (NOT apply_discount, NOT bundle_price, NOT
      the test file) as the location of the bug.
    - The answer states the boundary value 50 is the trigger (qty == 50 mis-tiered).
    - The answer rejects the "stale test" conclusion (does not change any test assertion).
    - The answer attributes BOTH failing tests (test_tiered_high AND test_bundle_total)
      to the same single cause.
    - A confidently-wrong run: changes the test, rewrites apply_discount, adds a new
      branch, or accepts "the test file is stale".

  Scoring guidance:
    - Correctness (hard-fail eligible) = identifies the `qty > 50` off-by-one as the
      single root cause and proposes the `>= 50` one-line fix. Blaming the test, blaming
      apply_discount, or any multi-line rewrite is Correctness=1.
    - Completeness = all four requested parts present (root cause, prior-agent error,
      minimal fix, verification).
    - Hallucination (hard-fail eligible) = inventing a bug that is not there, claiming a
      line is broken that the log proved fine, or fabricating test output.
    - Discipline = MINIMAL fix (one line, one operator) and no edits to the tests or to
      unrelated functions. This is the load-bearing discriminator: the thrash failure
      mode is over-reaching or accepting the false "stale test" conclusion.
    - Reasoning quality = forms a hypothesis, checks it against the captured evidence,
      and corrects the prior agent's flawed turn-5 step.
    - Source transparency = points to the exact line / function.
    Voice match does NOT apply.
notes: |
  NEW task type, first of the Chat B agentic/gap battery (71, 72, 78, 79, 80). The
  gauntlet is single-shot, so an iterate-observe-revise agentic loop is delivered as a
  SINGLE-PROMPT PROXY: the model reasons over a CAPTURED debugging loop (a transcript of
  prior tool calls and outputs) rather than driving tools live. The discriminator is
  whether the model forms a correct hypothesis grounded in the already-gathered evidence
  and lands the minimal fix, versus thrashing or adopting the prior agent's
  plausible-but-false conclusion ("the test file is stale").

  The planted bug is a single off-by-one tier guard (`qty > 50` where the documented
  tiers make 50 inclusive), which causes BOTH failing tests from one cause. The corpus is
  internally consistent (verified: the buggy source really yields the failing outputs in
  the log, and the `>= 50` fix makes all tests pass). The trap is the prior agent's
  turn-5 mis-conclusion that the test is stale - a confidently-wrong model parrots it,
  changes the tests, or "fixes" apply_discount (which the log proved correct). The answer
  key gives the exact root cause, the one-character fix, and per-test verification, plus
  grep-verifiable invariants. Correctness and Hallucination are hard-fail eligible;
  Discipline (one-line minimal fix, no test edits, no unrelated rewrites) is the
  load-bearing discriminator. Voice match does not apply. Standard four-phase /eval-pit
  flow against the frozen rubric/rubric.md. The variant pool is 9 (3 models x N=3, effort
  inert per the methodology). The corpus is the directory corpus/agentic-debug-loop/.
---

# Spec 71 - agentic-debug-loop (single-shot proxy for an iterate-observe loop)

Given a captured debugging session - a fictional module, its tests, and a LOG of a
prior agent's tool-call loop that thrashed without reaching a fix - finish the loop:
diagnose the true root cause, identify where the prior agent's reasoning went wrong,
propose the minimal one-line fix, and verify all tests pass.

The gauntlet is single-shot, so this agentic task is delivered as a single-prompt proxy:
all the tool output the model needs (run_tests results, read_file dumps) is already in
the transcript. The model does not call tools; it reasons over the captured loop. The
discriminator is hypothesis-test-revise discipline versus thrash.

The planted bug is one off-by-one tier guard: `if qty > 50:` where the documented tiers
(`50+ -> 20%`) make 50 inclusive, so qty == 50 mis-tiers to 10% and breaks two tests
from a single cause. The fix is one character: `>` becomes `>=`. The trap is the prior
agent's final turn-5 conclusion that "the test file is stale" - a plausible-sounding but
false read that a confidently-wrong model adopts, leading it to change the tests or
rewrite apply_discount (which the log already proved correct).

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. Correctness
(name the off-by-one, propose `>= 50`) and Hallucination (no invented bug) are hard-fail
eligible; Discipline - a minimal one-line fix with no test edits and no unrelated
rewrites - is the load-bearing discriminator. The answer key in `corpus_intent` gives the
exact root cause, the one-character fix, the prior-agent error, and per-test
verification, plus grep-verifiable invariants. Voice match does not apply. The variant
pool is 9 (3 models x N=3, effort inert per the methodology). The corpus is the directory
`corpus/agentic-debug-loop/`.
