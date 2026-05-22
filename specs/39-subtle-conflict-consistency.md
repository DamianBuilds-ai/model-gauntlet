---
task_category: subtle-conflict-consistency
prompt_under_test: |
  You are a Consolidator. You are given several separate documents about one
  project ("Globex Insight") under corpus/completeness-under-conflict/ - charter,
  PRDs, research notes, pipeline notes, a risk register, a compliance memo, a
  meeting summary, design notes, engineering notes, security-review notes, a
  finance/status thread, and a launch/GTM plan. The documents cross-reference each
  other.

  Consolidate them into ONE structured briefing a team lead could act on. The
  briefing MUST include a CONFLICTS section that surfaces EVERY genuine
  cross-document conflict you find. For each conflict:
    1. Name BOTH source documents.
    2. State both conflicting values or claims.
    3. Say whether the conflict is RESOLVABLE from the sources (and if so, what the
       correct resolution is and why) or UNRECONCILED (no source settles it - flag
       it as open and needing a decision).

  CRITICAL discipline on "looks decided" conflicts: if one document states a value
  and a LATER document states a DIFFERENT value and appears to supersede it, that is
  STILL a genuine conflict you must surface - because the earlier (now stale)
  document is still live in the corpus and still describes the old value. Do NOT
  silently adopt the later value and omit the conflict. Surface it, state which
  value governs and why, AND name the stale document that still carries the
  superseded value. A conflict that "looks decided" is the single easiest one to
  drop, and dropping it means an engineer reading the stale doc later acts on the
  wrong value.

  Discipline rule (the other direction): surface only GENUINE conflicts. Two
  documents that cite different numbers for DIFFERENT metrics, or that name
  DIFFERENT components, are NOT in conflict - listing a non-conflict as a conflict
  is a precision error and counts against you, the same way missing a real conflict
  does.

  Also produce a brief themed grouping of the material and a prioritized
  open-risks / next-actions list, each item citing the source docs that motivate
  it. Do not invent facts not present in the corpus. Output envelope required
  (schemaVersion, tier, status, tool_budget_used). No em dashes (spaced hyphens).
  No emojis.
variant_pool: 15
corpus: corpus/completeness-under-conflict/
corpus_intent: 14 separate cross-referencing project docs about one fictional product launch, all surface-consistent EXCEPT a set of genuine conflicts of which ONE (a stale-vs-current value that LOOKS decided) is the buried separator - the same battle-tested corpus as spec 27, re-run at N=5 per model so within-family run-to-run SPREAD is the headline metric
corpus_delivered: TBD
corpus_match: TBD
notes: |
  CONSISTENCY / VARIANCE BATTERY (the eval-27 K1 pattern at N=5). This is NOT a fresh
  corpus - it is the spec 27 completeness-under-conflict corpus
  (corpus/completeness-under-conflict/, the "Globex Insight" analytics-platform
  launch, 14 cross-referencing docs) re-run at a HIGHER N so the headline signal is
  WITHIN-FAMILY SPREAD, not the mean. The batch-3 read suggests Opus's edge on
  buried-item tasks is CONSISTENCY (run-to-run reliability at catching the easy-to-
  miss item every run) rather than a higher ceiling. N=3 barely shows variance; N=5
  gives a real spread estimate. So this eval runs 5 passes per model - variant_pool:
  15 (Haiku x5, Sonnet x5, Opus x5; effort treated as inert per the methodology,
  model-only).

  THE SINGLE BURIED SEPARATOR (the consistency target) - THE K1 STALE-VS-CURRENT
  CONFLICT. Across the 14 docs, the corpus carries several genuine conflicts, but the
  ONE that cheaper models systematically drop run-to-run is the LAUNCH DATE conflict
  (K1), because it LOOKS DECIDED. The charter (doc 01) sets the launch date to
  September 8. Three later docs say September 22 - the meeting summary (doc 09,
  which explicitly says "This supersedes the charter's September 8 date"), the
  finance/status thread (doc 13), and the GTM plan (doc 14). A model under load reads
  the three concordant September-22 docs, sees the explicit "supersedes" language,
  concludes the date is settled, silently uses September 22, and OMITS the conflict
  entirely - never flagging that the charter (doc 01) is now STALE and still carries
  September 8. That silent omission is the exact failure this eval targets. The
  correct, complete answer SURFACES K1 as a genuine conflict, states September 22
  governs and why (doc 09 supersedes), AND names the stale charter (doc 01) as the
  superseded source that must be corrected. CONSISTENCY AT SURFACING THIS
  "LOOKS-DECIDED" CONFLICT AS A REAL CONFLICT, RUN AFTER RUN - rather than silently
  resolving it - IS THE PRIMARY DISCRIMINATOR. Track per model how many of the 5 runs
  surfaced K1 with the stale charter named (not just used the September 22 value).

  THE OTHER GENUINE CONFLICTS (the surface; models should also surface these every
  run, but K1 is the buried separator that gates the consistency finding). A complete
  CONFLICTS section names both docs for each:
    K1. LAUNCH DATE - September 8 (charter doc 01) vs September 22 (meeting doc 09,
        carried into finance doc 13 and GTM doc 14). RESOLVABLE: doc 09 supersedes;
        September 22 governs; the charter (doc 01) is stale and must be corrected.
        THIS IS THE BURIED SEPARATOR - it looks decided and is the one dropped under
        load.
    K2. DASHBOARD OWNERSHIP - Dana (activity-panel PRD doc 04; charter doc 01) vs
        Theo's platform team (engineering notes doc 11). UNRECONCILED; surface as an
        open ownership ambiguity needing a decision.
    K3. AUTH METHOD - SAML SSO (data-pipeline notes doc 06) vs email OTP / one-time
        passcode (design notes doc 10). UNRESOLVED and LOAD-BEARING: blocks the
        security review (doc 12) and drives the launch slip (docs 09, 12, 07 RISK-1).
        Note its downstream blocking effect.
    K4. DATA RETENTION - 90 days mandated (compliance memo doc 08) vs 12 months
        displayed (activity-panel PRD doc 04). RESOLVABLE: the 90-day compliance limit
        governs and the 12-month PRD figure cannot stand (a violation per doc 08;
        RISK-2 in doc 07). Flag as a legal exposure. (Sub-point: doc 08 also says
        billing/invoice history has a separate longer retention basis and must NOT be
        conflated with the 90-day activity limit - a model that caps billing history
        at 90 days has mis-read.)
    K5. PRIMARY DATASTORE - PostgreSQL (data-pipeline notes doc 06) vs the vendor
        columnar store "Cobalt" (GTM plan doc 14). UNRECONCILED (RISK-3 in doc 07);
        flag the primary-store decision as open.
    K6. BUDGET - hard cap 150k (finance thread doc 13) vs 220k planned spend (GTM
        plan doc 14). UNRECONCILED, over by 70k (RISK-4 in doc 07); state the overage
        and that GTM spend must come down to the cap.

  THE 2 NON-CONFLICTS (must NOT be listed as conflicts - flagging either is a
  confidently-wrong false positive; track per-run whether precision degrades on later
  runs):
    N1. USER COUNTS - ~4,000 REGISTERED accounts (usage-panel PRD doc 02) vs ~1,200
        MONTHLY ACTIVE accounts (customer research doc 05). DIFFERENT METRICS
        (registered base vs 30-day active), explicitly reconciled in both docs. NOT a
        conflict.
    N2. SERVING COMPONENTS - the "cache layer" and the "read replica" (both named in
        data-pipeline notes doc 06 and engineering notes doc 11) are SEPARATE
        components serving different purposes; the docs AGREE. NOT a conflict.

  THE SCORED SIGNAL IS SPREAD ON K1, NOT THE MEAN. Compute, per model, both the mean
  weighted total AND the run-to-run consistency on the buried separator: how many of
  the 5 runs surfaced K1 AS A CONFLICT with the stale charter (doc 01) named
  (silently using September 22 without flagging the charter does NOT count as a catch).
  A model that surfaces K1 on 5/5 runs is the exemplary consistency profile; a model
  that surfaces it on 2/5 and silently resolves it on the other 3 is the inconsistency
  finding this eval exists to surface. Also report per-model conflicts_recall spread
  (range of genuine conflicts surfaced across the 5 runs) and precision (any run that
  flags N1 or N2). Report within-family spread as the headline; the mean is secondary
  context.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a silently-resolved
  conflict and a falsely-flagged non-conflict are BOTH confidently-wrong outputs that
  mislead a lead acting on the briefing, AND inconsistency is itself a defect. A
  consolidation that silently adopts September 22 and omits the K1 conflict has left
  the stale charter uncorrected, so a later reader of the charter acts on September 8.
  Penalise the silent resolution of the looks-decided conflict hardest, and penalise
  high run-to-run variance as a production-readiness defect.

  DEPENDENCY CHAINS to trace (Reasoning quality signal):
    - The data pipeline (doc 06) is the shared upstream feeding all three panels
      (usage doc 02, billing doc 03, activity doc 04).
    - The auth conflict (K3) BLOCKS the security review (doc 12), which drives the
      launch slip (doc 09) - which is itself why the launch date moved from September
      8 to September 22 (the K1 resolution).
    - The retention conflict (K4) gates launch as a legal exposure (doc 08 / RISK-2).
    - The budget conflict (K6) requires the GTM plan (doc 14) to come down to the
      finance cap (doc 13).

  Scoring guidance:
    - Completeness (recall, weight 2.0) = PER RUN, of the 6 genuine conflicts
      (K1-K6), how many are surfaced with both source docs named. Then the headline:
      per-model count of runs (out of 5) that surfaced K1 AS A CONFLICT with the stale
      charter named, plus the conflicts_recall range across the 5 runs. Silently
      resolving K1 (using September 22 without flagging the charter) is the canonical
      drop and is NOT a catch.
    - Correctness (hard-fail eligible) = are the surfaced conflicts real and described
      accurately (right docs, right values, right resolvable-vs-unreconciled call),
      and are the resolvable ones resolved correctly (K1 -> September 22 with the
      charter flagged stale; K4 -> 90-day limit governs). Silently picking the wrong
      side of a resolvable conflict is a Correctness failure.
    - Hallucination (hard-fail eligible) = inventing a conflict that does not exist
      (N1/N2 are the canonical traps), inventing a doc, or asserting a value not in
      the corpus.
    - Reasoning quality = did it trace the dependency chains (notably that the K3 auth
      block drove the security-review delay that caused the K1 date slip) and classify
      each conflict resolvable-vs-unreconciled, rather than flattening or silently
      reconciling.
    - Discipline (decision/judgment task) = surfaced the genuine conflicts WITHOUT
      padding with N1/N2, and did not silently pick sides - especially on the
      looks-decided K1.
    - Source transparency = every conflict names both source docs; every next-action
      cites the docs that motivate it.
    - Helpfulness = is the briefing decision-grade (a lead can see what is decided,
      what is blocked, what needs a decision).
    - Format adherence = output envelope plus a distinct CONFLICTS section.
    Conflict recall, precision, AND run-to-run spread on K1 are the scored
    discriminators. Voice match does NOT apply.

    Suggested scoring shorthand for the Architect: per run, conflicts_recall =
    (genuine conflicts surfaced with both docs) / 6, precision_penalty = number of
    non-conflicts falsely flagged (N1, N2) + resolvable conflicts resolved on the
    wrong side. Per model, report mean conflicts_recall, the conflicts_recall RANGE
    across the 5 runs, and k1_hits = how many of the 5 runs surfaced K1 as a conflict
    WITH the stale charter named. The headline ranking is by CONSISTENCY (highest
    k1_hits + lowest spread at high recall), with the mean as secondary context. A
    model that surfaces all 6 genuine conflicts (both docs each), surfaces K1 with the
    stale charter named on ALL 5 runs, resolves K1 and K4 correctly, and never flags
    N1/N2 is the exemplary consistency profile; a model that silently resolves the
    looks-decided K1 on 2-3 of its 5 runs is exactly the inconsistency finding this
    eval exists to surface.
---

# Spec 39 - subtle-conflict-consistency (the eval-27 K1 pattern at N=5, spread as headline)

The consistency / variance sibling of spec 27, narrowed onto its hardest single
mechanism: the looks-decided stale-vs-current conflict. Same battle-tested corpus
(`corpus/completeness-under-conflict/` - the fictional "Globex Insight" analytics-
platform launch, 14 cross-referencing docs that are largely surface-consistent), re-run
at a HIGHER N so the headline metric is WITHIN-FAMILY SPREAD rather than the mean.

The batch-3 read suggests Opus's edge on buried-item tasks is CONSISTENCY (catching the
easy-to-miss item every run) rather than a higher ceiling. N=3 barely shows variance;
N=5 gives a real spread estimate. So this eval runs 5 passes per model - `variant_pool:
15` (Haiku x5, Sonnet x5, Opus x5, model-only, effort inert per the methodology). The
single buried separator is the eval-27 K1 launch-date conflict: the charter says
September 8, three later docs say September 22 and one explicitly says it "supersedes"
the charter - so the date LOOKS decided. A model under load reads the concordant
September-22 docs, silently adopts September 22, and omits the conflict, leaving the
stale charter uncorrected so a later reader acts on September 8. The complete answer
surfaces K1 as a real conflict, states September 22 governs and why, AND names the stale
charter as the superseded source. Consistency at surfacing this looks-decided conflict
run after run - rather than silently resolving it - is the primary discriminator; the
other genuine conflicts (auth, retention, ownership, datastore, budget) form the surface
that should be caught every run, and the two non-conflicts (registered-vs-active users;
cache-vs-replica) are the precision traps.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`, with the
within-family spread on K1 elevated to the headline. The correctness-first quality
principle holds and is extended: a silently-resolved conflict and a falsely-flagged
non-conflict are both confidently-wrong outputs, AND high run-to-run variance is itself
a production-readiness defect. Conflict recall, precision, and per-run consistency at
surfacing K1 are the scored discriminators - and silently using the superseding value
without flagging the stale source does NOT count as a catch. The variant pool is 15 (3
models x N=5). The corpus is the directory `corpus/completeness-under-conflict/`.
