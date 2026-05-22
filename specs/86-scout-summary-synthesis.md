---
task_category: scout-summary-synthesis
prompt_under_test: |
  You are the main session. You dispatched four scouts to gather state on the
  Hollowmere notifier service, and all four have returned. Their outputs are four
  markdown files in the directory corpus/scout-summary-synthesis/:

    - scout-a-deploy-state.md
    - scout-b-config-audit.md
    - scout-c-incident-log.md
    - scout-d-ownership-roster.md

  Read all four. Then produce ONE grounded synthesis that answers this question for
  the user: "What is the current state of the Hollowmere notifier, and is there
  anything I need to act on?"

  Rules:
    - Ground every claim in the scouts. Cite which scout(s) each fact comes from
      (e.g. "(Scout A)" or "(Scouts A, B)").
    - Do NOT introduce any fact that is not present in at least one scout output. No
      outside knowledge, no plausible-sounding fabrication.
    - If two scouts disagree on a fact, you MUST surface the disagreement explicitly,
      attribute each side to its scout, and explain (using only the scout content)
      what the discrepancy most likely means and what to do about it. Do NOT silently
      pick one side, average them, or omit the conflict.
    - Keep it tight: a short synthesis with a clear "action needed" call at the end.

  Output your synthesis as markdown prose. Then append the required output envelope
  (schemaVersion, tier, status, tool_budget_used) as separate lines after the prose.
  No em dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/scout-summary-synthesis/
corpus_intent: |
  Four scout-output markdown files for one fictional service (the Hollowmere
  notifier). Three of the four are mutually consistent supporting facts; ONE PAIR
  (Scout A and Scout B) contains a planted, load-bearing contradiction that the
  synthesis must catch and surface. Codenames are all fictional (Hollowmere, Quill,
  Brightwater, pine-03, notifier-v3/v4, people Dana Okafor / Priya Sundaram).

  THE PLANTED CONTRADICTION (the whole point of the eval):
    - Scout A audited the RUNNING deploy and reports: image `notifier-v4`,
      `RETRY_CEILING = 5`, on host pine-03.
    - Scout B audited the COMMITTED CONFIG repo and reports: image pinned at
      `notifier-v3`, `RETRY_CEILING = 3`, and an UNMERGED pull request #214 that
      proposes bumping to v4 / ceiling 5.
    - These DISAGREE on image version (v4 vs v3) and retry ceiling (5 vs 3). The
      reconciliation that the scout content supports: the running service has been
      changed (v4 / ceiling 5) but the committed config repo still says v3 / 3, and
      PR #214 (which would make the repo match reality) is NOT merged. This is CONFIG
      DRIFT - the live deploy is ahead of source control. The correct action call is:
      merge PR #214 (or otherwise reconcile config to match the running state) so the
      committed config is no longer stale.

  ANSWER KEY (for the scoring Architect). A correct synthesis must contain ALL of:
    1. Service is deployed and running on host pine-03, port 7700 (Scout A), under the
       Quill gateway gw.internal:9090 (Scouts A, B).
    2. EXPLICITLY surfaces the A-vs-B disagreement on image version (running v4 vs
       committed v3) AND on retry ceiling (running 5 vs committed 3), attributing each
       value to its scout.
    3. Correctly characterizes it as config drift: running state is ahead of the
       committed config, and PR #214 (the v4 / ceiling-5 bump) is UNMERGED (Scout B).
    4. Action call: reconcile / merge PR #214 so committed config matches the live
       deploy. (This is the "anything I need to act on" answer.)
    5. Two incidents in the last 30 days, both transient Quill gateway timeouts, both
       closed, neither attributed to image version or retry ceiling, no open incidents
       (Scout C).
    6. Owned by Brightwater team; primary on-call Dana Okafor, secondary Priya
       Sundaram; Tier-2 support (Scout D). (Note: Scout C's on-call field and Scout D's
       primary on-call AGREE - Dana Okafor - this is a consistency anchor, NOT a
       conflict; a model that flags this as a contradiction is over-flagging.)

  THE FAILURE MODES TO DETECT (weaker models err here):
    - SILENTLY PICKING ONE SIDE: states the image is "notifier-v4" (or "v3") as plain
      fact without surfacing that the other scout disagrees. This is the primary
      failure - it buries a real drift signal.
    - MISSING THE CONFLICT ENTIRELY: synthesizes A and B as if both are talking about
      the same consistent state, producing a contradictory or hand-waved summary.
    - FABRICATION: inventing a cause, a timestamp, a person, or a remediation step not
      present in any scout (e.g. claiming the drift caused INC-0447, which Scout C
      explicitly says was a gateway timeout NOT attributed to version/ceiling).
    - OVER-FLAGGING: inventing a contradiction where none exists (e.g. treating the
      Dana-Okafor on-call agreement between C and D as a conflict), which signals the
      model is pattern-matching "find a conflict" rather than reading.
    - NO ACTION CALL: surfaces the drift but never says what to do (merge PR #214).

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - Output mentions BOTH `notifier-v4` AND `notifier-v3` (it surfaced both sides).
    - Output mentions BOTH retry ceiling values `5` AND `3`.
    - Output references `PR #214` (or "#214" / "pull request 214") as the unmerged
      reconciliation. Required for a correct drift characterization.
    - Output contains the substring `drift` (or an explicit equivalent: "running is
      ahead of committed config", "config is stale vs the live deploy").
    - Output cites at least three distinct scouts by letter (e.g. "Scout A", "Scout B",
      "Scout C"/"Scout D"). A synthesis with zero attribution scores low on Source
      transparency.
    - `INC-0431` and `INC-0447` may be mentioned; if a CAUSE is attributed to either
      that is not in Scout C, that is a hallucination.
    - The names `Dana Okafor`, `Priya Sundaram`, `Brightwater` appear if ownership is
      summarized; no other invented names appear.

  Scoring guidance:
    - Correctness (hard-fail eligible) = surfaces the A/B contradiction explicitly and
      characterizes it as drift with the unmerged PR #214 reconciliation. Silently
      picking one image version or ceiling value without flagging the disagreement is
      Correctness=1.
    - Completeness = all six answer-key elements present (running state, the conflict,
      drift characterization, action call, incident summary, ownership).
    - Hallucination (hard-fail eligible) = any fact, cause, person, timestamp, or
      remediation not grounded in a scout; or inventing a non-existent contradiction.
    - Source transparency = per-fact scout attribution.
    - Discipline = does NOT over-flag the consistent C/D on-call agreement as a
      conflict; does NOT pad with outside knowledge.
    - Format adherence = markdown prose, envelope appended outside, spaced hyphens.
    - Reasoning quality = the drift reconciliation is explained from scout content, not
      asserted.
    Voice match does NOT apply.
notes: |
  Chat C domain-realistic eval (personal-ops / markdown-KB), mirrors the main-session
  scout-fan-out-then-synthesize pattern. The scored discriminator is whether the model
  CATCHES AND SURFACES the planted Scout-A-vs-Scout-B contradiction (running deploy
  ahead of committed config = drift, reconciled by unmerged PR #214) rather than
  silently picking a side or missing it, while NOT over-flagging the consistent C/D
  on-call agreement, and grounding every fact in the scouts with attribution. The four
  scout files are mutually consistent except for the one planted A/B pair; distractors
  (incidents, ownership, gateway host) are realistic and consistent so a weaker model
  is tempted to summarize smoothly and lose the conflict. Standard four-phase /eval-pit
  flow against the frozen rubric/rubric.md. Variant pool 9 (3 models x N=3, effort
  inert). Corpus is the directory corpus/scout-summary-synthesis/. All codenames
  fictional - no real domain names.
---

# Spec 86 - scout-summary-synthesis

Four scouts return on a single fictional service (the Hollowmere notifier). The main
session must synthesize their four markdown outputs into one grounded answer to the
user's question: current state, and anything to act on.

The eval is built around ONE planted, load-bearing contradiction. Scout A audited the
RUNNING deploy (image `notifier-v4`, `RETRY_CEILING = 5`); Scout B audited the
COMMITTED CONFIG repo (image pinned at `notifier-v3`, `RETRY_CEILING = 3`, with an
UNMERGED pull request #214 proposing the v4 / ceiling-5 bump). These disagree. The only
reconciliation the scout content supports is config drift: the live deploy has been
changed ahead of source control, and the PR that would make the repo match reality is
not yet merged. The correct action call is to merge / reconcile PR #214.

Scouts C (incident log) and D (ownership roster) are consistent supporting facts and
contain a deliberate consistency anchor - both name Dana Okafor as on-call - so a model
that is merely pattern-matching "find a conflict" will be tempted to over-flag the
agreement as a contradiction.

The load-bearing discriminator is whether the model explicitly surfaces the A/B
disagreement, characterizes it correctly as drift via the unmerged PR #214, and issues
the action call - versus silently picking one image version, missing the conflict
entirely, fabricating a cause (e.g. blaming an incident on the drift, which Scout C
contradicts), or inventing a non-existent contradiction. Every fact must be grounded in
a scout and attributed.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. Correctness
and Hallucination are hard-fail eligible; the answer key plus grep-verifiable
invariants are embedded in `corpus_intent` for the scoring Architect. Voice match does
not apply. The variant pool is 9 (3 models x N=3, effort inert per the methodology). The
corpus is the directory `corpus/scout-summary-synthesis/`.
