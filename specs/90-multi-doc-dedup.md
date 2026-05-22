---
task_category: multi-doc-dedup
prompt_under_test: |
  You are given six overlapping documents about a fictional deployment tool called
  Larkfield, in the directory corpus/multi-doc-dedup/:

    - doc-1-onboarding.md
    - doc-2-deploy-runbook.md
    - doc-3-staging-guide.md
    - doc-4-prod-policy.md
    - doc-5-secrets-note.md
    - doc-6-gotchas.md

  The docs repeat a lot of the same basic facts. Your job is to produce ONE
  consolidated reference document that:
    - Removes the true duplicate content (facts repeated across docs are stated ONCE).
    - PRESERVES every unique fact - any fact that appears in only one (or a few) of the
      docs and is NOT part of the common repeated set must survive into the merged doc.
    - Loses zero information. If you are unsure whether something is a duplicate or a
      unique detail, keep it.

  Do NOT invent any fact that is not in the source docs. Do NOT drop a unique fact just
  because it appeared only once.

  Output the consolidated reference as markdown. Then append the required output
  envelope (schemaVersion, tier, status, tool_budget_used) as separate lines after the
  document. No em dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/multi-doc-dedup/
corpus_intent: |
  Six overlapping fictional docs about one deployment tool (Larkfield). The eval tests
  DEDUP WITH ZERO UNIQUE-FACT LOSS - recall (every buried unique fact survives) AND
  precision (true duplicates collapsed to one statement). The trap: the docs share a
  large COMMON set of repeated facts, so a model summarizing for brevity is tempted to
  also drop the unique facts that sit among the duplicates. All codenames fictional
  (Larkfield, lark ship, larkfield.yaml, #larkfield-deploys, vault.internal).

  THE COMMON (DUPLICATED) FACTS - appear in 4+ docs, must be stated EXACTLY ONCE in the
  merged doc (stating each more than once is a precision miss, not a fatal error):
    C1. Larkfield deploys to three environments: dev, staging, prod.
    C2. Deploy command is `lark ship <env>`.
    C3. Prod deploys require two approvals.
    C4. Config lives in `larkfield.yaml` at the repo root.
    C5. Deploy notices post to the `#larkfield-deploys` Slack channel.

  THE BURIED UNIQUE FACTS - each must SURVIVE into the merged doc (this is the scored
  recall set; dropping any one is the core failure):
    U1 (doc-1): the prod two-approval rule was ADDED AFTER THE 2026-01 OUTAGE; before
        that prod needed only ONE approval. (Historical origin - easy to drop as
        "background".)
    U2 (docs 2 + 6): rollback command is `lark rollback <env>`, reverting to the
        previous shipped build. (Appears in TWO docs - it is a real shared fact, not a
        per-doc unique, but it is NOT in the common C-set and MUST be preserved; merge
        the two mentions into one.)
    U3 (doc-3): staging AUTO-DEPLOYS the latest main branch every night at 01:00; manual
        ship to staging is only needed for an off-cycle build. (Also: staging requires
        no approvals - a minor unique detail; preserving it is a bonus, not required for
        a pass, but inventing a different approval count for staging is an error.)
    U4 (doc-4): prod deploys are only permitted in the deploy window 09:00 to 16:00 on
        weekdays; outside it `lark ship prod` is rejected unless an incident override
        flag is set.
    U5 (doc-5): secrets are NOT in larkfield.yaml; they are pulled at deploy time from
        the vault at `vault.internal/larkfield`, and the deploy token must be rotated
        every 30 days or `lark ship` fails with an auth error.
    U6 (doc-6): the dev environment SHARES A DATABASE with staging; a destructive
        migration in dev WILL affect staging data; use a fresh schema name when testing
        migrations in dev.

  ANSWER KEY (for the scoring Architect): the merged doc must contain ALL SIX unique
  facts U1-U6 (recall = 6/6) and should state each common fact C1-C5 once (precision).
  A perfect score is 6/6 unique facts preserved, common facts not duplicated, nothing
  invented. Each dropped unique fact is a recall loss; each common fact repeated
  verbatim multiple times is a minor precision loss.

  THE FAILURE MODES TO DETECT (weaker models err here):
    - DROPPING a buried unique fact while keeping the common scaffolding - especially U1
      (the historical outage origin, reads like skippable background) and U3's 01:00
      auto-deploy detail. This is the primary failure: a clean-looking merged doc that
      silently lost a unique fact.
    - Treating U2 (rollback) as fully redundant and dropping it because it appeared in
      two docs, OR keeping it twice (failing to merge the two mentions).
    - FABRICATION: inventing a fact not in any doc (a fourth environment, a different
      rotation interval, a CI tool name).
    - Over-collapsing: merging U5 (no secrets in larkfield.yaml) and C4 (config in
      larkfield.yaml) into a single contradictory statement instead of keeping both
      (config IS in larkfield.yaml; secrets are NOT, they come from the vault).

  GREP-VERIFIABLE INVARIANTS (for the Architect - each must appear in the merged doc):
    - U1: mentions `2026-01` outage AND that prod previously needed `one` approval
      (or "single approval"). Both halves preserved.
    - U2: `lark rollback` appears (the rollback command survives) - and ideally only
      once.
    - U3: `01:00` (or "nightly"/"every night") AND `auto-deploy` (or "automatically
      deploys") for staging from `main`.
    - U4: the prod deploy window `09:00` and `16:00` (or "9 to 5"/"weekdays window")
      AND the `incident override` exception.
    - U5: `vault.internal/larkfield` AND the `30 days` token rotation.
    - U6: dev `shares a database` (or "shared database") with staging AND the destructive
      migration warning.
    - Common facts: `lark ship`, `larkfield.yaml`, `two approvals`, `#larkfield-deploys`,
      `dev, staging, prod` each appear (present) but NOT repeated many times.
    - No invented environment beyond dev/staging/prod; no rotation interval other than
      30 days; no Slack channel other than #larkfield-deploys.

  Scoring guidance:
    - Correctness (hard-fail eligible) = all six unique facts U1-U6 preserved AND no
      invented fact AND the config-vs-secrets distinction (C4 vs U5) kept non-
      contradictory. Dropping a unique fact or merging C4/U5 into a contradiction is
      Correctness=1.
    - Completeness = recall: count of U1-U6 present (target 6/6).
    - Hallucination (hard-fail eligible) = any fact not in the source docs.
    - Discipline = precision: true duplicates collapsed to one statement; the merged doc
      is genuinely deduplicated, not just six docs concatenated.
    - Format adherence = single consolidated markdown doc, envelope outside, spaced
      hyphens.
    - Reasoning quality = SKIP-eligible (the output is the merged doc).
    Voice match does NOT apply.
notes: |
  Chat C domain-realistic eval (personal-ops / markdown-KB), the multi-doc-dedup task
  type. The scored discriminator is RECALL + PRECISION on a merge: zero unique-fact loss
  (all six buried unique facts U1-U6 survive) while collapsing the heavily-repeated
  common facts (C1-C5) to single statements. Six overlapping fictional Larkfield docs
  share a large common scaffolding so a model summarizing for brevity is tempted to drop
  the unique facts that sit among the duplicates - especially the historical outage
  origin (U1) and the staging auto-deploy detail (U3). A secondary trap is the
  config-vs-secrets pair (config IS in larkfield.yaml C4; secrets are NOT, they come
  from the vault U5) which must not be collapsed into a contradiction, and the rollback
  fact (U2) which appears in two docs and must be merged once, not dropped or
  duplicated. Standard four-phase /eval-pit flow against the frozen rubric/rubric.md.
  Correctness and Hallucination are hard-fail eligible; the answer key (every planted
  unique fact U1-U6 + the common-fact set) plus grep-verifiable invariants are embedded
  in corpus_intent. Voice match does not apply. Variant pool 9 (3 models x N=3, effort
  inert). Corpus is the directory corpus/multi-doc-dedup/. All codenames fictional - no
  real domain names.
---

# Spec 90 - multi-doc-dedup

Consolidate six overlapping fictional docs about a deployment tool (Larkfield) into one
reference, removing true duplicates while preserving every unique fact. The corpus is
the six docs in corpus/multi-doc-dedup/.

The eval tests recall plus precision on a merge. The six docs share a large common set
of repeated facts (three environments, the `lark ship` command, the two-approval prod
rule, `larkfield.yaml`, the `#larkfield-deploys` channel), and each doc also carries a
buried unique fact that does NOT appear in the common set: the historical origin of the
two-approval rule (the 2026-01 outage, U1), the rollback command (U2, shared by two
docs), the staging nightly auto-deploy at 01:00 (U3), the prod deploy window with its
incident override (U4), the vault-sourced secrets and 30-day token rotation (U5), and
the dev/staging shared-database migration gotcha (U6).

The load-bearing discriminator is zero unique-fact loss while genuinely deduplicating
the common scaffolding. A model summarizing for brevity is tempted to drop the unique
facts that read like background - U1 and U3 are the highest-signal drops. A secondary
trap is collapsing the config-vs-secrets pair into a contradiction (the config IS in
larkfield.yaml; secrets are NOT, they come from the vault) and either dropping or
double-keeping the rollback fact that appears in two docs.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. Correctness
and Hallucination are hard-fail eligible; the answer key (every planted unique fact
U1-U6 plus the common-fact set) and grep-verifiable invariants live in `corpus_intent`
for the scoring Architect. Voice match does not apply. The variant pool is 9 (3 models x
N=3, effort inert per the methodology). The corpus is the directory
`corpus/multi-doc-dedup/`.
