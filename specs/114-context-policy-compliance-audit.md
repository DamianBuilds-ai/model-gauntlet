---
task_category: context-policy-compliance-audit
prompt_under_test: |
  You are given two synthetic documents in
  corpus/context-policy-compliance-audit/:

    1. ordinance.md - the consolidated Public-Use Ordinance of a fictional
       municipal authority named "Cobalthaven Municipal Authority". It is
       roughly 200,000 tokens long and contains many numbered clauses.
    2. incident-log.md - a short fragment of an incident log with 17 entries
       (LOG-001 through LOG-017), each describing one field observation by an
       inspector.

  Read the ordinance in full. Then, for EACH log entry (LOG-001 through
  LOG-017), determine whether the observation in that entry violates ANY
  clause in the ordinance. For every log entry you assess as a violation,
  state:
    - the log entry identifier (e.g. LOG-002),
    - the EXACT clause number violated (e.g. Clause 7.4.2),
    - a short quotation from that clause that establishes the prohibition,
    - one sentence explaining why the log entry meets the clause's full
      conditions.

  For every log entry you assess as NOT a violation (a near-violation that
  looks relevant but does not in fact breach any clause once the clause's full
  conditions are applied), say so explicitly and briefly state why (wrong
  zone, outside the regulated window, exempt category, below threshold, named
  exemption on file, etc.).

  Do NOT guess. If the ordinance does not contain a clause that the log entry
  violates, say so honestly. Do NOT invent a clause number, and do NOT pair a
  real violation with the wrong clause. Confidently wrong pairings are worse
  than honest "no violation" assessments.

  Append the required output envelope (schemaVersion, tier, status,
  tool_budget_used) as separate lines. No em dashes (use spaced hyphens). No
  emojis.
variant_pool: 9
corpus: corpus/context-policy-compliance-audit/
corpus_intent: |
  GENERATED CORPUS. corpus/context-policy-compliance-audit/ordinance.md and
  corpus/context-policy-compliance-audit/incident-log.md are produced
  deterministically by
  corpus/context-policy-compliance-audit/generate.py (seed=114). The ordinance
  is ~800,000 chars (~200,000 tokens at ~4 chars/token); the log fragment is
  small (~5k chars / ~1.2k tokens). To regenerate byte-identically: cd into
  the corpus dir and run `python3 generate.py`. The script asserts each of
  the five planted violation-clauses appears exactly once by its distinctive
  unique-phrase grep, that the log contains exactly 17 entries, and that no
  spoiler annotations have leaked into either file.

  WHAT THIS EVAL PROBES: long-context (~200k token) policy-compliance audit -
  can the model, given a long ordinance and a separate short log, correctly
  identify (i) which log entries are violations, (ii) the EXACT clause number
  violated, AND (iii) reject the ~12 near-violations as non-violations once
  each clause's full conditions (zone scope, time window, category, threshold,
  documented exemption) are applied? This is the long-context policy-audit
  dimension of the gauntlet map: eval 75 is single-doc needle synthesis, eval
  113 is multi-doc cross-reference synthesis, and this eval (114) is
  long-context judgment-under-policy across TWO documents.

  QUALITY PRINCIPLE (correctness-first, no-confidently-wrong pairings): an
  audit that flags a near-violation as a violation, or pairs a real violation
  with the wrong clause number, is WORSE than one that honestly catches three
  of five and flags two as uncertain. The traps are all "looks like a
  violation" cases that fail one of the clause's full conditions:
    - LOG-001: solvent in basement BUT it's commercial, not residential (C7.4.2
      governs residential only; commercial is C7.4.7).
    - LOG-003: amplified outdoor sound in residential overlay BUT at 19:30,
      well before the 22:00-07:00 regulated window.
    - LOG-004: amplified sound after 22:00 in residential overlay BUT INDOOR
      (governed by C12.3.1), not outdoor.
    - LOG-006: feeding wildfowl in Cloverhill Park BUT Cloverhill Park is NOT
      on Schedule W-2; supervised feeding outside W-2 is permitted (C18.6.9).
    - LOG-008: feeding fauna BUT on private property entirely outside the
      W-2 boundary.
    - LOG-009: rooftop fixture on a heritage building BUT Schedule-B
      (1.5m allowance under C23.9.4), fixture is 1.2m - below the Schedule-B
      threshold.
    - LOG-010: rooftop fixture on Schedule-A BUT 0.5m - below the 0.6m
      Schedule-A ceiling in C23.9.1.
    - LOG-012: commercial UAV near school BUT 350m away (above the 200m
      threshold in C31.5.7).
    - LOG-013: commercial UAV within 200m of school BUT at 17:30 (outside
      the 08:00-16:00 school-hours window in C31.5.7).
    - LOG-015: UAV near school during school hours BUT RECREATIONAL, not
      commercial (governed by C31.6.2, not C31.5.7).
    - LOG-016: solvent storage in residential structure BUT above grade
      (C7.4.2 is below-grade only).
    - LOG-017: feeding fauna in a W-2 reserve BUT under written exemption
      EX-2024-117 on file. Clause language is absolute, BUT the entry asserts
      a named exemption on file and asks the auditor to treat it as fact;
      this is the most subtle bait. (Models that fail to read the exemption
      assertion will mis-flag this entry.)

  NO SPOILER ANNOTATIONS in either corpus file (no `VIOLATION [Vx]` markers,
  no `NEEDLE [Nx]` markers, no `DISTRACTOR` tags, no `ANSWER KEY` strings).
  The violation-clauses are identifiable ONLY by their distinctive natural-
  language headings. The generator's assertions and this corpus_intent are
  the ONLY places the answer key lives.

  ANSWER KEY (the five planted violations - the scoring Architect verifies by
  matching log-entry-id to clause-number pairs):
    V1: LOG-002 violates Clause 7.4.2 - 12 litres of paint thinner plus 8
        litres of acetone stored in the basement (below grade) of a
        residential dwelling (unit 47B, Tidefall). Clause 7.4.2 is absolute
        for residential below-grade.
    V2: LOG-005 violates Clause 12.1.5 - amplified outdoor sound from a DJ
        rig on a forecourt at 23:40 in Greenmarsh (a Schedule R-1 residential
        overlay zone), inside the 22:00-07:00 prohibited window.
    V3: LOG-007 violates Clause 18.6.3 - approximately 400g of bread fed to
        mallard ducks at 10:20 in Brindlepath Park, which is a Schedule W-2
        designated waterfowl conservation zone; the prohibition is absolute
        regardless of hour, food type, or supervision.
    V4: LOG-011 violates Clause 23.9.1 - a 1.4 metre satellite dish installed
        on Mendlewick Almshouse Row (Appendix H entry 14, Schedule-A heritage),
        well above the 0.6m Schedule-A ceiling.
    V5: LOG-014 violates Clause 31.5.7 - a commercial UAV delivery hover at
        90 metres from Mendlewick Primary School (registered educational
        premises) at 09:15 on a school day, inside the 08:00-16:00 school-
        hours window.

    LOG-001, LOG-003, LOG-004, LOG-006, LOG-008, LOG-009, LOG-010, LOG-012,
    LOG-013, LOG-015, LOG-016, LOG-017 are NEAR-VIOLATIONS that do NOT
    violate any clause once the full conditions are read. Each is explained
    in the bullets above. A model that flags any of these twelve as
    violations, or pairs a real violation with the wrong clause, is wrong.

  GREP-VERIFIABLE INVARIANTS (for the Architect, against the corpus and the
  model output):
    In the corpus (must be exactly 1 hit each):
      - `grep -c "Clause 7.4.2 - Below-grade storage of flammable solvents in residential structures" ordinance.md`
        -> 1.
      - `grep -c "Clause 12.1.5 - Amplified outdoor sound in residential overlay zones after 22:00" ordinance.md`
        -> 1.
      - `grep -c "Clause 18.6.3 - Provisioning of fauna in designated waterfowl conservation zones" ordinance.md`
        -> 1.
      - `grep -c "Clause 23.9.1 - Rooftop fixtures on Schedule-A heritage structures" ordinance.md`
        -> 1.
      - `grep -c "Clause 31.5.7 - Commercial unmanned aerial vehicle operations near registered educational premises" ordinance.md`
        -> 1.
      - `grep -c "VIOLATION \[" ordinance.md incident-log.md` -> 0 (no
        spoilers leaked into either file).
      - `grep -c "^## LOG-" incident-log.md` -> 17 (all entries present).
    A CORRECT model output pairs LOG-002 with C7.4.2, LOG-005 with C12.1.5,
    LOG-007 with C18.6.3, LOG-011 with C23.9.1, LOG-014 with C31.5.7, and
    classifies all other entries as non-violations with a brief reason.
    A WRONG output: flags any of LOG-001/003/004/006/008/009/010/012/013/015/
    016/017 as a violation; OR pairs LOG-002 / LOG-005 / LOG-007 / LOG-011 /
    LOG-014 with the WRONG clause number; OR misses one of the five real
    violations; OR invents a clause number not in the ordinance.

  Scoring guidance:
    - Correctness (hard-fail eligible) = exactly the five real violations are
      identified, each paired with the exact correct clause number, AND no
      near-violation is mis-flagged. One mis-flagged near-violation OR one
      missed real violation OR one wrong-clause pairing is Correctness=2;
      multiple errors is Correctness=1.
    - Completeness = every log entry (LOG-001 through LOG-017) is addressed
      with an explicit violation / not-violation verdict.
    - Hallucination (hard-fail eligible) = inventing a clause number that is
      not in the ordinance, or fabricating a quoted clause sentence.
    - Discipline = applied each clause's FULL conditions (zone scope, time
      window, category, threshold, documented exemption) before issuing a
      verdict. Did not bait on the surface-resemblance.
    - Source transparency (load-bearing) = each violation pairing quotes the
      exact prohibition sentence from the clause so the pairing is verifiable.
    - Reasoning quality = correctly distinguished violations from near-
      violations, with the reason for each near-violation classification.
    Voice match does NOT apply.
notes: |
  Chat B gap-filler: the long-context policy-compliance audit dimension. The
  corpus is GENERATED (not hand-written) by a deterministic seeded Python
  script (corpus/context-policy-compliance-audit/generate.py, seed=114) that
  emits two files: ordinance.md (~800k chars, ~200k tokens) and
  incident-log.md (~5k chars, 17 entries). Five real violation-clauses are
  planted in the ordinance at roughly the 9%, 27%, 46%, 67%, and 88% marks;
  five of the seventeen log entries violate one each; the remaining twelve
  log entries are near-violations that fail one of each clause's full
  conditions (zone scope, time window, category, threshold, exemption).
  Regenerate byte-identically with `python3 generate.py` in the corpus dir.

  This is the second of the two new context-heavy script-generated evals
  authored alongside 113. Where 113 probes recall-at-distance + cross-doc
  synthesis (find all 4 needles across 50 sub-docs), 114 probes
  long-context-judgment-under-policy: read a long policy, judge each short
  log entry against it, and resist the surface-resemblance bait of the
  near-violations.

  CRITICAL: NO spoiler annotations are written into either corpus file. The
  violation-clauses are identifiable only by their distinctive natural-
  language headings. The generator's assertions and this corpus_intent are
  the ONLY places the answer key lives. The log entries deliberately mix
  obvious and subtle near-violations; LOG-017 (named exemption on file
  against an absolutely-worded clause) is the most subtle bait and tests
  whether the model reads the log entries as carefully as the ordinance.

  Correctness and Hallucination are hard-fail eligible; source transparency
  (quoting the violated clause for each pairing) and Discipline (applying
  full clause conditions before issuing a verdict) are load-bearing.
  Standard four-phase /eval-pit flow against the frozen rubric/rubric.md.
  The variant pool is 9 (3 models x N=3, effort inert per the methodology).
  The corpus is the directory corpus/context-policy-compliance-audit/.
---

# Spec 114 - context-policy-compliance-audit (the long-context policy-audit gap)

Hand a model a ~200,000-token synthetic municipal ordinance plus a separate
17-entry incident log fragment and ask which entries violate which specific
clauses. Five log entries each violate exactly one of five planted clauses
(at the 9%, 27%, 46%, 67%, 88% marks of the ordinance). Twelve log entries
are near-violations that LOOK relevant but fail one of each clause's full
conditions (zone scope, time window, category, threshold, named exemption
on file).

The corpus is GENERATED, not hand-written.
`corpus/context-policy-compliance-audit/generate.py` (seed=114) emits
`ordinance.md` (~800k chars, ~200k tokens) and `incident-log.md`
(~5k chars, 17 entries) deterministically - re-running produces byte-
identical output, and it asserts each of the five planted violation-clauses
appears exactly once by its distinctive unique-phrase grep AND that no
spoiler annotations (no `VIOLATION [Vx]` markers, no `NEEDLE [Nx]` markers,
no `ANSWER KEY` strings) have leaked into either file.

The five planted clauses and their pairings: Clause 7.4.2 prohibits
below-grade flammable-solvent storage in residential structures and is
violated by LOG-002 (basement solvents in a residential dwelling); Clause
12.1.5 prohibits amplified outdoor sound after 22:00 in residential overlay
zones and is violated by LOG-005 (DJ rig at 23:40 in Greenmarsh); Clause
18.6.3 prohibits any provisioning of fauna in Schedule W-2 waterfowl
conservation zones and is violated by LOG-007 (bread to mallard ducks at
Brindlepath Park); Clause 23.9.1 caps rooftop fixtures on Schedule-A
heritage buildings at 0.6m and is violated by LOG-011 (1.4m satellite dish
on Mendlewick Almshouse Row); and Clause 31.5.7 prohibits commercial UAV
operation within 200m of registered educational premises during the
08:00-16:00 school-hours window and is violated by LOG-014 (commercial
delivery hover at 90m from Mendlewick Primary School at 09:15).

The discriminator is judgment under policy + bait resistance + exact clause
pairing. The twelve near-violations each fail a different condition: wrong
category (commercial-not-residential, recreational-not-commercial),
outside the regulated time window (19:30-not-after-22:00,
17:30-not-during-school-hours), wrong zone (park-not-on-W-2,
private-property-outside-boundary), wrong heritage schedule (Schedule-B
not-Schedule-A), below threshold (0.5m below 0.6m, 350m above 200m,
above-grade-not-below-grade), or documented exemption on file. A model that
mis-flags any near-violation, mis-pairs a real violation with the wrong
clause, or misses one of the five real violations is wrong.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`.
Correctness and Hallucination are hard-fail eligible; source transparency
(quoting the violated clause for each pairing) and Discipline (applying
full clause conditions before issuing a verdict) are load-bearing. Voice
match does not apply. The variant pool is 9 (3 models x N=3, effort inert
per the methodology). The corpus is the directory
`corpus/context-policy-compliance-audit/`.
