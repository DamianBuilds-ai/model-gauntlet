---
task_category: self-consistency-under-rephrase
prompt_under_test: |
  You are given a single file at corpus/self-consistency-under-rephrase/deployment-log.md
  containing a fictional deployment log (14 deploys over two weeks for the Marlowe
  service). Read it once, then answer THREE questions about it. The three questions ask
  for the SAME underlying answer in three different phrasings - your three answers
  should be identical. Answer each question independently, in its own labelled section.
  Do not look at the other questions while answering each one. Do not collapse them into
  a single answer. Treat them as three independent asks of the same underlying thing.

  Produce, in this order:

    ## Q1
    Looking at the deployment log, how many deploys failed and got rolled back during
    the two-week window? Give a single integer answer, then in one sentence say how you
    counted (which rows / which signal in the table).

    ## Q2
    A colleague asks: "Over the last fortnight, can you tell me the count of bad
    Marlowe pushes - the ones we had to revert?" Answer their question. Give a single
    integer, then in one sentence describe what you treated as a "bad push" in the log.

    ## Q3
    For the post-incident review, the platform lead wants the rollback total for
    Marlowe across the entire deployment log shown. Provide the number of rollbacks
    and, in one sentence, identify which deploy ids you are counting as rollbacks.

    ## CONSISTENCY CHECK
    State, in one line, whether your three integer answers above are identical (Q1 == Q2
    == Q3). If they are not, do NOT go back and edit Q1, Q2, or Q3. State the
    discrepancy here and explain why the three framings yielded different numbers.

  Append the required output envelope (schemaVersion, tier, status, tool_budget_used) as
  separate lines after your answer. No em dashes (use spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/self-consistency-under-rephrase/
corpus_intent: |
  One file (corpus/self-consistency-under-rephrase/deployment-log.md): a 14-row
  deployment log with an `outcome` column (success / failure), a `rolled_back` column
  (yes / no), and a notes block stating that every failure was rolled back and every
  success was not. The underlying question - "how many deploys failed and got rolled
  back?" - has ONE correct integer answer: FIVE (5). Deploys with outcome=failure AND
  rolled_back=yes: dpl-0343, dpl-0346, dpl-0348, dpl-0352. Wait - that is four. Let me
  recount: dpl-0343 v8.3.0 failure rolled back; dpl-0346 v8.4.1 failure rolled back;
  dpl-0348 v8.5.0 failure rolled back; dpl-0352 v8.7.0 failure rolled back. That is
  FOUR rollbacks total. The correct answer to all three questions is FOUR (4).

  THE REPHRASE FRAGILITY TEST. The eval is NOT a counting eval - the count is easy and
  every competent model should arrive at 4 on a single straightforward read. The eval is
  whether the three rephrasings cause the SAME model to produce DIFFERENT numbers across
  its three sections, because the framings deliberately tempt different counting
  strategies:

    Q1 frames as "deploys that FAILED AND got rolled back" - the conjunction phrasing
       could tempt a model to count the intersection (still 4) or to over-count if it
       reads "and" as "or" (would yield more).
    Q2 frames as "bad pushes / ones we had to revert" - the colloquial framing ("bad
       push") has fuzzy boundaries. Does a hotfix count as a "bad" push if it was the
       FIX to a previous bad push? The notes block names FOUR hotfixes (dpl-0344,
       0347, 0349, 0353) which are NOT the bad pushes themselves but follow them. A
       model that reads "bad pushes" loosely might include the hotfixes (yielding 8)
       or include only the originals (yielding 4 - correct). The colloquial framing is
       the fragility-tempt.
    Q3 frames as "rollback total / which deploy ids you are counting as rollbacks" -
       the framing pivots on the `rolled_back` column directly. This is the cleanest
       phrasing and should reliably yield 4. If a model produces 4 here but 5 or 8
       elsewhere, the rephrase-fragility is evident.

  The eval scores SELF-CONSISTENCY across the three rephrasings PER RUN, then aggregates
  across 5 runs PER FAMILY. The discriminator is rephrase-invariance, not counting
  accuracy. A model that gets all three wrong consistently (e.g. answers "5" to all
  three because it miscounts) is still SELF-CONSISTENT and is the better outcome on the
  rephrase-fragility dimension than a model that gets Q1=4, Q2=8, Q3=4 (correct on two
  but inconsistent across phrasings).

  QUALITY PRINCIPLE (consistency-first across phrasings): the eval scores whether the
  SAME underlying question, framed three ways, yields the SAME answer. Correctness of
  the count is secondary - the primary failure mode is the model giving Q1=4 / Q2=8 /
  Q3=4, which means its answer is determined by phrasing rather than by the data. If
  any model is genuinely rephrase-invariant, that is a usable routing edge
  (prompt-robust).

  ANSWER KEY (for the scoring Architect):

    THE CORRECT COUNT for all three questions is FOUR (4). The four failed-and-rolled-
    back deploys are: dpl-0343 (v8.3.0), dpl-0346 (v8.4.1), dpl-0348 (v8.5.0), dpl-0352
    (v8.7.0). The four hotfixes (dpl-0344, dpl-0347, dpl-0349, dpl-0353) are
    SUCCESSFUL deploys that followed failures and should NOT be counted as bad pushes,
    rollbacks, or failures. The notes block makes this explicit.

    PER-RUN SELF-CONSISTENCY METRIC (the primary metric, the eval's discriminator):
      - record the integer answer in each of Q1, Q2, Q3 (parse the first standalone
        integer in each section, or the integer explicitly labelled as the count).
      - compute consistency: 1 if Q1 == Q2 == Q3, else 0.
      - a run that produces (4, 4, 4) is consistent AND correct.
      - a run that produces (5, 5, 5) is consistent but incorrect (the rephrase-
        invariance test still passes; the model just miscounted - separately scored).
      - a run that produces (4, 8, 4) is INCONSISTENT (rephrase-fragility - the
        failure mode the eval exists to catch).
      - the model's own CONSISTENCY CHECK section should match the actual numeric
        consistency. A model that reports "all three identical" while having actually
        produced (4, 8, 4) ALSO loses on Source Transparency.

    PER-FAMILY METRICS (across 5 runs per model, reported by the scoring Architect):
      - rephrase-consistency rate (out of 5 runs, how many had Q1==Q2==Q3) - PRIMARY.
      - answer-correctness rate (out of 5 runs, how many had Q1==Q2==Q3==4) -
        SECONDARY.
      - drift pattern (when inconsistent, WHICH section diverges - is Q2 the colloquial
        framing the typical fragility-point, or is the drift distributed).
      - CONSISTENCY-CHECK accuracy (does the model's self-reported check match the
        actual numeric consistency).

  GREP-VERIFIABLE STRUCTURAL INVARIANTS (for the Architect's first-pass triage):
    - Section headings "Q1", "Q2", "Q3", and "CONSISTENCY CHECK" each appear exactly
      once. A model that collapses Q1/Q2/Q3 into a single answer has failed the
      structural setup of the eval.
    - Each of Q1, Q2, Q3 contains at least one standalone integer (the answer).
    - CONSISTENCY CHECK section is present and is one line.
    - Output envelope present after the answer.

  Scoring guidance:
    - Correctness (hard-fail eligible) = the answer is 4 (or honestly inconsistent
      with the model's own stated counting method - a model that states it is counting
      "outcome == failure" rows and produces 4 is correct; one that states the same
      method and produces 5 is internally inconsistent).
    - Consistency (the eval's load-bearing metric) = Q1 == Q2 == Q3 across the run.
      Reported as a per-run binary AND a per-family rate across the 5 runs.
    - Completeness (hard-fail eligible) = all four sections present (Q1, Q2, Q3,
      CONSISTENCY CHECK), envelope present.
    - Hallucination (hard-fail eligible) = inventing a deploy id not in the log,
      inventing a column the log does not have, or stating "all three identical" when
      the numbers are not identical.
    - Reasoning quality = the counting method stated in each section is the correct
      one for that framing AND the model genuinely treats the three questions as
      independent asks (does not say "see Q1" in Q2 or Q3 - the prompt explicitly
      forbids collapsing).
    - Discipline = does not edit Q1/Q2/Q3 after noticing inconsistency in the
      CONSISTENCY CHECK section (the prompt explicitly forbids this); honestly reports
      a discrepancy when one exists.
    - Format adherence = the four labelled sections, integer answer in each, clean
      envelope.
    - Source transparency = grounded in the log table and notes; does not invent a
      column that does not exist.
    - Voice match does NOT apply.

  The single largest separator: a model that produces (Q1=4, Q2=8, Q3=4) - the canonical
  rephrase-fragility pattern (the colloquial Q2 framing tempts the wrong scope) - and
  then claims "all three identical" in the CONSISTENCY CHECK section is the worst
  outcome. A model that produces (4, 4, 4) consistently across all 5 runs is the
  strong outcome - even if the rephrase-design failed to actually tempt that
  particular model, the model demonstrated robustness. A model that is correct on
  some runs and inconsistent on others (e.g. 3 of 5 runs are (4,4,4), 2 are (4,8,4))
  is mid-range and the most diagnostic case - it shows the rephrase-fragility is real
  but probabilistic.
notes: |
  NEW task type. Probes rephrase-invariance - whether the SAME underlying question
  framed three different ways yields the SAME answer from a given model on a given run.
  This is a cleaner consistency probe than the buried-item battery (batch 4) because the
  three "questions" are SEMANTICALLY IDENTICAL and the data is small/clean - the only
  variable is the phrasing. If Opus is more rephrase-invariant than Sonnet/Haiku, that
  is a usable routing edge (prompt-robustness). Pool 15 (N=5) - fundamentally a
  variance/consistency question, high N is mandatory.

  DIFFICULTY SELF-CHECK: would a weak model (Haiku) genuinely diverge across the three
  framings? Prediction: YES - the Q2 colloquial framing ("bad pushes / ones we had to
  revert") has fuzzy enough boundaries that a model under speed pressure could include
  the hotfixes (yielding 8) or include only originals (yielding 4). Q3's "rollback
  total" framing pivots on the explicit `rolled_back: yes` column and should reliably
  yield 4. The gap is the test. Risk: if the phrasings are too similar in spirit, all
  three families consistently produce (4, 4, 4) = ceiling tie. Author judgment: the
  Q2 colloquial framing IS materially different from Q1's precise conjunction and Q3's
  column-pivot - the rephrase-fragility should be real for at least Haiku. If it is a
  ceiling tie at N=5, the eval has falsified the rephrase-fragility hypothesis (also
  useful - it would mean modern models are rephrase-robust on simple counting tasks).

  CONTAMINATION CHECK (eval-43 lesson): the corpus has ZERO hints telling the model
  which deploys to count. The notes block does explicitly state that hotfixes are NOT
  failures - this is GROUNDING, not contamination, because the data needs the
  hotfix vs failure distinction to be unambiguous to the eval's purpose. A model that
  reads the notes carefully gets 4; a model that pattern-matches "v8.3.1, v8.4.2, v8.5.1,
  v8.7.1 follow failures, so they look like hotfixes, but maybe they ALSO count as bad
  pushes?" - that ambiguity is the rephrase-fragility surface. The notes block CLARIFIES
  the counting logic but the colloquial Q2 framing can still tempt the wrong scope.

  Standard four-phase /eval-pit flow against the frozen rubric/rubric.md. The variant
  pool is 15 (3 models x N=5). The corpus is the directory
  corpus/self-consistency-under-rephrase/.
---

# Spec 108 - self-consistency-under-rephrase (the prompt-robustness probe)

The SAME underlying question - "how many Marlowe deploys failed and got rolled back?" -
asked three different ways within a single run, with an explicit CONSISTENCY CHECK
section asking the model to report (without editing) whether its three answers were
identical. The correct count is 4 (four failed-and-rolled-back deploys). The eval scores
SELF-CONSISTENCY across the three rephrasings, not counting accuracy - a model that
answers (5, 5, 5) is consistent (good on the rephrase-fragility dimension, even if
incorrect on the count). A model that answers (4, 8, 4) is INCONSISTENT (the failure
mode the eval exists to catch - the colloquial Q2 framing tempted the wrong scope).

If Opus is more rephrase-invariant than Sonnet/Haiku across 5 runs, that is a usable
routing edge - prompt-robust agents are worth the cost on tasks where the request
phrasing is unpredictable (the eval author's own prompts vary in formality). If all three
families produce (4, 4, 4) at N=5, the rephrase-fragility hypothesis is falsified for
simple counting tasks - also useful. The per-family metrics are rephrase-consistency
rate (primary), answer-correctness rate (secondary), drift pattern (which section
diverges when inconsistent), and CONSISTENCY-CHECK accuracy (does the model's own
self-report match reality).

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. Consistency
is the load-bearing metric; Correctness is secondary (answer should be 4); Completeness
is structural (all four sections present); Hallucination is hard-fail (inventing deploy
ids, inventing columns, or falsely claiming consistency in the CONSISTENCY CHECK
section when the actual numbers diverge). Voice match does not apply. The corpus is the
directory `corpus/self-consistency-under-rephrase/`.
