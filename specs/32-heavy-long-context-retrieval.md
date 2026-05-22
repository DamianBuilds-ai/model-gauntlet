---
task_category: long-context-retrieval
prompt_under_test: |
  You are given a single internal operations reference manual at
  corpus/heavy-long-context-retrieval/northwind-operations-manual.md (about 8000
  words, 31 numbered sections) and eight questions at
  corpus/heavy-long-context-retrieval/questions.md.

  Answer all eight questions using ONLY the manual. Rules:
    1. For each question, give the answer AND cite the section number it came from
       (e.g. "Section 4"). One numbered answer per question (Q1..Q8).
    2. Use ONLY information stated in the manual. Do not use outside knowledge and do
       not guess.
    3. If the manual does not state the answer, write exactly "not stated" for that
       question - do not infer, estimate, or fill from a related fact. Cite the
       section that makes the absence explicit if there is one.
    4. Be precise with numbers and units. The manual is deliberately salted with
       near-duplicate values: several different ports, multiple "30 minute" and
       "30 day" and "72 hour" and "7 day" and "14 day" and "35 day" windows that mean
       different things, a historical value that was later changed, and several
       different "second approver" rules that apply to different actions. Make sure
       your answer is the one that actually answers the question asked, not a
       look-alike from a different section.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/heavy-long-context-retrieval/
corpus_intent: 1 long operations manual (~8000 words, 31 sections) plus 1 questions file (8 questions, one of which is "not stated")
corpus_delivered: TBD
corpus_match: TBD
notes: |
  HEAVY long-context-retrieval probe (the scaled-up sibling of spec 14). Where spec 14
  is a ~3000-word handbook with 5 questions, this is a ~8000-word, 31-section
  operations manual with 8 pointed questions. The document is long enough that the
  relevant needle for each question sits far from the others, and it is densely salted
  with near-duplicate distractors so that a model skimming or pattern-matching a value
  can be confidently wrong. Run the full 9-variant model-only pool (Haiku x3, Sonnet
  x3, Opus x3; effort treated as inert per the methodology). Aggregate the 3 passes per
  model (mean weighted total); flag any model whose 3 passes diverge by more than 0.5
  as a consistency finding.

  HEAVY NOTE. The manual at ~8000 words pushes the context window much harder than the
  spec-14 handbook. The discriminator is recall (find the right needle for every one of
  the 8 questions), precision (resist the many near-duplicate distractor values), and
  the discipline to answer "not stated" for the one question the manual explicitly does
  not answer. Numerically-similar distractor clusters are deliberately spread across
  distant sections: at least four different "30 minute" facts (the regional-failover
  RTO, the on-call out-of-hours work threshold, the status-page initial-update window,
  the scale-down sustained window is "15 minutes" nearby), several "72 hour" facts
  (notification content retention, routine-maintenance notice period), several "7 day"
  facts (trace retention, staging-data retention, disruptive-maintenance notice), and
  several "second approver" rules (the two-person promotion rule, the just-in-time
  access approval, the escalation manager) - each attached to a different action.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong
  retrieval is worse than an honest "not stated". The manual is salted precisely so a
  weaker model can be confidently wrong - reporting a look-alike value from the wrong
  section (a historical value, a numerically-similar value attached to a different
  concept), or fabricating an answer to the "not stated" question rather than admitting
  absence. The strong behaviour is: pull the EXACT value that answers the question
  asked, cite the right section, and say "not stated" when the manual is silent.
  Fabricating a Priority transit-days figure that the manual explicitly defers to
  Commerce is the worst outcome and is Hallucination hard-fail eligible.

  ANSWER KEY (for the scoring Architect). Every answer is grep-verifiable against the
  manual. There are 8 questions; exactly one (Q6) is "not stated".

    Q1 - Single public edge port: 8443 (Section 2). The Gateway terminates TLS on
         8443 and it is the only public port. TRAPS: the internal service ports
         7001-7006 (the 700x range), the internal admin console port 7000, and the
         shared internal metrics port 9100 are all internal-only. Reporting any of
         700x, 7000, or 9100 as the public port is confidently-wrong.

    Q2 - Current minimum canary bake: 45 minutes (Section 4, corroborated by Section
         14 incident narrative and the Section 19/30 glossary). TRAP: 20 minutes is
         the HISTORICAL value (revisions 7.x/8.x), explicitly raised to 45 minutes in
         revision 9.0 after the March incident. Answering 20 minutes is
         confidently-wrong. (Also nearby: the 10-minute soak between production waves -
         not the bake.)

    Q3 - Notification CONTENT retention: 72 hours (Section 6; restated in Section 18).
         TRAP: notification delivery METADATA is 90 days, application LOGS are 30 days
         hot, traces 7 days, staging data 7 days, metrics 15 days, audit trail 3 years,
         booking records 7 years. Answering "90 days" (the metadata) for content is the
         canonical confidently-wrong answer. The content body is 72 hours.

    Q4 - Just-in-time grant max validity for the production DATABASE: 2 hours (Section
         7). TRAP: the GENERAL just-in-time production grant is 8 hours; the database
         grant is capped tighter at 2 hours. Answering 8 hours conflates the general
         grant with the database-specific one and is confidently-wrong. (Also nearby
         distractors: service certificates valid 24 hours, customer JWT 60 minutes,
         refresh token 30 days.)

    Q5 - Regional failover target RTO: 30 minutes (Section 13; corroborated in Sections
         17 and 21). TRAP: the COLD full-cluster restore from backup targets 4 hours
         (Section 17) - a different recovery operation. The regional failover promotes a
         warm standby in 30 minutes. Answering 4 hours conflates the cold restore with
         the warm failover and is confidently-wrong. (The RPO is 60 seconds - that is
         the recovery POINT objective, not the RTO; answering 60 seconds for the RTO is
         also wrong.)

    Q6 - Priority service-level committed transit days: NOT STATED. Section 26
         explicitly says "the specific committed transit days per service level are not
         stated in this manual" (deferred to Commerce as commercial terms). The only
         correct answer is "not stated" with a cite to Section 26. ANY numeric
         transit-days figure here is a fabrication and Hallucination hard-fail eligible.

    Q7 - Circuit-breaker trip threshold: error rate exceeding 50 percent over the last
         20 calls (Section 20). TRAPS: the autoscaler scale-up trigger is 60 percent
         CPU and scale-down is 40 percent (Section 9); the Tracker ingest cap is 50,000
         events per second (Section 3); the availability SLOs are 99.x percent (Section
         5); the rate limit is 600 requests per minute (Section 19). Answering "60
         percent" (the CPU autoscale trigger) or any availability percentage for the
         circuit-breaker trip is confidently-wrong. The full correct answer names both
         the 50-percent error rate AND the 20-call window.

    Q8 - Production rollback second-approval: NO, a rollback does NOT require a second
         engineer; a single on-call engineer can execute it (Section 4, corroborated by
         Section 11). TRAP: the two-person promotion rule (release owner + second
         approver) applies to canary-to-PRODUCTION PROMOTION, not to rollback; Section 4
         explicitly says "do not conflate the two-person promotion rule with rollback;
         rollback is single-approver by design." A model that conflates promotion with
         rollback will wrongly say yes. (Also nearby: just-in-time access needs a second
         engineer's approval, and an emergency deploy during a freeze needs a Director -
         neither is the rollback rule.)

  Scoring guidance:
    - Correctness (hard-fail eligible) = how many of the 8 are exactly right (the right
      value AND the right "not stated" call on Q6). A run that reports a near-duplicate
      look-alike for several questions, or invents a Priority transit-days figure for
      Q6, fails Correctness.
    - Hallucination (hard-fail eligible) = inventing a transit-days figure for Q6, or
      fabricating any value not in the manual. Q6 is the canonical hallucination trap.
    - Completeness (weight 2.0) = all 8 questions answered (recall). A skipped question
      is an incompleteness, distinct from a wrong answer.
    - Source transparency (applies to all tasks) is load-bearing here - every answer
      must cite the correct section, and citing the WRONG section for a right-looking
      value is a tell that the model matched a distractor. Penalise right-value /
      wrong-section and wrong-value / confident-section.
    - Discipline (decision/judgment) = saying "not stated" for Q6 instead of guessing,
      and resisting the urge to pad an answer with a related-but-wrong fact.
    - Reasoning quality = resolving each near-duplicate cluster to the correct section
      (the 30-minute cluster for Q5, the 72-hour/90-day cluster for Q3, the
      8-hour/2-hour cluster for Q4, the 50%/60% cluster for Q7, the promotion-vs-rollback
      distinction for Q8, the 20-vs-45-minute history for Q2). This is where a model
      that genuinely read the whole manual separates from one that pattern-matched.
    - Format adherence = the output envelope plus eight cleanly numbered answers each
      with a section citation.
    Recall (all 8 found) and precision (the right needle, not a look-alike) are the
    scored discriminators. Voice match does NOT apply.

    Suggested scoring shorthand for the Architect: correctness = (questions exactly
    right) / 8, where Q6 is correct only if answered "not stated". A run that gets all 8
    exactly right with correct section citations is the exemplary 5 on Correctness and
    Source transparency; pulling a near-duplicate distractor value, citing the wrong
    section, or fabricating the Q6 figure is where the score falls.
---

# Spec 32 - heavy-long-context-retrieval (buried needles vs near-duplicate distractors, at scale)

The heavy, scaled-up sibling of spec 14 (long-context-retrieval). Where spec 14 answers
five questions against a ~3000-word handbook, this answers EIGHT pointed questions
against a single ~8000-word, 31-section fictional operations manual for a fictional
logistics platform ("Northwind") under `corpus/heavy-long-context-retrieval/`. The
manual spreads its facts across 31 sections and is densely salted with near-duplicate
distractors: several internal ports plus one public port, multiple "30 minute" facts
(failover RTO, on-call work threshold, status-page update window), multiple "72 hour"
and "7 day" and "14 day" and "35 day" windows attached to different concepts, a canary
bake value that was historically 20 minutes before being raised to 45, and several
distinct "second approver" rules each governing a different action. Exactly one question
(Q6, the Priority service-level transit days) has no answer in the manual - it is
explicitly deferred to Commerce - and must be returned as "not stated".

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is central: a model that pulls a look-alike value
from the wrong section (a historical value, or a numerically-similar value attached to a
different concept), or fabricates a transit-days figure rather than admitting the manual
is silent, has produced confidently-wrong output that is worse than an honest "not
stated". Correctness and Hallucination are hard-fail eligible (fabricating the missing
Q6 figure is the canonical hard-fail). Source transparency (citing the correct section)
is load-bearing - right-value / wrong-section is a tell - and Discipline (the "not
stated" answer on Q6) is a key differentiator. Reasoning quality captures whether the
model resolved each near-duplicate cluster to the correct section rather than
pattern-matching the first matching number. Voice match does not apply. The variant pool
is 9 (3 models x N=3, effort inert per the methodology). The corpus is the directory
`corpus/heavy-long-context-retrieval/`.
