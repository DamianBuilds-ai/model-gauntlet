---
task_category: correction-without-regression
prompt_under_test: |
  You are given a single target file at
  corpus/correction-without-regression/prior-output-and-correction.md. The
  file contains a PRIOR DRAFT report (produced by another agent) inside a
  fenced code block, followed by a CORRECTION NOTE from a reviewer
  identifying ONE error in the draft.

  Your task: produce a REVISED version of the prior-draft report block with
  the reviewer's correction applied AND every other byte of the report
  block left identical to the prior draft.

  Output the revised report as a SINGLE FENCED CODE BLOCK containing the
  full report content from "# Veldt Systems - Q1 2026 Quarterly Operations
  Report" through the last bullet of section 6. The fence and content
  shape must match the prior draft's structure (same headings, same table
  syntax, same bullets, same prose). Outside the code block, do not
  reproduce the corpus's outer headings or the correction note - output
  ONLY the revised report block.

  Apply ONLY the correction the reviewer identified. Do NOT recompute,
  reformat, re-phrase, or "improve" any other figure, sentence, table
  cell, or bullet, even if you notice something that looks adjacent or
  related. Surgical patch only - any other change is a regression.

  After the code block, append the required output envelope
  (schemaVersion, tier, status, tool_budget_used) as separate lines
  OUTSIDE the code block. No em dashes (spaced hyphens). No emojis. Do
  not add commentary inside or after the code block beyond the envelope.
variant_pool: 15
corpus: corpus/correction-without-regression/
corpus_intent: |
  One target file
  (corpus/correction-without-regression/prior-output-and-correction.md):
  a Veldt Systems Q1 2026 quarterly operations report DRAFT (containing
  one deliberate error in section 4 headcount) plus a reviewer's
  CORRECTION NOTE identifying the error and asking for a surgical fix.
  The report block has ~50 lines of structured content across 6
  sections: headline metrics (5 figures), service availability table
  (6-row table), incidents (5 bullets), headcount (4 lines with
  start->end values and a total), quarterly themes (prose), and Q2
  priorities (4 numbered bullets). The error is in ONE line (Operations
  end-of-quarter figure) with a knock-on in ONE other line (Total
  end-of-quarter figure) - 2 lines must change, ~48 lines must stay
  byte-identical.

  THE CORRECTION-WITHOUT-REGRESSION PROBE. Tests whether fixing one
  thing breaks others - a real agentic-loop failure mode that 100 prior
  evals have not directly probed. Untested Opus niche: Opus's larger
  working set MIGHT hold the unchanged parts intact where Sonnet/Haiku
  regenerate wholesale and silently mutate adjacent state. The hypothesis
  to test: does a model patch surgically (touch only the named line + its
  arithmetic knock-on), or does it regenerate the whole report and
  silently drift one of the ~48 unchanged figures, table cells, or
  sentences?

  The corpus is deliberately laden with MANY subtly-correct adjacent
  numbers that a regenerating model might drift: the revenue figure
  ($4,820,000), the up-12% comparison, 1,847 active customers, 142 net
  new customers, the gross margin 68.4%, operating margin 14.2%, six
  table uptime values with a ledger row that fails SLA (the only `no`),
  incident counts (7 total / 2 high / 3 medium / 2 low), the 38-minute
  MTTR, the Engineering 24 -> 27 line, the Product 6 -> 7 line, the
  start-of-quarter Total 34, the prose dates (March 14th, INC-2026-
  0314-A, 31 minutes / 45 minutes), Q2 priority dates (April 14th, April
  21st). Every one of those is a candidate regression target.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a revised
  report that silently mutated an adjacent number is WORSE than one
  that applied the correction and left everything else intact. A
  regenerating model that produces a "polished" version with rounded
  margins (68% instead of 68.4%), reformatted table column widths, or a
  rewritten prose section has REGRESSED the document even if the named
  correction is applied. Surgical patching is the load-bearing
  behaviour; wholesale regeneration with even one drift = failure.

  ANSWER KEY (for the scoring Architect - the exact end-state of the
  revised report block).

    THE TWO LINES THAT MUST CHANGE (the correction):
    - Section 4 Operations line: `Operations: 4 -> 5` becomes
      `Operations: 4 -> 4`.
    - Section 4 Total line: `Total: 34 -> 39` becomes `Total: 34 -> 38`.

    EVERYTHING ELSE THAT MUST STAY BYTE-IDENTICAL (the ~48 unchanged
    pieces - the regression-risk surface):
    - Section 1 headline metrics: all 5 bullets unchanged exactly
      (Revenue $4,820,000, up 12%, 1,847 active, 142 net new, gross
      margin 68.4%, operating margin 14.2%). No rounding, no rephrase,
      no currency-format change.
    - Section 2 service-availability table: all 6 rows unchanged (gateway
      99.94 yes; ledger 99.87 no; courier 99.96 yes; beacon 99.91 yes;
      almanac 99.99 yes; marlowe 99.93 yes). The `no` for ledger is
      load-bearing - a model that "corrects" it to yes has regressed.
      Header row, separator row, column widths all unchanged.
    - Section 3 incidents: 7 total / 2 high / 3 medium / 2 low / 38 min
      MTTR - all five bullets unchanged.
    - Section 4 Engineering line: `Engineering: 24 -> 27` unchanged.
    - Section 4 Product line: `Product: 6 -> 7` unchanged.
    - Section 5 quarterly themes prose: all sentences exactly as the
      draft has them. The three themes, the INC-2026-0314-A reference,
      March 14th, 45-minute, 31-minute, hotfix narrative - all
      byte-identical. No rephrase, no smoothing.
    - Section 6 Q2 priorities: 4 numbered bullets, each unchanged
      including the April 14th and April 21st dates.
    - All section headings (`## 1. Headline metrics` through `## 6. Q2
      priorities`) unchanged. The `# Veldt Systems - Q1 2026 Quarterly
      Operations Report` H1 unchanged.

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    POSITIVE (must be true in the revised output):
    - `Operations: 4 -> 4` appears exactly once in section 4.
    - `Total: 34 -> 38` appears exactly once in section 4.
    - `Operations: 4 -> 5` appears ZERO times.
    - `Total: 34 -> 39` appears ZERO times.

    REGRESSION INVARIANTS (must STILL be true - any change = regression):
    - The exact string `$4,820,000` appears exactly once.
    - The exact strings `1,847`, `142`, `68.4%`, `14.2%` each appear
      exactly once with the same formatting.
    - The exact strings `99.94`, `99.87`, `99.96`, `99.91`, `99.99`,
      `99.93` each appear exactly once in the table.
    - The cell value `no` appears in the ledger row exactly once (the
      only ledger-row trap - a regenerating model "correcting" the SLA
      miss is a regression).
    - The exact string `Engineering: 24 -> 27` appears exactly once.
    - The exact string `Product: 6 -> 7` appears exactly once.
    - The strings `INC-2026-0314-A`, `March 14th`, `31 minutes`,
      `45 minutes`, `45-minute`, `eight-week` each appear exactly once
      (or as in the draft).
    - The strings `April 14th` and `April 21st` each appear exactly
      once.
    - The four Q2-priority bullets are present in the same order as
      the draft (idempotency keys first, marlowe second, platform-
      engineering hire third, failover drill fourth).
    - The H1 title `# Veldt Systems - Q1 2026 Quarterly Operations
      Report` appears exactly once.
    - Total line count of the revised report block matches the draft's
      total line count (no added or removed blank lines, no merged or
      split sections).

  REGRESSION-DISTRIBUTION TRACKING SPEC (for the Architect): for each
  of the 5 runs per family, record (a) whether the correction was
  applied correctly (the 2-line change), and (b) HOW MANY of the
  regression invariants drifted (and which ones - revenue, table cell,
  prose sentence, Q2 date, etc.). Tally per family: total runs
  fully-correct (correction applied AND zero regressions); mean
  regression count per run; which regression invariants drift most
  often (numerics, prose, table, headings). If Opus reliably patches
  surgically (zero regressions) while Sonnet/Haiku produce
  high-regression "regenerated" outputs, that is the surgical-patch
  signal this eval is designed to surface.

  Scoring guidance:
    - Correctness (hard-fail eligible) = the correction is applied
      exactly (Operations end-of-quarter = 4, Total end-of-quarter =
      38) AND every regression invariant holds. ANY regression =
      Correctness fails the primary metric, even if the correction
      itself is right.
    - Completeness = the revised report contains all 6 sections with
      the same shape as the draft.
    - Hallucination (hard-fail eligible) = inventing a new figure,
      modifying a number the spec did not name, "improving" a sentence
      the spec did not touch, recomputing a margin or sum the spec did
      not flag, claiming the output is identical when it drifted.
    - Format adherence = output is a single fenced code block holding
      the revised report; envelope is outside the code block; no
      extraneous prose.
    - Discipline = surgical patch (2 lines changed, all other lines
      byte-identical to the draft). THE load-bearing discriminator for
      this eval.
    - Reasoning quality = SKIP-eligible; if reasoning is shown, it
      should not justify additional "improvements".
    Voice match does NOT apply.
notes: |
  Eval 106. NEW task_category (correction-without-regression). Tests
  whether fixing one thing breaks others - a real agentic-loop failure
  mode untested in the prior 100 evals. The hypothesis: Opus's larger
  working set MAY hold the unchanged parts intact where Sonnet/Haiku
  regenerate wholesale and silently mutate adjacent state. Pool 15
  (N=5) because regression rate is a variance/drop-rate question and
  needs high N to read.

  DIFFICULTY SELF-CHECK (the eval-48 lesson): would a weak model
  (Haiku) genuinely regress something here? Honest prediction: YES,
  plausibly. The corpus has ~48 lines of unchanged content adjacent to
  the 2-line fix, including: a deliberately-failing SLA cell (ledger
  99.87 no - a model that "tidies" might flip it to yes), specific
  numeric formatting (68.4% vs 68%, $4,820,000 with comma), and
  multi-sentence prose paragraphs. A model that regenerates the report
  wholesale (rather than patching the 2 named lines surgically) is
  likely to drift at least one numeric, smooth at least one sentence,
  or "correct" the ledger SLA cell. If Haiku reliably patches
  surgically across 5 runs, the eval is a ceiling tie; the
  regression-risk surface above is calibrated to bite.

  HINT-FREE compliance (the eval-43 lesson): the corpus contains ZERO
  comments naming or pointing at any regression-risk line, ZERO
  structural tells, ZERO suspicious section labels. The 6-section
  report shape is natural for a quarterly report; the ledger SLA fail
  reads as ordinary content (it is a realistic miss); the headcount
  arithmetic error sits in section 4 because that is where headcount
  goes. The reviewer's correction note is direct and unambiguous (no
  ambiguity about which line is wrong). No comment in the corpus says
  "do not touch this" or "watch out for the ledger SLA".

  Codenames: Veldt Systems (company), Hollowmere + Marlowe (project
  names), Q1 2026 (synthetic quarter), INC-2026-0314-A (incident
  handle - reused from eval 105 for consistency across Veldt corpus
  but not a problem since both are synthetic). All neutral fictional
  per repo hygiene. Variant pool 15 (N=5, regression-rate question).
  Corpus dir: corpus/correction-without-regression/.
---

# Spec 106 - correction-without-regression (the surgical-patch probe)

Given a prior agent's draft output (containing one deliberate error) plus a
reviewer's correction note identifying that error, produce a revised version
that applies ONLY the named correction and leaves every other byte of the
prior output identical. This is a NEW task category that closes an
agentic-loop failure mode not directly probed by the prior 100 evals: does
fixing one thing silently break others?

The hypothesis worth testing: Opus's larger working set may hold the
unchanged ~48 lines intact where Sonnet/Haiku regenerate the whole report
and silently mutate adjacent state - a precise margin, a table cell, a
prose sentence. If true, surgical-patch reliability is a usable Opus niche.
If false (all three models patch reliably, or all three regress equally),
the question closes.

The corpus
(`corpus/correction-without-regression/prior-output-and-correction.md`) is
a Veldt Systems Q1 2026 quarterly operations report draft (~50 lines, six
sections: headline metrics, service-availability table, incident counts,
headcount, quarterly themes prose, Q2 priorities) plus a reviewer
CORRECTION NOTE identifying ONE error (the section-4 Operations
end-of-quarter figure should be 4, not 5; the Total end-of-quarter on the
next line therefore should be 38, not 39). The fix is 2 lines; the
regression-risk surface is ~48 lines, including a deliberately-failing SLA
cell (ledger 99.87 marked `no`) that a "tidying" model might flip,
specific numeric formatting ($4,820,000, 68.4%), and multi-sentence prose
paragraphs that a regenerating model might smooth.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`.
The correctness-first quality principle holds: a revised report that
silently mutated an adjacent number is WORSE than one that applied the
correction cleanly with everything else intact. The
regression-distribution metric records (a) whether the correction was
applied and (b) how many regression invariants drifted per run so the
Architect can compare surgical-patch families to regenerate-and-drift
families. Correctness and Hallucination are hard-fail eligible; Discipline
(surgical patch, 2 lines changed, all other lines byte-identical) is THE
load-bearing discriminator. Voice match does not apply. The variant pool
is 15 (3 models x N=5, effort inert per the methodology). The corpus is
the directory `corpus/correction-without-regression/`.
