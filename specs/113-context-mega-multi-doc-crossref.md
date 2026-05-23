---
task_category: context-mega-multi-doc-crossref
prompt_under_test: |
  You are given a single large reference archive at
  corpus/context-mega-multi-doc-crossref/vellforge-archive.md - the consolidated
  archive of a fictional research consortium named "Vellforge Cooperative". It is
  roughly 250,000 tokens long and is composed of approximately 50 sub-documents
  (charters, council minutes, research notes, policy briefs, financial summaries,
  glossary fragments) drawn from multiple committees and regional chapters. Read
  the whole archive.

  Answer this ONE question, drawing ONLY on facts stated in the archive:

    "Under the Vellforge Cooperative's amended charter, what four governing
     parameters together determine whether a new Class-IV Frontier research
     initiative may be launched? Specifically: (a) what percentage of the annual
     Frontier reserve fund is allocated to a Class-IV Frontier initiative, (b)
     what voting threshold of the Standing Council is required to launch one,
     (c) what minimum sponsoring-researcher tenure (in consecutive cycles of
     accredited standing) is required, and (d) within how many calendar days of
     the close of the deliberation window must the launch be ratified?"

  The archive contains many near-duplicate statements about budget allocations,
  voting thresholds, tenure minima, and ratification windows for OTHER initiative
  classes (Class-I Survey, Class-II Applied, Class-III Sustained, Class-V
  Restricted). Several of these closely resemble the correct answers but state
  different values. You must find the statements that govern the Class-IV
  Frontier class SPECIFICALLY and not be misled by the look-alike distractors.

  For each of (a), (b), (c), (d): state the value AND quote the exact sentence
  from the archive that supports it (so your source is verifiable). If the
  archive does not support a part, say so - do NOT guess or fill from general
  knowledge. Finally, give a one-sentence synthesis combining all four into the
  complete launch rule for a Class-IV Frontier initiative.

  Append the required output envelope (schemaVersion, tier, status,
  tool_budget_used) as separate lines. No em dashes (use spaced hyphens). No
  emojis.
variant_pool: 9
corpus: corpus/context-mega-multi-doc-crossref/
corpus_intent: |
  GENERATED CORPUS. corpus/context-mega-multi-doc-crossref/vellforge-archive.md
  is produced deterministically by
  corpus/context-mega-multi-doc-crossref/generate.py (seed=113). The file is
  ~1,000,000 chars (~250,000 tokens at ~4 chars/token), a fictional "Vellforge
  Cooperative" archive composed of approximately 50 sub-documents. To regenerate
  byte-identically: cd into the corpus dir and run `python3 generate.py`. The
  script asserts each of the four needles appears exactly once (by distinctive
  unique-phrase grep) and that no spoiler annotations have leaked into the
  corpus.

  WHAT THIS EVAL PROBES: extra-long-context (~250k token) cross-document
  synthesis - can the model find ALL FOUR planted facts scattered across a 50-
  sub-document, ~250k-token window (at roughly the 11%, 34%, 58%, and 81% marks)
  and synthesise them into one answer WITHOUT being baited by the ~14 near-
  duplicate distractors that state the WRONG values for other initiative
  classes? This is the >250k-context cross-doc dimension on the gauntlet map,
  one step bigger and broader than eval 75 (which is a single document, 3
  needles). The discriminator is full-recall at distance + cross-sub-doc
  navigation + distractor resistance + no fabrication.

  QUALITY PRINCIPLE (recall-at-distance + cross-doc cross-reference +
  distractor resistance): the archive plants ~14 near-duplicate distractors
  (Class-I 9.0% allocation, Class-II 12.5%, Class-III 22.0%; simple-majority
  for Class-I, two-thirds for Class-II/III, unanimous for Class-V; 3-cycle,
  5-cycle, 10-cycle tenures; 14-day, 30-day, 45-day ratification windows; and
  two averaging-style observations) that resemble the true needles but apply to
  OTHER classes. A model that grabs a plausible-looking distractor instead of
  the Class-IV-specific needle is confidently wrong. Finding 3 of 4 needles
  and honestly flagging the fourth as not-found is better than fabricating a
  fourth value. The needles are quotable; an answer must quote them.

  NO SPOILER ANNOTATIONS in the corpus (no `NEEDLE [Nx]` markers, no
  `ANSWER KEY` strings, no `DISTRACTOR` tags). The needles are identifiable
  ONLY by their distinctive natural-language phrasing. The generator's own
  assertions and this corpus_intent are the ONLY places the answer key lives.

  ANSWER KEY (the four planted needles - the scoring Architect verifies by grep):
    (a) Annual budget allocation for Class-IV Frontier = 14.7 percent of the
        annual Frontier reserve fund. NEEDLE N1. The 9.0%, 12.5%, and 22.0%
        figures are DISTRACTORS - those apply to Class-I, Class-II, and
        Class-III respectively. The 13-percent "average across all five
        classes" line is also a distractor (averages, not class-specific).
    (b) Standing Council voting threshold for launching a Class-IV Frontier
        initiative = a three-quarters supermajority of the Standing Council.
        NEEDLE N2. "Simple majority" applies to Class-I, "two-thirds" applies
        to Class-II and Class-III, "unanimous" applies to Class-V. Picking any
        of those is the bait failure.
    (c) Sponsoring-researcher eligibility tenure for Class-IV Frontier = at
        least 7 consecutive cycles of accredited standing. NEEDLE N3. The 3-,
        5-, and 10-cycle figures are DISTRACTORS for other classes; the
        "6-cycle average across all classes" line is also a distractor.
    (d) Ratification deadline for a Class-IV Frontier launch = within 21
        calendar days from the close of the deliberation window. NEEDLE N4.
        The 14-day, 30-day, and 45-day figures are DISTRACTORS for other
        classes.
    Synthesis: launching a Class-IV Frontier initiative under the amended
    charter requires 14.7% of the annual Frontier reserve fund, a
    three-quarters supermajority of the Standing Council, a sponsoring
    researcher with at least 7 consecutive cycles of accredited standing, and
    ratification within 21 calendar days of the close of the deliberation
    window.

  GREP-VERIFIABLE INVARIANTS (for the Architect, against the corpus and the
  model output):
    In the corpus (must be exactly 1 hit each):
      - `grep -c "14.7 percent of the annual Frontier reserve fund" vellforge-archive.md`
        -> 1 (N1 needle).
      - `grep -c "three-quarters supermajority of the Standing Council" vellforge-archive.md`
        -> 1 (N2 needle).
      - `grep -c "at least 7 consecutive cycles of accredited standing on the Tenure Registrar" vellforge-archive.md`
        -> 1 (N3 needle).
      - `grep -c "must be ratified within 21 calendar days from the close of the deliberation window" vellforge-archive.md`
        -> 1 (N4 needle).
      - `grep -c "NEEDLE \[" vellforge-archive.md` -> 0 (no spoilers leaked).
    A CORRECT model output contains all four of: "14.7" (with "percent" or "%"),
    "three-quarters" (or "75%" / "three quarter"), "7 consecutive cycles" (or
    "seven consecutive cycles"), and "21 calendar days" (or "21 days") - as the
    answers to (a)(b)(c)(d) respectively, paired with quoted supporting
    sentences from the corpus.
    A BAITED/wrong output instead contains "9.0", "12.5", or "22.0" for (a);
    "simple majority", "two-thirds", or "unanimous" for (b); "3", "5", "6", or
    "10" cycles for (c); or "14", "30", or "45" calendar days for (d).

  Scoring guidance:
    - Correctness (hard-fail eligible) = all four answers match the needles
      (14.7% / three-quarters / 7 cycles / 21 days) AND the synthesis is right.
      Any distractor value substituted for a needle is Correctness=1.
    - Completeness = all four of (a)(b)(c)(d) answered, each with its
      supporting quote, plus the synthesis.
    - Hallucination (hard-fail eligible) = inventing a value not in the archive,
      or claiming a part is supported when only a distractor exists.
    - Discipline = answered ONLY from the archive, quoted sources, flagged any
      unsupported part rather than guessing.
    - Source transparency (load-bearing here) = each answer quotes the exact
      supporting sentence so recall-at-distance is verifiable.
    - Reasoning quality = correctly distinguished the Class-IV-specific needle
      from each look-alike distractor; correctly rejected the averaging-style
      observations as not-per-class figures.
    Voice match does NOT apply.
notes: |
  Chat B gap-filler: the >250k-token cross-doc synthesis dimension. The corpus
  is GENERATED (not hand-written) by a deterministic seeded Python script
  (corpus/context-mega-multi-doc-crossref/generate.py, seed=113) that emits
  ~1,000,000 chars (~250k tokens) across approximately 50 sub-documents and
  plants four needles at ~11%, ~34%, ~58%, ~81% of the archive among ~14
  scattered near-duplicate distractors plus thousands of filler paragraphs.
  Regenerate byte-identically with `python3 generate.py` in the corpus dir.

  This is one step BIGGER and BROADER than eval 75: single-doc 220k 3-needle
  becomes ~50-sub-doc 250k 4-needle. The probe is recall-at-distance +
  cross-sub-doc navigation + distractor resistance: find all four
  class-specific facts across the full ~250k window, scattered across roughly
  fifty distinct sub-documents, and synthesise them without grabbing a
  plausible look-alike distractor (Class-I 9.0% / Class-II 12.5% / Class-III
  22.0% allocations; simple-majority / two-thirds / unanimous thresholds; 3-,
  5-, 6-, 10-cycle tenure figures; 14-, 30-, 45-day ratification windows). The
  answer key names the four needles (14.7% / three-quarters / 7 cycles / 21
  days) with grep-verifiable invariants for the scoring Architect.

  CRITICAL: NO spoiler annotations are written into the corpus. The needles
  are identifiable only by their distinctive natural-language phrasing. The
  generator's assertions and this corpus_intent are the ONLY places the answer
  key lives. This is stricter than eval 75 (which uses `NEEDLE [Nx]` markers
  in-corpus) and matches the public-repo hygiene requirement.

  Correctness and Hallucination are hard-fail eligible; source transparency
  (quoting each needle) is load-bearing because it proves recall at distance.
  Standard four-phase /eval-pit flow against the frozen rubric/rubric.md. The
  variant pool is 9 (3 models x N=3, effort inert per the methodology). The
  corpus is the directory corpus/context-mega-multi-doc-crossref/.
---

# Spec 113 - context-mega-multi-doc-crossref (the >250k-token multi-doc cross-reference gap)

Hand a model a ~250,000-token synthetic archive composed of approximately fifty
distinct sub-documents and ask one question whose answer requires four facts
scattered across the full window - at roughly the 11%, 34%, 58%, and 81% marks,
each living in a different sub-document - while many near-duplicate distractors
state the WRONG values for other initiative classes. This fills the
>250k-context cross-doc cross-reference blank on the gauntlet map: prior long-
context evals (notably eval 75 at 220k single-doc 3-needle) stayed inside one
document with a smaller window.

The corpus is GENERATED, not hand-written.
`corpus/context-mega-multi-doc-crossref/generate.py` (seed=113) emits
`vellforge-archive.md` (~1,000,000 chars, ~250k tokens) deterministically - re-
running it produces byte-identical output, and it asserts each of the four
needles appears exactly once by its distinctive unique-phrase grep AND that no
spoiler annotations (no `NEEDLE [Nx]` markers, no `ANSWER KEY` strings) have
leaked into the corpus. The needles are: (N1) the Class-IV Frontier annual
budget allocation is 14.7 percent of the annual Frontier reserve fund; (N2)
launching a Class-IV Frontier initiative requires a three-quarters
supermajority of the Standing Council; (N3) the sponsoring researcher must
hold at least 7 consecutive cycles of accredited standing; (N4) the
ratification deadline is 21 calendar days from the close of the deliberation
window.

The discriminator is full recall at distance combined with cross-sub-doc
navigation and distractor resistance: Class-I 9.0% / Class-II 12.5% /
Class-III 22.0% allocations, simple-majority / two-thirds / unanimous
thresholds for other classes, 3- / 5- / 10-cycle tenure figures for other
classes, and 14- / 30- / 45-day ratification windows for other classes all
appear as look-alike bait, alongside two "averaging across all classes" lines
that resemble per-class figures but are not. A model that substitutes a
distractor value for a needle is confidently wrong; finding three of four and
honestly flagging the fourth beats fabricating a fourth value. Each answer
must quote its supporting sentence so recall is verifiable.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`.
Correctness and Hallucination are hard-fail eligible; source transparency
(quoting each needle) is load-bearing. Voice match does not apply. The variant
pool is 9 (3 models x N=3, effort inert per the methodology). The corpus is
the directory `corpus/context-mega-multi-doc-crossref/`.
