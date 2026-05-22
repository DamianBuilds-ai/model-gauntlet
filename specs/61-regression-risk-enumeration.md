---
task_category: regression-risk-enumeration
prompt_under_test: |
  You are given a single corpus file at
  corpus/regression-risk-enumeration/codebase.md - a snapshot of a fictional
  pricing platform ("Aldous") with roughly 25 pseudo-TypeScript modules.

  A CHANGE is being made to ONE function:
  `module Bronte / discountEngine.applyTierDiscount()` will now round the
  discounted price DOWN to the nearest whole cent (Math.floor(amount * (1 - rate)
  * 100) / 100) instead of returning the raw float.

  Your task: enumerate EVERY behaviour in this codebase that this change could
  regress or alter. For each risk, name (a) the affected module/function and
  (b) WHY the change reaches it (the call path). Be complete - a missed
  regression path is the failure this task measures.

  Output a numbered list of distinct regression risks. For each: the
  module/function, the call path from applyTierDiscount() to it, and the
  observable behaviour that could change. Do NOT invent risks that the corpus
  does not support. Append the output envelope (schemaVersion, tier, status,
  tool_budget_used) as separate lines after the list. No em dashes (use spaced
  hyphens). No emojis.
variant_pool: 15
corpus: corpus/regression-risk-enumeration/
corpus_intent: |
  One corpus file (corpus/regression-risk-enumeration/codebase.md): ~25 fictional
  pseudo-TypeScript modules for a pricing platform. The changed function is
  Bronte/discountEngine.applyTierDiscount(), which is moving from returning a raw
  float to rounding the result DOWN to the nearest whole cent. The eval measures
  whether a run enumerates the COMPLETE set of regression paths, including one
  non-obvious transitive path that is reached two hops away through a
  reconciliation assertion.

  QUALITY PRINCIPLE (completeness-first): the easy direct callers are obvious; the
  scored signal is whether a run catches the BURIED transitive regression. A run
  that lists the three direct callers but misses the ledger-reconciliation path has
  found the shallow risk and dropped the dangerous one (a silent data-mismatch in
  production). Inventing regressions the corpus does not support (e.g. claiming
  taxEngine or shippingCalc is affected) is a precision error.

  ANSWER KEY (for the scoring Architect - the full enumerable list of true
  regression paths):

    DIRECT CALLERS of applyTierDiscount (one hop, easy to find):
      D1. Carrow/quoteBuilder.buildQuote() - the quote total and its formatted
          display value change (rounding now applied to `discounted`).
      D2. Carrow/loyaltyAccrual.accruePoints() - loyalty points are 1 per dollar
          of discounted spend; rounding down the spend can change accrued points.
      D3. Hadley/refundCalc.calcRefund() - refund amount changes by the rounding.

    BURIED TRANSITIVE PATH (the discriminator - two hops, no direct call to
    applyTierDiscount in the chain's entry module):
      B1. Greaves/ledgerReconcile.reconcileLedger() throws LedgerMismatchError.
          Path: invoiceController.handleInvoice -> Dunmore/invoiceRenderer
          .renderInvoice -> Farrow/lineTotals.computeLineTotals -> (hop 1)
          Greaves/ledgerReconcile.reconcileLedger -> (hop 2) it calls
          Carrow/quoteBuilder.getQuotedTotal -> buildQuote -> applyTierDiscount.
          reconcileLedger asserts the freshly-recomputed total EQUALS the stored
          quoted total. After the change, a stored pre-change quote total and a
          recomputed post-change total can differ by sub-cent amounts, tripping
          the equality assert and throwing on previously-valid invoices. THIS is
          the buried item - it does not import discountEngine directly and is two
          hops from the change.

    SECONDARY DISPLAY/DOWNSTREAM (acceptable, lower-weight, derived from D1):
      S1. Eddison/moneyFormat.formatMoney called on the new total (display value).
      S2. Marlow/emailReceipt.sendReceipt if it receives the changed total.

    NOT AFFECTED (precision traps - listing these is a false-positive error):
      taxEngine, shippingCalc, currencyConvert, promoEngine, cartValidator,
      tierResolver, sessionStore, featureFlags, metricsEmitter, rateLimiter,
      configLoader, healthCheck, retryPolicy, auditLog. None consume the
      discounted value.

  GREP-VERIFIABLE INVARIANTS (for the Architect, against the run's output):
    - A correct run names "reconcileLedger" OR "ledgerReconcile" OR
      "LedgerMismatch" (grep -i "reconcile\|ledgermismatch"). MISSING this string
      means the buried transitive path was dropped - the primary scored signal.
    - A correct run names all three direct callers: grep -i "buildQuote" AND
      "accruePoints" (or "loyalty") AND "calcRefund" (or "refund").
    - A correct run names "getQuotedTotal" or describes the re-derivation through
      buildQuote as the hop-2 mechanism.
    - PRECISION: the output must NOT assert that taxEngine, shippingCalc,
      currencyConvert, or promoEngine are regressed. grep -i "tax\|shipping\|
      promo\|currency" appearing as an ASSERTED regression is a false positive.

  Scoring guidance:
    - Buried-item catch (load-bearing) = did the run find the reconcileLedger
      transitive path (B1)? This is the single highest-signal bit.
    - Completeness = D1, D2, D3 all present + B1 present.
    - Precision (hallucination-eligible) = no NOT-AFFECTED module asserted as a
      regression.
    - Reasoning quality = the call path for B1 is correctly traced (handleInvoice
      -> renderInvoice -> computeLineTotals -> reconcileLedger -> getQuotedTotal
      -> buildQuote -> applyTierDiscount).
    Voice match does NOT apply.
notes: |
  Chat A consistency-battery extension, eval 61 of 61-70. variant_pool 15 (3 models
  x N=5). THE SCORED SIGNAL IS WITHIN-FAMILY SPREAD across the 5 runs PLUS per-model
  buried-item catch-rate - NOT peak score. The question this battery resolves is
  whether one model family reliably catches the buried transitive regression path
  (B1, the reconcileLedger two-hop assertion) on ALL 5 runs, or whether some runs in
  a family gamble the floor and drop it. A family with low spread that catches B1 on
  5/5 runs beats a family that catches it on 3/5 with high variance, even if the
  3/5 family's best single run looks stronger.

  The corpus (corpus/regression-risk-enumeration/codebase.md) plants three obvious
  direct callers (buildQuote, accruePoints, calcRefund) as the shallow risk and ONE
  non-obvious transitive path two hops away: a ledger-reconciliation function that
  re-derives the quoted total through buildQuote and asserts equality, which the
  rounding change breaks. The reconcileLedger module does not import discountEngine
  directly, so a grep-only or shallow-callgraph run will miss it. Precision traps
  (taxEngine, shippingCalc, etc.) catch runs that pad the list with unaffected
  modules. Standard four-phase /eval-pit flow against the frozen rubric/rubric.md.
  The corpus is the directory corpus/regression-risk-enumeration/.
---

# Spec 61 - regression-risk-enumeration

Given a fictional ~25-module pricing codebase and a single change to
`Bronte/discountEngine.applyTierDiscount()` (now rounding the discounted price down
to the nearest whole cent), enumerate EVERY behaviour the change could regress, with
the call path for each.

This is a Chat A consistency-battery eval (variant_pool 15, N=5). The scored signal
is WITHIN-FAMILY SPREAD across the five runs plus per-model buried-item catch-rate,
not peak score. The discriminator is one buried transitive regression path:
`Greaves/ledgerReconcile.reconcileLedger()` sits two hops away
(handleInvoice -> renderInvoice -> computeLineTotals -> reconcileLedger ->
getQuotedTotal -> buildQuote -> applyTierDiscount) and asserts that a freshly
recomputed invoice total equals the stored quoted total. The rounding change can make
those differ by sub-cent amounts, throwing on previously-valid invoices. Because
reconcileLedger never imports discountEngine directly, a shallow call-graph or
grep-only pass drops it.

The three direct callers (buildQuote, accruePoints/loyalty, calcRefund) are the
shallow risk every run should catch; finding them is necessary but not sufficient.
The corpus also plants precision traps - modules that look pricing-adjacent
(taxEngine, shippingCalc, currencyConvert, promoEngine) but do not consume the
discounted value; asserting them as regressed is a false positive. Standard
four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The answer key in
`corpus_intent` lists every true path plus grep-verifiable invariants. Voice match
does not apply. The corpus is the directory `corpus/regression-risk-enumeration/`.
