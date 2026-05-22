---
task_category: subtle-spec-violation-detection
prompt_under_test: |
  You are auditing an implementation against its written specification. The
  specification for a fictional REST service "Globex Orders API" is at
  corpus/subtle-spec-violation-detection/CONTRACT.md (a single contract document,
  16 numbered rules). The implementation under audit is at
  corpus/subtle-spec-violation-detection/handlers.py (a single large module of
  endpoint handlers and helpers).

  The implementation is believed to be correct and has passed an informal review.
  Your job: audit handlers.py against CONTRACT.md and report whether the
  implementation FULLY complies. There is reason to believe at most a small number
  of subtle deviations slipped through. For the audit:
    1. Go through the contract rule by rule (Rule 1 through Rule 16). For EACH
       rule, state COMPLIES or VIOLATES, cite the handler/function and line region
       in handlers.py that implements it, and give a one-line justification.
    2. If you find a VIOLATION, describe it precisely: which rule, which line, what
       the code does, what the contract requires instead, and the concrete input
       that would expose the bug.
    3. Be exact about boundaries, rounding modes, ordering, off-by-one, inclusive
       vs exclusive ranges, and default values. These are where subtle violations
       hide. A rule that LOOKS satisfied at a glance may be violated at a boundary.

  Rules:
    - Do NOT report a false violation. If a handler correctly implements its rule,
      it COMPLIES, even if the code is ugly or could be written more clearly. Style
      is not a violation. Flagging a compliant handler as a violation is a precision
      error and counts against you harder than missing a real one.
    - Do NOT pad the report with speculative "could be improved" notes. The audit
      is a compliance verdict against the 16 rules, not a code review.
    - A confidently-wrong verdict (declaring full compliance when there is a
      violation, OR flagging a compliant rule as violated) is the worst outcome.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/subtle-spec-violation-detection/
corpus_intent: 1 contract document (CONTRACT.md, 16 numbered rules), 1 large implementation module (handlers.py, ~16 handlers/helpers) that is fully compliant on 15 rules with exactly ONE subtle buried violation
corpus_delivered: TBD
corpus_match: TBD
notes: |
  OPUS-CONSISTENCY / VARIANCE BATTERY (subtle-violation detection under load). This
  eval runs at variant_pool: 15 - five runs per model (Haiku x5, Sonnet x5, Opus
  x5; effort treated as inert per the methodology). The headline metric is
  WITHIN-FAMILY SPREAD, not the family mean: the question is whether Opus finds the
  one buried violation on EVERY one of its five runs while a cheaper model finds it
  on its lucky runs but declares full compliance (misses it) on one or two of five.
  Three runs barely shows variance; five gives a real spread estimate. The
  separator is run-to-run reliability at catching the single subtle violation, NOT
  the peak.

  THE BURIED VIOLATION (the separator). The contract has 16 rules. The
  implementation in handlers.py satisfies 15 of them faithfully. EXACTLY ONE rule
  is violated, and the violation is subtle: the discount-tier boundary in the
  apply_volume_discount helper uses a STRICT greater-than (quantity > 100) where
  CONTRACT.md Rule 9 specifies the 10-percent tier applies "at 100 units or more"
  (i.e. quantity >= 100). The code therefore gives the wrong discount for the exact
  boundary value of 100 units: a 100-unit order gets the lower 5-percent tier
  instead of the contract-mandated 10-percent tier. Every other rule - auth,
  pagination defaults, sort order, currency rounding, idempotency, the 404/409
  status codes, field validation, the rate-limit header, the ISO timestamp format,
  the soft-delete flag - is implemented correctly. The bug is a single comparison
  operator (> vs >=) on one line, in a helper that otherwise reads as obviously
  correct, surrounded by tiers that look symmetric. This is the canonical "looks
  right, off-by-one at the boundary" defect.

  WHY IT IS HARD TO SEE. (a) The helper is structured as a clean if/elif ladder of
  three tiers; the eye reads the SHAPE (three tiers, ascending thresholds) and
  accepts it, because the shape is correct - only the boundary inclusivity of one
  branch is wrong. (b) The two SURROUNDING tier boundaries are written with the
  correct operators, so the wrong one does not stand out as anomalous. (c) The
  contract's wording ("at 100 units or more") is in prose in Rule 9, while the code
  uses a numeric literal, so catching it requires comparing the prose semantics to
  the operator, not pattern-matching a number. (d) The module is long (~16
  handlers, ~300 lines) so the auditor must hold attention across the whole file
  and not relax once the first dozen rules check out. (e) A model that audits
  rule-by-rule but treats each rule as a yes/no glance, rather than constructing the
  boundary input (quantity == 100), will read the discount ladder as compliant.

  DELIBERATE NEAR-MISS DECOYS (these are COMPLIANT - flagging any is a false
  positive). The implementation contains several spots that look suspicious but are
  actually correct, planted to draw a careless auditor into a false-positive:
    DECOY-1. The pagination default page size is 25 and the max is 100; the code
      clamps page_size to [1, 100]. This LOOKS like it might be off-by-one but Rule
      4 says "page size defaults to 25, capped at 100 inclusive" - the inclusive
      clamp to 100 is CORRECT. Do not flag it.
    DECOY-2. The currency rounding helper uses round-half-to-even (banker's
      rounding) which matches Rule 7 exactly. A model primed to expect a rounding
      bug (a common defect) may wrongly flag it; it is CORRECT. Do not flag it.
    DECOY-3. The created/updated timestamps are emitted with a trailing "Z" and no
      microseconds; Rule 12 requires exactly "ISO 8601 UTC, second precision, Z
      suffix". This is CORRECT. Do not flag it.
    DECOY-4. The list endpoint sorts by created_at DESCENDING then id ascending as
      a tiebreak; Rule 6 specifies exactly that. A model that misreads the tiebreak
      direction may wrongly flag it; it is CORRECT. Do not flag it.
    DECOY-5. The soft-delete handler sets deleted_at and returns 204 with no body;
      Rule 14 requires exactly that (NOT a hard delete, NOT a 200). CORRECT.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers). Declaring "fully
  compliant" when the >= boundary bug is present is the canonical confidently-wrong
  failure: a reviewer would approve a contract-violating implementation that
  silently under-discounts every 100-unit order. EQUALLY bad is flagging one of the
  five DECOYS as a violation - that sends an engineer to "fix" correct code and
  erodes trust in the audit. Reward the run that finds the ONE real violation
  (Rule 9, the > vs >= boundary) AND correctly clears all five decoys AND clears
  the other ten rules. A run that flags three "violations" (the real one plus two
  decoys) is NOT better than one that finds only the real one - precision counts.

  ANSWER KEY (for the scoring Architect). The contract states 16 rules (Rule
  1-Rule 16). The implementation VIOLATES exactly ONE: Rule 9. All others COMPLY.

    THE VIOLATION:
    Rule 9 (volume discount tiers) - VIOLATED. CONTRACT.md Rule 9 states the
      discount tiers as: under 50 units -> 0 percent; 50 to 99 units -> 5 percent;
      100 units OR MORE -> 10 percent. The helper apply_volume_discount in
      handlers.py implements the top tier with `if quantity > 100:` (strict
      greater-than) returning the 10-percent rate, and the middle tier with
      `elif quantity >= 50:` returning 5 percent. The boundary value quantity == 100
      therefore falls through the strict `> 100` and lands in the `>= 50` branch,
      receiving 5 percent instead of the contract-required 10 percent. EXPOSING
      INPUT: an order line with quantity exactly 100 is charged a 5-percent discount
      when the contract requires 10 percent. The fix is `if quantity >= 100:`. This
      is the single subtle buried violation; finding it run-to-run is the separator.

    THE 15 COMPLYING RULES (a model that flags any of these as a violation has
    produced a false positive - the heaviest precision penalty):
    Rule 1  (auth) - COMPLIES. Every handler checks the bearer token via
      require_auth and returns 401 when absent/invalid.
    Rule 2  (content type) - COMPLIES. Non-JSON request bodies are rejected with
      415.
    Rule 3  (required fields) - COMPLIES. create_order validates customer_id and a
      non-empty items list; missing -> 422 with the field name.
    Rule 4  (pagination defaults) - COMPLIES. Default page size 25, clamp to
      [1, 100] inclusive (see DECOY-1). Page number defaults to 1, min 1.
    Rule 5  (filtering) - COMPLIES. status filter accepts only the enum
      {pending, paid, shipped, cancelled}; an unknown status -> 422.
    Rule 6  (sort order) - COMPLIES. created_at DESC, id ASC tiebreak (see
      DECOY-4).
    Rule 7  (currency rounding) - COMPLIES. round-half-to-even to 2 dp (see
      DECOY-2).
    Rule 8  (tax) - COMPLIES. Tax is computed on the post-discount subtotal at the
      region rate, rounded per Rule 7.
    Rule 10 (idempotency) - COMPLIES. create_order honours the Idempotency-Key
      header; a repeat key returns the original 201 response, not a duplicate.
    Rule 11 (status codes) - COMPLIES. 201 on create, 200 on read, 404 on missing
      order, 409 on a state-transition conflict (e.g. paying a cancelled order).
    Rule 12 (timestamps) - COMPLIES. ISO 8601 UTC, second precision, Z suffix (see
      DECOY-3).
    Rule 13 (rate limit headers) - COMPLIES. X-RateLimit-Remaining is set on every
      response; 429 when exhausted.
    Rule 14 (soft delete) - COMPLIES. DELETE sets deleted_at and returns 204, no
      hard delete (see DECOY-5).
    Rule 15 (totals) - COMPLIES. order total = post-discount subtotal + tax +
      shipping, all rounded per Rule 7; the arithmetic is correct.
    Rule 16 (response envelope) - COMPLIES. Every success response is wrapped in
      {"data": ...} and every error in {"error": {"code", "message"}}.

  NOTE on the boundary: the contract is unambiguous (Rule 9 says "100 units or
  more"). The exposing input is quantity == 100. A correct audit names Rule 9,
  cites the `> 100` line in apply_volume_discount, states that 100 units gets 5
  percent instead of 10, and gives quantity == 100 as the trigger. An audit that
  says "Rule 9 looks fine, the tiers are present" has missed the violation. An
  audit that flags Rule 4 (pagination), Rule 6 (sort), Rule 7 (rounding), Rule 12
  (timestamps), or Rule 14 (soft delete) has produced a false positive on a decoy.

  CONSISTENCY SCORING (the headline). For EACH model (Haiku, Sonnet, Opus), score
  all 5 runs, then report:
    - per-run weighted total (mean-of-5 is the family score, SPREAD is the
      headline)
    - the SPREAD = (max run - min run) weighted total within the family
    - the VIOLATION HIT RATE = how many of the 5 runs correctly identified Rule 9
      as the (only) violation with the > vs >= boundary explanation. This is the
      single most important number: e.g. "Opus 5/5, Sonnet 3/5, Haiku 1/5".
    - the FALSE-POSITIVE RATE = how many runs flagged a decoy (Rule 4/6/7/12/14) as
      a violation. A run that finds Rule 9 but ALSO flags a decoy is partially
      penalised on precision.
    - flag any family whose 5 runs diverge by more than 0.5 weighted total as
      HIGH-VARIANCE; spread under 0.2 is HIGH-CONSISTENCY.
  The corpus_intent is explicit: WITHIN-FAMILY SPREAD is the key signal. A model
  that nails Rule 9 on three runs and declares full compliance on two is LESS useful
  for audit work than one that finds it on all five at a slightly lower polish.

  Scoring guidance:
    - Correctness (hard-fail eligible, weight 3.0) = did the audit reach the right
      verdict (exactly one violation, Rule 9, correctly explained as the > vs >=
      boundary). Declaring full compliance (missing Rule 9) is Correctness <= 2.
      Reporting a DIFFERENT rule as the violation while clearing Rule 9 is
      Correctness 1 (wrong verdict).
    - Completeness (weight 2.0) = did the audit address all 16 rules with a
      per-rule verdict, not just announce the one violation. A bare "Rule 9 is
      wrong" with no per-rule pass is incomplete even if the headline is right.
    - Hallucination (hard-fail eligible) = inventing a violation that is not there
      (flagging a decoy or any of the 15 complying rules), or citing a line/handler
      that does not exist. Flagging a decoy is the canonical hallucination here.
    - Reasoning quality = did the model construct the boundary input (quantity ==
      100) and trace it through the if/elif ladder, rather than glancing at the
      tier shape. This is where the careful auditor separates from the skimmer and
      where Opus is hypothesised to hold consistency.
    - Source transparency = every verdict cites the handler/function and line
      region; the Rule 9 finding cites the specific `> 100` line.
    - Discipline = found the real violation AND cleared all five decoys without
      flagging them; did not pad with style nits. Correctly clearing a decoy that
      "looks" buggy (e.g. explicitly noting "Rule 7 uses banker's rounding, which
      matches the contract, COMPLIES") is a discipline POSITIVE.
    - Format adherence = the output envelope plus a clean per-rule structure (Rule,
      verdict, cite, justification).
    Correctness on the single buried violation (Rule 9) and within-family
    consistency on it are the scored discriminators. Voice match does NOT apply.

    Suggested scoring shorthand for the Architect: a run is "correct" iff it (a)
    names Rule 9 as the violation, (b) explains it as the > vs >= boundary giving
    100-unit orders the wrong tier, and (c) does NOT flag any of the five decoys. A
    run that does all three is the exemplary 5 on Correctness and Discipline.
    Missing Rule 9 (declaring full compliance) caps Correctness at 2; flagging a
    decoy caps Hallucination/Discipline. The headline output is the per-family
    VIOLATION HIT RATE and the within-family SPREAD.
---

# Spec 44 - subtle-spec-violation-detection (the buried-violation variance battery)

A HEAVY consistency probe. The model audits a large, correct-looking implementation
module (`handlers.py`, ~16 endpoint handlers and helpers for a fictional "Globex
Orders API") against its written contract (`CONTRACT.md`, 16 numbered rules) and
must deliver a per-rule compliance verdict. The implementation faithfully satisfies
fifteen of the sixteen rules. EXACTLY ONE rule is violated, and the violation is
deliberately subtle: the volume-discount helper uses a strict greater-than
(`quantity > 100`) on the top tier where Rule 9 specifies "100 units or more"
(`>= 100`), so an order of exactly 100 units silently receives the 5-percent tier
instead of the contract-mandated 10-percent tier. It is a single comparison operator
in an if/elif ladder whose overall shape is correct, flanked by two correctly-written
tier boundaries, with the contract's requirement stated in prose rather than as a
matching numeric literal - the canonical "looks right, off-by-one at the boundary"
defect.

Five near-miss decoys are planted (a pagination clamp, banker's rounding, an ISO
timestamp format, a sort tiebreak, a soft-delete status code) - each looks like it
could be a defect but is actually compliant, so a careless auditor is drawn toward a
false positive. The eval runs at `variant_pool: 15` - five runs per model (Haiku x5,
Sonnet x5, Opus x5, effort inert per the methodology). The headline metric is
WITHIN-FAMILY SPREAD: the question (per the batch-4 redesign) is whether Opus finds
the one buried violation on every one of its five runs while a cheaper model finds it
on its lucky runs but declares full compliance on one or two of five. The single most
important number the scoring Architect reports is the per-family VIOLATION HIT RATE
(e.g. "Opus 5/5, Sonnet 3/5, Haiku 1/5") plus the FALSE-POSITIVE RATE on the decoys
and the within-family weighted-total spread.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is central: declaring full compliance when the
boundary bug is present is the canonical confidently-wrong failure (a reviewer would
approve contract-violating code), and flagging one of the five decoys is the
canonical false-positive failure (sending an engineer to fix correct code). Both are
penalised; the run that finds the one real violation AND clears all five decoys is
the exemplary result. Reasoning quality captures whether the model constructed the
boundary input (quantity == 100) and traced it through the ladder rather than
glancing at the tier shape. Voice match does not apply. The corpus is the directory
`corpus/subtle-spec-violation-detection/`.
