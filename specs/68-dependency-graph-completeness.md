---
task_category: dependency-graph-completeness
prompt_under_test: |
  You are given a fictional JavaScript codebase at
  corpus/dependency-graph-completeness/modules.js. It contains 22 modules in one file,
  each delimited by a "// ========== module: NAME ==========" banner. Modules depend on
  each other via `import` statements and, in one case, a dynamically-constructed
  `require(...)`.

  Your task: enumerate the COMPLETE TRANSITIVE dependency set of the module named
  `orchestrator`. That is, list every module that `orchestrator` depends on directly or
  indirectly (the full reachable set from orchestrator following the dependency edges).

  Read every module carefully. Dependency edges are not only the literal static
  `import` statements - one module is loaded at runtime via a dynamically-constructed
  module path (a `require(prefix + name)` where the name comes from config). That
  dynamically-loaded module, and anything IT depends on, are part of orchestrator's
  transitive dependency set even though no static `import` statement names them. A
  module that exists in the file but is NOT reachable from orchestrator must NOT be
  listed.

  Output a plain list of every module in orchestrator's transitive dependency set (use
  the module names from the banners, e.g. `planner`, `handlers/fastpath`). After the
  list, append the required output envelope (schemaVersion, tier, status,
  tool_budget_used) on separate lines. No em dashes (use spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/dependency-graph-completeness/
corpus_intent: |
  One file (corpus/dependency-graph-completeness/modules.js) with 22 fictional modules
  delimited by banner comments. The task is to compute the full transitive dependency
  set reachable from the `orchestrator` module. Most edges are ordinary static
  `import "./x"` statements that grep finds. The buried discriminator is ONE edge that
  is NOT a static import: the `planner` module loads a handler via
  `require(HANDLER_PREFIX + (cfg.handler || "default"))`, and cfg.handler defaults to
  "fastpath" (set in the `defaults` module). So `handlers/fastpath` is a real transitive
  dependency of orchestrator reached only through a dynamically-constructed import
  string - no static `import` statement names it, so a grep-for-imports approach misses
  it. And `handlers/fastpath` itself imports `meter`, so `meter` is reachable ONLY
  through the dynamic edge too.

  THE BURIED ITEM (the scored discriminator): `handlers/fastpath` (and, transitively
  through it, `meter`). A weak model that enumerates the graph by following only static
  `import` statements will produce a set that is MISSING handlers/fastpath and meter.
  The correct answer includes both, reasoning that the default config resolves the
  dynamic require to handlers/fastpath. Catch-rate on this dynamic edge across the 5
  runs of a family is the load-bearing signal.

  PRECISION TRAPS (must NOT be included):
    - `unused-legacy`: exists in the file, imports `backoff`, but NOTHING in
      orchestrator's graph imports unused-legacy. It is unreachable from orchestrator -
      a distractor. Listing it is a false positive.
    - `handlers/default`: a SECOND possible dynamic-require target (cfg.handler ===
      "default"), but with the DEFAULT config (cfg.handler = "fastpath" per the
      `defaults` module) it is NOT the resolved target and is NOT reached. Including it
      is a defensible edge case ONLY if the model explicitly notes it is a conditional
      alternate; listing it flatly as a dependency under the default config is a
      precision miss. The answer key treats the default-config resolution (fastpath) as
      canonical; handlers/default is NOT in the required set.

  QUALITY PRINCIPLE (correctness-first): completeness (catching the dynamic edge) AND
  precision (excluding the unreachable distractor) both matter. Missing
  handlers/fastpath+meter is the recall miss; including unused-legacy or
  handlers/default (under default config) is the precision/hallucination error.

  ANSWER KEY (for the scoring Architect). orchestrator's transitive dependency set is
  EXACTLY these 19 modules:
    1. planner            (direct import)
    2. config             (direct import)
    3. reporter           (direct import)
    4. steps              (planner -> steps)
    5. validator          (planner -> validator)
    6. handlers/fastpath  (planner -> DYNAMIC require, resolves to fastpath via defaults) [BURIED]
    7. env                (config -> env)
    8. defaults           (config -> defaults)
    9. formatter          (reporter -> formatter)
    10. sink              (reporter -> sink)
    11. graph             (steps -> graph)
    12. schema            (validator -> schema)
    13. theme             (formatter -> theme)
    14. transport         (sink -> transport)
    15. dsu               (graph -> dsu)
    16. rules             (schema -> rules)
    17. retry             (transport -> retry)
    18. backoff           (retry -> backoff)
    19. meter             (handlers/fastpath -> meter) [reachable ONLY via the dynamic edge]

  NOT in the set: orchestrator itself (the root), handlers/default (not resolved under
  default config), unused-legacy (unreachable distractor).

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - The output lists `handlers/fastpath`. Grep for `fastpath` - present == dynamic
      edge caught.
    - The output lists `meter`. Grep for `meter` - present == the transitive dependency
      of the dynamic handler caught. (meter is reachable ONLY through fastpath, so its
      presence is a strong proxy for the dynamic edge being followed.)
    - The output does NOT list `unused-legacy`. Grep for `unused-legacy` - absent ==
      precision held. Present == false positive.
    - The output count of distinct dependency modules is 19 (the list above). 19 with
      fastpath+meter present and unused-legacy absent = full correctness.
    - All 13 statically-imported transitive modules are present (planner, config,
      reporter, steps, validator, env, defaults, formatter, sink, graph, schema, theme,
      transport, dsu, rules, retry, backoff) - the easy recall floor.

  Scoring guidance:
    - Correctness (hard-fail eligible) = the exact 19-module set, including the dynamic
      handlers/fastpath + meter and excluding unused-legacy.
    - Completeness = all 19 present (recall), with the dynamic edge as the high-signal
      member.
    - Hallucination (hard-fail eligible) = listing unused-legacy, handlers/default (flat,
      under default config), or a module name not in the file.
    - Discipline = following the dynamic require edge AND excluding the unreachable
      distractor.
    - Voice match does NOT apply.
notes: |
  Chat A consistency battery (61-70). variant_pool 15 (3 models x N=5). The SCORED
  SIGNAL is WITHIN-FAMILY SPREAD across the 5 runs PLUS per-model buried-item catch-rate:
  did all 5 runs of a family follow the dynamically-constructed require edge (planner ->
  handlers/fastpath -> meter) and include both in orchestrator's transitive set, or did
  some runs enumerate only the static-import graph and drop them. Peak score on one run
  is not the question; consistency of catching the one dynamic edge across 5 runs is.

  This is a dependency-graph completeness task: 22 fictional modules in one file
  (corpus/dependency-graph-completeness/modules.js). Most dependency edges are ordinary
  static imports a grep finds; the buried edge is a dynamic require
  (require(prefix + cfg.handler), cfg.handler defaults to "fastpath") that no static
  import statement names, plus meter which is reachable only through it. The precision
  traps are unused-legacy (unreachable distractor) and handlers/default (alternate
  dynamic target not resolved under default config). Answer key gives the exact
  19-module set plus the dynamic edge plus grep-verifiable invariants. Standard
  four-phase /eval-pit flow against the frozen rubric/rubric.md. Codenames are neutral
  fictional. Voice match does not apply.
---

# Spec 68 - dependency-graph-completeness

Given a fictional 22-module codebase, enumerate the complete transitive dependency set
reachable from the `orchestrator` module - following not only static `import`
statements but the one dynamically-constructed `require(...)` edge as well.

The corpus (`corpus/dependency-graph-completeness/modules.js`) wires most modules with
ordinary static imports (the easy recall floor: planner, config, reporter, and their
transitive imports). The buried discriminator is a dynamic edge: `planner` loads a
handler via `require(HANDLER_PREFIX + (cfg.handler || "default"))`, and cfg.handler
defaults to "fastpath" (set in the `defaults` module). So `handlers/fastpath` is a real
transitive dependency reached only through a constructed import string - a
grep-for-imports approach never finds it - and `meter` is reachable only through
fastpath. The correct answer includes both.

The precision traps are `unused-legacy` (present in the file but unreachable from
orchestrator) and `handlers/default` (an alternate dynamic target not resolved under the
default config). The correct set is exactly 19 modules: all statically-reachable
modules plus handlers/fastpath and meter, and NOT unused-legacy or handlers/default.

This is a Chat A consistency-battery eval. Standard four-phase `/eval-pit` flow against
the frozen `rubric/rubric.md`. The scored signal is within-family SPREAD across the 5
runs plus per-model catch-rate on the single buried dynamic edge (fastpath + meter), not
peak score on one lucky run. The variant pool is 15 (3 models x N=5, effort inert per
the methodology). The answer key in `corpus_intent` gives the exact 19-module set, the
precision-trap exclusions, and grep-verifiable invariants for the scoring Architect.
Codenames are neutral fictional. Voice match does not apply.
