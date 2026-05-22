---
task_category: long-context-retrieval
prompt_under_test: |
  You are given a single internal operations and policy manual at
  corpus/long-context-needle-consistency/cardinal-operations-manual.md (about
  64000 words, 60 numbered sections) and eight questions at
  corpus/long-context-needle-consistency/questions.md.

  Answer all eight questions using ONLY the manual. Rules:
    1. For each question, give the answer AND cite the section number it came from
       (e.g. "Section 41"). One numbered answer per question (Q1..Q8).
    2. Use ONLY information stated in the manual. Do not use outside knowledge and
       do not guess.
    3. If the manual does not state the answer, write exactly "not stated" for that
       question - do not infer, estimate, or fill from a related fact. Cite the
       section that makes the absence explicit if there is one.
    4. Be precise with numbers and units. The manual is deliberately salted with
       near-duplicate values: several different recovery windows measured in hours
       that mean different things, multiple grant windows that share a number, a
       canary value that was changed across revisions, and one recovery target that
       is restated with a SUPERSEDED historical figure in a later section. Make sure
       your answer is the one that actually answers the question asked, not a
       look-alike from a different section and not a historical value that the
       manual marks as superseded.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/long-context-needle-consistency/
corpus_intent: 1 long operations manual (~64000 words, 60 sections) plus 1 questions file (8 questions, one "not stated"). variant_pool 15 = 5 runs per model (Haiku x5, Sonnet x5, Opus x5). The HEADLINE metric is WITHIN-FAMILY SPREAD across the 5 runs, not the mean - the question is whether a family lands the one deeply buried needle (Q7, the cold archive Tier 3 restore at 26 hours) on EVERY run or only on some runs.
corpus_delivered: TBD
corpus_match: TBD
notes: |
  HEAVY long-context-needle CONSISTENCY probe. This is the variance battery sibling
  of spec 32. Where spec 32 runs N=3 per model and reports the mean, this runs N=5
  per model (variant_pool: 15 - Haiku x5, Sonnet x5, Opus x5; effort treated as
  inert per the methodology) and the SCORED HEADLINE is the WITHIN-FAMILY SPREAD:
  does a model family land the deeply buried needle on all five runs, or does it hit
  the peak on some runs and drop it on others. A family that scores 5/5 on the
  buried item is the consistency winner; a family that scores 4/5 or 3/5 on the same
  item - hitting the same ceiling but gambling on the floor - is the loser even if
  its single best run matches.

  THE BURIED ITEM (the separator). Seven of the eight questions are answerable from a
  reasonable read. Q7 asks for the committed target window for the full COLD ARCHIVE
  restore (the Tier 3 restore). The answer, 26 hours, lives in Section 41 - deep in
  the document, far from any question keyword - and it sits inside a dense cluster of
  other recovery windows that are all measured in hours and all attached to DIFFERENT
  operations (warm regional failover 30 minutes, hot store rebuild 2 hours, full
  cluster cold restore 4 hours, warm store rebuild 6 hours). Worse, Section 58
  ("Historical Recovery Notes") silently restates a SUPERSEDED revision-8 value of 18
  hours for the same cold archive restore, explicitly flagged as historical and
  superseded by Section 41 - but a model that skims and pattern-matches the phrase
  "cold archive restore target was 18 hours" in Section 58 reports 18 hours. The
  consistency separator is whether a family reads to Section 41, resolves the
  hour-cluster, ignores the Section-58 historical restatement, and reports 26 hours
  on EVERY one of its five runs.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong
  retrieval is worse than an honest "not stated". The manual is salted precisely so a
  weaker model can be confidently wrong - reporting a look-alike hour-value from the
  wrong recovery operation, reporting the superseded 18 hour historical figure for
  Q7, or fabricating a transit-days figure for Q6 rather than admitting the manual is
  silent. The strong behaviour is: pull the EXACT value that answers the question
  asked, cite the section that OWNS the topic (not the glossary cross reference and
  not the historical notes), and say "not stated" when the manual is silent.

  ANSWER KEY (for the scoring Architect). Every answer is grep-verifiable against the
  manual. There are 8 questions; exactly one (Q6) is "not stated".

    Q1 - Single public ingress port: 8443 (Section 2). The gateway terminates TLS on
         8443 and it is the only public port. TRAPS: the internal service ports
         7101-7106, the internal admin console port 7100, and the shared internal
         metrics port 9100 are all internal-only. Reporting any of those as the public
         port is confidently-wrong.

    Q2 - Current minimum canary bake: 45 minutes (Section 12, corroborated by the
         Section 14 incident narrative and the Section 19 glossary). TRAP: 20 minutes
         is the HISTORICAL value (revision 7 series), explicitly raised to 45 minutes
         in revision 9.0. Answering 20 minutes is confidently-wrong. (Also nearby: the
         10 minute soak between production waves - not the bake.)

    Q3 - Notification CONTENT retention: 72 hours (Section 6; restated in Section 18).
         TRAP: delivery METADATA is 90 days. Answering 90 days for the content body is
         the canonical confidently-wrong answer. The content body is 72 hours.

    Q4 - Just-in-time grant max validity for the production DATABASE: 2 hours (Section
         7). TRAPS: the GENERAL production grant is 8 hours and the CUSTOMS grant is 1
         hour. Answering 8 hours conflates the general grant with the database-specific
         one and is confidently-wrong. (Note Section 28 also mentions a 2 hour HOT
         STORE REBUILD that shares the number but is an unrelated control - it is the
         right number for Q4 but for the wrong stated reason if cited from Section 28.)

    Q5 - Warm regional failover target RTO: 30 minutes (Section 13; corroborated in
         Sections 19 and 21). TRAPS: the full cluster COLD restore targets 4 hours
         (Section 17) and the recovery POINT objective is 60 seconds (Section 13).
         Answering 4 hours or 60 seconds is confidently-wrong.

    Q6 - Standard commercial service level committed transit days: NOT STATED. Section
         26 explicitly says the committed transit days are commercial terms and are
         "not stated in this operations manual" (deferred to the commercial team). The
         only correct answer is "not stated" with a cite to Section 26. ANY numeric
         transit-days figure here is a fabrication and Hallucination hard-fail eligible.

    Q7 - Cold archive (Tier 3) restore committed target: 26 hours (Section 41). THIS IS
         THE BURIED SEPARATOR. Section 41 commits the cold archive restore to 26 hours
         and explicitly states it supersedes all earlier figures. TRAP-HISTORICAL:
         Section 58 restates the SUPERSEDED revision-8 value of 18 hours for the same
         operation, flagged as historical. Answering 18 hours is the canonical
         confidently-wrong skim error. TRAP-CLUSTER: the warm failover (30 minutes),
         hot store rebuild (2 hours), full cluster cold restore (4 hours), and warm
         store rebuild (6 hours) are all nearby and all WRONG for Q7. The full correct
         answer is 26 hours cited to Section 41. Citing Section 58's 18 hours, or any
         of the cluster values, is the run that drops the needle.

    Q8 - Production rollback second-approval: NO, a rollback does NOT require a second
         approver; a single on-call engineer can execute it (Section 23). TRAP: the
         two-person promotion rule (release owner + second approver) applies to a
         customer-facing CHANGE, not to a rollback; Section 23 explicitly says do not
         conflate the two-person promotion rule with the single-approver rollback rule.
         A model that conflates them will wrongly say yes.

  Scoring guidance:
    - The HEADLINE is WITHIN-FAMILY SPREAD on Q7. For each model family, record how
      many of the 5 runs got Q7 exactly right (26 hours, Section 41). 5/5 is the
      consistency exemplar; 4/5 or worse on Q7 is a consistency miss even if the best
      run is perfect. Report the per-family Q7 hit rate as the lead finding, then the
      per-family hit rate on the other near-duplicate items (Q2 history, Q4 grant
      cluster, Q5 failover-vs-restore), then the mean weighted total.
    - Correctness (hard-fail eligible) = how many of the 8 are exactly right per run
      (the right value AND the right "not stated" call on Q6). A run that reports the
      superseded 18 hour figure for Q7, or invents a transit-days figure for Q6, fails
      Correctness for that run.
    - Hallucination (hard-fail eligible) = inventing a transit-days figure for Q6, or
      fabricating any value not in the manual. Q6 is the canonical hallucination trap.
    - Completeness (weight 2.0) = all 8 questions answered (recall). A skipped question
      is an incompleteness, distinct from a wrong answer.
    - Source transparency (applies to all tasks) is load-bearing - citing Section 58
      (historical notes) or Section 19 (glossary) for Q7 instead of Section 41 (the
      owning section) is a tell that the model matched a restatement rather than the
      authoritative value. Penalise right-value / wrong-section and the superseded
      18 hour value cited confidently to Section 58.
    - Discipline (decision/judgment) = saying "not stated" for Q6 instead of guessing,
      and reporting the current owning-section value for Q7 rather than the historical
      restatement.
    - Reasoning quality = resolving the hour-cluster to the correct operation (the
      26 hour cold archive vs the 4 hour cold restore vs the 6 hour warm rebuild vs the
      2 hour hot rebuild) and the 18-vs-26-hour current-vs-historical distinction. This
      is where a model that genuinely read to Section 41 separates from one that
      pattern-matched the first "cold archive ... hours" string it found.
    - Format adherence = the output envelope plus eight cleanly numbered answers each
      with a section citation.
    Within-family SPREAD on the buried Q7 needle is THE scored discriminator. Voice
    match does NOT apply.

    Suggested scoring shorthand for the Architect: for each family compute the Q7 hit
    rate over 5 runs (correct = "26 hours" cited to Section 41). A family at 5/5 on Q7
    with correct citations is the consistency exemplar; a family that hits 26 hours on
    its best run but reports 18 hours (or a cluster value) on one or more of its five
    runs is the consistency loser even at an identical peak.
---

# Spec 40 - long-context-needle-consistency (within-family spread on a deeply buried needle)

The variance-battery sibling of spec 32. Where spec 32 answers eight questions
against an ~8000-word manual at N=3 per model and reports the mean, this answers
eight questions against a single ~64000-word, 60-section fictional operations
manual for a fictional logistics platform ("Cardinal Freight Systems") under
`corpus/long-context-needle-consistency/`, at N=5 per model (variant_pool: 15 -
Haiku x5, Sonnet x5, Opus x5; effort inert per the methodology). The corpus is
large enough (60000+ tokens) that the relevant needle for each question sits far
from the others, and it is densely salted with near-duplicate distractors.

The HEADLINE metric is WITHIN-FAMILY SPREAD, not the mean. Seven of the eight
questions are answerable from a careful read. The eighth, Q7, asks for the
committed target window of the full cold archive (Tier 3) restore - the answer,
26 hours, lives in Section 41, deep in the document, inside a dense cluster of
other recovery windows all measured in hours and all attached to different
operations (warm failover 30 minutes, hot store rebuild 2 hours, full cluster
cold restore 4 hours, warm store rebuild 6 hours). Section 58 silently restates a
SUPERSEDED revision-8 value of 18 hours for the same operation, flagged as
historical. The consistency separator is whether a model family reads to Section
41, resolves the hour-cluster, ignores the Section-58 historical restatement, and
reports 26 hours on EVERY one of its five runs - or hits 26 hours on its best run
while dropping to the superseded 18 hour figure (or a cluster look-alike) on one
or more of the other four. Exactly one question (Q6, the commercial transit days)
has no answer in the manual and must be returned as "not stated".

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`, with
the within-family spread reported as the lead finding. The correctness-first
quality principle is central: a model that pulls the superseded 18 hour figure
for Q7, or fabricates a transit-days figure for Q6, has produced confidently-wrong
output that is worse than an honest miss. Correctness and Hallucination are
hard-fail eligible. Source transparency (citing Section 41, the owning section,
not Section 58's historical notes or Section 19's glossary) is load-bearing.
Reasoning quality captures whether the model resolved the hour-cluster and the
current-vs-historical distinction rather than pattern-matching the first matching
string. Voice match does not apply. The variant pool is 15 (3 models x N=5, effort
inert per the methodology). The corpus is the directory
`corpus/long-context-needle-consistency/`.
