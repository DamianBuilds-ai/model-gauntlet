---
task_category: instruction-conflict-resolution
prompt_under_test: |
  You are a release engineer for a product called Acme Ledger. You are given a set
  of documents under corpus/instruction-conflict-resolution/ - an engineering
  runbook, a security policy, a release checklist, a recent incident postmortem, and
  a manager's Slack export. Your task: write the step-by-step procedure the on-call
  engineer must follow to ship the v4.2 hotfix that is described in the postmortem.

  Read all the documents. Then produce the hotfix release procedure as a numbered
  list of concrete steps the on-call engineer can follow.

  IMPORTANT: the source documents do not all agree. Where two documents give
  instructions that genuinely conflict, you MUST:
    1. Surface the conflict explicitly in a "CONFLICTS FOUND" section BEFORE the
       procedure: name BOTH source documents, quote or paraphrase both conflicting
       instructions, and state which one governs and WHY.
    2. Resolve it using the documents' own stated authority (a document that says it
       overrides another, a dated decision that supersedes an older one, a policy
       marked mandatory vs a guideline marked recommended). Do not flip a coin and do
       not silently pick a side - the reader must be able to see that a conflict
       existed and why your procedure resolved it the way it did.
    3. If a conflict is genuinely unresolvable from the sources (no document has
       authority over the other and no later decision settles it), flag it as
       UNRESOLVED and say what decision is needed and from whom - do NOT invent an
       answer.

  Discipline rule: surface only GENUINE conflicts. Two documents that cover different
  steps, or that say compatible things in different words, are NOT in conflict -
  listing a non-conflict counts against you exactly as missing a real conflict does.

  Do not invent steps, approvals, or tools that no document mentions. Output envelope
  required (schemaVersion, tier, status, tool_budget_used). No em dashes (spaced
  hyphens). No emojis.
variant_pool: 9
corpus: corpus/instruction-conflict-resolution/
corpus_intent: 5 cross-referencing release/ops docs for one fictional product (Acme Ledger) containing 2 genuine, authority-resolvable instruction conflicts + 1 genuinely unresolvable conflict + 2 planted non-conflicts (look-alikes that are compatible)
corpus_delivered: TBD
corpus_match: TBD
notes: |
  NEW task type. Tests whether a model surfaces and correctly RESOLVES genuine
  instruction conflicts in a multi-doc operational corpus, rather than silently
  picking a side (the dangerous failure) or padding with false-positive conflicts.
  This is the conflict-RESOLUTION cousin of spec 27 (completeness-under-conflict):
  27 asks "find every conflict"; 55 asks "find them AND resolve each using the
  documents' own authority, and know which one you cannot resolve". The corpus is a
  NEW scenario (Acme Ledger, a hotfix release), deliberately not reusing spec 27's
  Globex or spec 08's Northwind, so the old answer cannot be pattern-matched.

  This is a JUDGMENT / DECISION task, so the conditional rubric dimensions Helpfulness
  (1.25) and Discipline (1.25) apply; Voice match does not.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): silently resolving a
  conflict the WRONG way is the worst outcome - worse than an honest "these two
  disagree and I cannot tell which wins". A procedure that quietly tells the on-call
  engineer to push straight to production (following the old runbook) when the newer
  security policy mandates a staged canary first has produced a confidently-wrong
  artifact a tired on-call engineer would execute at 3am. Reward the model that
  surfaces each conflict, cites the governing document, and flags the one conflict it
  genuinely cannot resolve. Penalise hardest the model that silently picks the wrong
  side and presents a clean, authoritative-looking procedure with no conflict section.
  A model that picks the RIGHT side but never tells the reader a conflict existed is
  also penalised (it got lucky; the reader cannot audit it).

  ANSWER KEY (for the scoring Architect - the conflicts as the corpus actually states
  them):

    GENUINE CONFLICT C1 (RESOLVABLE - the security policy governs):
      - The engineering runbook (runbook.md) says hotfixes may be pushed directly to
        production to minimise time-to-fix: "for hotfixes, skip the canary and deploy
        straight to prod".
      - The security policy (security-policy.md) says ALL production deploys,
        including hotfixes, MUST go through a 10% canary for at least 15 minutes, and
        the policy header states it is MANDATORY and "overrides any conflicting
        guidance in team runbooks".
      - RESOLUTION: the security policy governs (it is marked mandatory AND explicitly
        says it overrides runbooks). Correct procedure = staged 10% canary for 15 min
        before full rollout. A procedure that skips the canary is CONFIDENTLY WRONG.

    GENUINE CONFLICT C2 (RESOLVABLE - the newer dated decision supersedes):
      - The release checklist (release-checklist.md, dated 2026-01-10) says the
        release approver is the Team Lead.
      - The manager's Slack export (slack-export.md, dated 2026-04-02) states a
        decision: "from now on hotfix approvals go through the on-call SRE, not the
        Team Lead - effective immediately". This is the more recent dated decision.
      - RESOLUTION: the 2026-04-02 Slack decision supersedes the older checklist (later
        dated decision wins; the Slack message explicitly says "from now on" and
        "effective immediately"). Correct approver = on-call SRE. A procedure naming
        the Team Lead as approver is wrong (used the stale checklist).

    GENUINE CONFLICT C3 (UNRESOLVABLE - flag it, do NOT invent an answer):
      - The runbook says to run the smoke-test suite "tag: critical" before promoting
        a hotfix.
      - The incident postmortem (postmortem.md) says the critical smoke tests are
        currently FLAKY and gave a false-green during the incident, and recommends
        running the FULL regression suite for this hotfix instead - but it is written
        as a recommendation ("we should consider"), is NOT marked as a policy or a
        decision, and no document grants the postmortem authority to override the
        runbook. There is no dated decision adopting the recommendation.
      - RESOLUTION: GENUINELY UNRESOLVED. The postmortem only recommends; nothing
        adopts the recommendation as binding, and the runbook is not marked
        overridable on this point. A strong answer FLAGS this as unresolved and says a
        decision is needed (e.g. from the Team Lead or SRE: do we trust the flaky
        critical smoke tests for this hotfix, or block on the full regression?). A
        model that silently picks either the runbook OR the postmortem and presents it
        as settled is wrong - the skill is recognising that authority is absent here.

    PLANTED NON-CONFLICT N1 (do NOT flag): the runbook says "deploy from the
    release/* branch" and the checklist says "tag the release commit as v{version}".
    These are compatible, sequential steps, NOT a conflict. Flagging it is a precision
    error.

    PLANTED NON-CONFLICT N2 (do NOT flag): the security policy requires "2FA on the
    deploy tool" and the runbook requires "VPN connection to deploy". Both are access
    requirements that coexist - satisfying both is required, neither contradicts the
    other. Flagging it as a conflict is a precision error.

  Scoring guidance:
    - Correctness (hard-fail eligible): did it resolve C1 toward the canary (security
      policy governs) and C2 toward the on-call SRE (newer decision supersedes), and
      did it correctly identify C3 as unresolved? A procedure that silently skips the
      canary (C1 wrong) or names the Team Lead approver (C2 wrong) is Correctness=1
      territory - it is a confidently-wrong operational instruction. Resolving C3 by
      inventing a binding answer is also a correctness failure.
    - Completeness: were all THREE genuine conflicts (C1, C2, C3) surfaced in the
      CONFLICTS FOUND section?
    - Discipline (judgment task): did it resist flagging the two non-conflicts (N1,
      N2) as conflicts? Padding the conflict list with false positives is the
      precision failure and counts against the score.
    - Reasoning quality (the differentiator): for each resolved conflict, did it cite
      the SPECIFIC source of authority (policy marked mandatory + overrides-runbooks
      clause for C1; the 2026-04-02 dated decision for C2) rather than asserting a
      resolution with no basis? And did it correctly reason that C3 lacks any such
      authority?
    - Helpfulness (judgment task): is the final numbered procedure something an
      on-call engineer could actually execute, with the resolved conflicts baked in
      correctly and the unresolved one flagged for a decision rather than blocking the
      whole procedure?
    - Format adherence: the CONFLICTS FOUND section BEFORE the numbered procedure, plus
      a clean output envelope.
    - Hallucination (hard-fail eligible): inventing an approval, a tool, a branch
      name, or a policy clause that no document states.
    - Source transparency: does it name the specific documents behind each conflict
      and each procedure step rather than speaking in generic release-process
      boilerplate?
    Voice match does NOT apply.
---

# Spec 55 - instruction-conflict-resolution (two docs that genuinely disagree)

Given five cross-referencing operational documents for a fictional product (Acme
Ledger) under `corpus/instruction-conflict-resolution/` - a runbook, a security
policy, a release checklist, an incident postmortem, and a manager's Slack export -
produce the step-by-step procedure to ship a hotfix. Standard four-phase `/eval-pit`
flow against the frozen `rubric/rubric.md`.

The defining skill is surfacing genuine instruction conflicts and resolving each using
the documents' OWN stated authority, while recognising the one conflict that is
genuinely unresolvable. The corpus plants three real conflicts: C1, the runbook says
"skip the canary for hotfixes" while the security policy mandates a 10% canary and
states it overrides runbooks (RESOLVABLE - the policy governs); C2, the older release
checklist names the Team Lead as approver while a newer dated Slack decision moves
hotfix approval to the on-call SRE (RESOLVABLE - the later decision supersedes); and
C3, the runbook says run the critical smoke tests while the postmortem recommends the
full regression suite because the smoke tests are flaky, but only as a non-binding
recommendation with no authority to override (genuinely UNRESOLVED - flag it, do not
invent an answer). It also plants two non-conflicts (compatible sequential steps;
co-existing access requirements) that a weaker model may pad the conflict list with.

This is the correctness-first quality principle in an operational setting: silently
resolving a conflict the WRONG way (telling a 3am on-call engineer to skip the
mandated canary) is worse than an honest "these disagree and I cannot tell which
wins". Correctness is hard-fail eligible - a confidently-wrong operational instruction
is a wrong answer, not merely an incomplete one. Reasoning quality (citing the
specific source of authority per conflict) is the differentiator; Discipline covers
resisting false-positive conflicts; Helpfulness covers whether the procedure is
executable. Voice match does not apply. The corpus is the directory
`corpus/instruction-conflict-resolution/`.
