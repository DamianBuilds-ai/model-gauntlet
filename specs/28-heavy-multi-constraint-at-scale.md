---
task_category: multi-constraint-satisfaction
prompt_under_test: |
  You are given a large Python module at
  corpus/heavy-multi-constraint-at-scale/settlement.py - the merchant settlement
  engine for a fictional payments processor "Northwind Payments" - a reference
  file corpus/heavy-multi-constraint-at-scale/collaborators.py documenting the
  fixed collaborator interfaces, and a list of TWENTY-FOUR constraints at
  corpus/heavy-multi-constraint-at-scale/constraints.md that the refactored
  module must satisfy.

  Refactor the settle_batch(merchant_id, transactions, batch_key) method so that
  ALL TWENTY-FOUR listed constraints (C1 through C24) hold SIMULTANEOUSLY.
  Several of the constraints interact or near-conflict - for example the
  atomic-balance-then-post constraint (C13) tensions with the no-network-under-
  lock constraint (C14), the audit-every-outcome constraint (C21) tensions with
  the idempotent-replay constraint (C22), the validation-rejection constraints
  (C1-C5) tension with the audit-and-metric-every-outcome constraints
  (C21/C24), and the per-merchant-concurrency constraint (C12) tensions with a
  naive global lock. You must hold all twenty-four at once - do NOT satisfy some
  at the expense of others.

  Rules:
    - Do not change the collaborator interfaces (LedgerClient, FxClient,
      FraudClient, AuditLog, MetricsSink, ReserveStore, ClockSource) described in
      collaborators.py.
    - Do not change the public field names of SettlementResult, LedgerEntry,
      Transaction, or the SettlementError subtypes.
    - Money must stay in integer minor units (cents); the only Decimal use is
      multiplying by the FX rate and the reserve rate, each immediately
      bankers'-rounded (ROUND_HALF_EVEN) back to integer minor units. No float
      may touch a money value.
    - Output the complete refactored module as a single Python code block.
    - After the code, include a checklist mapping each constraint C1..C24 to the
      line(s) or construct in your code that satisfies it, so the satisfaction is
      verifiable. Do not claim a constraint is satisfied if your code does not
      actually satisfy it - a confidently-wrong "satisfied" claim is worse than
      omitting the claim.
    - Do not introduce new constraint violations while fixing others.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/heavy-multi-constraint-at-scale/
corpus_intent: 1 large module to refactor + 1 collaborator-interface reference file + 1 constraints file listing 24 simultaneous requirements (HEAVY - the deficient module plus the reference collaborators run several hundred lines, so the model must hold a long module and a 24-item constraint set in working memory at once)
corpus_delivered: TBD
corpus_match: TBD
notes: |
  HEAVY OPUS-STRESS PROBE (simultaneous-constraint load at scale /
  forgetting-under-load). This is eval-23 (multi-constraint-satisfaction, 12
  constraints, one short module) scaled up until the field stops bunching at the
  top: 24 constraints over a large module plus a reference collaborators file, so
  the model must read a long corpus AND hold two dozen tensioned requirements in
  working memory simultaneously. At 12 constraints over a 60-line module the
  cheaper models can hold the set; the hypothesis is that at 24 constraints over
  a several-hundred-line corpus they satisfy a visible subset (validation, the
  obvious float fix, the global-lock fix) and silently drop the buried tensions -
  the once-per-currency FX memo (C16), the replay-no-double-audit rule (C21 vs
  C22), the metrics-on-the-reject-path rule (C24), the reserve-only-on-success
  rule (C20). Run the full 9-variant model-only pool (Haiku x3, Sonnet x3, Opus
  x3; effort treated as inert per the methodology). Aggregate the 3 passes per
  model (mean weighted total); flag any model whose 3 passes diverge by more than
  0.5 as a consistency finding.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong
  satisfaction claim is worse than an unmet constraint honestly flagged. A model
  that asserts "C14 satisfied" while its FX quote still runs inside the lock has
  produced code an engineer would ship believing it correct - worse than a model
  that says "I could not hold C14 with C13". The discriminator is the COUNT of
  constraints actually satisfied in the code (verified by READING the code, not
  the model's self-report), with self-reported-but-violated constraints penalised
  hardest.

  SATISFIABILITY: all twenty-four constraints ARE simultaneously satisfiable - a
  reference solution exists with no mutually-exclusive pair. The shape: validate
  C1-C5 first and audit+metric the validation rejections (C21/C24); fraud-screen
  ONCE and FX-quote once-per-distinct-currency BEFORE acquiring any lock
  (C14-C16); compute money in integer cents with the FX-rate and reserve-rate
  Decimal multiplications each quantised ROUND_HALF_EVEN (C6-C11); acquire a
  per-merchant lock only around balance-read + post_entry + reserve-hold
  (C12-C14, C20); raise InsufficientBalanceError with an audit on a short balance
  (C19, C21); cache only successful settlements and short-circuit a replay before
  any network call or audit (C22); reverse + re-raise on post failure with a
  "post_failed" audit (C23); and metric every terminal path with no time.sleep
  (C24). A model that claims two constraints conflict and drops one is wrong -
  they all hold.

  ANSWER KEY (for the scoring Architect - the 24 constraints as a verifiable
  checklist; mark each SATISFIED or VIOLATED by READING the model's refactored
  code, NOT its self-report). The starting-state status is given so the Architect
  can see which constraints the deficient code already meets and which the
  refactor had to fix.

    --- Input + structural validation ---
    C1  - EMPTY BATCH returns status "skipped_empty", money fields 0, entry_id
          "", txn_count 0, no post, no raise. (Start: VIOLATED - no empty guard.)
    C2  - OVERSIZED BATCH (> 500 txns) raises SettlementError (base type) naming
          the limit; no silent truncation. (Start: VIOLATED - no size guard.)
    C3  - DUPLICATE TXN IDS raise SettlementError before any network call. (Start:
          VIOLATED - duplicates double-count.)
    C4  - MIXED-MERCHANT: any txn whose merchant_id != the argument raises
          SettlementError before any network call. (Start: VIOLATED - no check.)
    C5  - UNSUPPORTED SETTLEMENT CCY raises CurrencyMismatchError before work.
          (Start: VIOLATED - no check.)

    --- Money correctness ---
    C6  - INTEGER CENTS THROUGHOUT: no float touches any money value; gross, fee,
          reserve, net are int at every step. (Start: VIOLATED - float gross/fee/
          reserve/net.)
    C7  - BANKERS' ROUNDING on each FX conversion via Decimal.quantize(Decimal(1),
          ROUND_HALF_EVEN); not int() truncation. (Start: VIOLATED - int() truncates
          net.)
    C8  - FEE ONLY ON SALES: refunds carry no fee. (Start: VIOLATED - fee accrues
          on every txn regardless of kind.)
    C9  - REFUNDS REDUCE GROSS (signed): sales add converted amount, refunds
          subtract. (Start: VIOLATED - kind ignored, all added.)
    C10 - FEE BPS ON CONVERTED AMOUNT (settlement currency), not pre-conversion
          amount_minor. (Start: BORDERLINE - bps taken on the float-converted value,
          but the whole money path is float so treat as VIOLATED.)
    C11 - RESERVE ON NET (gross minus fee), bankers' rounded; net_minor is
          net-after-reserve. (Start: VIOLATED - reserve on net but float, and
          net_minor truncated.)

    --- Concurrency + atomicity ---
    C12 - PER-MERCHANT LOCK: different merchants run in parallel; no single global
          lock. (Start: VIOLATED - one self._lock for all merchants.)
    C13 - ATOMIC BALANCE-CHECK-THEN-POST under the per-merchant lock, no TOCTOU.
          (Start: VIOLATED - balance read mixed into the same global-lock block but
          not per-merchant, and the read/compare is float; treat as VIOLATED.)
    C14 - NO NETWORK UNDER LOCK EXCEPT THE LEDGER PAIR: fraud.screen and ALL
          fx.quote calls happen before the lock; only balance-read + post_entry
          (+ reversal) under it. (Start: VIOLATED - fraud + FX are inside the lock.)

    --- Network-call efficiency ---
    C15 - SINGLE FRAUD SCREEN for the whole batch (one screen call with all ids).
          (Start: VIOLATED - screen called per transaction in the loop.)
    C16 - ONE FX QUOTE PER DISTINCT CURRENCY (memoised). A 300-USD batch triggers
          exactly one USD quote. (Start: VIOLATED - quote called per transaction.)

    --- Fraud handling ---
    C17 - SKIP FRAUD-DECLINED TXNS: a declined txn contributes nothing to gross/
          fee/reserve and is not an error. (Start: PARTIAL - the per-txn loop skips
          declined via continue, but because screening is per-txn and under the
          lock the surrounding handling is wrong; treat C17's intent as VIOLATED in
          the refactor sense since it depends on the single batched screen.)
    C18 - ALL-DECLINED non-empty batch returns status "rejected_fraud", money
          fields 0, entry_id "", txn_count == number of input txns, no post.
          (Start: VIOLATED - would post a zero/garbage entry.)

    --- Balance + failure handling ---
    C19 - INSUFFICIENT BALANCE raises InsufficientBalanceError (not return None,
          not post). (Start: VIOLATED - returns None silently.)
    C20 - RESERVE HOLD ONLY ON SUCCESS, after a successful post_entry; never on a
          rejected/failed/empty batch. (Start: VIOLATED - hold runs even though the
          post may have failed and been swallowed.)
    C21 - AUDIT EVERY OUTCOME exactly once (settled, skipped_empty, rejected_fraud,
          insufficient_balance, each validation rejection) with a "ts" from
          clock.now() and an "outcome" field, AND no second audit on an idempotent
          replay. (Start: VIOLATED - audits success only, no ts, no outcome taxonomy.)
    C22 - IDEMPOTENT BATCH KEY: a replay of an already-settled batch_key returns
          the cached result with no re-screen/re-quote/re-post/re-hold/re-audit;
          cache write only on a settled outcome. (Start: VIOLATED - cache never
          written, replays re-post.)
    C23 - POST-FAILURE REVERSAL + RAISE: a post_entry exception is not swallowed;
          no reserve hold, no cache, no success audit; an outcome "post_failed"
          audit is written and the exception propagates. (Start: VIOLATED -
          exception swallowed, entry_id set to "", continues to hold + audit success.)

    --- Observability + hygiene ---
    C24 - METRICS ON EVERY TERMINAL PATH (settled, skipped_empty, rejected_fraud,
          insufficient_balance, replayed) AND no time.sleep / busy-wait. (Start:
          VIOLATED - no metrics at all, time.sleep(0) present.)

  Net starting state: the deficient code VIOLATES the large majority (C1-C16,
  C18-C24 are violated or effectively violated; C17's skip-on-continue is the only
  fragment that resembles correct behaviour and even that is entangled with the
  per-txn screen). A correct refactor satisfies all 24. The score tracks how many
  of the 24 a model's refactor GENUINELY holds when the Architect reads the code.

  Scoring guidance:
    - Completeness (weight 2.0) = count of the 24 constraints the refactored code
      actually satisfies (verified by reading the code). 24/24 is exemplary; each
      genuinely-unmet constraint drops the score. This is the primary
      discriminator. Count dropped constraints explicitly. The buried tensions
      (C16 once-per-currency, C20 reserve-only-on-success, C21-vs-C22 replay
      audit, C24 metrics on reject paths) are the strongest signal of
      forgetting-under-load.
    - Correctness (hard-fail eligible) = does the refactor run as valid Python and
      preserve the happy-path settlement behaviour. A refactor that satisfies
      constraints but breaks the basic settle flow, mis-handles the dataclasses,
      or fails to import fails Correctness.
    - Hallucination (hard-fail eligible) = claiming a constraint is satisfied when
      the code does NOT satisfy it (the canonical confidently-wrong here), or
      inventing a collaborator method that does not exist (e.g. a batch reserve
      API, a ledger lock primitive). A self-report that says "all 24 satisfied"
      over code that holds 17 is the heaviest penalty.
    - Reasoning quality = did the model correctly resolve the tensions (C13/C14
      ledger-pair-under-lock vs network-outside-lock, C21/C22 audit-every-outcome
      vs no-double-audit-on-replay, C1-C5/C21 validation-rejections-still-audited,
      C12/C13 per-merchant lock granularity) rather than satisfying one side and
      breaking the other. This is where Opus is hypothesised to separate - holding
      all twenty-four at once.
    - Discipline = stayed in scope (refactored settle_batch + supporting private
      helpers, did not change collaborator interfaces or public field names, did
      not invent constraints or relax stated ones).
    - Format adherence = output envelope + a single code block + the per-constraint
      verification checklist mapping each C1..C24 to a construct.
    - Source transparency = the checklist maps each constraint to the line/construct
      that satisfies it.
    Constraint-satisfaction count and zero false satisfaction-claims are the scored
    discriminators. Summary quality and prose elegance are NOT the point - that is
    where Opus tied Sonnet on the earlier consolidation eval. Voice match does NOT
    apply.

    Suggested scoring shorthand for the Architect: satisfied = (constraints the
    code genuinely holds) / 24; false-claim penalty = number of constraints the
    self-report claims satisfied that the code does not. A refactor that holds
    24/24 with a fully accurate checklist is the exemplary 5 on Completeness and
    Correctness; dropping the buried tensions or over-claiming the checklist is
    where the score falls.
---

# Spec 28 - heavy-multi-constraint-at-scale (the 24-simultaneous-constraints probe)

The heavy, scaled-up analog of spec 23 (multi-constraint-satisfaction): eval-23
is twelve constraints over a sixty-line module, and every model could roughly
hold that set. This spec scales the constraint count to TWENTY-FOUR over a large
module (the settlement engine, its data types, and configuration) plus a
reference collaborators file, so the model must read a long corpus AND hold two
dozen tensioned requirements in working memory at once. That is the load level
where the field stops bunching at the top.

The corpus (`corpus/heavy-multi-constraint-at-scale/`) is a deficient merchant
settlement engine for a fictional payments processor "Northwind Payments"
(`settlement.py`), a fixed collaborator-interface reference (`collaborators.py`),
and a list of twenty-four constraints (`constraints.md`) the refactor must
satisfy. The constraints are engineered with at least five genuine tensions: the
ledger balance-read + post must be atomic UNDER a per-merchant lock (C13) while
the fraud screen and FX quotes must be OUTSIDE it (C14); audit-every-outcome
(C21) must not double-audit an idempotent replay (C22); validation rejections
(C1-C5) must still be audited and metric'd before any network call (C21/C24);
the reserve must be held only on a successful post (C20) yet the success audit
follows the post (C21/C23); and money must stay integer cents through Decimal
FX-rate and reserve-rate multiplications with bankers' rounding (C6-C11). All
twenty-four ARE simultaneously satisfiable (a reference solution exists with no
mutually-exclusive pair); the starting code satisfies almost none of them.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is central: a confidently-wrong "constraint
satisfied" claim over code that does not satisfy it is worse than an honestly
flagged miss, because it is code an engineer would ship believing it correct.
Completeness (the COUNT of constraints genuinely satisfied, verified against the
code rather than the self-report) and Hallucination (false satisfaction claims,
invented collaborator methods) are the scored discriminators - not prose elegance,
since elegance is where Opus tied Sonnet on the earlier consolidation eval.
Reasoning quality captures whether the model resolved the five tensions
correctly. The variant pool is 9 (3 models x N=3, effort inert per the
methodology). The corpus is the directory
`corpus/heavy-multi-constraint-at-scale/`.
