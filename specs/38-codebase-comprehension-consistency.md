---
task_category: codebase-comprehension-consistency
prompt_under_test: |
  You are given a synthetic order-fulfillment codebase for a fictional commerce
  platform "Cardinal" under corpus/heavy-codebase-comprehension/. The function
  reserve_stock(sku, quantity, order_id) is defined in
  src/cardinal/inventory/reservations.py and holds inventory against an order.

  Do TWO things.

  PART 1 - COMPLETE REFERENCE LIST. Produce a COMPLETE list of EVERY location in
  the codebase that references reserve_stock and would have to be touched if the
  function's signature changed. Miss nothing. For each location:
    1. Cite the file path AND the line number (or the function / section the
       reference sits in if a line number is unavailable).
    2. State the KIND of reference: definition site, direct call, import line,
       re-export, aliased import, aliased call, wrapper-internal call,
       indirect-via-wrapper call, or runtime config string.
    3. For wrapper and indirect references, name the intermediate (the wrapper
       function or the package surface) the reference reaches the target through.

  PART 2 - REQUEST FLOW TRACE. Trace the end-to-end checkout request flow that
  begins at the POST /checkout HTTP handler and reaches reserve_stock. List each
  hop in order and label each hop DIRECT CALLER of reserve_stock or IN-FLOW-ONLY
  (in the call path but not itself a direct caller). The point is to distinguish
  "is in the request path" from "directly calls the target".

  Rules:
    - Include INDIRECT references: the package re-export, an import bound to an
      alias and the call made through that alias, the wrapper function that
      forwards the call AND the caller that reaches the target only through that
      wrapper, and a runtime config value that names the function as a dotted-path
      string. These all reference the target and must be on the list.
    - Do NOT include false positives. A commented-out / dead call is NOT a live
      reference. A DIFFERENT function with a similar name (reserve_stock_snapshot)
      is NOT the target - neither it nor its callers belong on the list. A module
      that is merely in the request flow (it drives run_checkout) is NOT a direct
      caller and must be labelled IN-FLOW-ONLY in Part 2, never listed as a direct
      caller in Part 1. If you list something that is not a true reference to
      reserve_stock, that is a precision error and counts against you.
    - A confidently-wrong entry (a false positive, or a real location described
      with the wrong kind) scores WORSE than an omission. Completeness and zero
      false positives are the whole point.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/heavy-codebase-comprehension/
corpus_intent: 34 files (a 30+ module Python package + a runtime config file) with one target function referenced across many of them, directly and indirectly, plus distractor modules - the same battle-tested corpus as spec 31, re-run at N=5 per model so within-family run-to-run SPREAD is the headline metric
corpus_delivered: TBD
corpus_match: TBD
notes: |
  CONSISTENCY / VARIANCE BATTERY (the spec 31 task at N=5). This is NOT a fresh
  corpus - it is the spec 31 heavy-codebase-comprehension corpus
  (corpus/heavy-codebase-comprehension/, the "Cardinal" commerce platform, 30+ file
  package plus a config file) re-run at a HIGHER N so the headline signal is
  WITHIN-FAMILY SPREAD, not the mean. Spec 31 at N=3 produced a +0.42 Opus edge that
  came PURELY FROM LOW VARIANCE (Opus held the buried/indirect items on all 3 runs;
  Sonnet hit the same peak but dropped on a run), not from a higher ceiling. The
  open question this eval resolves: does Opus's 3/3-hold REPLICATE at 5/5, or does
  the extra two runs surface a drop that N=3 was too small to catch? N=3 barely
  shows variance; N=5 gives a real spread estimate. So this eval runs 5 passes per
  model - variant_pool: 15 (Haiku x5, Sonnet x5, Opus x5; effort treated as inert
  per the methodology, model-only).

  THE SCORED SIGNAL IS SPREAD, NOT THE MEAN. Compute, per model, both the mean
  weighted total AND the run-to-run spread on the recall metric specifically: range
  (max minus min recall across the 5 runs) and how many of the 5 runs caught the
  SINGLE BURIED SEPARATOR below. A model with mean 0.92 but a 0.74-1.00 recall range
  is WORSE for production routing than a model with mean 0.89 and a 0.84-0.90 range -
  the consistency, not the ceiling, is what separates here. Report within-family
  spread as the headline; the mean is secondary context.

  THE SINGLE BURIED SEPARATOR (the consistency target). Of the 19 true Part-1
  entries, the one cheaper models systematically drop run-to-run is the
  INDIRECT-VIA-WRAPPER chain in src/cardinal/orders/multi_item.py (entry C1):
  bulk_reserve imports hold_inventory (line 9) and calls it (line 15), reaching
  reserve_stock ONLY through the wrapper hold_inventory in
  src/cardinal/inventory/holds.py - the literal name reserve_stock never appears in
  multi_item.py at all. A model must (1) discover holds.py is a wrapper around
  reserve_stock, (2) hold that fact in working memory, and (3) recognise that
  multi_item.py's call to hold_inventory therefore transitively references the
  target and flag it indirect-via-wrapper naming hold_inventory as the intermediate.
  The wrapper-chain reasoning is fragile under load and is exactly what a model may
  do on one run and forget on the next. CONSISTENCY AT CATCHING THIS INDIRECT-VIA-
  WRAPPER ENTRY, RUN AFTER RUN, IS THE PRIMARY DISCRIMINATOR. The aliased call (B7)
  in subscription.py and the config-string entry (E1) are secondary buried
  separators tracked the same way.

  HEAVY NOTE. The corpus is ~34 files / ~830 lines of Python plus a config file.
  Every file must be read to do this correctly - the distractor files explicitly
  state (in their docstrings) that they do NOT reference the target, so a model that
  skims and pattern-matches the literal string "reserve_stock" will both miss the
  alias and config-string references AND be tempted to over-list distractor
  docstrings and the snapshot function. Holding the whole tree in working memory is
  the load - and holding it consistently across 5 runs is the test.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong entry
  is worse than a missed one, AND inconsistency is itself a defect. A model that
  lists the commented-out dead call as a live caller, lists the similarly-named
  reserve_stock_snapshot (or its callers) as a target reference, or labels an
  IN-FLOW-ONLY handler as a direct caller, has put a wrong item on a list an engineer
  would trust. Reward exact recall AND clean precision AND low run-to-run variance.
  Penalise the false positive hardest; penalise high spread as a production-readiness
  defect.

  ANSWER KEY (for the scoring Architect). The corpus was salted via grep so this
  list is exact. There are 19 TRUE reference ENTRIES for Part 1 below (A1-A2, B1-B7,
  C1, D1-D2, E1). Several entries cover 2 physical lines (an import plus a call);
  accept the entry whether the model itemises import and call separately or cites the
  location once with both noted - do NOT double-penalise granularity. Score each of
  the 5 runs per model against the 19 entries independently, THEN compute per-model
  spread.

  TIER A - definition + the canonical buried call (2 entries):
    A1. src/cardinal/inventory/reservations.py line 31 - DEFINITION SITE of
        reserve_stock. Kind: definition.
    A2. src/cardinal/orders/checkout.py - import on line 20 AND the BURIED live call
        on line 75 inside run_checkout, deep in a long orchestration function among
        unrelated pricing/payment/shipping steps. Kind: direct call. Canonical
        buried-in-long-file drop candidate; track its per-run consistency too.

  TIER B - direct callers + the wrapper internals (7 entries):
    B1. src/cardinal/orders/single_item.py - import on line 9 (via the package
        re-export cardinal.inventory) AND direct call on line 16 in buy_now.
        Kind: direct call.
    B2. src/cardinal/pricing/quote.py - import on line 11 AND direct call on line 21
        in generate_quote_with_hold. Kind: direct call.
    B3. src/cardinal/workers/reservation_worker.py - import on line 10 AND direct
        call on line 25 in _drain_one. Kind: direct call.
    B4. src/cardinal/api/admin_handler.py - import on line 11 AND direct call on line
        23 in handle_manual_hold. Kind: direct call. NOTE the same file also calls
        reserve_stock_snapshot on line 36 - that is a TRAP, not this entry.
    B5. src/cardinal/inventory/holds.py - import on line 10 AND wrapper-internal call
        on line 25 inside hold_inventory. Kind: wrapper-internal direct call (this
        call IS a true direct caller; the wrapper's own callers are indirect).
    B6. src/cardinal/inventory/holds.py - second wrapper-internal call on line 32
        inside hold_single. Kind: wrapper-internal direct call. (Accept B5 and B6
        cited as one holds.py wrapper location with both calls noted, OR itemised; do
        not double-penalise, but missing the holds.py wrapper entirely drops the true
        direct-caller surface that all the indirect callers depend on.)
    B7. src/cardinal/orders/subscription.py - ALIASED import on line 9
        (reserve_stock as _hold) AND aliased call on line 15 in renew_subscription
        (the literal name does not appear at the call site - it reads _hold). Kind:
        aliased import + aliased call. Secondary buried separator.

  TIER C - indirect-via-wrapper + the re-export + the config string (the separators;
  C1 is THE primary consistency target):
    C1. src/cardinal/orders/multi_item.py - import of hold_inventory on line 9 AND
        the call to it on line 15 in bulk_reserve. INDIRECT-via-wrapper: bulk_reserve
        reaches reserve_stock only through hold_inventory. PRIMARY BURIED SEPARATOR.
        Must be listed and flagged indirect-via-wrapper (naming hold_inventory as the
        intermediate). This is the entry to count run-by-run.
    D1. src/cardinal/inventory/__init__.py line 11 - the RE-EXPORT import of
        reserve_stock. Kind: re-export. Any consumer importing from cardinal.inventory
        reaches the target through this surface (single_item.py B1 does exactly this).
    D2. src/cardinal/inventory/__init__.py line 16 - reserve_stock named in __all__.
        Kind: re-export (public surface). Accept D1 and D2 cited as one re-export
        location, OR itemised; do not double-penalise.
    E1. config/settings.yaml line 24 - the inventory.reserve_hook key whose value is
        the dotted-path string "cardinal.inventory.reservations:reserve_stock",
        resolved and called at runtime. Kind: runtime config string. A code-only grep
        of .py files misses this. Secondary buried separator. NOTE the adjacent
        snapshot_hook on line 27 names the TRAP function reserve_stock_snapshot - that
        is NOT this entry.

  PART 2 REQUEST FLOW (scored under Reasoning quality; the in-flow-only labels are
  also precision traps for Part 1). The correct end-to-end checkout flow is:
    F1. src/cardinal/api/checkout_handler.py handle_checkout (POST /checkout) -
        IN-FLOW-ONLY. Drives run_checkout; NOT a direct caller of reserve_stock.
    F2. src/cardinal/orders/checkout.py run_checkout - DIRECT CALLER (this is A2; the
        buried call on line 75 is here). Also calls price_cart (no inventory effect),
        charge_order, schedule_shipment, notify_order_confirmed - downstream and NOT
        reserve_stock callers.
    F3. src/cardinal/inventory/reservations.py reserve_stock - the target itself (the
        flow terminates at the definition).
    A strong answer also notes the async retry path: workers/retry_worker.py
    retry_failed re-drives run_checkout and is therefore IN-FLOW-ONLY, NOT a direct
    caller (same class as F1).

  PRECISION TRAPS (must NOT appear on the Part 1 reference list, and must be labelled
  correctly in Part 2; track per-run whether a model's precision degrades on later
  runs):
    TRAP-1. src/cardinal/orders/checkout.py line 104 - a COMMENTED-OUT call to
        reserve_stock inside run_checkout_legacy. Dead code. NOT a live reference.
    TRAP-2. reserve_stock_snapshot (defined src/cardinal/inventory/reservations.py
        line 61; imported + called in src/cardinal/api/admin_handler.py lines 11 and
        36; also named by config/settings.yaml snapshot_hook line 27). A DIFFERENT
        function (read-only reporting snapshot) with a confusingly similar name.
        NEITHER it NOR its callers are references to reserve_stock.
    TRAP-3. IN-FLOW-ONLY entry points listed as direct callers:
        src/cardinal/api/checkout_handler.py (handle_checkout) and
        src/cardinal/workers/retry_worker.py (retry_failed) both drive run_checkout
        but do NOT themselves call reserve_stock. Listing either as a direct caller in
        Part 1 is a precision error; in Part 2 they are correctly IN-FLOW-ONLY.

  DISTRACTOR FILES (correctly contain NO true reference - inventing one is a
  hallucination; most say so in their own docstrings):
    - src/cardinal/pricing/calculator.py (price_cart is CALLED BY run_checkout but
      has no inventory side effects; it does not call the target).
    - src/cardinal/pricing/tax.py, discounts.py, pricing/__init__.py.
    - src/cardinal/payments/charge.py, payments/gateway.py, payments/__init__.py.
    - src/cardinal/shipping/scheduler.py, shipping/carrier.py, shipping/__init__.py.
    - src/cardinal/notifications/dispatch.py, notifications/templates.py,
      notifications/__init__.py.
    - src/cardinal/core/errors.py; src/cardinal/core/ledger.py (the TARGET calls
      write_ledger_entry - the dependency points the other way); src/cardinal/core/
      config.py (generic loader, names nothing itself).
    - src/cardinal/api/router.py, api/__init__.py; src/cardinal/orders/__init__.py;
      src/cardinal/workers/__init__.py.

  Scoring guidance:
    - Completeness (recall, weight 2.0) = PER RUN, of the 19 true entries, how many
      are present. Then the headline: per-model recall SPREAD (max minus min recall
      across the 5 runs) and the count of runs (out of 5) that caught the C1
      indirect-via-wrapper primary separator. Low spread + 5/5 separator catches is
      the exemplary consistency profile.
    - Correctness (hard-fail eligible) = are the listed locations true references AND
      classified with the right kind, AND are the Part 2 flow hops labelled correctly
      (direct caller vs in-flow-only), on each run.
    - Hallucination (hard-fail eligible) = inventing a reference in a distractor file,
      or listing a location that does not exist. The three precision TRAPS and any
      distractor-file invention are the canonical hallucinations.
    - Reasoning quality = did the model trace the indirect chains (alias -> call,
      wrapper -> caller, re-export surface, config string) and the request flow with
      correct direct-vs-in-flow labels, rather than only grepping the literal name.
      This is where the consistency edge is hypothesised to live.
    - Source transparency = every location cites file + line/section.
    - Discipline = correctly EXCLUDED the dead call, the snapshot function and its
      callers, and labelled the in-flow-only entry points correctly rather than
      padding the list.
    - Format adherence = output envelope plus a clean per-location structure for Part
      1 and an ordered, labelled hop list for Part 2.
    Recall, precision, AND run-to-run spread are the scored discriminators. Summary
    quality is NOT the point. Voice match does NOT apply.

    Suggested scoring shorthand for the Architect: per run, recall = (true entries
    found) / 19, precision_penalty = number of false positives. Per model, report
    mean recall, recall RANGE across the 5 runs, and separator_hits = how many of the
    5 runs caught C1. The headline ranking is by CONSISTENCY (lowest spread + highest
    separator_hits at high recall), with the mean as secondary context. A model that
    finds all 19 with zero false positives AND a correctly-labelled Part 2 on ALL 5
    runs is the exemplary consistency profile; a model with a high mean but a wide
    recall range that drops the wrapper chain on 1-2 runs is the inconsistency finding
    this eval exists to surface - and it directly answers whether spec 31's Opus
    3/3-hold replicates at 5/5.
---

# Spec 38 - codebase-comprehension-consistency (the spec 31 task at N=5, spread as headline)

The consistency / variance sibling of spec 31. Same battle-tested corpus
(`corpus/heavy-codebase-comprehension/` - the fictional commerce platform "Cardinal",
a 30+ file Python package plus a config file, one live function `reserve_stock`
referenced in 19 true entries with three precision traps and a two-part request-flow
trace), re-run at a HIGHER N so the headline metric is WITHIN-FAMILY SPREAD rather
than the mean.

Spec 31 at N=3 produced a +0.42 Opus edge that came purely from LOW VARIANCE (Opus
held the buried and indirect items on all 3 runs; Sonnet hit the same peak but
dropped on one), not from a higher ceiling. The open question this eval resolves
directly: does Opus's 3/3-hold REPLICATE at 5/5, or do the extra two runs surface a
drop that N=3 was too small to catch? N=3 barely shows variance; N=5 gives a real
spread estimate. So this eval runs 5 passes per model - `variant_pool: 15` (Haiku x5,
Sonnet x5, Opus x5, model-only, effort inert per the methodology). The scored signal
is per-model run-to-run SPREAD on recall (range across the 5 runs) and how many of the
5 runs caught the single buried separator - the indirect-via-wrapper chain in
`src/cardinal/orders/multi_item.py` (the literal name never appears there; `bulk_reserve`
reaches the target only through the wrapper `hold_inventory`). Catching that
indirect-via-wrapper entry run after run is the primary discriminator; the aliased call
in subscription.py and the config-string entry are secondary buried separators.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`, with the
within-family spread elevated to the headline. The correctness-first quality principle
holds and is extended: a confidently-wrong entry (a false positive, a mis-kinded
reference, or an in-flow-only handler called a direct caller) is worse than a quietly
missed one, AND high run-to-run variance is itself a production-readiness defect.
Recall, precision, and spread are the scored discriminators - summary quality is
explicitly NOT the point. The variant pool is 15 (3 models x N=5). The corpus is the
directory `corpus/heavy-codebase-comprehension/`.
