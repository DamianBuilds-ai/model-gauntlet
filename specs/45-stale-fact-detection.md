---
task_category: stale-fact-detection
prompt_under_test: |
  You are auditing a set of internal documents for a fictional company "Cardinal
  Logistics" for STALE FACTS - statements that were once true but have since been
  superseded by a documented change, and were never updated. The document set is
  the directory corpus/stale-fact-detection/ (a numbered set of internal reference
  docs: runbooks, policies, an onboarding guide, a config reference, a changelog,
  and a decisions log).

  Somewhere in this set, the documents agree on most facts, but at least one fact
  is STALE: one document states an old value or rule that a LATER document (a
  changelog entry, a decision record, or an updated policy) has explicitly
  superseded. The stale statement was never corrected. Your job:
    1. Identify the stale fact (or facts). For each, state: the STALE statement and
       where it appears (doc + section/line), the CURRENT statement that supersedes
       it and where IT appears (the authoritative source), and the change that made
       the old one stale (cite the changelog/decision entry by id or date).
    2. Confirm the rest of the corpus is internally consistent on the facts you
       checked - i.e. do not just hunt one needle; show you verified the
       surrounding facts are NOT stale.

  Rules:
    1. A fact is STALE only if a LATER, AUTHORITATIVE document supersedes it. Two
       documents that simply differ with no supersession evidence is a CONFLICT,
       not staleness - and is out of scope here unless you can point to the
       superseding change. Do not label a difference "stale" without the
       superseding source.
    2. Do NOT invent a supersession. If you cannot cite the changelog/decision
       entry that changed the value, do not claim the value is stale. A claimed
       stale fact with no superseding evidence is a false positive and counts
       against you harder than a miss.
    3. Many facts in the corpus are repeated across documents and are CONSISTENT
       (the same current value in several places). Repetition of a CURRENT value is
       not staleness. Only a value that contradicts a documented later change is
       stale.
    4. Be precise about which document is authoritative. The changelog and the
       decisions log are the authoritative record of changes; a runbook or
       onboarding doc that disagrees with a documented change is the stale one, not
       the other way round.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/stale-fact-detection/
corpus_intent: a numbered set of internal reference docs (runbooks, policies, onboarding, config reference, changelog, decisions log) for a fictional logistics company - mostly current and mutually consistent, with exactly ONE fact left stale (a value superseded by a documented change but never updated in one downstream doc), among several decoy near-repetitions of current facts
corpus_delivered: TBD
corpus_match: TBD
notes: |
  OPUS-CONSISTENCY / VARIANCE BATTERY (stale-fact detection under load). This eval
  runs at variant_pool: 15 - five runs per model (Haiku x5, Sonnet x5, Opus x5;
  effort treated as inert per the methodology). The headline metric is WITHIN-FAMILY
  SPREAD, not the family mean: the question is whether Opus finds the single stale
  fact on EVERY one of its five runs while a cheaper model finds it on its lucky
  runs but reports the corpus as fully consistent (misses it) on one or two of five.
  Three runs barely shows variance; five gives a real spread estimate. The separator
  is run-to-run reliability at catching the one silently-superseded fact, NOT the
  peak. This generalises the K1 needle from eval 27 (the buried superseded value) to
  a dedicated, scaled, multi-document detection task.

  THE STALE FACT (the separator). Across the corpus, the on-call ESCALATION
  TIMEOUT - how long a primary on-call has to acknowledge a page before it
  escalates to the secondary - appears in multiple places and is mostly stated as
  the CURRENT value of 10 minutes. The changelog (CHANGELOG.md, entry CL-2026-014)
  and the decisions log (DECISIONS.md, ADR-031) BOTH explicitly record that the
  escalation timeout was CHANGED from 15 minutes to 10 minutes on 2026-03-18 after
  a missed-page incident. The onboarding guide, the incident runbook, and the
  config reference all carry the current 10 minutes. BUT exactly one document - the
  on-call rotation runbook (04-oncall-rotation.md), in a paragraph deep in its
  "Acknowledgement and handoff" section - still states the OLD value of 15 minutes
  ("the primary has 15 minutes to acknowledge before the page rolls to the
  secondary"). This single sentence was never updated when ADR-031 / CL-2026-014
  landed. It is the stale fact. A model that reads the onboarding 10-minute value,
  sees it corroborated in the config reference, and concludes "escalation timeout
  is consistently 10 minutes" has MISSED the one document still carrying 15. The
  within-family question: does Opus catch the lone 15-minute sentence on 5/5 runs
  while a cheaper model catches it on 2/5 or 3/5.

  WHY IT IS HARD TO SEE. (a) The CURRENT value (10 minutes) is stated in three
  documents and the stale value (15 minutes) in only one - so the majority signal
  says "10 minutes, consistent" and a model that tallies values rather than checking
  each against the changelog accepts the majority. (b) The stale sentence is buried
  mid-section in a long runbook whose heading ("Acknowledgement and handoff") is
  about a broader topic, so the eye does not land on the number. (c) The number 15
  also appears legitimately elsewhere in the corpus in UNRELATED current facts (a
  15-day data-retention window, a 15-minute autoscale cooldown, a $15 per-parcel
  surcharge) - so seeing "15" is not itself a flag; the model must tie THIS 15 to
  the escalation-timeout concept and to the documented change. (d) The supersession
  is real and citable (CL-2026-014 and ADR-031 both name the 15 -> 10 change with a
  date), so the discipline is to confirm the change happened and then find the doc
  that did not get updated - not to guess. (e) The corpus also contains DECOY
  near-repetitions of OTHER current facts that look like they might be stale but are
  not (see decoys below), so a careless model can burn its finding on a false
  positive.

  DELIBERATE DECOYS (these are NOT stale - flagging any is a false positive).
    DECOY-1. The standard delivery SLA is stated as "3 business days" in the SLA
      policy and "three business days" in the onboarding guide. Same value, two
      spellings (digit vs word). This is a CONSISTENT current fact, not staleness.
      Do not flag it.
    DECOY-2. CHANGELOG.md entry CL-2026-009 records that the API rate limit was
      raised from 300 to 600 req/min on 2026-02-02, AND every document that mentions
      the rate limit (config reference, onboarding) already states 600. This change
      WAS propagated correctly - there is no document still carrying 300. A model
      that sees the changelog entry and assumes a stale value exists somewhere is
      chasing a phantom; the 300 value does NOT appear anywhere as a live current
      statement. Do not invent a stale 300.
    DECOY-3. The data-retention window is "15 days" for hot logs in the config
      reference and "15 days" in the security policy - consistent, and unrelated to
      the escalation timeout despite sharing the number 15. Not stale.
    DECOY-4. The decisions log ADR-028 records a PROPOSED change to the deploy
      freeze window that was REJECTED ("status: rejected"). The old freeze window
      therefore still stands and is correctly stated in the runbook. A model that
      treats a rejected proposal as a supersession and flags the (correct) current
      freeze window as stale has misread ADR-028's status. Not stale.
    DECOY-5. The warehouse cutoff time is "16:00 local" in two regional runbooks
      and "4 PM local" in the onboarding guide - same value, two notations. Not
      stale.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers). Reporting the corpus as
  fully consistent (missing the lone 15-minute escalation sentence) is the canonical
  confidently-wrong failure: a new on-call engineer reading the rotation runbook
  would wait 15 minutes before the system actually escalates at 10, or would build
  a mental model that contradicts the live config. EQUALLY bad is flagging a DECOY
  as stale - declaring the rate limit, the retention window, the freeze window, or
  the SLA "stale" sends a maintainer to "fix" a correct, consistent fact and to
  trust a non-existent supersession. Reward the run that finds the ONE real stale
  fact (the 15-minute escalation timeout in 04-oncall-rotation.md, superseded by
  CL-2026-014 / ADR-031) AND clears all five decoys. A run that flags three "stale"
  facts (the real one plus two decoys) is NOT better than one that finds only the
  real one - precision counts.

  ANSWER KEY (for the scoring Architect). Every fact and supersession below is
  grep-verifiable against the corpus.

    THE STALE FACT:
    - STALE statement: 04-oncall-rotation.md, "Acknowledgement and handoff"
      section - "the primary has 15 minutes to acknowledge before the page rolls
      to the secondary." (the only live statement of 15 minutes for the escalation
      timeout in the corpus).
    - CURRENT (authoritative) value: 10 minutes. Stated in 02-onboarding.md
      ("Getting paged"), 06-config-reference.md (the oncall.ack_timeout_minutes
      key = 10), and 03-incident-runbook.md.
    - SUPERSEDING CHANGE: CHANGELOG.md entry CL-2026-014 (dated 2026-03-18) -
      "on-call acknowledgement timeout reduced from 15 to 10 minutes following the
      2026-03-14 missed-page incident." Corroborated by DECISIONS.md ADR-031 (same
      date, same change, status: accepted). The 04-oncall-rotation.md sentence
      predates the change and was never updated.
    A correct audit names the stale sentence in 04-oncall-rotation.md, the current
    10-minute value with at least one authoritative cite, and CL-2026-014 (and/or
    ADR-031) as the superseding change. Missing the stale sentence (reporting "all
    consistent at 10 minutes") is the miss. Flagging any decoy is the false
    positive.

    THE CONSISTENT FACTS THE AUDIT SHOULD CONFIRM (a model that flags any of these
    as stale has produced a false positive):
    - Standard delivery SLA = 3 business days (DECOY-1; consistent, two spellings).
    - API rate limit = 600 req/min everywhere (DECOY-2; CL-2026-009 propagated; no
      live 300 anywhere).
    - Hot-log retention = 15 days (DECOY-3; consistent; unrelated to the timeout).
    - Deploy freeze window = the current value (DECOY-4; ADR-028 proposal was
      REJECTED, so no supersession).
    - Warehouse cutoff = 16:00 local (DECOY-5; consistent, two notations).

  CONSISTENCY SCORING (the headline). For EACH model (Haiku, Sonnet, Opus), score
  all 5 runs, then report:
    - per-run weighted total (mean-of-5 is the family score, SPREAD is the headline)
    - the SPREAD = (max run - min run) weighted total within the family
    - the STALE-FACT HIT RATE = how many of the 5 runs correctly identified the
      15-minute escalation-timeout statement in 04-oncall-rotation.md as stale,
      WITH the CL-2026-014 / ADR-031 supersession cited. This is the single most
      important number: e.g. "Opus 5/5, Sonnet 3/5, Haiku 1/5".
    - the FALSE-POSITIVE RATE = how many runs flagged a decoy as stale. A run that
      finds the real stale fact but ALSO flags a decoy is partially penalised on
      precision.
    - flag any family whose 5 runs diverge by more than 0.5 weighted total as
      HIGH-VARIANCE; spread under 0.2 is HIGH-CONSISTENCY.
  The corpus_intent is explicit: WITHIN-FAMILY SPREAD is the key signal. A model
  that finds the stale fact on three runs and reports "all consistent" on two is
  LESS useful for documentation-maintenance work than one that finds it on all five
  at slightly lower polish.

  Scoring guidance:
    - Correctness (hard-fail eligible, weight 3.0) = did the audit identify the
      stale fact correctly (the 15-minute escalation timeout, superseded by
      CL-2026-014 / ADR-031). Reporting the corpus as fully consistent (missing it)
      is Correctness <= 2. Naming a DIFFERENT fact as the stale one is Correctness
      1.
    - Completeness (weight 2.0) = did the audit BOTH find the stale fact AND confirm
      the surrounding facts are consistent (not just hunt one needle). A bare "the
      timeout is stale" with no verification of the decoys is less complete than one
      that explicitly clears them.
    - Hallucination (hard-fail eligible) = inventing a supersession (claiming a fact
      is stale with no changelog/decision evidence), or inventing a stale value that
      does not appear in the corpus (e.g. claiming a live 300 rate limit exists when
      it does not - DECOY-2). Flagging a decoy as stale is the canonical
      hallucination here.
    - Reasoning quality = did the model tie the lone 15 to the escalation-timeout
      concept and to the documented change, rather than tallying values by majority
      or pattern-matching the number 15 (which appears in unrelated current facts).
      Did it correctly treat the REJECTED ADR-028 as a non-supersession. This is
      where the careful auditor separates from the skimmer and where Opus is
      hypothesised to hold consistency.
    - Source transparency = the finding cites the stale doc + section, at least one
      authoritative current source, and the superseding changelog/decision id.
    - Discipline = found the real stale fact AND cleared all five decoys without
      flagging them; did not claim staleness without a citable supersession.
      Explicitly noting "the 15 in the retention window is unrelated and current" is
      a discipline POSITIVE.
    - Format adherence = the output envelope plus a clean structure (stale
      statement, current statement, superseding change, then the consistency
      confirmation).
    Correctness on the single stale fact and within-family consistency on it are the
    scored discriminators. Voice match does NOT apply.

    Suggested scoring shorthand for the Architect: a run is "correct" iff it (a)
    names the 15-minute escalation-timeout sentence in 04-oncall-rotation.md as
    stale, (b) cites the current 10-minute value and the CL-2026-014 / ADR-031
    supersession, and (c) does NOT flag any of the five decoys. A run that does all
    three is the exemplary 5 on Correctness and Discipline. Missing the stale fact
    (reporting full consistency) caps Correctness at 2; flagging a decoy caps
    Hallucination/Discipline. The headline output is the per-family STALE-FACT HIT
    RATE and the within-family SPREAD.
---

# Spec 45 - stale-fact-detection (the silently-superseded-fact variance battery)

A HEAVY consistency probe that generalises the K1 buried-superseded-value needle of
eval 27 into a dedicated, scaled, multi-document detection task. The model audits a
set of internal reference documents for a fictional "Cardinal Logistics" (runbooks,
policies, an onboarding guide, a config reference, a changelog, and a decisions log)
for STALE FACTS - statements once true but since superseded by a documented change
and never updated. The corpus is mostly current and mutually consistent. EXACTLY ONE
fact is left stale: the on-call escalation timeout is recorded as the current 10
minutes in three documents (onboarding, config reference, incident runbook) and
explicitly changed from 15 to 10 minutes by both CHANGELOG.md (CL-2026-014) and
DECISIONS.md (ADR-031) on 2026-03-18 - but one document, the on-call rotation
runbook, still carries the old 15-minute value in a sentence buried mid-section that
was never updated. Finding that lone stale sentence is the separator.

The fact is hard to see because the current value holds a 3-to-1 majority (so a
value-tallying model accepts "10, consistent"), the stale sentence is buried in a
long runbook, and the number 15 also appears in unrelated CURRENT facts (a 15-day
retention window, a 15-minute autoscale cooldown, a $15 surcharge) so the digit
itself is not a flag. Five decoys are planted - consistent facts with two spellings
or notations, an already-propagated change with no surviving stale value, an
unrelated 15-day window, and a REJECTED proposal (ADR-028) that a careless model
might treat as a supersession - each engineered to draw a false positive.

The eval runs at `variant_pool: 15` - five runs per model (Haiku x5, Sonnet x5, Opus
x5, effort inert per the methodology). The headline metric is WITHIN-FAMILY SPREAD:
the question (per the batch-4 redesign) is whether Opus finds the one stale fact on
every one of its five runs while a cheaper model finds it on its lucky runs but
reports full consistency on one or two of five. The single most important number the
scoring Architect reports is the per-family STALE-FACT HIT RATE (e.g. "Opus 5/5,
Sonnet 3/5, Haiku 1/5") plus the FALSE-POSITIVE RATE on the decoys and the
within-family weighted-total spread.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is central: reporting the corpus as fully
consistent (missing the stale 15-minute sentence) is the canonical confidently-wrong
failure (a new on-call engineer would build a wrong mental model), and flagging a
decoy as stale is the canonical false-positive failure (sending a maintainer to fix
a correct fact and trust a non-existent supersession). Both are penalised; the run
that finds the one real stale fact AND clears all five decoys is the exemplary
result. Reasoning quality captures whether the model tied the lone 15 to the
escalation-timeout concept and the documented change, and correctly treated the
rejected ADR-028 as a non-supersession, rather than tallying values by majority.
Voice match does not apply. The corpus is the directory `corpus/stale-fact-detection/`.
