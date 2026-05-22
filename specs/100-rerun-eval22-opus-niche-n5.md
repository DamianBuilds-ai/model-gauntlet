---
task_category: cross-reference-completeness
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
corpus_intent: 16 interlinked files (code modules + config + spec doc + test) with one deprecated function referenced across many of them
corpus_delivered: TBD
corpus_match: TBD
notes: |
  N=5 RE-RUN OF EVAL 22 (statistical confidence on the strongest Opus-niche win).
  This is a re-run of eval 22 (cross-reference-completeness) at variant_pool: 15
  (Haiku x5, Sonnet x5, Opus x5; effort treated as inert per the methodology). Eval 22
  produced the STRONGEST clear Opus-niche win in the gauntlet so far - a +0.45
  buried-reference recall edge for Opus on this cross-reference forgetting-under-load
  task. That win was the single clearest signal that Opus has a real, separable niche;
  it deserves N=5 confirmation that the edge holds rather than being an N=3 artifact.
  This re-run repeats the identical task at N=5 to confirm the one clear Opus edge holds
  at higher N. The corpus, prompt, task_category, and answer key are REUSED VERBATIM
  from eval 22 - the only changes are the spec number, slug, and variant_pool. Do NOT
  re-author the corpus.

  OPUS-STRESS PROBE (cross-reference load / forgetting-under-load). This is the
  direct test of the failure mode where a model drops items on a big
  cross-matching task. At small scale every model finds the obvious calls; the
  hypothesis is that as the references spread across 16 files - some obvious, some
  buried deep in long files among unrelated code, some indirect (re-export,
  alias, wrapper, config string, prose) - the cheaper models start to DROP true
  locations (recall failure) or invent / mis-classify locations (precision
  failure). Run the full 15-variant model-only pool (Haiku x5, Sonnet x5, Opus x5;
  effort treated as inert per the methodology). Aggregate the 5 passes per model
  (mean weighted total); flag any model whose 5 passes diverge by more than 0.5 as
  a consistency finding. The headline is whether Opus's +0.45 buried-reference
  recall edge from N=3 holds at N=5.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong
  entry is worse than a missed one. A model that lists the commented-out dead call
  as a live location, or lists the similarly-named legacy_compute_taxonomy as a
  target, has put a wrong item on a migration checklist that an engineer would
  trust and act on - worse than quietly missing one real location. Reward exact
  recall AND clean precision. Penalise the false positive hardest.

  ANSWER KEY (for the scoring Architect). The corpus was salted via grep so this
  list is exact. There are 20 TRUE reference ENTRIES below (A1-A8, B1-B3, C1-C9),
  covering 23 physical reference lines once the re-export entry B3 (2 lines: the
  import and the __all__) and the test entry C9 (3 lines: the import and two
  calls) are expanded. Score against the 20 entries; the 23-line figure is just
  the grep-verifiable physical count. The entries split into three tiers by how
  easy they are to find - the discriminator is whether a model holds ALL of them,
  especially the INDIRECT ones, without dropping any and without adding the two
  traps.

  TIER A - obvious / direct (8 locations; every model should get these):
    A1. src/tax/legacy.py line 13 - DEFINITION SITE of legacy_compute_tax (the
        function being removed). Migration: delete after all callers gone.
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
        _tax_adjusted_revenue. Migration: replace call. This is the canonical
        "buried in a long file" drop candidate.
    B3. src/tax/__init__.py line 9 - re-export import of the deprecated fn (also
        named in __all__ on line 11; accept either the line-9 import, the line-11
        __all__ entry, or both cited as one re-export location - do NOT double-
        penalise, but a model that misses the re-export entirely drops a real
        downstream-breaking location). Migration: update / remove re-export.

  TIER C - indirect (the OPUS separators; 9 locations across alias, wrapper,
  config, doc, test - these are where cross-reference load bites hardest):
    C1. src/billing/proforma.py line 12 - ALIASED import
        (legacy_compute_tax as _calc_tax). Migration: update import.
    C2. src/billing/proforma.py line 20 - ALIASED call site reading _calc_tax
        (the literal name does not appear at the call). Migration: replace call.
        A model that searches only for the literal name misses this.
    C3. src/reports/helpers.py line 11 - import line for the wrapper module.
        Migration: update import.
    C4. src/reports/helpers.py line 17 - call inside the wrapper _apply_tax that
        forwards to the deprecated fn. Migration: replace call (or retarget the
        wrapper).
    C5. src/reports/annual.py line 13 - import of the wrapper _apply_tax.
        INDIRECT-via-wrapper. Migration: depends on strategy; must be listed and
        flagged indirect.
    C6. src/reports/annual.py line 20 - call to _apply_tax. INDIRECT-via-wrapper.
        Must be listed and flagged indirect (the strong answer notes annual.py
        reaches the deprecated behaviour only through the wrapper).
    C7. config/settings.yaml line 19 - the tax.calculator key whose value is the
        string "src.tax.legacy:legacy_compute_tax", resolved at runtime. Migration:
        repoint the dotted path. A code-only grep of .py files misses this.
    C8. docs/tax-migration-spec.md - prose references the function name (the doc
        must be updated when the function is removed so it does not describe a
        deleted function). Accept the file cited once as a doc/prose location.
    C9. tests/test_tax.py - the test file references the deprecated fn: import on
        line 13 and live calls on line 18 (test_compute_tax_au) and line 22
        (test_compute_tax_default_region). Accept the test file cited as one test
        location OR the individual import+two-calls itemised; do NOT double-
        penalise granularity, but a model that misses the test entirely drops a
        real location. Migration: retarget tests to TaxEngine.compute.

  PRECISION TRAPS (must NOT appear on the checklist - listing either is a
  confidently-wrong false positive and the heaviest penalty):
    TRAP-1. src/billing/invoice.py line 88 - a COMMENTED-OUT call to
        legacy_compute_tax inside render_pdf. Dead code. NOT a live location. A
        model that lists it has put a no-op item on the migration checklist.
    TRAP-2. legacy_compute_taxonomy (defined src/tax/legacy.py line 23; used in
        tests/test_tax.py line 31). A DIFFERENT function (product taxonomy code,
        not tax money) with a confusingly similar name. NOT the migration target.
        Listing it is a precision error.

  DISTRACTOR FILES (correctly contain NO true reference - a model that invents a
  reference in any of these has hallucinated a location):
    - src/tax/engine.py (the new TaxEngine; mentions the old name only in
      docstrings as "the thing it replaces", not as a call).
    - src/billing/__init__.py (clean package init).
    - src/api/webhooks.py (mentions the word "tax" in a log string only).

  Scoring guidance:
    - Completeness (recall, weight 2.0) = of the 20 true entries, how many are
      present. Count DROPPED locations explicitly. Tier C drops are the strongest
      signal of forgetting-under-load; Tier A drops indicate a serious miss.
    - Correctness (hard-fail eligible) = are the listed locations actually true
      references AND classified with the right kind. A checklist dominated by
      wrong/mis-kinded entries fails Correctness.
    - Hallucination (hard-fail eligible) = inventing a reference in a distractor
      file, or listing a location that does not exist. The two precision TRAPS
      and any distractor-file invention are the canonical hallucinations here.
    - Reasoning quality = did the model trace the indirect chains (alias ->
      call, wrapper -> caller, config string, doc) rather than only the literal
      name. This is where Opus is hypothesised to separate.
    - Source transparency = every location cites file + line/section.
    - Discipline = did it correctly EXCLUDE the commented-out dead call and the
      taxonomy function rather than padding the list. A model that lists the traps
      to look thorough is penalised, not rewarded.
    - Format adherence = the output envelope plus a clean per-location structure
      (path, kind, migration action).
    Recall and precision are the scored discriminators. Summary quality is NOT the
    point. Voice match does NOT apply.

    Suggested scoring shorthand for the Architect: recall = (true entries found)
    / 20; precision penalty = number of false positives (each trap or invented
    location listed). A model that finds 20/20 with zero false positives is the
    exemplary 5 on Completeness and Correctness; dropping Tier C indirect items or
    listing a trap is where the score falls. With 5 runs per model, also report the
    per-model buried-reference recall edge so the eval-22 +0.45 Opus advantage can
    be confirmed or overturned at N=5.
---

# Spec 100 - rerun-eval22-opus-niche-n5 (N=5 re-run of eval 22, the strongest Opus-niche win)

This is a statistical-confidence RE-RUN of eval 22 (cross-reference-completeness) at
`variant_pool: 15` (3 models x N=5). Eval 22 produced the strongest clear Opus-niche
win in the gauntlet so far - a +0.45 buried-reference recall edge for Opus on this
cross-reference forgetting-under-load task, the single clearest evidence Opus has a
real separable niche. This re-run repeats the identical task at N=5 to confirm that one
clear edge holds at higher N rather than being an N=3 artifact. The corpus, prompt,
task_category, and answer key are REUSED VERBATIM from eval 22 - only the spec number,
slug, and variant pool change. Do NOT re-author the corpus.

The corpus (`corpus/cross-reference-completeness/`) is a synthetic billing platform
"Acme Ledger" of 16 files. The deprecated `legacy_compute_tax(amount, region)` is
referenced in 20 true entries (covering 23 physical reference lines) spread across the
tree: 8 obvious direct calls and imports, 3 buried in long report modules, and 9
indirect ones - a re-export, an aliased import and its aliased call site, a wrapper
function and the callers that reach the deprecated behaviour only through it, a runtime
config value that names the function as a dotted-path string, a migration spec doc that
names it in prose, and a test file. Two precision traps are planted: a commented-out
dead call (not a live location) and a confusingly similar function
`legacy_compute_taxonomy` (a different concern entirely).

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is central: a confidently-wrong checklist entry (a
false positive, or a real location given the wrong kind) is worse than a quietly missed
one, because an engineer acts on the checklist. Completeness (recall against the
20-entry answer key) and Correctness / Hallucination (zero false positives, no invented
references) are the scored discriminators - summary quality is explicitly NOT the point,
since that is where Opus tied Sonnet on the earlier consolidation eval. Reasoning
quality captures whether the model traced the indirect chains rather than grepping the
literal name. With 5 runs per model, the headline is whether Opus's +0.45
buried-reference recall edge holds at N=5. The variant pool is 15 (3 models x N=5,
effort inert per the methodology). The corpus is the directory
`corpus/cross-reference-completeness/`.
