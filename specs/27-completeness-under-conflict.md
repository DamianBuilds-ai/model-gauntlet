---
task_category: completeness-under-conflict
prompt_under_test: |
  You are a Consolidator. You are given several separate documents about one project
  ("Globex Insight") under corpus/completeness-under-conflict/ - charter, PRDs,
  research notes, pipeline notes, a risk register, a compliance memo, a meeting
  summary, design notes, engineering notes, security-review notes, a finance/status
  thread, and a launch/GTM plan. The documents cross-reference each other and several
  of them DISAGREE with each other.

  Consolidate them into ONE structured briefing a team lead could act on. The briefing
  MUST:
    1. Group the material into coherent themes (not one flat summary per doc).
    2. Trace the cross-document dependency chains where docs reference each other.
    3. Produce a CONFLICTS section that surfaces EVERY genuine cross-document conflict
       you find. For each conflict: name BOTH source documents, state both conflicting
       values/claims, and say whether the conflict is RESOLVABLE from the sources (and
       if so, what the correct resolution is and why) or UNRECONCILED (no source
       settles it - flag it as open and needing a decision). Do NOT silently pick one
       side of a conflict without saying you did so and why.
    4. Produce a prioritized open-risks / next-actions list, each item citing the
       source docs that motivate it, and distinguish decided / in-progress / blocked
       items.

  Discipline rule: surface only GENUINE conflicts. Two documents that cite different
  numbers for DIFFERENT metrics, or that name DIFFERENT components, are NOT in conflict
  - listing a non-conflict as a conflict is a precision error and counts against you,
  the same way missing a real conflict does.

  Do not invent facts not present in the corpus. If something is unowned or undecided,
  say so. Output envelope required (schemaVersion, tier, status, tool_budget_used). No
  em dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/completeness-under-conflict/
corpus_intent: 14 separate cross-referencing project docs about one fictional product launch, with 6 genuine planted cross-document conflicts and 2 planted non-conflicts (look-alikes that reconcile cleanly)
corpus_delivered: TBD
corpus_match: TBD
notes: |
  COMPLETENESS-UNDER-CONFLICT PROBE (the scaled conflict version of spec 08). Spec 08
  planted 3 cross-doc conflicts; THIS spec plants 6 genuine conflicts across 14 docs,
  PLUS 2 deliberate non-conflicts (look-alikes that reconcile cleanly), to test two
  things at once under load: (a) Completeness - does the model surface ALL 6 genuine
  conflicts or does it silently resolve / miss some as the conflict count and doc count
  rise; and (b) Discipline - does it correctly NOT flag the 2 non-conflicts, or does it
  pad the conflicts list with false positives to look thorough. The corpus is a NEW
  scenario ("Globex Insight", an analytics-platform migration + customer dashboard),
  deliberately not spec 08's "Northwind Pulse", so the old answer cannot be
  pattern-matched.

  Variant pool is 9, not 12. Reasoning effort is treated as INERT under the current
  methodology, so this is a clean MODEL comparison: 3 models x N=3 - Haiku x3,
  Sonnet x3, Opus x3. Aggregate the 3 passes per model (mean weighted total); flag any
  model whose 3 passes diverge by more than 0.5 as a consistency finding.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a silently-resolved conflict
  and a falsely-flagged non-conflict are BOTH confidently-wrong outputs and score worse
  than an honest gap. A consolidation that silently picks one side of the retention
  conflict (and so green-lights a compliance violation) or that quietly drops the auth
  conflict (which is blocking the security review) has produced a briefing a lead would
  act on wrongly. Equally, a model that flags the registered-vs-active user counts as a
  contradiction has invented a conflict that does not exist. Penalise both directions.
  Flag any confidently-wrong conflict-handling for an extra penalty.

  ANSWER KEY (for the scoring Architect). The corpus was salted via grep so the source
  docs for each conflict are exact.

  THE 6 GENUINE CONFLICTS (a complete answer surfaces ALL six, names both docs each):
    K1. LAUNCH DATE. September 8 (charter, doc 01) vs September 22 (meeting summary,
        doc 09; carried into the finance/status thread doc 13 and the GTM plan doc 14).
        RESOLVABLE: the later planning review (doc 09) explicitly supersedes the
        charter date; the correct value is September 22. A strong answer surfaces it,
        states September 22 wins, AND names the stale charter date (doc 01) as
        superseded - it does not just silently use September 22 without flagging that
        the charter says otherwise.
    K2. DASHBOARD OWNERSHIP. Dana (activity-panel PRD doc 04 - "Dana is the product
        owner for the Globex Insight dashboard"; charter doc 01) vs Theo's platform
        team (engineering notes doc 11 - "owned by Theo's platform team end to end").
        UNRECONCILED in the source (the eng note itself observes product-owner vs
        delivery-owner MAY be the intent, but as written both claim dashboard
        ownership). A strong answer surfaces it as an open ownership ambiguity needing
        a decision, names both docs, and does NOT silently assert one owner.
    K3. AUTH METHOD. SAML SSO (data-pipeline notes doc 06) vs email OTP / one-time
        passcode (design notes doc 10). UNRESOLVED and LOAD-BEARING: it BLOCKS the
        security review from starting (doc 12) and is a driver of the launch slip (docs
        09, 12, 07 RISK-1). A strong answer surfaces it, names both docs, and notes its
        downstream blocking effect on the security review and the launch date. Dropping
        this conflict loses a launch-blocking dependency - the heaviest single miss.
    K4. DATA RETENTION. 90 days mandated (compliance memo doc 08) vs 12 months
        displayed (activity-panel PRD doc 04). RESOLVABLE with a clear correct outcome:
        the compliance 90-day limit is mandated and the 12-month PRD figure CANNOT
        stand (displaying older than 90 days is a compliance violation per doc 08;
        logged as RISK-2 in doc 07). A strong answer surfaces it, names both docs,
        states the 90-day limit governs and the PRD must change, and flags it as a
        legal exposure - it does NOT silently keep the 12-month figure. (Discipline
        sub-point: doc 08 also says billing/invoice history has a separate longer
        retention basis and must NOT be conflated with the 90-day activity limit; a
        model that claims billing history is also capped at 90 days has mis-read.)
    K5. PRIMARY DATASTORE. PostgreSQL (data-pipeline notes doc 06) vs the vendor
        columnar store "Cobalt" (launch/GTM plan doc 14). UNRECONCILED (logged as
        RISK-3 in doc 07). A strong answer surfaces it, names both docs, and flags the
        primary-store decision as open - it does not silently pick one.
    K6. BUDGET. Hard cap 150k (finance/status thread doc 13) vs 220k planned spend
        (launch/GTM plan doc 14). UNRECONCILED and over budget by 70k (logged as RISK-4
        in doc 07; finance states the cap is hard and GTM must come down). A strong
        answer surfaces it, names both docs, states the overage, and flags GTM spend as
        needing to come down to the cap - it does not silently average or ignore it.

  THE 2 NON-CONFLICTS (must NOT be listed as conflicts - flagging either is a
  confidently-wrong false positive, penalised like a missed real conflict):
    N1. USER COUNTS. ~4,000 REGISTERED accounts (usage-panel PRD doc 02) vs ~1,200
        MONTHLY ACTIVE accounts (customer research doc 05). These are DIFFERENT METRICS
        (registered base vs 30-day active), explicitly reconciled in both docs as not
        the same number. NOT a conflict. A model that lists "4,000 vs 1,200 users" as a
        contradiction has invented a conflict.
    N2. SERVING COMPONENTS. The "cache layer" and the "read replica" (both named in
        data-pipeline notes doc 06 and engineering notes doc 11) are SEPARATE
        components serving different purposes (read-burst cache vs analytical-read
        replica), and the two docs AGREE on this. NOT a conflict. A model that frames
        cache-vs-replica as contradictory architecture has invented a conflict.

  DEPENDENCY CHAINS to trace (Reasoning quality signal):
    - The data pipeline (doc 06) is the shared upstream feeding ALL three panels
      (usage doc 02, billing doc 03, activity doc 04).
    - The auth conflict (K3) BLOCKS the security review (doc 12), which is on the
      critical path and drives the launch slip (doc 09).
    - The retention conflict (K4) gates launch as a legal exposure (doc 08 / RISK-2).
    - The usage panel additionally needs the unassigned endpoint-tagging work (RISK-5,
      docs 07/11) before it is complete.
    - The budget conflict (K6) requires the GTM plan (doc 14) to come down to the
      finance cap (doc 13).

  Scoring guidance:
    - Completeness (recall, weight 2.0) = of the 6 genuine conflicts (K1-K6), how many
      are surfaced with both source docs named. Count silently-resolved or missed
      conflicts explicitly. Missing K3 (auth, the load-bearing blocker) or K4
      (retention, the legal exposure) is the heaviest recall miss. Also: were all 14
      docs' key points retained, or were some silently dropped.
    - Correctness (hard-fail eligible) = are the surfaced conflicts real and described
      accurately (right docs, right values, right resolvable-vs-unreconciled call), and
      are the resolvable ones resolved correctly (K1 -> September 22; K4 -> 90-day
      limit governs). Silently picking the WRONG side of a resolvable conflict (e.g.
      asserting the 12-month retention is fine) is a Correctness failure.
    - Hallucination (hard-fail eligible) = inventing a conflict that does not exist (the
      two non-conflicts N1/N2 are the canonical traps), inventing a doc, or asserting a
      value not in the corpus. Flagging N1 or N2 as a conflict is the canonical
      hallucination here.
    - Reasoning quality = did it trace the dependency chains (pipeline -> panels; auth
      conflict -> blocked security review -> launch slip; retention -> legal gate) and
      correctly classify each conflict as resolvable or unreconciled, rather than
      flattening everything into a flat list or silently reconciling.
    - Discipline (decision/judgment task) = surfaced the 6 genuine conflicts WITHOUT
      padding the list with the 2 non-conflicts, and did not silently pick sides. The
      explicit non-flagging of N1/N2 (or treating them as "not a conflict" with a
      one-line reason) is a discipline POSITIVE.
    - Source transparency = every conflict names both source docs; every next-action
      cites the docs that motivate it.
    - Helpfulness = is the briefing decision-grade (a lead can see what is decided,
      what is blocked, and what needs a decision).
    - Format adherence = output envelope plus themed structure with a distinct
      CONFLICTS section.
    Voice match does NOT apply.

    Suggested scoring shorthand for the Architect: conflicts_recall = (genuine
    conflicts surfaced with both docs) / 6; precision_penalty = number of non-conflicts
    falsely flagged (N1, N2) + number of resolvable conflicts resolved on the WRONG
    side. A model that surfaces all 6 genuine conflicts (with both docs each), resolves
    K1 and K4 correctly, flags K2/K3/K5/K6 as unreconciled-and-open, and does NOT flag
    N1 or N2 is the exemplary 5 on Completeness, Correctness, and Discipline. The most
    damaging single failures are: dropping K3 (auth blocker) or K4 (legal retention),
    silently keeping the 12-month retention, or inventing the user-count or
    cache-vs-replica non-conflict - each is confidently-wrong and penalised hardest.
---

# Spec 27 - completeness-under-conflict (the scaled conflict-surfacing probe)

The scaled conflict companion to spec 08. Where spec 08 planted 3 cross-document
conflicts, this plants 6 genuine cross-document conflicts across 14 docs, plus 2
deliberate non-conflicts (look-alikes that reconcile cleanly), about one fictional
product launch ("Globex Insight", an analytics-platform migration + customer dashboard)
under `corpus/completeness-under-conflict/`. The documents are varied in shape (charter,
PRDs, research notes, pipeline notes, risk register, compliance memo, meeting summary,
design notes, engineering notes, security-review notes, finance/status thread, GTM plan)
and they cross-reference each other.

The test runs completeness and discipline under load at once: surface ALL 6 genuine
conflicts (launch date, dashboard ownership, auth method, data retention, primary
datastore, budget) with both source docs named and the resolvable-vs-unreconciled call
made correctly, WITHOUT padding the list with the 2 non-conflicts (registered-vs-active
user counts; cache-layer-vs-read-replica components). Some conflicts are resolvable from
the sources (the launch date - the later meeting supersedes; the retention figure - the
compliance 90-day limit governs and the 12-month PRD figure cannot stand) and some are
genuinely unreconciled (ownership, datastore, budget, and the load-bearing auth conflict
that blocks the security review and drives the launch slip).

The eval runs the standard `/eval-pit` four-phase flow against the frozen
`rubric/rubric.md`. The correctness-first quality principle is central: a
silently-resolved conflict and a falsely-flagged non-conflict are both confidently-wrong
outputs that mislead a lead acting on the briefing, and both are penalised harder than
an honest gap. Load-bearing dimensions: Completeness (recall against the 6-conflict
answer key, none silently dropped), Correctness / Hallucination (real conflicts only,
resolvable ones resolved on the right side, zero invented conflicts), Discipline (the 2
non-conflicts correctly NOT flagged, no silent side-picking), Reasoning quality (the
dependency chains traced, each conflict classified resolvable-vs-unreconciled), and
Source transparency (both docs named per conflict). Voice match does not apply. The
variant pool is 9 (3 models x N=3, effort treated as inert per the methodology). The
corpus is the directory `corpus/completeness-under-conflict/`.
