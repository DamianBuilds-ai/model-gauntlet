---
task_category: cross-reference-completeness
prompt_under_test: |
  You are given a synthetic Python package for a fictional data pipeline "Acme
  Pipeline" under corpus/dependency-completeness-consistency/acme_pipeline/.

  Produce the COMPLETE set of modules INSIDE the acme_pipeline package that the
  module acme_pipeline.transform.normalizer (file
  acme_pipeline/transform/normalizer.py) transitively depends on. "Transitively
  depends on" means: every acme_pipeline module that would be imported, directly
  or indirectly, as a consequence of importing and running normalizer under its
  DEFAULT configuration. Start from normalizer and follow every dependency edge
  to its leaves.

  For each module in the closure:
    1. Give the dotted module name (e.g. acme_pipeline.common.units).
    2. State the edge by which it enters the closure: a direct import from
       normalizer, or "via X" naming the intermediate module it is reached
       through.
    3. Flag whether the edge is a STATIC import (a top-of-file import line) or a
       DYNAMIC import (resolved at runtime, e.g. via importlib from a config
       string). At least one true dependency is reached only through a dynamic
       import; you must include it and everything reachable through it.

  Rules:
    - Include INDIRECT dependencies reached through any number of intermediate
      modules. A module two or three hops away from normalizer is still in the
      closure.
    - Include the dependency reached through the runtime / dynamic import. A scan
      of only the static top-of-file import lines will miss it and everything
      below it; that omission is the main failure this task probes.
    - Do NOT include false positives. A module that imports normalizer (an edge in
      the OTHER direction) is NOT a dependency of normalizer. A module reached only
      through a COMMENTED-OUT (dead) import is NOT in the closure. A sibling module
      in the same package that normalizer does not import is NOT a dependency. An
      ALTERNATE plugin that is not the configured default is NOT reached. Listing
      any of these is a precision error and counts against you.
    - Package __init__ files in this package are empty (no re-exports) and add no
      edges; do not invent edges through them.
    - A confidently-wrong entry (a false positive, or a real module with the wrong
      edge described) scores WORSE than an omission.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/dependency-completeness-consistency/
corpus_intent: 1 synthetic Python package (acme_pipeline, ~26 files across 7 subpackages) with one target module whose transitive dependency closure is 9 modules, of which 2 are reachable ONLY through a single dynamic (runtime importlib) edge. variant_pool 15 = 5 runs per model (Haiku x5, Sonnet x5, Opus x5). The HEADLINE metric is WITHIN-FAMILY SPREAD across the 5 runs: does a family find the buried dynamic edge (and the 2 modules below it) on EVERY run, or only on some.
corpus_delivered: TBD
corpus_match: TBD
notes: |
  HEAVY transitive-dependency-completeness CONSISTENCY probe. This is a variance
  battery: N=5 per model (variant_pool: 15 - Haiku x5, Sonnet x5, Opus x5; effort
  treated as inert per the methodology) and the SCORED HEADLINE is WITHIN-FAMILY
  SPREAD, not the mean. The question: does a model family trace the one buried
  dynamic-import edge on all five runs, or hit the full closure on its best run while
  dropping the dynamic edge (and the subtree below it) on one or more of the others.

  THE BURIED EDGE (the separator). normalizer.py has three ordinary top-of-file
  imports (common.config, common.units, storage.cache) whose static closure is 7
  modules. But normalizer also resolves a rounding plugin at RUNTIME via
  importlib.import_module from a dotted-path string in config
  (_load_rounding_plugin); the configured default is
  acme_pipeline.transform.plugins.rounding. That dynamic edge pulls in
  plugins.rounding, which in turn imports common.precision. So the TRUE closure is 9
  modules and the 2 extra modules (plugins.rounding, common.precision) are reachable
  ONLY through the single dynamic edge. A model that scans top-of-file imports finds
  7 and stops; a model that reads _load_rounding_plugin, follows the config default
  string to plugins.rounding, and continues to common.precision finds all 9. The
  consistency separator is whether a family finds those 2 buried modules on EVERY one
  of its 5 runs.

  This closure is machine-verified. The corpus ships a verifier
  (corpus/dependency-completeness-consistency/verify_closure.py) that computes the
  static closure (7), the true closure (9), and the buried subtree (2) by AST. The
  verifier is NOT part of what the model under test reads - the model is given the
  acme_pipeline package and must compute the closure itself. The verifier exists only
  so the scoring Architect has a machine-checked answer key.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong entry
  is worse than a missed one. A model that lists transform.enricher (reached only via
  a COMMENTED-OUT import in normalizer), or transform.validator (a sibling normalizer
  never imports), or ingest.reader (which imports normalizer - the edge runs the
  OTHER way), or the alternate plugins.truncating and its leaf common.floors (not the
  configured default), has put a wrong module on a dependency list that an engineer
  would trust - worse than quietly missing one. Reward exact recall of all 9 AND clean
  precision (none of the 5 distractor modules). Penalise the false positive hardest.

  ANSWER KEY (for the scoring Architect; machine-verified by verify_closure.py).

  THE TRUE CLOSURE - 9 modules (all must be present):
    Direct STATIC imports from normalizer (3):
      1. acme_pipeline.common.config   - direct static import.
      2. acme_pipeline.common.units    - direct static import.
      3. acme_pipeline.storage.cache   - direct static import.
    Indirect STATIC (reached through the direct ones; 4):
      4. acme_pipeline.common.schema    - via common.config (config imports schema).
      5. acme_pipeline.common.constants - via common.units (units imports constants).
      6. acme_pipeline.storage.backend  - via storage.cache (cache imports backend).
      7. acme_pipeline.vendor.kvstore   - via storage.backend (backend imports kvstore).
        (Note storage.cache also imports common.config, already counted.)
    THE BURIED DYNAMIC subtree (the separator; 2):
      8. acme_pipeline.transform.plugins.rounding - via the DYNAMIC importlib edge in
         normalizer._load_rounding_plugin (config default
         "acme_pipeline.transform.plugins.rounding"). NOT a static import line.
      9. acme_pipeline.common.precision - via plugins.rounding (which imports
         common.precision). Reachable from normalizer ONLY through the dynamic edge.

  PRECISION TRAPS / DISTRACTORS (must NOT appear in the closure - each is a
  confidently-wrong false positive):
    TRAP-1. acme_pipeline.transform.enricher - normalizer's ONLY reference to it is a
        COMMENTED-OUT import ("# from acme_pipeline.transform import enricher").
        Dead code. NOT in the closure. (And its leaf acme_pipeline.common.geo, reached
        only through enricher, is likewise NOT in the closure.)
    TRAP-2. acme_pipeline.transform.validator - a sibling of normalizer in the
        transform package that normalizer never imports. NOT in the closure.
    TRAP-3. acme_pipeline.ingest.reader - imports normalizer. The edge runs reader ->
        normalizer, NOT normalizer -> reader. NOT a dependency of normalizer.
    TRAP-4. acme_pipeline.transform.plugins.truncating - an ALTERNATE rounding plugin
        in the same plugins package that is NOT the configured default, so normalizer
        never loads it. NOT in the closure. (And its leaf acme_pipeline.common.floors,
        reached only through truncating, is likewise NOT in the closure.)
    TRAP-5. acme_pipeline.export.writer / acme_pipeline.export.formats - the export
        path. normalizer does not depend on export. NOT in the closure.
    Also: the package __init__ files are all empty (no re-exports). They add no edges;
    inventing a dependency through a package __init__ is a precision error.

  Scoring guidance:
    - The HEADLINE is WITHIN-FAMILY SPREAD on the buried dynamic subtree. For each
      model family, record how many of the 5 runs included BOTH plugins.rounding AND
      common.precision (via the dynamic edge), with the edge correctly flagged dynamic.
      5/5 is the consistency exemplar; 4/5 or worse is a consistency miss even if the
      best run is the full 9. Report the per-family buried-subtree hit rate as the lead
      finding, then the per-family false-positive rate on the 5 distractors, then the
      mean weighted total.
    - Completeness (recall, weight 2.0) = of the 9 true modules, how many present per
      run. Count DROPPED modules explicitly. Dropping the dynamic subtree (8 and 9) is
      the strongest signal; dropping a static indirect (4-7) indicates a shallow trace.
    - Correctness (hard-fail eligible) = are the listed modules actually in the closure
      AND classified with the right edge (static vs dynamic, and the correct "via X").
      A list dominated by wrong edges or distractor modules fails Correctness.
    - Hallucination (hard-fail eligible) = inventing a module that does not exist, or
      inventing an edge through an empty package __init__. The five distractor traps
      are the canonical confidently-wrong false positives.
    - Reasoning quality = did the model READ _load_rounding_plugin, follow the config
      default string to the plugin module, and continue to its import - rather than
      scanning only the top-of-file imports. This is the separator.
    - Source transparency = every module cites its edge (direct, or "via X") and its
      static/dynamic flag.
    - Discipline = correctly EXCLUDING the commented-out enricher, the reverse-edge
      ingest.reader, the unimported sibling validator, the non-default truncating
      plugin, and the export path - rather than padding the list to look thorough.
    - Format adherence = the output envelope plus a clean per-module structure (name,
      edge, static/dynamic flag).
    Within-family SPREAD on the buried dynamic subtree is THE scored discriminator.
    Summary quality is NOT the point. Voice match does NOT apply.

    Suggested scoring shorthand for the Architect: per run, recall = (true modules
    found) / 9; precision penalty = number of distractor modules listed. Per family,
    the lead number is the buried-subtree hit rate over 5 runs (correct = both
    plugins.rounding and common.precision present and flagged dynamic). A family at 5/5
    with zero distractors is the exemplary consistency winner; a family that finds the
    full 9 on its best run but drops the dynamic subtree on one or more of its five
    runs is the consistency loser at an identical peak.
---

# Spec 41 - dependency-completeness-consistency (within-family spread on a buried dynamic edge)

The transitive-dependency sibling of the cross-reference completeness specs,
rebuilt as a consistency / variance battery. The corpus
(`corpus/dependency-completeness-consistency/`) is a synthetic Python package
"Acme Pipeline" of about 26 files across seven subpackages (common, storage,
transform, transform.plugins, vendor, ingest, export). The target module is
`acme_pipeline.transform.normalizer`, and the task is to produce the COMPLETE set
of acme_pipeline modules it transitively depends on under its default
configuration.

The variant pool is 15 (3 models x N=5; Haiku x5, Sonnet x5, Opus x5; effort
inert per the methodology) and the HEADLINE metric is WITHIN-FAMILY SPREAD, not
the mean. normalizer has three ordinary top-of-file imports whose static closure
is 7 modules. But normalizer resolves a rounding plugin at RUNTIME via
`importlib.import_module` from a dotted-path string in config (the default is
`acme_pipeline.transform.plugins.rounding`), and that plugin imports
`acme_pipeline.common.precision`. So the TRUE closure is 9 modules, and the 2
extra (`plugins.rounding`, `common.precision`) are reachable ONLY through the one
dynamic edge. The consistency separator is whether a model family traces that
dynamic edge - and the subtree below it - on EVERY one of its five runs, or finds
the full closure on its best run while dropping the dynamic subtree on one or more
of the others. The closure is machine-verified by a shipped AST verifier
(`verify_closure.py`, which the model under test does NOT read - it exists only to
give the scoring Architect a machine-checked key).

Five precision traps are planted: a module reached only through a commented-out
dead import (`transform.enricher` and its leaf `common.geo`), an unimported
sibling (`transform.validator`), a reverse-edge module that imports normalizer
(`ingest.reader`), an alternate non-default plugin (`plugins.truncating` and its
leaf `common.floors`), and the unrelated export path (`export.writer`,
`export.formats`). The package `__init__` files are all empty and add no edges.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`, with
the within-family spread on the buried dynamic subtree reported as the lead
finding. The correctness-first quality principle is central: a model that lists
the commented-out enricher, the reverse-edge reader, the unimported validator, the
non-default plugin, or the export path has produced a confidently-wrong dependency
list that an engineer would act on, worse than quietly missing a module.
Completeness (recall against the 9-module key) and Correctness / Hallucination
(zero distractors, correct static-vs-dynamic edges) are the scored discriminators.
Reasoning quality captures whether the model read `_load_rounding_plugin` and
followed the config default string rather than scanning only the static imports.
Voice match does not apply. The variant pool is 15 (3 models x N=5, effort inert
per the methodology). The corpus is the directory
`corpus/dependency-completeness-consistency/`.
