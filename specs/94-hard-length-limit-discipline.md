---
task_category: hard-length-limit-discipline
prompt_under_test: |
  You are given a single source file at
  corpus/hard-length-limit-discipline/outage-report.md - a long Q1 reliability narrative
  for a fictional cloud provider, with six incidents, four headline metrics, and three
  Q2 priorities.

  Write an executive blurb summarising the quarter. The reader is a busy executive who
  will read ONLY this blurb.

  HARD LENGTH LIMIT: the blurb must be 60 words OR FEWER. This is a hard ceiling, not a
  target - 61 words is a failure. Count words (whitespace-separated tokens) in the blurb
  body only.

  Within that ceiling, the blurb must still convey ALL of:
    - the availability verdict (did the quarter hit or miss the availability target),
    - the mean-time-to-recovery direction (improved or worsened),
    - the customer-impacting-incident-count direction (up or down),
    - all THREE Q2 priorities.

  So you must be both UNDER the limit and COMPLETE. Output the blurb only. After it,
  append the output envelope (schemaVersion, tier, status, tool_budget_used) as separate
  lines OUTSIDE and not counted toward the word limit. No em dashes. No emojis.
variant_pool: 9
corpus: corpus/hard-length-limit-discipline/
corpus_intent: |
  One source file (corpus/hard-length-limit-discipline/outage-report.md): a deliberately
  long, detail-rich Q1 reliability narrative - six incidents each with a root cause, four
  headline metrics, three Q2 priorities, plus prose. The task asks for an executive blurb
  of 60 words or fewer that STILL conveys four required facts plus all three priorities.
  This is the eval-15 hard-constraint probe at a new task: the source has SO much material
  that the natural, helpful summary blows past 60 words, and a model that tries to honour
  everything tends to overrun. The discipline test is staying strictly under the ceiling
  WHILE keeping all required content - the two pulls fight each other.

  THE TENSION (why it discriminates): there is far more than 60 words of "summarisable"
  material (six incidents alone). A disciplined model RUTHLESSLY drops the six incident
  details and the exact metric numbers, keeping only the four required directional facts
  and the three priorities, and lands under 60 words. An undisciplined model either (a)
  overruns the ceiling trying to include incident detail, or (b) stays short by dropping a
  required item (e.g. omits one of the three Q2 priorities, or omits the MTTR direction).

  REQUIRED CONTENT (positive answer key - all must be present, even compressed):
    - Availability MISSED the target (99.94% vs 99.95% target) - "narrowly missed target"
      or equivalent. Direction = miss.
    - MTTR IMPROVED (21 min, down from 34) - "recovery time improved" / "faster recovery".
    - Incident count REGRESSED / went UP (6, up from 4) - "more incidents" / "incidents up".
    - All THREE Q2 priorities: (1) multi-provider DNS, (2) migration lock-timeouts,
      (3) certificate renewal/expiry alarms.

  THE CEILING (negative answer key): the blurb body is 60 words or fewer. 61+ = a hard
  FAIL regardless of how complete or polished it is.

  QUALITY PRINCIPLE (both-or-fail): the eval rewards the model that is simultaneously
  UNDER the limit AND complete. Being under-limit by dropping a required item is an
  incompleteness fail; being complete by overrunning is a length fail. Neither half alone
  passes. The right move is aggressive compression of the optional detail (incidents,
  exact numbers) to make room for the seven required signals (4 facts + 3 priorities) under
  60 words. (A tight target is achievable: e.g. "Availability narrowly missed target;
  recovery time improved but incident count rose. Q2 priorities: multi-provider DNS,
  migration lock-timeouts, and certificate-expiry alarms." is well under 60 words and
  complete.)

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - LENGTH FAIL TRIGGER: word count of the blurb body (whitespace-split tokens, envelope
      excluded) > 60. This is the load-bearing negative invariant - count it directly.
    - COMPLETENESS: the blurb conveys availability-miss, MTTR-improved, incidents-up, and
      all three priorities. Each missing required item = an incompleteness deduction; a
      dropped Q2 priority is the most common one to check.
    - No incident-by-incident enumeration (a model listing all six incidents will overrun -
      its presence is a strong signal of length failure).

  Scoring guidance:
    - Discipline (hard-fail eligible, LOAD-BEARING) = blurb body <= 60 words. 61+ = a hard
      FAIL. This is the headline discriminator.
    - Completeness (hard-fail eligible) = all four directional facts + all three priorities
      present. Dropping a required item to stay short = Completeness 1.
    - Correctness = the directions stated are right (miss not hit, improved not worsened,
      up not down) and priorities match the source.
    - Hallucination (hard-fail eligible) = inventing a metric direction, a priority, or a
      number not in the source.
    - Format adherence = blurb only, envelope outside and uncounted, no em dashes/emojis.
    - Reasoning quality = SKIP-eligible. Voice match does NOT apply.
notes: |
  NEW output-discipline eval (Chat D battery, 91-96). Probes hard-length-limit discipline -
  the eval-15 hard-constraint probe at a fresh task. The corpus is a deliberately overloaded
  reliability narrative (six incidents with root causes, four metrics, three priorities), and
  the task demands a 60-word-or-fewer executive blurb that STILL carries four directional
  facts plus all three Q2 priorities. The two constraints fight: there is far more than 60
  words of material, so a helpful instinct overruns, while a model that stays short by
  dropping a required priority fails completeness. Success is being under the ceiling AND
  complete simultaneously, achieved by ruthlessly cutting the incident detail.

  The load-bearing discriminator is a direct word count of the blurb body: 61+ words is a
  hard FAIL. Completeness (four facts + three priorities) is also hard-fail eligible, as is
  Hallucination. The answer key in corpus_intent gives the required directional facts, the
  three priorities, the ceiling, and a worked sub-60-word example proving the constraint is
  satisfiable. Reasoning is skip-eligible; voice does not apply. Standard four-phase
  /eval-pit flow against the frozen rubric/rubric.md. The variant pool is 9 (3 models x N=3,
  effort inert per the methodology). The corpus is the directory
  corpus/hard-length-limit-discipline/.
---

# Spec 94 - hard-length-limit-discipline

Summarise a long, detail-heavy quarterly reliability report into an executive blurb of
60 words or fewer that STILL conveys four required directional facts and all three Q2
priorities. This is the eval-15 hard-constraint probe at a fresh task. The two
constraints fight each other: the source
(`corpus/hard-length-limit-discipline/outage-report.md`) carries far more than 60 words
of summarisable material - six incidents each with a root cause, four metrics, three
priorities - so the helpful instinct to include detail blows past the ceiling, while a
model that stays short by dropping a required priority fails completeness.

This is a hard-length-limit discipline probe. The success state threads both pulls:
ruthlessly drop the optional detail (the six incidents, the exact metric numbers) to
make room, under 60 words, for the seven required signals - availability missed target,
recovery time improved, incident count rose, and the three Q2 priorities (multi-provider
DNS, migration lock-timeouts, certificate-expiry alarms). A worked sub-60-word example in
`corpus_intent` proves the constraint is satisfiable.

The load-bearing discriminator is a direct word count of the blurb body: 61+ words is a
hard FAIL no matter how complete or polished. Completeness (the four facts plus all three
priorities) is also hard-fail eligible - staying short by dropping a required item fails
too - as is Hallucination. The answer key in `corpus_intent` gives the required
directional facts, the three priorities, and the ceiling for the scoring Architect.
Reasoning is skip-eligible; voice does not apply. Standard four-phase `/eval-pit` flow
against the frozen `rubric/rubric.md`. The variant pool is 9 (3 models x N=3, effort
inert per the methodology). The corpus is the directory
`corpus/hard-length-limit-discipline/`.
