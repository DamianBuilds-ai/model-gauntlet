---
task_category: long-context-cross-file-refactor
prompt_under_test: |
  You are given a single large file at corpus/200k-cross-file-refactor/codebase.md - a
  concatenated snapshot of a fictional Python codebase, roughly 200,000 tokens. Each
  fenced block is one source file, headed by its path ("### File: src/...").

  Your task: the function `compute_settlement_fee` is being RENAMED to
  `compute_batch_settlement_fee`. Find EVERY site in the codebase that must change - its
  one definition AND every call site - and produce the complete rename.

  The codebase contains DECOY functions with deliberately similar names (for example
  compute_service_fee, compute_settlement_total, settlement_fee_table,
  compute_settlement_fees, compute_settlementfee, get_settlement_fee_rate). These are
  NOT the target and must be left UNCHANGED. Rename ONLY the exact symbol
  `compute_settlement_fee`.

  Output a list of every file path that must change, and for each, the exact line(s) you
  would edit, showing the before and after token. Count and state the total number of
  sites you found. Do NOT rename any decoy. Do NOT change anything other than the exact
  target symbol.

  Append the required output envelope (schemaVersion, tier, status, tool_budget_used) as
  separate lines. No em dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/200k-cross-file-refactor/
corpus_intent: |
  GENERATED CORPUS. corpus/200k-cross-file-refactor/codebase.md is produced
  deterministically by corpus/200k-cross-file-refactor/generate.py (seed=76). The file
  is ~801,000 chars (~200,000 tokens at ~4 chars/token), a fictional concatenated
  Python codebase. To regenerate byte-identically: cd into the corpus dir and run
  `python3 generate.py`. The script asserts exactly 1 definition + 12 total target
  sites.

  WHAT THIS EVAL PROBES: cross-file refactor across a >200k-token window - can the model
  catch EVERY one of the 12 target sites spread evenly from ~3% to ~97% of the corpus
  (none dropped at distance) while NOT touching the many decoy symbols with similar
  names. This is the >200k-context cross-file dimension of the gauntlet gap. The
  discriminator is full recall at distance (all 12 sites, none missed at the far end of
  the window) + precision (zero decoys renamed).

  QUALITY PRINCIPLE (recall-at-distance + precision): the failure modes are symmetric -
  MISSING a target site (especially the ones near the end of the 200k window, the
  classic long-context recall decay) is an under-recall error; RENAMING a decoy
  (compute_service_fee, compute_settlement_total, etc.) is a precision/over-reach error.
  Both are penalised. A model that honestly reports "I found 11 sites and am unsure
  whether one near the end is a 12th" is better than one that confidently renames a
  decoy to pad the count. The exact target token is `compute_settlement_fee` with an
  open paren or as a def; the decoys differ by suffix/prefix and must be left alone.

  ANSWER KEY (the 12 sites - the scoring Architect verifies by grep on the corpus):
    - There is EXACTLY 1 definition of `compute_settlement_fee` (the line marked
      "# TARGET: the refactor renames this function").
    - There are EXACTLY 11 call sites (each marked "# TARGET CALL SITE").
    - Total = 12 sites that must be renamed to `compute_batch_settlement_fee`.
    - Every decoy (compute_service_fee, compute_settlement_total, settlement_fee_table,
      compute_settlement_fees, compute_settlementfee, get_settlement_fee_rate) must be
      LEFT UNCHANGED.

  GREP-VERIFIABLE INVARIANTS (for the Architect, against the corpus):
    - `grep -oc "compute_settlement_fee(" codebase.md` == 12 (the exact target sites:
      1 def + 11 calls; the `(` boundary excludes the plural decoy
      `compute_settlement_fees` and the no-underscore `compute_settlementfee`).
    - `grep -c "def compute_settlement_fee(" codebase.md` == 1 (the single definition).
    - `grep -c "# TARGET CALL SITE" codebase.md` == 11.
    - Decoys are present: `grep -c "compute_service_fee" codebase.md` > 0 etc. - a
      CORRECT model output renames NONE of these.
    - A CORRECT model output reports total sites == 12 and lists 12 file paths; it does
      NOT list any file solely because of a decoy occurrence.

  Scoring guidance:
    - Correctness (hard-fail eligible) = all 12 target sites identified for rename AND
      zero decoys renamed. Renaming a decoy, or fabricating a 13th site, is
      Correctness=1.
    - Completeness = all 12 sites found (the load-bearing recall metric - missing a
      far-window site is the primary failure to detect).
    - Hallucination (hard-fail eligible) = inventing a site that does not exist, or
      claiming a decoy is a target.
    - Discipline = renamed ONLY the exact symbol; left every decoy and every unrelated
      line untouched (precision).
    - Source transparency = cited exact file path + line for each of the 12 sites.
    - Reasoning quality = correctly distinguished target from decoys by exact token, not
      fuzzy name match.
    Voice match does NOT apply.
notes: |
  Chat B gap-filler: the >200k-token cross-file-refactor dimension, complement to eval
  75's needle synthesis. The corpus is GENERATED by a deterministic seeded Python script
  (corpus/200k-cross-file-refactor/generate.py, seed=76) emitting ~801k chars (~200k
  tokens) of fictional concatenated Python modules. The target symbol
  `compute_settlement_fee` appears at exactly 12 sites (1 definition + 11 call sites)
  spread evenly from ~3% to ~97% of the corpus, among hundreds of decoy occurrences of
  similarly-named functions. Regenerate byte-identically with `python3 generate.py` in
  the corpus dir; the script asserts the site counts.

  The probe is full recall at distance + precision: catch all 12 sites (the ones near
  the end of the 200k window are the long-context recall-decay trap) while renaming none
  of the decoys (compute_service_fee, compute_settlement_total, settlement_fee_table,
  etc.). Both under-recall (missing a far site) and over-reach (renaming a decoy) are
  penalised. The answer key gives the 12-site count with grep-verifiable invariants
  (`grep -oc "compute_settlement_fee(" codebase.md` == 12; def count == 1). Correctness
  and Hallucination are hard-fail eligible; Completeness (full recall) and Discipline
  (precision) are the load-bearing discriminators. Standard four-phase /eval-pit flow
  against the frozen rubric/rubric.md. The variant pool is 9 (3 models x N=3, effort
  inert per the methodology). The corpus is the directory corpus/200k-cross-file-refactor/.
---

# Spec 76 - 200k-cross-file-refactor (the >200k-token cross-file gap)

Hand a model a ~200,000-token concatenated fictional codebase and ask it to rename one
function - `compute_settlement_fee` -> `compute_batch_settlement_fee` - finding every
one of its 12 sites (1 definition + 11 call sites) spread evenly from ~3% to ~97% of the
window, while leaving the many decoy functions with similar names untouched. This is the
cross-file half of the >200k-context gap (eval 75 is the needle-synthesis half).

The corpus is GENERATED, not hand-written. `corpus/200k-cross-file-refactor/generate.py`
(seed=76) emits `codebase.md` (~801k chars, ~200k tokens) deterministically and asserts
exactly 1 definition plus 12 total target sites. The 12 sites are spread across the full
window so distance, not clustering, is the challenge; decoy symbols
(compute_service_fee, compute_settlement_total, settlement_fee_table,
compute_settlement_fees, compute_settlementfee, get_settlement_fee_rate) are scattered
throughout to bait fuzzy matching.

The discriminator is symmetric: full recall at distance (catch all 12, especially the
far-window sites that long-context models tend to drop) AND precision (rename zero
decoys). An honest "found 11, unsure about a possible 12th near the end" beats a
confident decoy-rename that pads the count. The answer key gives the 12-site count and
grep-verifiable invariants (`grep -oc "compute_settlement_fee(" codebase.md` == 12, def
count == 1).

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. Correctness
and Hallucination are hard-fail eligible; Completeness (recall) and Discipline
(precision) are the load-bearing discriminators. Voice match does not apply. The variant
pool is 9 (3 models x N=3, effort inert per the methodology). The corpus is the directory
`corpus/200k-cross-file-refactor/`.
