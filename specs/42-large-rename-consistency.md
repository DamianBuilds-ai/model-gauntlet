---
task_category: cross-reference-completeness
prompt_under_test: |
  You are given a synthetic Python package for a fictional billing platform
  "Globex Billing" under corpus/large-rename-consistency/globex_billing/.

  The function compute_shipping_fee (defined in core/fees.py) is being renamed to
  calculate_shipping_charge. Produce a COMPLETE rename checklist of EVERY location
  in the package that must change so the rename is correct and the package still
  runs. Miss nothing. For each location:
    1. Cite the file path AND the line number (or the section/function the
       reference sits in if a line number is unavailable).
    2. State the KIND of site: definition, direct call, import, aliased import,
       qualified call (module.compute_shipping_fee), call inside another function's
       body, config string (a dotted path that names the function), doc/prose
       mention, comment, error-message string, or test.
    3. Give the new text for that site.

  Rules:
    - Rename ONLY the exact symbol compute_shipping_fee. Sites appear in code
      positions AND in non-code positions: a dotted-path STRING in a config file
      that the platform resolves at runtime, a prose mention in a docs file, a
      comment, and a logged error-message string. ALL of these reference the
      function and must be on the checklist - a code-only identifier rename that
      skips the config string, the doc, the comment, and the error string is
      INCOMPLETE.
    - Do NOT rename a DIFFERENT symbol that merely shares a substring. Specifically:
      compute_handling_fee is a different function. recompute_shipping_fee_total is
      a different function whose name CONTAINS "shipping_fee" but is not
      compute_shipping_fee - do NOT rename it and do NOT substring-replace inside
      its name. compute_shipping_fee_v2 is a different function whose name STARTS
      with compute_shipping_fee - do NOT rename its definition (but a call to the
      real compute_shipping_fee INSIDE its body IS a real site that must change).
    - A COMMENTED-OUT (dead) call is not a live site; do not count it as a live
      rename location (you may note it separately, but listing it as a live site is
      an error).
    - A confidently-wrong entry (renaming a decoy symbol, or describing a real site
      with the wrong new text) scores WORSE than an omission.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/large-rename-consistency/
corpus_intent: 1 synthetic Python package (globex_billing, 14 files across 6 subpackages) where one function must be renamed across 14 live sites in 8 files, one of which is buried in a YAML config dotted-path string (the easy-to-miss separator). variant_pool 15 = 5 runs per model (Haiku x5, Sonnet x5, Opus x5). The HEADLINE metric is WITHIN-FAMILY SPREAD across the 5 runs: does a family catch the buried config-string site on EVERY run, or only on some.
corpus_delivered: TBD
corpus_match: TBD
notes: |
  HEAVY large-rename CONSISTENCY probe. This is a variance battery: N=5 per model
  (variant_pool: 15 - Haiku x5, Sonnet x5, Opus x5; effort treated as inert per the
  methodology) and the SCORED HEADLINE is WITHIN-FAMILY SPREAD, not the mean. The
  question: does a model family catch the one easy-to-miss rename site on all five
  runs, or hit the obvious code sites every time while dropping the buried site on
  one or more runs.

  THE BURIED SITE (the separator). The symbol compute_shipping_fee must be renamed at
  14 live sites across 8 files. Most are ordinary code positions (def, imports, calls)
  that any rename catches. The separator is config/fee_registry.yaml line 7, where the
  function is named as a dotted-path STRING ("globex_billing.core.fees:
  compute_shipping_fee") that the platform resolves at runtime via importlib. A
  code-only find-and-replace of identifiers does NOT touch this string, yet renaming
  the function without repointing the dotted path silently breaks runtime resolution.
  Three further easy-to-miss non-code sites reinforce the same failure mode: a prose
  mention in docs/billing-guide.md, a comment in handlers/audit.py, and a logged
  error-message string in handlers/audit.py. The consistency separator is whether a
  family catches the buried config string (and the other non-code sites) on EVERY one
  of its five runs.

  This rename is machine-verified. Applying the rename to exactly the 14 live sites
  below (and to no decoy) produces a package that imports and runs, with the new
  symbol present, the old gone, and all three decoy functions intact - this was
  confirmed by applying a word-bounded rename with a negative lookahead for the _v2
  decoy and re-importing the package.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong entry
  is worse than a missed one. A model that renames compute_handling_fee, or
  substring-corrupts recompute_shipping_fee_total, or renames the compute_shipping_fee_v2
  definition, or counts the commented-out dead call as a live site, has put a wrong
  edit on a rename checklist that an engineer would apply and break the build with -
  worse than quietly missing one site. Reward exact recall of all 14 live sites AND
  clean precision (none of the decoys touched). Penalise the false positive hardest.

  ANSWER KEY (for the scoring Architect; the rename was machine-verified). There are
  14 LIVE sites across 8 files. Score against these 14. Test FUNCTION NAMES that
  contain the symbol (tests/test_fees.py lines 10 and 14: test_compute_shipping_fee_*)
  are accept-either - renaming them for consistency is fine, leaving them is fine; do
  NOT double-penalise either choice. They are NOT among the 14 required live sites.

  TIER A - obvious code sites (every model should get these; 9 sites):
    A1. core/fees.py line 6 - DEFINITION SITE (def compute_shipping_fee). New:
        def calculate_shipping_charge.
    A2. core/fees.py line 18 - call inside recompute_shipping_fee_total's body. New:
        calculate_shipping_charge(...). (The ENCLOSING function name stays
        recompute_shipping_fee_total - only the call changes.)
    A3. api/quote.py line 3 - import line (from ... import compute_shipping_fee). New:
        import calculate_shipping_charge.
    A4. api/quote.py line 7 - direct call. New: calculate_shipping_charge(...).
    A5. api/checkout.py line 7 - qualified call (fees.compute_shipping_fee). New:
        fees.calculate_shipping_charge(...). (The decoy fees.recompute_shipping_fee_total
        on line 8 stays unchanged.)
    A6. handlers/batch.py line 3 - ALIASED import
        (from ... import compute_shipping_fee as ship_fee). New: import
        calculate_shipping_charge as ship_fee. (The call site uses ship_fee and does
        not change.)
    A7. handlers/legacy.py line 13 - LIVE call to fees.compute_shipping_fee INSIDE the
        body of compute_shipping_fee_v2. New: fees.calculate_shipping_charge(...). (The
        DEFINITION compute_shipping_fee_v2 on line 11 is a decoy and stays.)
    A8. tests/test_fees.py line 5 - import. New: calculate_shipping_charge.
    A9. tests/test_fees.py lines 11 and 15 - call sites (line 15 has TWO calls on one
        line). New: calculate_shipping_charge(...). Count line 11 and line 15 as the
        test-call sites; the two calls on line 15 are one physical line.

  TIER B - the easy-to-miss NON-CODE sites (where weaker runs drop; 5 sites,
  including THE buried separator):
    B1. config/fee_registry.yaml line 7 - THE BURIED SEPARATOR. The dotted-path string
        "globex_billing.core.fees:compute_shipping_fee" resolved at runtime. New:
        "...:calculate_shipping_charge". A code-only identifier rename misses this. The
        decoy strings on lines 11 (compute_handling_fee) and 13
        (recompute_shipping_fee_total) stay unchanged.
    B2. docs/billing-guide.md line 7 - prose mention of `compute_shipping_fee`. New:
        `calculate_shipping_charge`. (The recompute_shipping_fee_total mention on line
        17 stays.)
    B3. handlers/audit.py line 9 - COMMENT mention ("originates from
        compute_shipping_fee"). New: comment names calculate_shipping_charge.
    B4. handlers/audit.py line 11 - logged ERROR-MESSAGE STRING
        ("compute_shipping_fee returned no value..."). New: the string names
        calculate_shipping_charge.
    (B1 is the canonical run-to-run separator; B2-B4 are the same non-code failure
    mode and a model that catches B1 but drops B2-B4 on some runs is also a
    consistency miss.)

    Total: A1-A9 (9 sites, counting the test calls A8/A9 as the two test sites) +
    B1-B4 (note B4 is the 5th non-code site after B1/B2/B3 plus the error string) =
    14 live sites across 8 files: core/fees.py (2), api/quote.py (2), api/checkout.py
    (1), handlers/batch.py (1), handlers/legacy.py (1), tests/test_fees.py (3),
    config/fee_registry.yaml (1), docs/billing-guide.md (1), handlers/audit.py (2).

  PRECISION TRAPS / DECOYS (must NOT be renamed - each is a confidently-wrong false
  positive):
    TRAP-1. compute_handling_fee (core/fees.py, called in tests) - a DIFFERENT
        function. Renaming it is a precision error.
    TRAP-2. recompute_shipping_fee_total (core/fees.py line 16 def; checkout.py line 8;
        fee_registry.yaml line 13; billing-guide.md line 17) - name CONTAINS
        "shipping_fee" but is a different symbol. Renaming it, or substring-replacing
        inside its name, is a precision error and breaks a different function.
    TRAP-3. compute_shipping_fee_v2 (handlers/legacy.py line 11 def) - name STARTS with
        compute_shipping_fee but is a different symbol. Renaming its DEFINITION is a
        precision error. (Its body's CALL to the real compute_shipping_fee is A7 and
        IS renamed - do not confuse the two.)
    TRAP-4. handlers/legacy.py line 7 - a COMMENTED-OUT dead call to
        fees.compute_shipping_fee. Not a live site. Listing it as a live rename
        location is the error.

  Scoring guidance:
    - The HEADLINE is WITHIN-FAMILY SPREAD on the buried site(s). For each model
      family, record how many of the 5 runs caught B1 (the config dotted-path string),
      and how many caught all of B1-B4 (the non-code sites). 5/5 on B1 is the
      consistency exemplar; 4/5 or worse on B1 is a consistency miss even if the best
      run is the full 14. Report the per-family B1 hit rate and the per-family all-non-
      code (B1-B4) hit rate as the lead findings, then the per-family decoy-rename rate
      (false positives), then the mean weighted total.
    - Completeness (recall, weight 2.0) = of the 14 true sites, how many per run. Count
      DROPPED sites explicitly. Dropping B1 is the strongest signal; dropping B2-B4 is
      the same non-code failure mode; dropping a Tier A code site indicates a shallow
      pass.
    - Correctness (hard-fail eligible) = are the listed sites actually live references
      to compute_shipping_fee AND given the right new text and kind. A checklist that
      renames a decoy, or substring-corrupts recompute_shipping_fee_total, fails
      Correctness.
    - Hallucination (hard-fail eligible) = inventing a site that does not exist, or
      claiming a rename in a file that has none. Renaming a decoy symbol is the
      canonical confidently-wrong false positive here.
    - Reasoning quality = did the model search beyond code identifiers - into the
      config string, the doc prose, the comment, and the error string - and correctly
      distinguish the exact symbol from the three substring decoys. This is the
      separator.
    - Source transparency = every site cites file + line/section and the kind.
    - Discipline = correctly EXCLUDING the three decoy functions and the commented-out
      dead call rather than padding the checklist; correctly keeping the enclosing
      names of recompute_shipping_fee_total (A2) and compute_shipping_fee_v2 (A7) while
      renaming the calls inside them.
    - Format adherence = the output envelope plus a clean per-site structure (path,
      kind, new text).
    Within-family SPREAD on the buried config-string site is THE scored discriminator.
    Summary quality is NOT the point. Voice match does NOT apply.

    Suggested scoring shorthand for the Architect: per run, recall = (true sites found)
    / 14; precision penalty = number of decoy symbols renamed or dead sites listed.
    Per family, the lead number is the B1 (config-string) hit rate over 5 runs, then
    the B1-B4 (all non-code) hit rate. A family at 5/5 on B1 with zero decoy renames is
    the exemplary consistency winner; a family that catches the full 14 on its best run
    but drops the config string (or a doc/comment/error-string site) on one or more of
    its five runs is the consistency loser at an identical peak.
---

# Spec 42 - large-rename-consistency (within-family spread on a buried config-string site)

The large-rename sibling of the cross-reference completeness specs, rebuilt as a
consistency / variance battery. The corpus
(`corpus/large-rename-consistency/`) is a synthetic Python package "Globex
Billing" of 14 files across six subpackages (core, api, handlers, config, docs,
tests). The function `compute_shipping_fee` (defined in `core/fees.py`) is being
renamed to `calculate_shipping_charge`, and the task is to produce a complete
rename checklist of every site that must change for the rename to be correct and
the package to still run.

The variant pool is 15 (3 models x N=5; Haiku x5, Sonnet x5, Opus x5; effort
inert per the methodology) and the HEADLINE metric is WITHIN-FAMILY SPREAD, not
the mean. The symbol appears at 14 live sites across 8 files. Most are ordinary
code positions (definition, imports, direct and qualified calls, an aliased
import, calls inside other functions' bodies, test imports and calls) that any
rename catches. The separator is `config/fee_registry.yaml` line 7, where the
function is named as a dotted-path STRING that the platform resolves at runtime,
which a code-only find-and-replace of identifiers does not touch - yet renaming
the function without repointing it silently breaks runtime resolution. Three
further easy-to-miss non-code sites (a prose mention in the docs, a comment, and a
logged error-message string) reinforce the same failure mode. The consistency
separator is whether a model family catches the buried config string - and the
other non-code sites - on EVERY one of its five runs, or catches the obvious code
sites every time while dropping the buried site on one or more of them. The rename
is machine-verified: applying it to exactly the 14 live sites (with a negative
lookahead for the `_v2` decoy) produces a package that imports and runs, with the
new symbol present, the old gone, and all three decoy functions intact.

Four precision traps are planted: a different function `compute_handling_fee`; a
different function `recompute_shipping_fee_total` whose name contains the substring
`shipping_fee`; a different function `compute_shipping_fee_v2` whose name starts
with the symbol (its definition must NOT be renamed, though the call to the real
function inside its body must be); and a commented-out dead call.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`, with
the within-family spread on the buried config-string site reported as the lead
finding. The correctness-first quality principle is central: a model that renames
a decoy symbol, substring-corrupts `recompute_shipping_fee_total`, renames the
`compute_shipping_fee_v2` definition, or counts the dead commented call as a live
site has produced a confidently-wrong checklist that an engineer would apply and
break the build with, worse than quietly missing a site. Completeness (recall
against the 14-site key) and Correctness / Hallucination (no decoys touched,
correct new text) are the scored discriminators. Reasoning quality captures
whether the model searched beyond code identifiers into the config string, doc,
comment, and error string, and distinguished the exact symbol from the three
substring decoys. Voice match does not apply. The variant pool is 15 (3 models x
N=5, effort inert per the methodology). The corpus is the directory
`corpus/large-rename-consistency/`.
