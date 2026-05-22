---
task_category: cross-reference-completeness-consistency
prompt_under_test: |
  You are given a synthetic codebase for a fictional billing platform "Acme
  Ledger" under corpus/cross-reference-completeness/. The deprecated function
  legacy_compute_tax(amount, region) (defined in src/tax/legacy.py) is being
  retired in favour of the new TaxEngine.compute(amount, region, *, inclusive)
  in src/tax/engine.py.

  Produce a COMPLETE migration checklist of EVERY location in the codebase that
  references the deprecated legacy_compute_tax and must change for the migration.
  Miss nothing. For each location:
    1. Cite the file path AND the line number (or the function / section the
       reference sits in if a line number is unavailable).
    2. State the KIND of reference: definition site, direct call, import line,
       re-export, aliased import or aliased call, wrapper, indirect-via-wrapper,
       config string, doc/prose mention, or test.
    3. Note one word on what the migration must do there (repoint, replace call,
       update import, delete, etc.).

  Rules:
    - Include INDIRECT references: a re-export, an import bound to an alias and
      the call made through that alias, a wrapper function that forwards the call
      and the callers that go through the wrapper, a config value that names the
      function as a dotted-path string, and a documentation file that names the
      function in prose. These all reference the deprecated function and must be
      on the checklist.
    - Do NOT include false positives. A reference that is commented-out / dead
      code is NOT a live location requiring a code change. A different function
      with a similar name is NOT the target. If you list something that is not a
      true reference to legacy_compute_tax, that is a precision error and counts
      against you.
    - A confidently-wrong entry (a false positive, or a real location described
      with the wrong kind) scores WORSE than an omission. Completeness and zero
      false positives are the whole point.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/cross-reference-completeness/
corpus_intent: 16 interlinked files (code modules + config + spec doc + test) with one deprecated function referenced across many of them - the same battle-tested corpus as spec 22, re-run at N=5 per model so within-family run-to-run SPREAD is the headline metric
corpus_delivered: TBD
corpus_match: TBD
notes: |
  N=5 RE-RUN OF EVAL 37 (statistical confidence on the contested consistency result).
  This is a re-run of eval 37 (cross-reference-completeness-consistency) at
  variant_pool: 15 (Haiku x5, Sonnet x5, Opus x5; effort treated as inert per the
  methodology). Eval 37 was the CONTESTED consistency result that CONTRADICTED the
  Opus-consistency thesis from batch 3 - it did not show Opus holding the buried
  wrapper-chain separator more reliably than Sonnet across runs. This re-run repeats
  the identical task at N=5 to confirm or overturn that contradicting result with
  statistical confidence on the run-to-run SPREAD. The corpus, prompt, task_category,
  and answer key are REUSED VERBATIM from eval 37 (same corpus as spec 22) - the only
  changes are the spec number and slug; the variant_pool stays 15. Do NOT re-author
  the corpus.

  CONSISTENCY / VARIANCE BATTERY (the spec 22 task at N=5). This is NOT a fresh
  corpus - it is the spec 22 cross-reference-completeness corpus
  (corpus/cross-reference-completeness/) re-run at a HIGHER N so the headline
  signal is WITHIN-FAMILY SPREAD, not the mean. The batch-3 read (eval 25 = exact
  opus/sonnet tie on the mean; eval 31 = a +0.42 edge that came purely from LOW
  VARIANCE, not a higher ceiling) suggests Opus's completeness advantage is
  CONSISTENCY (run-to-run reliability at holding the hard buried item every single
  run) rather than a higher peak Sonnet cannot reach. N=3 barely shows variance;
  N=5 gives a real spread estimate. So this eval runs 5 passes per model -
  variant_pool: 15 (Haiku x5, Sonnet x5, Opus x5; effort treated as inert per the
  methodology, model-only).

  THE SCORED SIGNAL IS SPREAD, NOT THE MEAN. The question this eval answers: does
  Opus reliably hold the buried indirect references on EVERY one of its 5 runs
  while Sonnet hits the same peak on its best run but gambles on the floor (drops a
  buried item on 1-2 of its 5)? Compute, per model, both the mean weighted total
  AND the run-to-run spread on the recall metric specifically: range (max minus min
  recall across the 5 runs) and how many of the 5 runs caught the SINGLE BURIED
  SEPARATOR below. A model with mean 0.90 but a 0.70-1.00 recall range is WORSE for
  production routing than a model with mean 0.88 and a 0.85-0.90 range - the
  consistency, not the ceiling, is what separates here. Report within-family spread
  as the headline; the mean is secondary context.

  THE SINGLE BURIED SEPARATOR (the consistency target). Of the 20 true entries, the
  one that cheaper models systematically drop run-to-run is the indirect-via-wrapper
  chain in src/reports/annual.py (entries C5 + C6): annual.py imports the wrapper
  _apply_tax (line 13) and calls it (line 20), reaching the deprecated function
  ONLY through the wrapper - the literal name legacy_compute_tax never appears in
  annual.py at all. A model grepping the literal string never sees it; a model that
  traced the wrapper from src/reports/helpers.py the run before may forget to carry
  it on the next run. CONSISTENCY AT CATCHING THIS WRAPPER-CHAIN ENTRY, RUN AFTER
  RUN, IS THE PRIMARY DISCRIMINATOR. The aliased call (C2) in proforma.py and the
  config-string entry (C7) are secondary buried separators tracked the same way.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong entry
  is worse than a missed one, AND inconsistency is itself a defect. A model that
  lists the commented-out dead call as a live location, or lists the similarly-named
  legacy_compute_taxonomy as a target, has put a wrong item on a migration checklist
  an engineer would trust. Reward exact recall AND clean precision AND low
  run-to-run variance. Penalise the false positive hardest; penalise high spread as
  a production-readiness defect.

  ANSWER KEY (for the scoring Architect). The corpus was salted via grep so this
  list is exact. There are 20 TRUE reference ENTRIES below (A1-A8, B1-B3, C1-C9),
  covering 23 physical reference lines once the re-export entry B3 (2 lines: the
  import and the __all__) and the test entry C9 (3 lines: the import and two calls)
  are expanded. Score each of the 5 runs per model against the 20 entries
  independently, THEN compute per-model spread.

  TIER A - obvious / direct (8 locations; every model should get these every run):
    A1. src/tax/legacy.py line 13 - DEFINITION SITE of legacy_compute_tax.
        Migration: delete after all callers gone.
    A2. src/billing/invoice.py line 13 - import line. Migration: update import.
    A3. src/billing/invoice.py line 52 - direct call in build_line_items
        (LIVE CALL 1). Migration: replace call.
    A4. src/billing/invoice.py line 77 - direct call in build_summary
        (LIVE CALL 2). Migration: replace call.
    A5. src/billing/credit_note.py line 9 - import line. Migration: update import.
    A6. src/billing/credit_note.py line 15 - direct call in build_credit_note.
        Migration: replace call.
    A7. src/api/checkout.py line 9 - import line. Migration: update import.
    A8. src/api/checkout.py line 15 - direct call in price_cart (hot path).
        Migration: replace call.

  TIER B - buried in long files (3 locations; weaker models start dropping these):
    B1. src/reports/quarterly.py line 12 - import line at top of a long report
        module. Migration: update import.
    B2. src/reports/quarterly.py line 59 - call buried deep in the middle inside
        _tax_adjusted_revenue. Migration: replace call. Canonical buried-in-long-
        file drop candidate; track its per-run consistency too.
    B3. src/tax/__init__.py line 9 - re-export import of the deprecated fn (also
        named in __all__ on line 11; accept either the line-9 import, the line-11
        __all__ entry, or both cited as one re-export location - do NOT double-
        penalise). Migration: update / remove re-export.

  TIER C - indirect (the separators; 9 locations across alias, wrapper, config,
  doc, test - C5+C6 are THE primary consistency target):
    C1. src/billing/proforma.py line 12 - ALIASED import
        (legacy_compute_tax as _calc_tax). Migration: update import.
    C2. src/billing/proforma.py line 20 - ALIASED call site reading _calc_tax (the
        literal name does not appear at the call). Migration: replace call.
        Secondary buried separator.
    C3. src/reports/helpers.py line 11 - import line for the wrapper module.
        Migration: update import.
    C4. src/reports/helpers.py line 17 - call inside the wrapper _apply_tax that
        forwards to the deprecated fn. Migration: replace call (or retarget wrapper).
    C5. src/reports/annual.py line 13 - import of the wrapper _apply_tax.
        INDIRECT-via-wrapper. PRIMARY BURIED SEPARATOR. Migration: depends on
        strategy; must be listed and flagged indirect.
    C6. src/reports/annual.py line 20 - call to _apply_tax. INDIRECT-via-wrapper.
        PRIMARY BURIED SEPARATOR (the strong answer notes annual.py reaches the
        deprecated behaviour only through the wrapper, and the literal name never
        appears in annual.py). This is the entry to count run-by-run.
    C7. config/settings.yaml line 19 - the tax.calculator key whose value is the
        string "src.tax.legacy:legacy_compute_tax", resolved at runtime. Migration:
        repoint the dotted path. A code-only grep of .py files misses this.
        Secondary buried separator.
    C8. docs/tax-migration-spec.md - prose references the function name (the doc
        must be updated when the function is removed). Accept the file cited once as
        a doc/prose location.
    C9. tests/test_tax.py - import on line 13 and live calls on line 18
        (test_compute_tax_au) and line 22 (test_compute_tax_default_region). Accept
        the test file cited as one test location OR itemised; do NOT double-
        penalise. Migration: retarget tests to TaxEngine.compute.

  PRECISION TRAPS (must NOT appear on the checklist - listing either is a
  confidently-wrong false positive and the heaviest penalty; track per-run whether
  a model's precision degrades on later runs):
    TRAP-1. src/billing/invoice.py line 88 - a COMMENTED-OUT call to
        legacy_compute_tax inside render_pdf. Dead code. NOT a live location.
    TRAP-2. legacy_compute_taxonomy (defined src/tax/legacy.py line 23; used in
        tests/test_tax.py line 31). A DIFFERENT function (product taxonomy, not tax
        money) with a confusingly similar name. NOT the migration target.

  DISTRACTOR FILES (correctly contain NO true reference - inventing one is a
  hallucination):
    - src/tax/engine.py (the new TaxEngine; mentions the old name only in
      docstrings as "the thing it replaces", not as a call).
    - src/billing/__init__.py (clean package init).
    - src/api/webhooks.py (mentions the word "tax" in a log string only).

  Scoring guidance:
    - Completeness (recall, weight 2.0) = PER RUN, of the 20 true entries, how many
      are present. Then the headline: per-model recall SPREAD (max minus min recall
      across the 5 runs) and the count of runs (out of 5) that caught the C5+C6
      wrapper-chain primary separator. Low spread + 5/5 separator catches is the
      exemplary consistency profile.
    - Correctness (hard-fail eligible) = are the listed locations true references AND
      classified with the right kind, on each run.
    - Hallucination (hard-fail eligible) = inventing a reference in a distractor
      file, or listing a location that does not exist. The two precision TRAPS and
      any distractor-file invention are the canonical hallucinations.
    - Reasoning quality = did the model trace the indirect chains (alias -> call,
      wrapper -> caller, config string, doc) rather than only the literal name. This
      is where the consistency edge is hypothesised to live.
    - Source transparency = every location cites file + line/section.
    - Discipline = correctly EXCLUDED the commented-out dead call and the taxonomy
      function rather than padding the list.
    - Format adherence = output envelope plus a clean per-location structure.
    Recall, precision, AND run-to-run spread are the scored discriminators. Summary
    quality is NOT the point. Voice match does NOT apply.

    Suggested scoring shorthand for the Architect: per run, recall = (true entries
    found) / 20, precision_penalty = number of false positives. Per model, report
    mean recall, recall RANGE across the 5 runs, and separator_hits = how many of the
    5 runs caught C5+C6. The headline ranking is by CONSISTENCY (lowest spread +
    highest separator_hits at high recall), with the mean as secondary context. A
    model that finds 20/20 with zero false positives on ALL 5 runs is the exemplary
    consistency profile; a model with a high mean but a wide recall range that drops
    the wrapper chain on 1-2 runs is the inconsistency finding this eval exists to
    surface.
---

# Spec 98 - rerun-eval37-consistency-n5 (N=5 re-run of eval 37, the contested consistency result)

This is a statistical-confidence RE-RUN of eval 37
(cross-reference-completeness-consistency) at `variant_pool: 15` (3 models x N=5). Eval
37 was the CONTESTED consistency result: at N=5 it contradicted the batch-3
Opus-consistency thesis rather than confirming it. This re-run repeats the identical
task again at N=5 to confirm or overturn that contradicting result with statistical
confidence on the within-family SPREAD. The corpus, prompt, task_category, and answer
key are REUSED VERBATIM from eval 37 (the same `corpus/cross-reference-completeness/`
corpus as spec 22) - only the spec number and slug change; the variant pool remains 15.
Do NOT re-author the corpus.

Same battle-tested corpus (`corpus/cross-reference-completeness/` - the fictional
billing platform "Acme Ledger", 16 interlinked files, one deprecated
`legacy_compute_tax` referenced in 20 true entries with two precision traps). The
scored signal is per-model run-to-run SPREAD on recall (range across the 5 runs) and
how many of the 5 runs caught the single buried separator - the indirect-via-wrapper
chain in `src/reports/annual.py` (the literal function name never appears there; it
reaches the deprecated behaviour only through the wrapper `_apply_tax`). Consistency at
catching that wrapper-chain entry run after run is the primary discriminator; the
aliased call in proforma.py and the config-string entry are secondary buried separators
tracked the same way.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`, with the
within-family spread elevated to the headline. The correctness-first quality principle
holds and is extended: a confidently-wrong entry (a false positive or a mis-kinded
reference) is worse than a quietly missed one, AND high run-to-run variance is itself a
production-readiness defect. A model with a high mean but a wide recall range is worse
for routing than a slightly lower mean with a tight range. Recall, precision, and
spread are the scored discriminators - summary quality is explicitly NOT the point. The
variant pool is 15 (3 models x N=5). The corpus is the directory
`corpus/cross-reference-completeness/`.
