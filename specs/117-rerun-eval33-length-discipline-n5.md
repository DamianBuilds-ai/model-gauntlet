---
task_category: multi-doc-consolidation
prompt_under_test: |
  You are a Consolidator. You are given 44 separate documents about ONE fictional
  product launch ("Globex Helios") under corpus/heavy-multi-doc-consolidation/ -
  charters, PRDs, status updates, meeting notes, a risk register, engineering and
  infra notes, a security review, design notes, billing and pricing docs, legal,
  finance, GTM, support, an org doc, a dependency map, a retro, a parking lot, and a
  glossary.

  Consolidate them into ONE structured plan a team lead could act on. The plan MUST:
    1. Group the documents' content into coherent themes (do NOT produce 44 flat
       summaries - the value is in the grouping and the cross-document connections).
    2. Trace the cross-document dependency chains (e.g. "X is blocked on Y which is
       blocked on Z"), where the chains are spread ACROSS documents.
    3. Surface EVERY cross-document CONFLICT - any place where two or more documents
       disagree on a fact (a date, an owner, a number, a scope decision, a status).
       For each conflict: name BOTH (or all) source documents, state each side's
       value, and reconcile it EXPLICITLY - either by a documented supersession (a
       later meeting overrides an earlier charter; a churn explains a count change) or
       by flagging it as UNRESOLVED where the sources genuinely disagree and nothing
       in the corpus settles it. Do NOT silently pick one side of a conflict and drop
       the other. A silently-resolved conflict (picking a value without naming the
       disagreement) is the primary failure this task tests for.
    4. Produce a prioritized open-risks / next-actions list, each item citing the
       source document numbers that motivate it.
    5. Distinguish DECIDED items, IN-PROGRESS items, and BLOCKED / unowned items.
  Do not invent facts not present in the corpus. Output envelope required
  (schemaVersion, tier, status, tool_budget_used). No em dashes (spaced hyphens). No
  emojis.
variant_pool: 15
corpus: corpus/heavy-multi-doc-consolidation/
corpus_intent: 44 documents about one fictional product launch ("Globex Helios"), each a different shape, cross-referencing each other, with 15 genuine planted cross-document conflicts plus one reconcilable count discrepancy
corpus_delivered: REUSED from eval 33
corpus_match: REUSED from eval 33
notes: |
  N=5 CONFIRMATION RE-RUN of eval 33 (heavy-multi-doc-consolidation). Original ran
  at variant_pool 9 (3 models x N=3) and surfaced a candidate Opus length-discipline
  failure under the 44-doc consolidation load (Opus produced longer, less themed
  output and missed conflict-handling discipline that Sonnet held). This re-run
  lifts the pool to 15 (3 models x N=5) to confirm or refute the length-discipline
  signal with two extra passes per model. Corpus, prompt, answer key, and scoring
  guidance are CLONED VERBATIM from eval 33 - the only deltas are variant_pool
  (9 -> 15) and this notes block. Do NOT regenerate the corpus; reuse
  corpus/heavy-multi-doc-consolidation/ as-is so the N=3-vs-N=5 comparison stays
  apples-to-apples.

  HEAVY multi-doc-consolidation probe (the scaled-up sibling of specs 01 and 08).
  Where spec 01 is one file with 40 threads and spec 08 is 15 docs with 3 planted
  conflicts, THIS is 44 separate documents about one product launch with FIFTEEN
  genuine cross-document conflicts plus one reconcilable count discrepancy. The
  conflicts are spread across distant documents (a charter says one date, a meeting
  six docs later overrides it, two status docs still carry the stale value), so a
  model must hold the whole 44-doc set in working memory to catch them all. Run the
  full 15-variant model-only pool (Haiku x5, Sonnet x5, Opus x5; effort treated as
  inert per the methodology). Aggregate the 5 passes per model (mean weighted total);
  flag any model whose 5 passes diverge by more than 0.5 as a consistency finding.

  HEAVY NOTE. The corpus is ~10,000 words across 44 files. The discriminator is
  CONFLICT RECALL (surface every one of the 15 conflicts, miss none) and CONFLICT
  HANDLING (reconcile each explicitly - name both source docs - rather than silently
  picking a side or flattening it). This is the eval-22 forgetting-under-load
  mechanism applied to cross-document conflict detection: at small scale (spec 08, 3
  conflicts) every model catches the conflicts; the hypothesis is that as the conflict
  count rises to 15 across 44 docs, cheaper models start to (a) DROP conflicts they
  did not hold (recall failure), (b) SILENTLY resolve a conflict by stating one value
  without naming the disagreement (the primary failure mode this tests), or (c)
  flatten the dependency chains into a flat list.

  QUALITY PRINCIPLE (correctness-first, no-silent-resolution): silently picking one
  side of a genuine conflict is WORSE than flagging it as unresolved, because a team
  lead acting on a consolidation that says "the launch date is September 15" (without
  noting the meeting moved it to October 6, or vice versa) will act on a wrong or
  contested fact believing it is settled. The strong behaviour is: surface the
  conflict, name both source docs, and either show the documented supersession or flag
  it unresolved. Inventing a resolution the corpus does not support (claiming a
  conflict is "decided" when no doc decides it) is Hallucination hard-fail eligible.

  ANSWER KEY (for the scoring Architect). Every conflict below is grep-verifiable -
  both sides physically appear in the named docs, and the risk register (doc 12) and
  glossary (doc 44) enumerate them. There are 15 GENUINE CONFLICTS (CONF-1..CONF-15)
  plus 1 RECONCILABLE discrepancy (CONF-R). A model is scored on how many of the 15 it
  surfaces AND handles correctly (names both docs, reconciles or flags unresolved
  rather than silently picking).

  THE 15 CONFLICTS:
    CONF-1 (Launch date) - September 15 (charter doc 01, kickoff doc 13, week-1 status
      doc 08, week-2 status doc 17) vs October 6 (May planning meeting doc 18, week-3
      status doc 24, GTM doc 30, and several cross-refs). CORRECT HANDLING: the later
      meeting (doc 18) SUPERSEDES; October 6 is current; the charter and week-1/week-2
      carry the stale September 15. A strong answer states October 6 AND names the
      stale docs. Silently reporting September 15 is the canonical confidently-wrong
      handling here.
    CONF-2 (Billing-adapter owner) - Dana (billing PRD doc 04) vs Raj's team
      (billing-integration notes doc 22). CORRECT HANDLING: UNRESOLVED - the corpus
      never settles it (RISK-3). Name both docs, flag unresolved.
    CONF-3 (Auth method) - SSO/SAML (data-pipeline doc 09) vs email magic-link (design
      doc 15). CORRECT HANDLING: UNRESOLVED and LOAD-BEARING - it blocks the security
      review (doc 20) from starting (RISK-5). A strong answer flags it unresolved AND
      traces the dependency to the blocked security review and the GA exit criteria.
    CONF-4 (Free-tier row cap) - 10,000 rows (product spec doc 05) vs 25,000 rows
      (pricing doc 26). CORRECT HANDLING: UNRESOLVED (RISK-4). Name both docs.
    CONF-5 (Data-retention window) - 90 days (privacy doc 28) vs 180 days (platform
      engineering notes doc 11). CORRECT HANDLING: UNRESOLVED (RISK-9). Name both docs.
    CONF-6 (Regions at GA) - US-only (charter doc 01, platform notes doc 11) vs US + EU
      (infra deployment doc 23, GTM doc 30). CORRECT HANDLING: UNRESOLVED (RISK-13).
      Name both sides.
    CONF-7 (Uptime SLA) - 99.9 percent (charter doc 01, product spec doc 05) vs 99.5
      percent (ops/SLA runbook doc 33). CORRECT HANDLING: UNRESOLVED (RISK-11). Name
      both docs.
    CONF-8 (Post-launch on-call ownership) - existing Platform team (platform notes doc
      11, ops runbook doc 33) vs a NEW dedicated Helios team (org doc doc 35). CORRECT
      HANDLING: UNRESOLVED (RISK-10). Name both docs; a strong answer notes Support (doc
      21) does not know who to escalate to.
    CONF-9 (Pricing model) - per-seat (pricing plan doc 26) vs usage-based/consumption
      (exec memo doc 39, later). CORRECT HANDLING: UNRESOLVED pending exec ratification
      (RISK-12). The exec memo is LATER but is a RECOMMENDATION not yet ratified, so it
      does NOT silently supersede - flag contested, note the exec memo is the later
      proposal, and trace the four downstream waiters (billing surface doc 04, billing
      adapter doc 22, GTM doc 30, analytics doc 27).
    CONF-10 (Mobile at GA) - in scope (mobile PRD doc 06) vs fast-follow / out of GA
      scope (May meeting doc 18, scope doc doc 37). CORRECT HANDLING: the meeting (doc
      18) and the ratified scope doc (doc 37) SUPERSEDE; mobile is a fast-follow; the
      mobile PRD doc 06 is the stale in-scope doc (RISK-6). State fast-follow AND name
      the stale PRD.
    CONF-11 (Analytics data store) - the Initech Warehouse (data-pipeline doc 09,
      aggregation notes doc 25, vendor doc 38) vs Postgres (platform engineering notes
      doc 11). CORRECT HANDLING: UNRESOLVED (RISK-7); a strong answer notes the
      aggregation service is built against the warehouse so a Postgres decision forces
      rework that threatens the date.
    CONF-12 (Accessibility level at GA) - WCAG 2.1 level A at GA (design docs 10 and
      15) vs level AA at GA (legal doc 34). CORRECT HANDLING: UNRESOLVED (RISK-8); the
      scope doc (doc 37) records the design plan but flags Legal contests it.
    CONF-13 (Security sign-off STATUS) - "complete / green" (week-3 status doc 24) vs
      "pending / blocked on auth" (security review doc 20). CORRECT HANDLING: doc 20 is
      authoritative; the status doc 24 OVERSTATES (RISK-15). A strong answer trusts doc
      20 and explicitly calls out the status overstatement.
    CONF-14 (GA marketing budget) - 250,000 dollars (GTM doc 30) vs 180,000 dollars
      approved (finance doc 40). CORRECT HANDLING: UNRESOLVED (RISK-14). Name both docs.

  The 15 REQUIRED SURFACES = the 14 value-conflicts CONF-1..CONF-14 enumerated above,
  PLUS one critical shared-DEPENDENCY surface (DEP-1 below). A complete consolidation
  must surface all 15. DEP-1 is not a value disagreement but a structural fact whose
  omission is the single worst miss:
    DEP-1 (Aggregation service shared upstream) - the aggregation service (data-pipeline
      doc 09, aggregation notes doc 25) is the shared upstream blocking BOTH the
      dashboard builder (doc 02) AND the connectors (doc 03). This is the highest-fanout
      dependency in the project (RISK-1 in the risk register doc 12) and the reason the
      GA date moved (doc 18). A consolidation that drops DEP-1 has missed the single most
      important structural fact, even if it caught the value-conflicts.

  RECONCILABLE DISCREPANCY (this one SHOULD be reconciled, not flagged unresolved):
    CONF-R (Beta customer count) - 12 (week-1 doc 08, week-2 doc 17) vs 8 (week-3 doc
      24, sales doc 31). CORRECT HANDLING: RECONCILE - 12 was the pre-churn active
      count, 4 churned during beta (research doc 07 interview 6), leaving 8 current.
      Sales doc 31 states the reconciliation explicitly. A strong answer reconciles this
      (12 original minus 4 churn equals 8 current) rather than flagging it as an
      unresolved contradiction. A model that lists 12-vs-8 as an unresolved conflict has
      OVER-flagged (a precision miss in the opposite direction); a model that silently
      reports only one number without explaining the churn has under-handled it.

  DEPENDENCY CHAINS the model should trace (spread across docs; the dependency map doc
  36 enumerates them, but a strong answer traces them from the primary docs, not just
  by copying doc 36):
    - RISK-1: aggregation service (docs 09/25) is the shared upstream blocking BOTH the
      dashboard builder (doc 02) AND the connectors (doc 03) - highest fanout.
    - Auth (CONF-3) -> security review (doc 20) blocked -> GA exit criteria (QA doc 14)
      blocked. The critical-path chain.
    - Pricing model (CONF-9) -> billing surface (doc 04) + billing adapter (doc 22) +
      GTM messaging (doc 30) + analytics (doc 27). Four waiters.
    - Free-tier row cap (CONF-4) -> billing display (doc 04) + onboarding copy (doc 16)
      + support FAQ (doc 21) + conversion funnel (doc 27).
    - Retention (CONF-5) -> infra sizing (doc 19) + deletion flow / security (doc 20) +
      EU residency (docs 23/28).
    - Regions (CONF-6) -> infra (doc 23) + privacy/residency (doc 28) + GTM markets (doc
      30) + finance budget (doc 40).
    - Data store (CONF-11) -> aggregation query path (doc 25) + QA integrity (doc 14) +
      infra storage profile (doc 19) + the warehouse vendor relationship (doc 38).

  Scoring guidance:
    - Completeness (recall, weight 2.0) = of the 15 required surfaces (CONF-1..CONF-14
      plus DEP-1 the shared dependency), how many are present, AND whether the content
      of the 44 docs is themed rather than dropped. Count DROPPED conflicts explicitly -
      a dropped conflict is the strongest forgetting-under-load signal.
    - Correctness (hard-fail eligible) = are the conflicts handled correctly: both
      source docs named, supersessions applied the right way (October 6 not September
      15 for CONF-1; mobile fast-follow not in-scope for CONF-10; security pending not
      green for CONF-13), genuine unresolved conflicts flagged unresolved (not silently
      picked), and CONF-R reconciled (not flagged unresolved). A consolidation that
      silently resolves multiple conflicts, or applies a supersession backwards, fails
      Correctness.
    - Hallucination (hard-fail eligible) = inventing a resolution the corpus does not
      support (claiming a contested conflict is "decided" when no doc decides it), or
      inventing facts/owners/numbers not present. Claiming the pricing model is settled
      (CONF-9) or the auth method is chosen (CONF-3) when the corpus leaves them open is
      the canonical hallucination here.
    - Reasoning quality (weight 2.5) = the dependency chains traced (especially the
      auth -> security -> GA-gate critical path and the aggregation-service shared
      upstream), and supersession logic applied correctly (later meeting governs;
      later-but-unratified exec memo does NOT silently govern). This is where the
      top-tier model is hypothesised to separate.
    - Source transparency = next-actions and conflicts cite the source doc numbers.
    - Structure = themed consolidation with decided / in-progress / blocked buckets, not
      44 flat summaries.
    - Discipline = surfacing conflicts rather than flattening, AND not over-flagging the
      reconcilable CONF-R as unresolved.
    Conflict recall and conflict handling are the scored discriminators. Voice match
    does NOT apply.

    Suggested scoring shorthand for the Architect: conflict score = (conflicts
    surfaced AND correctly handled) / 15 (CONF-1..CONF-14 + DEP-1). A consolidation
    that surfaces all 15, handles each correctly (both docs named, supersession or
    unresolved applied correctly, CONF-R reconciled), traces the critical-path chains,
    and themes the content is the exemplary 5 on Completeness, Correctness, and
    Reasoning quality; dropping conflicts, silently resolving them, or applying a
    supersession backwards is where the score falls.
---

# Spec 117 - rerun-eval33-length-discipline-n5 (N=5 confirmation of the Opus length-discipline failure)

N=5 CONFIRMATION RE-RUN of eval 33 (heavy-multi-doc-consolidation). Eval 33 ran
at the standard variant_pool 9 (3 models x N=3) and surfaced a candidate Opus
length-discipline failure under the 44-document consolidation load (Opus
produced longer, less themed output and missed conflict-handling discipline that
Sonnet held). This re-run lifts the pool to 15 (3 models x N=5) to confirm or
refute the length-discipline signal with two extra passes per model.

Corpus, prompt-under-test, answer key (the 15 required surfaces plus the
reconcilable CONF-R), dependency-chain map, and scoring guidance are CLONED
VERBATIM from eval 33 - the only deltas are variant_pool (9 -> 15) and this
notes block. Do NOT regenerate the corpus; reuse
`corpus/heavy-multi-doc-consolidation/` as-is so the N=3-vs-N=5 comparison stays
apples-to-apples.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first / no-silent-resolution quality principle and the conflict-recall
+ conflict-handling discriminators remain the scored signals (same as eval 33);
the only change is variance resolution at the model level. Voice match does not
apply. The variant pool is 15 (3 models x N=5, effort inert per the methodology).
The corpus is the directory `corpus/heavy-multi-doc-consolidation/`.
