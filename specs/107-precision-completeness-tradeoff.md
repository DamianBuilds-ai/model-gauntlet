---
task_category: precision-completeness-tradeoff
prompt_under_test: |
  You are given a single file at corpus/precision-completeness-tradeoff/incident-tickets.md
  containing 24 closed tickets from a fictional internal platform team's backlog. Read all
  24 tickets, then produce a single output with the following structure.

  Your colleague is preparing the quarterly review. They asked you to identify which
  tickets represent "customer-impacting production incidents" - the kind that should be
  counted in the incident-rate metric, get a postmortem, and feed the reliability budget.
  Some tickets are clear yeses, some are clear nos, and some are genuinely borderline.

  Produce, in this order:

    1. INCLUDE - the tickets that clearly belong in the customer-impacting production
       incident count. List by ticket id, one per line, with a brief (one-clause) reason.

    2. EXCLUDE - the tickets that clearly do NOT belong (engineering hygiene, internal-only
       issues, non-system work, single-customer report-only issues with no underlying
       platform fault). List by ticket id, one per line, with a brief (one-clause) reason.

    3. BORDERLINE / FLAG FOR DISCUSSION - the tickets where reasonable engineers would
       disagree, where the answer depends on a definition your colleague has NOT given
       you, or where a single yes/no would silently smuggle in a judgment call. List by
       ticket id, one per line, with the specific ambiguity that puts the ticket here
       (not a generic "it depends").

    4. THE TRADEOFF - a short paragraph (3-6 sentences) explicitly naming the
       precision/completeness tradeoff in this exercise. If you maximise completeness
       (include every plausible customer-impact ticket), you will over-count and inflate
       the incident-rate metric with edge cases. If you maximise precision (include only
       the unambiguous yeses), you will under-count and miss real incidents that fall in
       grey areas. State which side you erred on and why, what your colleague should
       confirm with you before treating the INCLUDE list as the final count, and what
       single definition (if added) would collapse most of the borderline cases.

  Every ticket id (TKT-2041 through TKT-2064) must appear in EXACTLY ONE of the three
  lists. Do not omit any ticket. Do not list any ticket in two sections.

  Append the required output envelope (schemaVersion, tier, status, tool_budget_used) as
  separate lines after your answer. No em dashes (use spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/precision-completeness-tradeoff/
corpus_intent: |
  One file (corpus/precision-completeness-tradeoff/incident-tickets.md): 24 closed
  tickets from a fictional platform team. The corpus is designed so the 24 tickets sort
  into three bands - clear INCLUDE, clear EXCLUDE, and a wide BORDERLINE band where the
  answer depends on a definition the prompt deliberately does not give. The wide
  borderline band is the eval - it forces a real precision-vs-recall choice and asks
  whether the model REASONS about the tradeoff (Section 4) or blindly maximises one side.

  QUALITY PRINCIPLE (judgment-first, surface-the-tradeoff): the eval has no single
  correct INCLUDE/EXCLUDE/BORDERLINE assignment - it scores whether the model RECOGNISES
  that several tickets are genuinely borderline and SURFACES THAT in section 3 +
  explicitly names the precision/completeness tradeoff in section 4. A confident
  yes/no on every ticket is the failure mode (smuggles in a definition the prompt did
  not give and presents a binary call as if it were obvious). A model that flags the
  borderline cases AND names the missing definition + which side it erred on is the
  strong outcome.

  ANSWER KEY (for the scoring Architect - the intended sorting. This is NOT a strict
  grading key for INCLUDE/EXCLUDE; the eval scores recognition-of-borderlines + tradeoff
  reasoning. But the bands below describe how a careful engineer would sort the corpus,
  and any model that misses the existence of a borderline band is under-performing):

    CLEAR INCLUDE (8 tickets - unambiguous customer-impacting production incidents that
    breached the platform and affected real external customers):
      - TKT-2041 (checkout 503 peak hour, postmortem written)
      - TKT-2043 (Android SDK crashes affecting ~2% installs for 3 days)
      - TKT-2046 (Courier webhook delivery degraded 40 min, B2B customer tickets)
      - TKT-2049 (gateway 5xx spike during failover drill, even though planned;
        customers were affected, CS got pings, postmortem was written)
      - TKT-2057 (order 422 errors on non-ASCII names for 26 hours, ~1k order attempts,
        postmortem PM-121)
      - TKT-2060 (regional EU-Central gateway 503s for 18 minutes, 22% of traffic,
        postmortem PM-122)
      - TKT-2063 (webhook schema change without deprecation, 14 B2B customers broken,
        postmortem PM-123)
      - TKT-2054 (docs site search broken 5 hours - this one is INCLUDE-leaning because
        third-party developers were impacted, but a strict "revenue-impacting only"
        definition would EXCLUDE it; if a model puts this in BORDERLINE that is also
        defensible - this is the cleanest example of the missing-definition problem)

    CLEAR EXCLUDE (8 tickets - engineering hygiene, internal-only, non-system, or
    report-only single-customer issues with no platform fault):
      - TKT-2042 (refactor behind a flag, no incidents)
      - TKT-2044 (HR / on-call rota update)
      - TKT-2047 (staging VM image migration)
      - TKT-2050 (observability improvement, no behaviour change)
      - TKT-2055 (compliance access review)
      - TKT-2056 (internal dashboard display bug, no external impact)
      - TKT-2058 (pre-prod staging load test)
      - TKT-2061 (developer-experience README update)

    BORDERLINE (8 tickets - genuinely depend on a definition the prompt did not give.
    A strong response puts MOST of these in Section 3 and names the specific missing
    definition for each):
      - TKT-2045 (gradual P99 drift, NO SLO breach, NO customer complaints, but a
        real degradation - depends on whether "incident" requires SLO breach or
        customer perception)
      - TKT-2048 (internal Almanac dashboard stale 2 hours - internal-only but it IS
        a system fault, not pure hygiene; some teams count internal incidents)
      - TKT-2051 (single-customer 12c reconciliation discrepancy - depends on
        whether single-customer correctness bugs count, even when re-issued and the
        underlying data is correct)
      - TKT-2052 (TLS cert expired, internal-only service down 4 hours - the
        silent-failure pattern often triggers an incident process even though no
        external customer was hit; depends on definition)
      - TKT-2053 (SDK session-expired uptick after deploy, below alert threshold,
        no complaints, reverted - depends on whether "telemetry-only signal that
        was within normal range" counts as a customer-impacting incident)
      - TKT-2059 (queue backlog drained within SLA - depends on whether
        "operationally noteworthy" near-miss counts when no SLA actually breached
        and no customer experience degraded)
      - TKT-2062 (single customer cannot reset password due to third-party email
        blocklist - depends on whether single-customer issues caused by a
        third-party with no platform fault count)
      - TKT-2064 (third-party IdP outage affected ~30% of customers' logins; the
        IdP owns the outage but customers experienced it as a Veldt incident -
        depends on whether "our" incident means our code/infra or the customer
        experience of using our platform)

  GREP-VERIFIABLE STRUCTURAL INVARIANTS (for the Architect's first-pass triage - these
  catch a model that ignored the format, not the judgment):
    - Section headings appear in order: "INCLUDE", "EXCLUDE", "BORDERLINE" (or "FLAG FOR
      DISCUSSION"), and "THE TRADEOFF" (or "TRADEOFF").
    - Every ticket id TKT-2041 through TKT-2064 appears EXACTLY ONCE across the three
      list sections (count: 24 distinct ids, no duplicates, no omissions).
    - The TRADEOFF section is present and contains the substring "precision" AND the
      substring "completeness" (or "recall") AND names the side the model erred on
      ("I erred on the side of..." / "I favoured X" / equivalent).
    - At least one ticket appears in the BORDERLINE section (a model that puts 0 tickets
      in borderline has collapsed the tradeoff and silently picked one side).

  JUDGMENT INVARIANTS (the actual discriminator - the Architect grades these qualitatively
  per family):
    - HIGH-quality: BORDERLINE section contains 5+ of the 8 borderline-band tickets and
      names a specific missing definition for each (not generic "depends"). TRADEOFF
      section names BOTH sides and specifies which definitional gap, if filled, would
      collapse most borderlines.
    - MEDIUM-quality: BORDERLINE section contains 2-4 tickets with reasoning; tradeoff
      named but only one side explored in depth.
    - LOW-quality / failure mode: 0-1 tickets in BORDERLINE (collapsed the tradeoff);
      OR section 4 is generic / does not actually name the precision-completeness
      tension; OR confidently classifies the 8 genuinely-borderline tickets as a clean
      yes/no without flagging the missing definition.
    - REPORTING per family (Haiku / Sonnet / Opus): mean borderline-count per run,
      variance across the 5 runs, share of runs that hit HIGH vs MEDIUM vs LOW.

  Scoring guidance:
    - Correctness (hard-fail eligible) = the clear-INCLUDE and clear-EXCLUDE tickets are
      not blatantly mis-sorted (e.g. TKT-2044 HR task classified as a production
      incident, or TKT-2041 checkout 503 classified as EXCLUDE). A model can disagree on
      borderlines without losing Correctness; flagrant mis-sorting on clear-band tickets
      is the failure.
    - Completeness (hard-fail eligible) = all 24 ticket ids appear, each in exactly one
      section; sections 1-4 all present.
    - Hallucination (hard-fail eligible) = inventing a ticket id, inventing facts about
      a ticket (e.g. "TKT-2049 caused $2M revenue loss" - no such number in the
      corpus), or claiming the prompt gave a definition it did not.
    - Reasoning quality = surfaces the missing definition, articulates the
      precision/recall tradeoff, gives non-generic reasoning for borderline picks.
    - Discipline = does not over-claim, does not collapse the tradeoff into a confident
      binary, does not invent a stricter or looser definition than the prompt allows
      and then sort against that.
    - Format adherence = the four labelled sections, ticket ids on their own lines,
      clean envelope.
    - Source transparency = grounded in the ticket text, distinguishes "the ticket
      says" from "I am inferring".
    - Voice match does NOT apply.

  The single largest separator: a variant that puts 0-1 tickets in BORDERLINE and writes
  a generic TRADEOFF paragraph scores LOW. A variant that puts 5-8 of the 8 borderline-
  band tickets in BORDERLINE with specific named ambiguities + TRADEOFF that names BOTH
  sides + the missing definition scores HIGH. Mid-range responses (2-4 borderlines, partial
  tradeoff reasoning) get MEDIUM.
notes: |
  NEW task type. Probes whether a model REASONS about the precision/completeness tradeoff
  vs blindly maximising one side. Pool 15 (N=5) - this is a consistency/variance
  question per family (does the model REGULARLY surface the tradeoff, or only on some
  runs).

  DIFFICULTY SELF-CHECK: would a weak model (Haiku) genuinely drop something here?
  Prediction: YES. The eval-37-adjacent pattern (Haiku tends to over-include / false-
  positive when uncertain) suggests Haiku is the most likely family to confidently
  classify the 8 borderline tickets as a clean yes/no without flagging the missing
  definition. Sonnet may collapse on some runs and surface on others (the variance
  question). Opus, if any model wins here, should consistently put MOST borderlines in
  Section 3 AND name the missing definition in Section 4. If all three families
  consistently produce 5+ borderlines and clean tradeoff sections, the eval is a ceiling
  tie and the eval has not isolated the discriminator - in which case the corpus borderline
  band needs to be wider (more genuinely-ambiguous tickets) before re-running. Initial
  judgment: the 8 borderline tickets are wide enough that a model under "give me the
  count" pressure will collapse at least some - that is the test.

  CONTAMINATION CHECK (eval-43 lesson): the corpus has ZERO hints naming the borderline
  tickets, ZERO "this one is ambiguous" comments, ZERO section headers grouping by
  difficulty. Each ticket is written as a flat factual entry. The ambiguity comes
  organically from the realistic mix of incident types (clear customer outages, clear
  hygiene, and the muddy middle of internal-only / SLA-met-but-degraded / third-party-
  caused / single-customer-but-real situations). The prompt explicitly does NOT define
  "customer-impacting production incident" - that gap IS the eval.

  Standard four-phase /eval-pit flow against the frozen rubric/rubric.md. The variant
  pool is 15 (3 models x N=5). The corpus is the directory
  corpus/precision-completeness-tradeoff/.
---

# Spec 107 - precision-completeness-tradeoff (the borderline-band test)

Given 24 closed tickets from a fictional platform team, sort them into INCLUDE /
EXCLUDE / BORDERLINE for the quarterly "customer-impacting production incident" count,
then explicitly name the precision/completeness tradeoff and which side you erred on.
The prompt deliberately does not define "customer-impacting production incident" - that
missing definition is the eval. The corpus is designed so 8 tickets are clear includes,
8 are clear excludes, and 8 sit in a wide borderline band where the answer depends on
a definition the prompt does not give.

This is eval-37-adjacent: probes whether a model reasons about the precision/recall
tradeoff (puts borderline tickets in Section 3, names the missing definition in Section
4) or blindly maximises one side (confident yes/no on every ticket, generic tradeoff
paragraph). A model that collapses the tradeoff by classifying 0-1 tickets as borderline
has silently picked a definition and presented its sort as obvious - the failure mode.
A model that flags 5-8 borderlines with specific named ambiguities AND names both sides
of the tradeoff AND identifies the single definitional gap that would resolve most
borderlines is the strong response.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. Helpfulness
and Discipline apply and are central. Correctness is judged as not-blatantly-misorting
the clear-band tickets (a model can defensibly disagree on borderlines); Completeness
is the structural invariant (all 24 ticket ids present, each in exactly one section);
Hallucination is hard-fail (inventing ticket facts, inventing a definition the prompt
did not give). The eval also reports per-family the mean borderline-count and variance
across the 5 runs, since consistency-of-tradeoff-recognition is part of the discriminator.
Voice match does not apply. The corpus is the directory
`corpus/precision-completeness-tradeoff/`.
