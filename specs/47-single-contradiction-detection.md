---
task_category: single-contradiction-detection
prompt_under_test: |
  You are auditing the internal employee and operations handbook of a fictional
  company, "Globex Logistics". The handbook is split across the fourteen markdown
  files in corpus/single-contradiction-detection/handbook/ (01 through 14). Read
  all of them.

  The handbook is meant to be internally consistent: a fact stated in one file
  should agree with the same fact stated elsewhere. Somewhere in these documents,
  exactly ONE genuine contradiction has crept in - two statements that refer to
  the SAME underlying fact but give DIFFERENT, incompatible values.

  Find that one contradiction.

    1. State on the FIRST line which fact is contradicted (a short label, for
       example: "audit log retention period").
    2. Quote BOTH conflicting statements. For each, cite the file (and the section
       or line if you can) and give the value it states.
    3. Explain in one sentence why the two are a genuine contradiction (they refer
       to the same thing yet disagree), not merely two different numbers about two
       different things.

  Rules:
    - There is exactly ONE genuine contradiction. Report THAT one.
    - The handbook contains MANY numbers, durations, dates, and named values.
      Most numbers that differ from each other do so legitimately because they
      describe DIFFERENT things (different data types, different policies,
      different teams, different thresholds). Two different numbers are NOT a
      contradiction unless they describe the SAME fact. Reporting a pair of
      legitimately-different numbers as "a contradiction" is a precision error and
      counts against you.
    - A confidently-wrong contradiction claim (pointing at a non-conflict) is
      WORSE than failing to find the real one, because an auditor acts on your
      finding and will "fix" a document that was correct, introducing a real error.
    - Do not invent a contradiction that is not in the text. If two statements
      genuinely agree, they are not a contradiction.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/single-contradiction-detection/
corpus_intent: |
  HEAVY consistency / variance battery (5 runs per model = 15-variant pool,
  model-only, effort inert per the methodology). The headline scored signal is
  WITHIN-FAMILY SPREAD: does a model find the one buried contradiction on EVERY one
  of its 5 runs, or only on some. Run-to-run reliability on a single buried
  needle - not a per-run ceiling - is the separator. The hypothesis (carried from
  the batch-3 consistency read): the stronger model surfaces the lone
  same-fact/different-value pair across all 5 runs while a cheaper model finds it
  on its best run but on floor runs either misses it or reports a legitimately
  -different number pair as a false contradiction. Aggregate per model as mean
  weighted total across the 5 runs AND report the spread (max minus min) plus the
  hit-rate (of 5 runs, how many correctly identified the audit-log retention
  contradiction with zero false contradictions). Flag any model whose 5 runs
  diverge by more than 0.5 weighted total, or whose hit-rate is below 5/5, as the
  consistency finding. Corpus: a 14-document internal handbook for the fictional
  "Globex Logistics" (15 files including the README). All facts are mutually
  consistent except ONE planted same-fact contradiction; several
  legitimately-different numbers are planted as precision decoys.
corpus_delivered: TBD
corpus_match: TBD
notes: |
  HEAVY SINGLE-CONTRADICTION-DETECTION PROBE (find-the-one-needle consistency).
  Many mutually consistent documents with exactly ONE subtle buried contradiction.
  On a good run, any model can spot a glaring conflict; the hypothesis is that as
  the conflicting fact is the SAME value stated consistently in three places and
  contradicted in just ONE buried spot, surrounded by many legitimately-different
  numbers that are NOT conflicts, the cheaper models become INCONSISTENT - finding
  the real contradiction on some of their 5 runs and on others either missing it or
  flagging a non-conflict (two different numbers about two different things). The
  5-runs-per-model design measures that run-to-run spread directly. Run the full
  15-variant model-only pool (Haiku x5, Sonnet x5, Opus x5; effort treated as
  inert). Within-family SPREAD is the scored headline.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong
  "contradiction" is worse than a miss. A model that reports the customer-order
  retention (24 months) versus the audit-log retention (90 days) as a
  contradiction has flagged two values that describe DIFFERENT data types - an
  auditor acting on that would wrongly "align" two correct, unrelated numbers and
  inject a real error. Reward exact identification of the ONE real same-fact
  contradiction AND clean precision (no false contradictions on the decoys).
  Penalise the false contradiction hardest.

  ANSWER KEY (for the scoring Architect). Verified by grep across the corpus; the
  contradiction was planted deliberately and is the only same-fact disagreement in
  the handbook.

  THE ONE TRUE CONTRADICTION (the buried needle every run must find):
    - Fact: the AUDIT LOG retention period (how long audit logs are kept in the
      central log platform before being purged).
    - Statement A (the outlier): 06-security-policy.md, "Logging and audit trails"
      section - "Audit logs are retained for 180 days in the central log platform
      before being purged."
    - Statement B (the consistent value, stated in THREE places): audit logs are
      retained for 90 days.
        - 07-data-handling.md, "Audit logs" section - "retained for 90 days, after
          which they are automatically purged. This 90-day window is the standard
          log retention period referenced throughout operations and incident
          response."
        - 08-incident-response.md, "Investigation and evidence" section - "Because
          audit logs are retained for 90 days ... the standard 90-day purge."
        - 14-glossary.md, "Audit log" entry - "Standard retention is 90 days."
    - Why it is a genuine contradiction: all four statements describe the SAME
      artifact (audit logs in the central log platform: authentication events,
      privileged actions, data access) and the SAME attribute (retention period
      before purge), yet 06-security-policy.md says 180 days while the other three
      say 90 days. 90 and 180 cannot both be the retention period for the same
      logs. Accept the answer as correct if it names the audit-log retention period
      and quotes the 180-vs-90 pair, citing 06-security-policy.md against any one
      (or more) of 07 / 08 / 14. The strongest answers note that 90 is corroborated
      in three places and 180 is the lone outlier.

  PRECISION DECOYS (legitimately-different numbers that are NOT contradictions -
  reporting any of these as the contradiction is a confidently-wrong false
  positive and the heaviest penalty):
    DECOY-1. Customer ORDER record retention = 24 months (07-data-handling.md,
        "Storage and encryption"). This is a DIFFERENT data type (Restricted
        customer order records) from audit logs. 24 months vs 90 days is not a
        conflict - different data, different policy. The closest-looking trap
        because both are "retention" numbers.
    DECOY-2. Session token expiry = 30 days of inactivity (06-security-policy.md,
        "Authentication"; restated in 14-glossary.md). Both mentions AGREE (both 30
        days), so this is consistent, not a contradiction. A model that reports the
        session-token figure as conflicting has misread - the two mentions match.
    DECOY-3. Dormant account auto-disable = 45 days with no sign-in
        (06-security-policy.md, "Access control"). A different control entirely
        (account dormancy, not log retention). Not a conflict with anything.
    DECOY-4. Probation = 3 months and post-probation notice = 4 weeks
        (02-employment-basics.md). Different durations for different things
        (probation length vs notice period); not a contradiction.
    DECOY-5. Annual leave carryover cap = 10 days and annual leave accrual = 20
        days/year (03-leave-policy.md). Two different leave numbers, both correct;
        not a conflict. Also note: data-subject-request, expense-claim,
        service-credit, and incident-status windows are all "30 days" or "30
        minutes" in various files - these AGREE where they overlap and describe
        different processes where they differ; none is a contradiction.

  Scoring guidance:
    - Correctness (hard-fail eligible, weight 3.0) = did the run identify the ONE
      real contradiction as the AUDIT LOG retention period (180 days in
      06-security-policy.md vs 90 days in 07 / 08 / 14). A run that names a decoy
      pair as the contradiction, or finds none, fails Correctness for that run.
    - Hallucination (hard-fail eligible, weight 2.5) = inventing a contradiction
      that is not in the text, or misquoting a value to manufacture a conflict. The
      five decoys (especially the 24-month customer-data retention) are the
      canonical false contradictions.
    - Completeness (weight 2.0) = did the run quote BOTH sides with citations and
      explain why they conflict, not just say "there is an inconsistency in the
      retention policy".
    - Reasoning quality (weight 2.5) = did the run reason about whether two numbers
      describe the SAME fact before calling them a contradiction (the discriminator
      between a real find and a decoy), and ideally note that 90 is corroborated
      three times while 180 stands alone. This is where floor runs of a cheaper
      model degrade - reporting any two different numbers as a conflict.
    - Discipline (decision task, weight 1.25) = did the run report exactly ONE
      contradiction (the real one) rather than listing several "possible
      inconsistencies" to look thorough.
    - Source transparency (weight 1.0) = cites the files (and sections) for both
      sides.
    - Format adherence (weight 1.5) = the output envelope plus the
      fact-label-on-first-line structure.

    THE HEADLINE METRIC IS WITHIN-FAMILY SPREAD across the 5 runs per model: the
    hit-rate (of 5 runs, how many correctly identified the audit-log retention
    contradiction with zero false contradictions) and the weighted-total spread
    (max minus min). A model that goes 5/5 with tight spread is consistent on the
    buried needle; a model that goes 3/5, or swings between the real contradiction
    and a decoy pair, is the inconsistent profile this eval is built to expose.
    Voice match does not apply.
---

# Spec 47 - single-contradiction-detection (find-the-one-needle consistency probe)

A HEAVY consistency battery. A fourteen-document internal handbook for the
fictional "Globex Logistics" is internally consistent EXCEPT for exactly one
planted contradiction: the audit-log retention period is stated as 90 days in
three places (data-handling, incident-response, glossary) and as 180 days in one
buried spot (security-policy). The task is to find that single same-fact /
different-value pair, quote both sides with citations, and explain the conflict -
without flagging any of the many legitimately-different numbers as a false
contradiction.

The corpus (`corpus/single-contradiction-detection/`) is the 14-file handbook plus
a README (15 files). The decoys are deliberate: customer ORDER records are retained
24 months (a different data type, the closest-looking trap), session tokens expire
after 30 days (two mentions that AGREE), dormant accounts auto-disable at 45 days
(a different control), and several process windows land on "30 days/minutes" across
unrelated policies. None of those is a contradiction; only the 90-vs-180 audit-log
retention is.

This is run at `variant_pool: 15` (5 runs per model, model-only, effort inert).
The scored headline is WITHIN-FAMILY SPREAD: per model, the hit-rate across the 5
runs (correct contradiction identification with zero false contradictions) and the
weighted-total spread. Run-to-run reliability on the single buried needle - whether
a model finds it EVERY run or only on its good runs - is the separator, per the
batch-3 consistency read. Correctness-first applies: a confidently-wrong "this is a
contradiction" claim on a legitimate non-conflict is penalised harder than a miss,
because an auditor acts on it and corrupts a correct document. Standard four-phase
`/eval-pit` flow against the frozen `rubric/rubric.md`.
