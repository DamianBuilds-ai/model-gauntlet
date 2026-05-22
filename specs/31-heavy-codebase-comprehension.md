---
task_category: codebase-comprehension
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
variant_pool: 9
corpus: corpus/heavy-codebase-comprehension/
corpus_intent: 33 files (a 30+ module Python package + a runtime config file) with one target function referenced across many of them, directly and indirectly, plus distractor modules that contain no true reference
corpus_delivered: TBD
corpus_match: TBD
notes: |
  OPUS-STRESS PROBE (codebase comprehension / caller-trace forgetting-under-load).
  This is the cross-reference-completeness mechanism (spec 22) scaled UP to a 30+
  file codebase: instead of 16 files and 20 entries, the reference set is spread
  across a deeper package tree where most files are distractors that mention the
  word "reserve_stock" only in docstrings saying they do NOT reference it. The
  hypothesis is the same and stronger at this scale: cheaper models find the
  obvious direct calls but DROP the buried call, the aliased call, the wrapper
  chain, and the config string (recall failure), or invent / mis-classify a
  location, or list a trap to look thorough (precision failure). Run the full
  9-variant model-only pool (Haiku x3, Sonnet x3, Opus x3; effort treated as inert
  per the methodology). Aggregate the 3 passes per model (mean weighted total);
  flag any model whose 3 passes diverge by more than 0.5 as a consistency finding.

  HEAVY NOTE. The corpus is ~30 files / ~830 lines of Python plus a config file.
  Every file must be read to do this correctly - the distractor files explicitly
  state (in their docstrings) that they do NOT reference the target, so a model
  that skims and pattern-matches the literal string "reserve_stock" will both (a)
  miss the alias and the config-string references that do not contain a clean call
  of the literal name AND (b) be tempted to over-list distractor docstrings and
  the snapshot function. Holding the whole tree in working memory is the load.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong
  entry is worse than a missed one. A model that lists the commented-out dead call
  as a live caller, lists the similarly-named reserve_stock_snapshot (or its
  callers) as a target reference, or labels an IN-FLOW-ONLY handler as a direct
  caller, has put a wrong item on a list an engineer would trust and act on -
  worse than quietly missing one real location. Reward exact recall AND clean
  precision. Penalise the false positive hardest.

  ANSWER KEY (for the scoring Architect). The corpus was salted via grep so this
  list is exact. There are 19 TRUE reference ENTRIES for Part 1 below (A1-A2,
  B1-B7, C1-C4, plus the re-export D1-D2 and config E1), organised into tiers by
  how easy they are to find. Several entries cover 2 physical lines (an import
  plus a call); accept the entry whether the model itemises import and call
  separately or cites the location once with both noted - do NOT double-penalise
  granularity, but a model that misses an entry entirely drops a real location.
  The discriminator is whether a model holds ALL of them, especially the INDIRECT
  ones (alias, wrapper-chain, config string), without dropping any and without
  adding the three traps.

  TIER A - definition + the canonical buried call (2 entries; the buried one is the
  primary drop candidate):
    A1. src/cardinal/inventory/reservations.py line 31 - DEFINITION SITE of
        reserve_stock (the function being traced). Kind: definition.
    A2. src/cardinal/orders/checkout.py - import on line 20 AND the BURIED live
        call on line 75 inside run_checkout, deep in a long orchestration function
        among unrelated pricing/payment/shipping steps. Kind: direct call. This is
        the canonical "buried in a long file" drop candidate.

  TIER B - direct callers + the wrapper internals (7 entries; every model should
  get the obvious ones, weaker models start dropping the wrapper-internal calls):
    B1. src/cardinal/orders/single_item.py - import on line 9 (via the package
        re-export cardinal.inventory) AND direct call on line 16 in buy_now.
        Kind: direct call (import is via re-export surface).
    B2. src/cardinal/pricing/quote.py - import on line 11 AND direct call on line
        21 in generate_quote_with_hold (soft hold on a quote). Kind: direct call.
    B3. src/cardinal/workers/reservation_worker.py - import on line 10 AND direct
        call on line 25 in _drain_one (background reservation worker). Kind: direct
        call.
    B4. src/cardinal/api/admin_handler.py - import on line 11 AND direct call on
        line 23 in handle_manual_hold (operator manual hold endpoint). Kind: direct
        call. NOTE the same file also calls reserve_stock_snapshot on line 36 - that
        is a TRAP, not this entry.
    B5. src/cardinal/inventory/holds.py - import on line 10 AND wrapper-internal
        call on line 25 inside hold_inventory. Kind: wrapper-internal direct call
        (this call IS a true direct caller; the wrapper's own callers are indirect).
    B6. src/cardinal/inventory/holds.py - second wrapper-internal call on line 32
        inside hold_single. Kind: wrapper-internal direct call. (Accept B5 and B6
        cited as one holds.py wrapper location with both calls noted, OR itemised;
        do not double-penalise, but missing the holds.py wrapper entirely drops the
        true direct-caller surface that all the indirect callers depend on.)
    B7. src/cardinal/orders/subscription.py - ALIASED import on line 9
        (reserve_stock as _hold) AND aliased call on line 15 in renew_subscription
        (the literal name does not appear at the call site - it reads _hold). Kind:
        aliased import + aliased call. A model that searches only for the literal
        name at call sites misses the call on line 15.

  TIER C - indirect-via-wrapper + the re-export + the config string (the OPUS
  separators; these are where comprehension load bites hardest):
    C1. src/cardinal/orders/multi_item.py - import of hold_inventory on line 9 AND
        the call to it on line 15 in bulk_reserve. INDIRECT-via-wrapper: bulk_reserve
        reaches reserve_stock only through hold_inventory. Must be listed and flagged
        indirect-via-wrapper (naming hold_inventory as the intermediate). A model
        that lists only direct callers drops this.
    D1. src/cardinal/inventory/__init__.py line 11 - the RE-EXPORT import of
        reserve_stock. Kind: re-export. Any consumer importing from cardinal.inventory
        reaches the target through this surface (single_item.py B1 does exactly this).
    D2. src/cardinal/inventory/__init__.py line 16 - reserve_stock named in __all__.
        Kind: re-export (public surface). Accept D1 and D2 cited as one re-export
        location, OR itemised; do not double-penalise, but a model that misses the
        re-export entirely drops the surface that B1 depends on.
    E1. config/settings.yaml line 24 - the inventory.reserve_hook key whose value is
        the dotted-path string "cardinal.inventory.reservations:reserve_stock",
        resolved and called at runtime. Kind: runtime config string. A code-only grep
        of .py files misses this. NOTE the adjacent snapshot_hook on line 27 names the
        TRAP function reserve_stock_snapshot - that is NOT this entry.

  PART 2 REQUEST FLOW (scored under Reasoning quality; the in-flow-only labels are
  also precision traps for Part 1). The correct end-to-end checkout flow is:
    F1. src/cardinal/api/checkout_handler.py handle_checkout (POST /checkout) -
        IN-FLOW-ONLY. Drives run_checkout; NOT a direct caller of reserve_stock.
    F2. src/cardinal/orders/checkout.py run_checkout - DIRECT CALLER (this is A2;
        the buried call on line 75 is here). Also calls price_cart (no inventory
        effect), charge_order, schedule_shipment, notify_order_confirmed - those are
        downstream and NOT reserve_stock callers.
    F3. src/cardinal/inventory/reservations.py reserve_stock - the target itself
        (the flow terminates at the definition).
    A strong answer also notes the async retry path: workers/retry_worker.py
    retry_failed re-drives run_checkout and is therefore IN-FLOW-ONLY, NOT a direct
    caller (same class as F1).

  PRECISION TRAPS (must NOT appear on the Part 1 reference list, and must be labelled
  correctly in Part 2 - listing any as a true reference / direct caller is a
  confidently-wrong false positive and the heaviest penalty):
    TRAP-1. src/cardinal/orders/checkout.py line 104 - a COMMENTED-OUT call to
        reserve_stock inside run_checkout_legacy. Dead code. NOT a live reference. A
        model that lists it has put a no-op item on the list.
    TRAP-2. reserve_stock_snapshot (defined src/cardinal/inventory/reservations.py
        line 61; imported + called in src/cardinal/api/admin_handler.py lines 11 and
        36; also named by config/settings.yaml snapshot_hook line 27). A DIFFERENT
        function (read-only reporting snapshot, not an inventory hold) with a
        confusingly similar name. NEITHER it NOR its callers are references to
        reserve_stock. Listing any of them is a precision error.
    TRAP-3. IN-FLOW-ONLY entry points listed as direct callers:
        src/cardinal/api/checkout_handler.py (handle_checkout) and
        src/cardinal/workers/retry_worker.py (retry_failed) both drive run_checkout
        but do NOT themselves call reserve_stock. Listing either as a direct caller in
        Part 1 is a precision error; in Part 2 they are correctly IN-FLOW-ONLY.

  DISTRACTOR FILES (correctly contain NO true reference - a model that invents a
  reference in any of these has hallucinated a location; most say so in their own
  docstrings):
    - src/cardinal/pricing/calculator.py (price_cart is CALLED BY run_checkout but
      has no inventory side effects; it does not call the target).
    - src/cardinal/pricing/tax.py, discounts.py, pricing/__init__.py.
    - src/cardinal/payments/charge.py (downstream of the reservation, no call),
      payments/gateway.py, payments/__init__.py.
    - src/cardinal/shipping/scheduler.py, shipping/carrier.py, shipping/__init__.py.
    - src/cardinal/notifications/dispatch.py, notifications/templates.py,
      notifications/__init__.py.
    - src/cardinal/core/errors.py; src/cardinal/core/ledger.py (the TARGET calls
      write_ledger_entry - the dependency points the other way, so ledger is NOT a
      caller); src/cardinal/core/config.py (generic loader, names nothing itself).
    - src/cardinal/api/router.py, api/__init__.py; src/cardinal/orders/__init__.py;
      src/cardinal/workers/__init__.py.

  Scoring guidance:
    - Completeness (recall, weight 2.0) = of the 19 true entries (A1-A2, B1-B7,
      C1, D1-D2, E1; counting the holds.py wrapper as 1-2 and the re-export as 1-2
      per the granularity note), how many are present. Count DROPPED locations
      explicitly. Tier C drops (indirect-via-wrapper, re-export, config string) are
      the strongest signal of forgetting-under-load; the A2 buried call and the B7
      aliased call are the next strongest; missing an obvious B1-B4 direct call is a
      serious miss at this scale.
    - Correctness (hard-fail eligible) = are the listed locations actually true
      references AND classified with the right kind, AND are the Part 2 flow hops
      labelled correctly (direct caller vs in-flow-only). A list dominated by
      wrong/mis-kinded entries, or a Part 2 that calls handle_checkout a direct
      caller, fails Correctness.
    - Hallucination (hard-fail eligible) = inventing a reference in a distractor
      file, or listing a location that does not exist. The three precision TRAPS and
      any distractor-file invention are the canonical hallucinations here.
    - Reasoning quality = did the model trace the indirect chains (alias -> call,
      wrapper -> caller, re-export surface, config string) and the request flow
      (handle_checkout -> run_checkout -> reserve_stock with correct direct vs
      in-flow labels) rather than only grepping the literal name. This is where Opus
      is hypothesised to separate.
    - Source transparency = every location cites file + line/section.
    - Discipline = did it correctly EXCLUDE the commented-out dead call, the
      snapshot function and its callers, and label the in-flow-only entry points
      correctly rather than padding the list. A model that lists the traps to look
      thorough is penalised, not rewarded.
    - Format adherence = the output envelope plus a clean per-location structure
      (path, kind, intermediate) for Part 1 and an ordered, labelled hop list for
      Part 2.
    Recall and precision are the scored discriminators. Summary quality is NOT the
    point. Voice match does NOT apply.

    Suggested scoring shorthand for the Architect: recall = (true entries found) /
    19; precision penalty = number of false positives (each trap, distractor-file
    invention, or in-flow-only-labelled-as-direct-caller). A model that finds all 19
    with zero false positives AND a correctly-labelled Part 2 flow is the exemplary 5
    on Completeness and Correctness; dropping Tier C indirect items, missing the
    buried or aliased call, or listing a trap is where the score falls.
---

# Spec 31 - heavy-codebase-comprehension (the caller-trace forgetting-under-load probe)

The heavy, scaled-up sibling of spec 22 (cross-reference-completeness). Where spec 22
traces one deprecated function across 16 interlinked files, this traces one live
function `reserve_stock(sku, quantity, order_id)` across a 30+ file Python package for
a fictional commerce platform "Cardinal" under `corpus/heavy-codebase-comprehension/`.
The task has two parts: (1) find EVERY location that references the target - direct
calls, imports, the package re-export, an aliased import and its aliased call, the
wrapper that forwards to it and the caller that reaches it only through that wrapper,
and a runtime config dotted-path string - without dropping the buried or indirect ones
and without inventing or mis-counting any; and (2) trace the end-to-end checkout
request flow, labelling each hop a direct caller or merely in-flow.

The corpus is ~33 files / ~830 lines plus a config file. Most files are distractors
whose docstrings state outright that they do NOT reference the target, so a model that
pattern-matches the literal string "reserve_stock" both misses the alias and config
references (which do not contain a clean literal call) and is tempted to over-list the
distractor docstrings and the similarly-named `reserve_stock_snapshot`. Holding the
whole tree in working memory is the load - this is the eval-22 forgetting-under-load
mechanism scaled to a codebase.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is central: a confidently-wrong entry (a false
positive, a mis-kinded reference, or an in-flow-only handler called a direct caller) is
worse than a quietly missed one, because an engineer acts on the list. Completeness
(recall against the 19-entry answer key) and Correctness / Hallucination (zero false
positives, no invented references, correct direct-vs-in-flow labels) are the scored
discriminators - summary quality is explicitly NOT the point. Reasoning quality
captures whether the model traced the indirect chains and the request flow rather than
grepping the literal name. Three precision traps are planted: a commented-out dead
call, a confusingly similar function (`reserve_stock_snapshot`) and its callers, and
in-flow-only entry points that drive `run_checkout` without calling the target
directly. The variant pool is 9 (3 models x N=3, effort inert per the methodology). The
corpus is the directory `corpus/heavy-codebase-comprehension/`.
