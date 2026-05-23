---
task_category: context-arithmetic-at-scale
prompt_under_test: |
  You are given a single large reference document at
  corpus/context-arithmetic-at-scale/report.md - approximately 200,000 tokens of
  fictional quarterly board-pack narrative for a company called "Northwind
  Group". Scattered throughout the document are EXACTLY 80 dollar-figure line
  items, each one tagged with a leading `[FIG]` marker at the start of its line
  and a trailing `(category=X)` tag at the end. Each [FIG] line is tagged with
  exactly one of these four categories:

    - infrastructure
    - personnel
    - marketing
    - legal

  Read the whole document. Find ALL 80 [FIG] lines. Sum their dollar amounts
  per category, and compute the grand total. ALL arithmetic must be exact - a
  single wrong figure fails the task.

  Output a single fenced JSON object with EXACTLY this structure and key order:

    {
      "figure_count_per_category": {
        "infrastructure": integer,
        "personnel": integer,
        "marketing": integer,
        "legal": integer
      },
      "category_totals_usd": {
        "infrastructure": integer,
        "personnel": integer,
        "marketing": integer,
        "legal": integer
      },
      "grand_total_usd": integer,
      "reconciliation_ok": boolean
    }

  Hard rules:
    - Every dollar value is an INTEGER number of US dollars (no decimals, no
      cents, no thousands separators - just the integer, e.g. 41844533).
    - `grand_total_usd` MUST equal the sum of the four `category_totals_usd`
      values. Set `reconciliation_ok` to true only if your own arithmetic
      verifies this; set false (and explain in one sentence outside the JSON)
      if it does not.
    - Sum the figures you actually extracted from [FIG] lines. Do NOT estimate.
      Do NOT pattern-fill. Do NOT invent a figure that is not on a [FIG] line.
    - If you cannot find all 80 figures, output what you DID find honestly
      (with the correct counts you observed) rather than fabricating to reach
      80. An honest partial beats a confident fabrication.
    - The total count of [FIG] lines across all four categories must be 80;
      if your counts do not sum to 80, say so outside the JSON.

  After the JSON object, append the required output envelope (schemaVersion,
  tier, status, tool_budget_used) as separate lines OUTSIDE the JSON. No em
  dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/context-arithmetic-at-scale/
corpus_intent: |
  GENERATED CORPUS. corpus/context-arithmetic-at-scale/report.md is produced
  deterministically by corpus/context-arithmetic-at-scale/generate.py (seed=120).
  The file is ~800,000 chars (~200,000 tokens at ~4 chars/token) of fictional
  quarterly board-pack narrative for "Northwind Group" - department reports,
  operating commentary, structural filler - with EXACTLY 80 dollar-figure line
  items scattered through it. Each figure line starts with `[FIG]` and ends
  with `(category=X)` where X is one of infrastructure, personnel, marketing,
  legal. The script also writes corpus/context-arithmetic-at-scale/answer-key.json
  containing the exact per-category counts, per-category totals, and grand
  total - this answer key is NOT shipped to the model under test; it is the
  scoring Architect's reference. To regenerate byte-identically: cd into the
  corpus dir and run `python3 generate.py`. The script asserts there are
  exactly 80 [FIG] markers, the per-category counts match, and the
  per-category totals reconcile to the grand total.

  WHAT THIS EVAL PROBES: long-context arithmetic survival at ~200k-token
  scale - whether eval 52's "Haiku arithmetic-survives-at-scale" finding (which
  held on a 60-line CSV at a few thousand tokens) ALSO holds when the figures
  are NOT in a clean CSV but scattered across ~200k tokens of mixed-format
  narrative, tables, and bullet lists. AND - the harder probe - whether ANY
  model (including Sonnet/Opus tier) fabricates totals under length pressure.
  A model that outputs a clean, well-formed, fully-populated JSON object in
  which one or more figures are silently wrong is the worst failure mode -
  a downstream system would trust every number. This is a step up from eval
  52 in both extraction difficulty (figures are NOT pre-tabulated) and context
  length (200k vs ~5k tokens).

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers, under length pressure):
  the [FIG] marker and (category=X) tag are deliberately mechanical and
  unambiguous - the eval is NOT testing whether the model can find ambiguous
  figures; it is testing whether the model can read the FULL 200k window
  without dropping figures and whether it can sum them correctly without
  fabricating. The 80-figure scale is the point: mechanical but unforgiving
  across an extreme context length. A model that "eyeballs" the count, that
  estimates totals, that pattern-fills, or that emits a clean JSON with a
  fabricated reconciliation_ok=true while the totals do not actually sum is
  confidently wrong. A model that honestly reports "I found 78 of 80 figures
  in categories X totalling Y, two figures appear lost" with accurate counts
  for the figures it DID find beats a confident fabrication.

  ANSWER KEY (the scoring Architect verifies against answer-key.json):
    figure_count_per_category:
      infrastructure = 22
      personnel      = 26
      marketing      = 18
      legal          = 14
      (total figures = 80)

    category_totals_usd:
      infrastructure = $11,769,359
      personnel      = $13,355,167
      marketing      = $10,208,317
      legal          = $6,511,690

    grand_total_usd  = $41,844,533

    reconciliation:
      11,769,359 + 13,355,167 + 10,208,317 + 6,511,690 == 41,844,533  (OK)

  GREP-VERIFIABLE INVARIANTS (against the corpus and the model output):
    - In the corpus: `grep -c "^\[FIG\]" report.md` == 80.
    - `grep -c "(category=infrastructure)" report.md` == 22.
    - `grep -c "(category=personnel)" report.md` == 26.
    - `grep -c "(category=marketing)" report.md` == 18.
    - `grep -c "(category=legal)" report.md` == 14.
    - answer-key.json grand_total == 41844533; sum(category_totals) == 41844533.
    - A CORRECT model output reports figure_count_per_category exactly matching
      22/26/18/14, category_totals_usd exactly matching 11769359 / 13355167 /
      10208317 / 6511690, grand_total_usd == 41844533, and reconciliation_ok ==
      true.
    - A WRONG output reports any miscounted category, any wrong per-category
      total, a grand_total that does not equal the sum of the four
      per-category totals, or reconciliation_ok=true while the arithmetic does
      not in fact reconcile.

  Scoring guidance:
    - Correctness (hard-fail eligible) = all four per-category counts AND all
      four per-category totals AND the grand total exactly match the answer
      key. A single wrong figure is Correctness=1. A correct grand total with
      a wrong per-category breakdown is also Correctness=1 (it means the model
      grouped wrong or compensated with offsetting errors).
    - Completeness = all four categories present in both the counts object and
      the totals object; grand_total_usd present; reconciliation_ok present.
    - Hallucination (hard-fail eligible) = inventing a figure that is not on a
      [FIG] line; reporting reconciliation_ok=true while the totals do not
      sum; emitting a clean fully-populated JSON whose underlying figures are
      fabricated.
    - Format adherence = single fenced JSON object with the exact key order
      specified; integers (no decimals, no strings, no commas); envelope
      OUTSIDE the JSON.
    - Discipline = honestly flagged any figure not found; did NOT pattern-fill
      to reach 80; did NOT estimate. An honest partial is better than a
      confident fabrication; this is the load-bearing scoring lever.
    - Reasoning quality applies weakly (this is a near-pure extract-and-sum
      task); if reasoning is shown, it should not invent scope.
    - Source transparency applies weakly (single target file).
    Voice match does NOT apply.
notes: |
  Chat C gap-filler: long-context arithmetic survival at ~200k-token scale,
  combined with the fabrication-under-length-pressure probe. The corpus is
  GENERATED (not hand-written) by a deterministic seeded Python script
  (corpus/context-arithmetic-at-scale/generate.py, seed=120) that emits
  report.md (~800k chars, ~200k tokens) of fictional Northwind Group quarterly
  narrative with EXACTLY 80 [FIG] dollar lines scattered through it across
  four categories with uneven counts (22/26/18/14). The script also writes
  answer-key.json with the exact per-category counts, per-category totals, and
  grand total - this is the Architect's reference and is NOT shipped to the
  model under test. Regenerate byte-identically with `python3 generate.py` in
  the corpus dir.

  The probe is twofold: (1) does eval 52's Haiku-arithmetic-survives-at-scale
  finding hold at MUCH larger scale (200k tokens, scattered figures, mixed
  format) rather than only at small CSV scale, and (2) does ANY model
  (including Sonnet/Opus tier) fabricate totals under the length pressure -
  emitting a clean JSON with confidently-wrong figures that a downstream
  system would trust. The 80-figure scale is uneven by design (22/26/18/14)
  so the model cannot guess by symmetry. The [FIG] marker and (category=X)
  tag are deliberately mechanical so the eval tests recall + arithmetic, not
  extraction-ambiguity. Correctness and Hallucination are hard-fail eligible;
  Discipline (honest partial over confident fabrication) is the load-bearing
  scoring lever. Voice match does not apply. Standard four-phase /eval-pit
  flow against the frozen rubric/rubric.md. The variant pool is 9 (3 models x
  N=3, effort inert per the methodology). The corpus is the directory
  corpus/context-arithmetic-at-scale/.
---

# Spec 120 - context-arithmetic-at-scale (the 200k-token sum-and-reconcile probe)

Hand a model a ~200,000-token synthetic quarterly board-pack narrative for a
fictional "Northwind Group" with EXACTLY 80 [FIG] dollar-figure line items
scattered through it across four categories with uneven counts (22
infrastructure, 26 personnel, 18 marketing, 14 legal). Ask the model to find
every [FIG] line, sum per category, and report the grand total - with a
self-reconciliation check. This fills the long-context arithmetic gap on the
gauntlet map: eval 52 tested arithmetic on a 60-line CSV at ~5k tokens; this
eval tests whether that survives at ~200k tokens with figures scattered through
mixed-format prose.

The corpus is GENERATED, not hand-written.
`corpus/context-arithmetic-at-scale/generate.py` (seed=120) emits `report.md`
(~800k chars, ~200k tokens) deterministically and writes
`answer-key.json` with the exact per-category counts, per-category totals, and
grand total (the Architect's reference, NOT shipped to the model). The
generator asserts there are exactly 80 [FIG] markers, the per-category counts
match 22/26/18/14, and the per-category totals reconcile to the grand total
($11,769,359 + $13,355,167 + $10,208,317 + $6,511,690 = $41,844,533).

The probe is twofold. First: does the eval 52 finding that Haiku-tier
arithmetic survives at small scale ALSO hold at ~200k-token scale with
scattered figures in mixed format? Second: does ANY model - including the
Sonnet/Opus tiers - fabricate totals under length pressure, emitting a clean
fully-populated JSON whose figures are silently wrong? A model that outputs
reconciliation_ok=true while the totals do not actually sum, or that
pattern-fills to reach 80 figures, or that estimates rather than extracts, is
confidently wrong - and a downstream finance system would trust every number.
A model that honestly reports "I found 78 of 80, here are the categories and
amounts I am confident in" with accurate underlying arithmetic beats a
confident fabrication.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`.
Correctness and Hallucination are hard-fail eligible; Discipline (honest
partial over confident fabrication) is the load-bearing discriminator. Voice
match does not apply. The variant pool is 9 (3 models x N=3, effort inert per
the methodology). The corpus is the directory
`corpus/context-arithmetic-at-scale/`.
