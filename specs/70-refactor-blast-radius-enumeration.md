---
task_category: refactor-blast-radius-enumeration
prompt_under_test: |
  You are given a fictional codebase at
  corpus/refactor-blast-radius-enumeration/codebase.js. It contains 24 files, each
  delimited by a "// ===== file: path =====" banner. A shared helper
  `normalizeSlug(s)` is defined in `util/slug.js`.

  A refactor is planned: the signature of `normalizeSlug` will change (and the team
  wants to ensure all slug normalization goes through the one helper). Your task:
  enumerate the COMPLETE BLAST RADIUS of this refactor - every file that would need to
  be reviewed or updated.

  Include:
    - the definition site,
    - every file that imports and calls `normalizeSlug`,
    - any file that DUPLICATES the helper's behaviour inline (a copy-pasted
      re-implementation of the same logic under a different name, with no call to the
      helper). Such a site will not appear in a search for the helper's name, but it is
      part of the blast radius because it must be migrated to the centralized helper.

  Do NOT include files that merely mention the helper in prose/documentation without a
  code dependency, and do NOT include unrelated files that have nothing to do with slug
  normalization.

  Output a list of every file in the blast radius, each with a one-line reason (call
  site, definition, inline duplicate). After the list, append the required output
  envelope (schemaVersion, tier, status, tool_budget_used) on separate lines. No em
  dashes (use spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/refactor-blast-radius-enumeration/
corpus_intent: |
  One file (corpus/refactor-blast-radius-enumeration/codebase.js) with 24 fictional
  files. A shared helper normalizeSlug lives in util/slug.js. Six source files import
  and call it (pages/article.js, pages/author.js, pages/tag.js, api/router.js,
  search/index.js, cli/generate.js), and one test file calls it (tests/slug.test.js).
  Those seven call sites plus the definition site are the grep-findable blast radius.
  The buried discriminator is ONE file - importers/legacy.js - that does NOT call
  normalizeSlug but RE-IMPLEMENTS its exact body inline (the same .trim().toLowerCase()
  .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") chain) under a local variable.
  A grep for the helper name will never surface this file, yet it is part of the
  refactor blast radius because the inlined duplicate must be migrated to the helper.

  THE BURIED ITEM (the scored discriminator): importers/legacy.js - the inlined
  copy-pasted duplicate. It has NO call to normalizeSlug, so a name-grep approach misses
  it; only recognizing the duplicated logic PATTERN catches it. The correct answer
  includes importers/legacy.js as part of the blast radius and explains it is an inline
  duplicate. Catch-rate on this single duplicate-site across the 5 runs of a family is
  the load-bearing signal.

  PRECISION TRAPS (must NOT be included):
    - docs/usage.md: mentions "the slug helper" in PROSE only, no code dependency.
      Listing it as part of the code blast radius is a false positive.
    - util/format.js, util/numbers.js, util/dates.js, models/*, services/*,
      middleware/*, config/*: unrelated files with no slug-normalization dependency.
      Listing any of them is a false positive.

  QUALITY PRINCIPLE (correctness-first): completeness (catching the inline duplicate)
  AND precision (excluding the prose mention and unrelated files) both matter. Missing
  importers/legacy.js is the recall miss (the high-signal one); including docs/usage.md
  or an unrelated file is the precision/hallucination error.

  ANSWER KEY (for the scoring Architect). The blast radius is EXACTLY these 9 files:
    1. util/slug.js          - definition site (the helper itself)
    2. pages/article.js      - call site (articleUrl)
    3. pages/author.js       - call site (authorUrl)
    4. pages/tag.js          - call site (tagUrl)
    5. api/router.js         - call site (route)
    6. search/index.js       - call site (indexKey)
    7. cli/generate.js       - call site (fileNameFor)
    8. tests/slug.test.js    - call site (test of the helper)
    9. importers/legacy.js   - INLINE DUPLICATE of the helper body, no call [BURIED]

  NOT in the blast radius: docs/usage.md (prose mention only), tests/article.test.js
  (calls articleUrl, an indirect/transitive caller - acceptable to note as transitive
  but NOT a direct slug site; the answer key does not require it and does not penalize a
  model that flags it as transitive), and all unrelated util/model/service/middleware/
  config files.

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - The output includes `importers/legacy.js` (or `legacy.js`) AND describes it as an
      inline duplicate / re-implementation / copy-paste of the helper logic. Grep the
      output for `legacy` co-occurring with `duplicate`/`inline`/`re-implement`/`copy`.
      Present == the buried item caught. Absent == missed.
    - The output includes all 6 source call sites (article, author, tag, router, index,
      generate) plus the definition (util/slug.js). These 7 are the recall floor.
    - The output does NOT include `docs/usage.md` as a code dependency. Grep for
      `usage.md` / `docs/usage` - present == precision false positive.
    - The output does NOT include unrelated files (format.js, numbers.js, mailer.js,
      etc.). Any such file listed is a false positive.

  Scoring guidance:
    - Correctness (hard-fail eligible) = the 9-file blast radius including the inline
      duplicate (importers/legacy.js) and excluding the prose mention and unrelated
      files.
    - Completeness = all 9 present (recall), with importers/legacy.js as the high-signal
      member.
    - Hallucination (hard-fail eligible) = listing docs/usage.md or an unrelated file as
      part of the code blast radius, or inventing a file not in the corpus.
    - Discipline = recognizing the inline duplicate by pattern (not just name) AND
      excluding the prose-only mention.
    - Voice match does NOT apply.
notes: |
  Chat A consistency battery (61-70). variant_pool 15 (3 models x N=5). The SCORED
  SIGNAL is WITHIN-FAMILY SPREAD across the 5 runs PLUS per-model buried-item catch-rate:
  did all 5 runs of a family include importers/legacy.js (the inline copy-pasted
  duplicate of the helper, which has no call site to grep) in the refactor blast radius,
  or did some runs enumerate only the name-matchable call sites and drop the duplicate.
  Peak score on one run is not the question; consistency of catching the one
  pattern-only duplicate across 5 runs is.

  This is a refactor-blast-radius enumeration task: 24 fictional files
  (corpus/refactor-blast-radius-enumeration/codebase.js). The shared helper
  normalizeSlug has six source call sites plus a test call site plus its definition -
  the grep-findable radius. The buried discriminator is importers/legacy.js, which
  re-implements the helper body inline under a different name with NO call, so it is
  reachable only by recognizing the duplicated logic pattern. The precision traps are
  docs/usage.md (prose mention only) and the many unrelated files. Answer key gives the
  exact 9-file blast radius plus the inline duplicate plus grep-verifiable invariants.
  Standard four-phase /eval-pit flow against the frozen rubric/rubric.md. Codenames are
  neutral fictional. Voice match does not apply.
---

# Spec 70 - refactor-blast-radius-enumeration

Given a fictional 24-file codebase and a planned refactor of the shared `normalizeSlug`
helper, enumerate the complete blast radius - every file that would need review or
update - including the one site that duplicates the helper's logic inline rather than
calling it.

The corpus (`corpus/refactor-blast-radius-enumeration/codebase.js`) has the helper
defined in `util/slug.js` and called from six source files (article, author, tag,
router, search index, cli generate) plus a test (`tests/slug.test.js`). Those are the
grep-findable radius. The buried discriminator is `importers/legacy.js`, which
re-implements the exact helper body (the same trim/lowercase/replace chain) inline under
a different name and never calls `normalizeSlug` - a name-grep approach never finds it,
so only recognizing the duplicated logic pattern catches it. The correct answer includes
importers/legacy.js and labels it an inline duplicate.

The precision traps are `docs/usage.md` (a prose mention of the helper with no code
dependency) and the many unrelated util/model/service/middleware/config files - listing
any of them is a false positive. The correct blast radius is exactly 9 files.

This is a Chat A consistency-battery eval. Standard four-phase `/eval-pit` flow against
the frozen `rubric/rubric.md`. The scored signal is within-family SPREAD across the 5
runs plus per-model catch-rate on the single buried inline-duplicate site, not peak
score on one lucky run. The variant pool is 15 (3 models x N=5, effort inert per the
methodology). The answer key in `corpus_intent` gives the exact 9-file radius, the
precision-trap exclusions, and grep-verifiable invariants for the scoring Architect.
Codenames are neutral fictional. Voice match does not apply.
