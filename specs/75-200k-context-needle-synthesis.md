---
task_category: long-context-needle-synthesis
prompt_under_test: |
  You are given a single large reference document at
  corpus/200k-context-needle-synthesis/ops-manual.md - the consolidated operations
  manual of a fictional logistics company. It is roughly 220,000 tokens long. Read the
  whole document.

  Answer this ONE question, drawing ONLY on facts stated in the document:

    "A pharmaceutical-grade reefer (refrigerated container) experiences a confirmed
     Tier-3 cold-chain breach. (a) What is the cold-chain cutoff temperature that
     defines the breach for this freight category? (b) Who must the breach be escalated
     to? (c) What is the maximum permitted time window from the detected failure to the
     logged escalation?"

  The document contains many near-duplicate statements about temperatures, escalation
  contacts, and timing windows for OTHER freight categories and OTHER scenarios. Several
  of these closely resemble the correct answer but state different values. You must find
  the statements that govern THIS specific case - a pharmaceutical-grade reefer with a
  Tier-3 cold-chain breach - and not be misled by the look-alike distractors.

  For each of (a), (b), (c): state the value AND quote the exact sentence from the
  document that supports it (so your source is verifiable). If the document does not
  support a part, say so - do NOT guess or fill from general knowledge. Finally, give a
  one-sentence synthesis combining all three into the complete escalation rule.

  Append the required output envelope (schemaVersion, tier, status, tool_budget_used) as
  separate lines. No em dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/200k-context-needle-synthesis/
corpus_intent: |
  GENERATED CORPUS. corpus/200k-context-needle-synthesis/ops-manual.md is produced
  deterministically by corpus/200k-context-needle-synthesis/generate.py (seed=75). The
  file is ~880,000 chars (~220,000 tokens at ~4 chars/token), a fictional "Stonebrook
  Logistics" operations manual. To regenerate byte-identically: cd into the corpus dir
  and run `python3 generate.py`. The script asserts each needle appears exactly once.

  WHAT THIS EVAL PROBES: long-context (>200k token) needle synthesis - can the model
  find ALL THREE planted facts scattered across a 220k-token window (at ~18%, ~52%, and
  ~86% of the document) and synthesise them into one answer WITHOUT being baited by the
  near-duplicate distractors that state the WRONG values for other categories. This is
  the >200k-context gap on the gauntlet map. The discriminator is full-recall at
  distance + distractor resistance + no fabrication.

  QUALITY PRINCIPLE (recall-at-distance + distractor resistance): the document plants
  near-duplicate distractors (a 4.0C general chill guideline, a -18.0C frozen target, a
  Regional-Manager returns-escalation, a 30-minute routine window) that resemble the
  true needles but apply to OTHER categories. A model that grabs a plausible-looking
  distractor instead of the category-specific needle is confidently wrong. Finding 2 of
  3 needles and honestly flagging the third as not-found is better than fabricating a
  third value. The needles are quotable; an answer must quote them.

  ANSWER KEY (the three planted needles - the scoring Architect verifies by grep):
    (a) Cold-chain cutoff temperature = 2.0 degrees Celsius (pharmaceutical-grade
        reefer). NEEDLE [N1]. The 4.0C general guideline and -18.0C frozen target are
        DISTRACTORS - wrong for this category.
    (b) Escalation contact = the Night Operations Duty Controller (NOT the Regional
        Manager). NEEDLE [N2]. "Regional Manager" appears in a returns-escalation
        distractor and as the after-the-fact-informed party - selecting Regional Manager
        as the escalation target is the bait failure.
    (c) Maximum failure-to-escalation window = 18 minutes. NEEDLE [N3]. The 30-minute
        figure is the general routine distractor and does NOT apply to Tier-3 cold-chain.
    Synthesis: a Tier-3 pharmaceutical-grade cold-chain breach (probe at/above 2.0C) must
    be escalated to the Night Operations Duty Controller within 18 minutes.

  GREP-VERIFIABLE INVARIANTS (for the Architect, against the corpus and the model output):
    - In the corpus: `grep -c "NEEDLE \[N1\]" ops-manual.md` == 1; same for N2, N3.
    - N1 corpus grep: `grep "cutoff temperature for pharmaceutical-grade freight is 2.0"`
      -> exactly 1 hit (the needle).
    - N2 corpus grep: `grep "Night Operations Duty Controller"` -> the escalation needle.
    - N3 corpus grep: `grep "maximum permitted window from a detected reefer-failure"`
      -> the 18-minute needle.
    - A CORRECT model output contains all three of: "2.0" (degrees), "Night Operations
      Duty Controller", "18 minutes" - as the answers to (a)(b)(c) respectively.
    - A BAITED/wrong output instead contains "4.0" or "-18.0" for (a), "Regional Manager"
      as the escalation target for (b), or "30 minutes" for (c).

  Scoring guidance:
    - Correctness (hard-fail eligible) = all three answers match the needles (2.0C /
      Night Operations Duty Controller / 18 minutes) AND the synthesis is right. Any
      distractor value substituted for a needle is Correctness=1.
    - Completeness = all three of (a)(b)(c) answered, each with its supporting quote,
      plus the synthesis.
    - Hallucination (hard-fail eligible) = inventing a value not in the document, or
      claiming a part is supported when only a distractor exists.
    - Discipline = answered ONLY from the document, quoted sources, flagged any
      unsupported part rather than guessing.
    - Source transparency (load-bearing here) = each answer quotes the exact supporting
      sentence so recall-at-distance is verifiable.
    - Reasoning quality = correctly distinguished the category-specific needle from the
      look-alike distractor.
    Voice match does NOT apply.
notes: |
  Chat B gap-filler: the >200k-token long-context dimension. The corpus is GENERATED
  (not hand-written) by a deterministic seeded Python script
  (corpus/200k-context-needle-synthesis/generate.py, seed=75) that emits ~880k chars
  (~220k tokens) and plants three needles at ~18%, ~52%, ~86% of the document among ~14
  scattered near-duplicate distractors plus thousands of filler paragraphs. Regenerate
  byte-identically with `python3 generate.py` in the corpus dir.

  The probe is recall-at-distance + distractor resistance: find all three
  category-specific facts across the full window and synthesise them, without grabbing a
  plausible look-alike distractor (4.0C general chill, -18.0C frozen, Regional-Manager
  returns escalation, 30-minute routine window) that states the wrong value for a
  different freight category. The answer key names the three needles (2.0C / Night
  Operations Duty Controller / 18 minutes) with grep-verifiable invariants for the
  scoring Architect. Correctness and Hallucination are hard-fail eligible; source
  transparency (quoting each needle) is load-bearing because it proves recall at
  distance. Standard four-phase /eval-pit flow against the frozen rubric/rubric.md. The
  variant pool is 9 (3 models x N=3, effort inert per the methodology). The corpus is the
  directory corpus/200k-context-needle-synthesis/.
---

# Spec 75 - 200k-context-needle-synthesis (the >200k-token gap)

Hand a model a ~220,000-token synthetic logistics operations manual and ask one
question whose answer requires three facts scattered across the full window - at roughly
18%, 52%, and 86% of the document - while many near-duplicate distractors state the
WRONG values for other freight categories. This fills the >200k-context blank on the
gauntlet map: prior long-context evals stayed well under 200k tokens.

The corpus is GENERATED, not hand-written. `corpus/200k-context-needle-synthesis/
generate.py` (seed=75) emits `ops-manual.md` (~880k chars, ~220k tokens) deterministically
- re-running it produces byte-identical output, and it asserts each of the three needles
appears exactly once. The needles are: (N1) the pharmaceutical-grade reefer cold-chain
cutoff is 2.0 degrees Celsius; (N2) a Tier-3 cold-chain breach escalates to the Night
Operations Duty Controller, not the Regional Manager; (N3) the maximum failure-to-
escalation window is 18 minutes, not the general 30-minute routine figure.

The discriminator is full recall at distance combined with distractor resistance: a 4.0C
general chill guideline, a -18.0C frozen target, a Regional-Manager returns-escalation,
and a 30-minute routine window all appear as look-alike bait. A model that substitutes a
distractor value for a needle is confidently wrong; finding two of three and honestly
flagging the third beats fabricating a third value. Each answer must quote its supporting
sentence so recall is verifiable.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. Correctness
and Hallucination are hard-fail eligible; source transparency (quoting each needle) is
load-bearing. Voice match does not apply. The variant pool is 9 (3 models x N=3, effort
inert per the methodology). The corpus is the directory
`corpus/200k-context-needle-synthesis/`.
