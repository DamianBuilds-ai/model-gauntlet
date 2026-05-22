---
task_category: test-coverage-gap-detection
prompt_under_test: |
  You are given a fictional billing module and its test suite:
    - corpus/test-coverage-gap-detection/billing.js   (the function calc() under test)
    - corpus/test-coverage-gap-detection/billing.test.js  (the existing test suite)

  Your task: identify EVERY branch in calc() that the test suite does NOT exercise. A
  "branch" is each decision outcome - both the true and the false side of every `if`,
  the throw paths of guards, the `continue` path, and any early return.

  Go through calc() branch by branch. For each branch, decide whether at least one test
  in billing.test.js drives execution down that path. List every branch that has NO
  covering test (the coverage gaps). For each gap, name the guard/branch and the
  specific condition that is never triggered.

  Be precise: most branches ARE covered by the suite. Do not report a branch as a gap if
  a test exercises it, and do not invent branches that do not exist in the code.

  Output a list of the uncovered branches. If a branch is covered, do not list it. After
  the list, append the required output envelope (schemaVersion, tier, status,
  tool_budget_used) on separate lines. No em dashes (use spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/test-coverage-gap-detection/
corpus_intent: |
  Two files (corpus/test-coverage-gap-detection/billing.js + billing.test.js). calc()
  has a series of guards and branches: G1 missing-invoice throw, G2 missing-account
  throw, G3 frozen-account EARLY RETURN, B1 negative-qty throw, B2 zero-qty continue,
  B3 volume-discount (true/false sides), B4 tax-unless-exempt (true/false sides). The
  test suite deliberately covers almost everything: G1, G2, B1, B2, both sides of B3,
  both sides of B4. The buried discriminator is the ONE uncovered branch: G3, the
  frozen-account early-return path. NO test in the suite ever passes an account with
  status === "frozen", so the early-return guard (and its { total: 0, skipped: true }
  result) is never exercised.

  THE BURIED ITEM (the scored discriminator): G3 - the frozen-account early-return
  guard. It is easy to miss because it is an EARLY RETURN buried among guards, the suite
  LOOKS thorough (7 tests covering throws, skips, discount, tax, exempt), and a model
  skimming for obviously-missing happy-path tests may declare full coverage. The correct
  answer names exactly the G3 frozen-account branch as the single coverage gap.
  Catch-rate on this one branch across the 5 runs of a family is the load-bearing
  signal.

  PRECISION TRAPS (these ARE covered - must NOT be reported as gaps):
    - G1 missing invoice: covered ("throws when invoice is missing").
    - G2 missing account: covered ("throws when account is missing").
    - B1 negative qty: covered ("throws on negative quantity").
    - B2 zero qty continue: covered ("skips zero-quantity lines").
    - B3 true (discount applied, subtotal > 1000): covered ("applies volume discount").
    - B3 false (no discount, subtotal <= 1000): covered ("applies no discount below threshold").
    - B4 true (tax applied): covered (within the discount and below-threshold tests).
    - B4 false (tax-exempt): covered ("applies no tax for tax-exempt accounts").
  Reporting any of these as an uncovered gap is a false positive (precision error).

  QUALITY PRINCIPLE (correctness-first): there is exactly ONE coverage gap (G3). Naming
  it precisely is full credit. Missing it (declaring full coverage, or naming a
  different branch) is the recall miss. Reporting a covered branch as a gap is the
  precision/hallucination error.

  ANSWER KEY (for the scoring Architect):
    UNCOVERED BRANCHES = exactly 1.
      G3: the frozen-account early-return guard - `if (account.status === "frozen")
          return { total: 0, skipped: true, reason: "account frozen" }`. No test passes
          an account with status "frozen", so this branch is never executed.
    ALL OTHER BRANCHES are covered (G1, G2, B1, B2, B3-true, B3-false, B4-true,
    B4-false). The single correct gap is G3.

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - The output names the frozen-account / G3 branch as the (or an) uncovered gap. Grep
      the output for `frozen` - present in a gap entry == buried item caught.
    - The output reports exactly ONE uncovered branch. Listing more than one means a
      covered branch was wrongly flagged (precision error); listing zero (or only
      non-G3 branches) means the buried item was missed.
    - The output does NOT list any of G1, G2, B1, B2, B3, B4 as uncovered. Grep for
      `tax-exempt`/`taxExempt`, `negative`, `discount`, `zero` in gap entries - any of
      these flagged as uncovered is a false positive.

  Scoring guidance:
    - Correctness (hard-fail eligible) = G3 (frozen-account early return) identified as
      the single uncovered branch.
    - Completeness = the one real gap present (recall).
    - Hallucination (hard-fail eligible) = reporting a covered branch as uncovered, or
      inventing a branch not in calc().
    - Discipline = exactly one gap reported (not over-listing, not declaring full
      coverage).
    - Voice match does NOT apply.
notes: |
  Chat A consistency battery (61-70). variant_pool 15 (3 models x N=5). The SCORED
  SIGNAL is WITHIN-FAMILY SPREAD across the 5 runs PLUS per-model buried-item catch-rate:
  did all 5 runs of a family identify the frozen-account early-return guard (G3) as the
  one uncovered branch, or did some runs declare full coverage (the suite looks thorough)
  or flag a covered branch as a gap. Peak score on one run is not the question;
  consistency of catching the one buried gap across 5 runs is.

  This is a test-coverage-gap detection task: a fictional billing module
  (corpus/test-coverage-gap-detection/billing.js) plus a near-complete test suite
  (billing.test.js) that covers G1, G2, B1, B2, and both sides of B3 and B4 - but never
  exercises the frozen-account early-return guard (G3). The buried item is that single
  early-return branch, easy to miss because the suite looks exhaustive. The precision
  traps are the eight covered branches. Answer key gives the single uncovered branch
  plus the covered-branch exclusion set plus grep-verifiable invariants. Standard
  four-phase /eval-pit flow against the frozen rubric/rubric.md. Codenames are neutral
  fictional. Voice match does not apply.
---

# Spec 69 - test-coverage-gap-detection

Given a fictional billing function and a near-complete test suite, identify every branch
of `calc()` that the suite does not exercise - resisting both the urge to declare full
coverage (the suite looks thorough) and the urge to over-report covered branches as
gaps.

The corpus (`corpus/test-coverage-gap-detection/billing.js` and `billing.test.js`)
covers almost every branch: the missing-invoice and missing-account throws (G1, G2), the
negative-quantity throw (B1), the zero-quantity skip (B2), both sides of the volume
discount (B3), and both sides of the tax-unless-exempt branch (B4). The buried
discriminator is the ONE uncovered branch: G3, the frozen-account early return. No test
ever passes an account with status "frozen", so that early-return guard is never
executed. The correct answer names exactly G3 as the single coverage gap.

The precision traps are the eight covered branches - flagging any of them as uncovered
is a false positive, and declaring full coverage misses the real gap.

This is a Chat A consistency-battery eval. Standard four-phase `/eval-pit` flow against
the frozen `rubric/rubric.md`. The scored signal is within-family SPREAD across the 5
runs plus per-model catch-rate on the single buried uncovered branch (G3), not peak
score on one lucky run. The variant pool is 15 (3 models x N=5, effort inert per the
methodology). The answer key in `corpus_intent` gives the one real gap, the covered-
branch exclusion set, and grep-verifiable invariants for the scoring Architect.
Codenames are neutral fictional. Voice match does not apply.
