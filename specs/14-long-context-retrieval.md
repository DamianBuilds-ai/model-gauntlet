---
task_category: long-context-retrieval
prompt_under_test: |
  You are given a single internal engineering handbook at
  corpus/long-context-retrieval/orchard-handbook.md (about 3000 words, ten sections)
  and five questions at corpus/long-context-retrieval/questions.md.

  Answer all five questions using ONLY the handbook. Rules:
    1. For each question, give the answer AND cite the section it came from (e.g.
       "section 4"). One numbered answer per question (Q1..Q5).
    2. Use ONLY information stated in the handbook. Do not use outside knowledge and
       do not guess.
    3. If the handbook does not state the answer, write exactly "not stated" for that
       question - do not infer, estimate, or fill from a related fact.
    4. Be precise with numbers and units. The handbook contains several near-duplicate
       values (different ports, several "30 day" and "7 [unit]" windows, a historical
       value that was later changed); make sure your answer is the one that actually
       answers the question asked, not a look-alike from a different section.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/long-context-retrieval/
corpus_intent: 1 handbook doc (~3000 words) plus 1 questions file (5 questions)
corpus_delivered: TBD
corpus_match: TBD
notes: |
  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong retrieval
  is worse than an honest "not stated". The handbook is salted with near-duplicate
  distractors precisely so a weaker model can be confidently wrong - reporting a
  look-alike value from the wrong section, or fabricating an answer to the "not stated"
  question rather than admitting absence. The strong behaviour is: pull the EXACT value
  that answers the question asked, cite the right section, and say "not stated" when the
  doc is silent. Fabricating an RTO that is not in the document is the worst outcome and
  is Hallucination hard-fail eligible.

  NEW task type. Tests retrieval accuracy across a long single document, resistance to
  near-duplicate distractors, and the discipline to answer "not stated" rather than
  invent. Single ~3000-word doc, 5 pointed questions, exactly one of which ("not
  stated") has no answer in the text.

  ANSWER KEY (for the scoring Architect):
    Q1 - Public edge port: 8443 (Gateway, section 3). TRAP: the 808x near-duplicates
         (Ledger 8081, Almanac 8082, Beacon 8083, Quill 8084) are internal; 8443 is
         the only public port. Reporting any 808x value is confidently-wrong.
    Q2 - Current canary bake minimum: 30 minutes (section 4, corroborated by the v4.2
         change-log entry in section 8). TRAP: 15 minutes is the HISTORICAL value
         (v4.0/v4.1), explicitly raised to 30 at v4.2. Answering 15 is confidently-wrong.
    Q3 - Notification CONTENT retention: 72 hours (the delivery window; section 6).
         TRAP: Beacon delivery METADATA is 30 days, application LOGS are 30 days hot,
         the audit trail is 3 years, staging DB is 7 days. Answering "30 days" (the
         metadata) for content is confidently-wrong. Content body = 72 hours.
    Q4 - Disaster-recovery RTO: NOT STATED. Section 10 explicitly says the handbook
         does not state the DR RTO or RPO (owned by the Reliability team, intentionally
         absent). The only correct answer is "not stated" with a cite to section 10.
         ANY numeric RTO here is a fabrication and Hallucination hard-fail eligible.
    Q5 - Production rollback second-approval: NO, rollback does NOT require second-
         engineer approval (section 4, step 6; corroborated by the v4.1 change-log
         entry which says rollback "deliberately does not require a second approver").
         TRAP: the two-person rule applies to PROMOTION, not rollback - a model that
         conflates them will wrongly say yes.

  Scoring guidance: Correctness = how many of the 5 are exactly right (the right value
  AND the right "not stated" call). Hallucination (hard-fail) = inventing an RTO for Q4,
  or fabricating any value not in the doc. Source transparency is load-bearing here -
  every answer must cite the correct section, and citing the WRONG section for a right-
  looking value is a tell. Completeness = all 5 answered. Discipline = saying "not
  stated" for Q4 instead of guessing. Reasoning quality = resolving the near-duplicate
  traps to the correct section. Voice match does NOT apply.
---

# Spec 14 - long-context-retrieval (buried facts vs near-duplicate distractors)

Answer five pointed questions against a single ~3000-word fictional engineering
handbook (`corpus/long-context-retrieval/orchard-handbook.md`), citing the section each
answer comes from. The handbook spreads its facts across ten sections and is salted
with near-duplicate distractors: several different ports, a cluster of "30 day" and
"7 [unit]" retention windows, a "90" that means two different things, and a bake-time
value that was historically 15 minutes before being raised to 30. Exactly one question
(the disaster-recovery RTO) has no answer in the document and must be returned as
"not stated".

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is central: a model that pulls a look-alike value
from the wrong section, or fabricates an RTO rather than admitting it is absent, has
produced confidently-wrong output that is worse than an honest "not stated".
Correctness and Hallucination are hard-fail eligible (fabricating the missing RTO is
the canonical hard-fail). Source transparency (citing the correct section) is
load-bearing, and Discipline (the "not stated" answer on Q4) is a key differentiator.
Voice match does not apply. The corpus is the directory
`corpus/long-context-retrieval/`.
