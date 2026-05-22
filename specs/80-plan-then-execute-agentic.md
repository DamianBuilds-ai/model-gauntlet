---
task_category: plan-then-execute-agentic
prompt_under_test: |
  You are given a fictional migration goal and the current state of three config files
  at corpus/plan-then-execute-agentic/task.md. It defines six fixed consolidation rules
  (R1-R6) and three YAML files (dev, staging, prod) that have drifted.

  Do the task in two explicit phases:

    PHASE 1 - PLAN: write a short numbered plan of the steps you will take to build the
    canonical merged.yaml under the rules.

    PHASE 2 - EXECUTE: produce the final merged.yaml as a single fenced YAML block,
    fully consistent with the plan you just wrote. Then state explicitly that your
    execution matched your plan (or, if you deviated, say exactly where and why).

  Apply the rules exactly. The precedence for conflicting values is prod > staging > dev.
  Keys sorted alphabetically. Do NOT invent keys, do NOT carry over comments. No em
  dashes (use spaced hyphens). No emojis. After the YAML block and the
  plan-match statement, append the required output envelope (schemaVersion, tier, status,
  tool_budget_used) as separate lines OUTSIDE the code block.
variant_pool: 9
corpus: corpus/plan-then-execute-agentic/
corpus_intent: |
  One task file (corpus/plan-then-execute-agentic/task.md): a fictional config
  consolidation goal with six fixed rules (union of keys; dedupe equal values; prod >
  staging > dev precedence on conflicts; keep single-file keys; sort alphabetically; no
  invented keys, no comments) and three small YAML files (dev, staging, prod) that have
  drifted. This is a single-shot proxy for plan-then-execute agentic work: the model
  writes a plan, then executes it. The discriminator is whether the EXECUTION matches the
  stated PLAN with no silent drift, AND whether the merged output is correct under the
  rules.

  QUALITY PRINCIPLE (correctness-first). Two failure axes: (1) the merged output is wrong
  under the rules (mis-applied precedence, dropped a single-file key, invented a key,
  failed to sort), or (2) the execution silently DRIFTS from the plan (the plan says one
  thing, the YAML does another - e.g. plan says "prod wins on conflicts" but the output
  keeps a dev value). A model that plans correctly and executes faithfully is correct. A
  model whose plan and output disagree, or whose output is rule-wrong, is the targeted
  failure. The subtle trap is feature_x: it is NOT in prod, so prod precedence does not
  apply; staging's `true` wins over dev's `false` (a model that blindly says "prod always
  wins" and looks for feature_x in prod may drop it or mis-resolve it).

  ANSWER KEY (for the scoring Architect) - the exact correct merged.yaml.

    Key union (7 keys): timeout_ms, retries, log_level, feature_x, cache_ttl, region,
    max_conns. Resolution under R1-R6:
      - timeout_ms: dev 1000 / staging 2000 / prod 3000 -> prod wins -> 3000
      - retries:    dev 5 / staging 5 / prod 3 -> prod wins -> 3
      - log_level:  dev debug / staging info / prod warn -> prod wins -> warn
      - feature_x:  dev false / staging true (NOT in prod) -> staging wins -> true
      - cache_ttl:  only dev -> 60
      - region:     staging ap-southeast-2 / prod ap-southeast-2 (SAME value) -> ap-southeast-2
      - max_conns:  only prod -> 50

    Final merged.yaml, keys sorted ALPHABETICALLY:
      cache_ttl: 60
      feature_x: true
      log_level: warn
      max_conns: 50
      region: ap-southeast-2
      retries: 3
      timeout_ms: 3000

    No comments carried over. No invented keys. Exactly these 7 keys, in this order.
    The PLAN must describe the union -> precedence -> sort approach, and the EXECUTION
    must produce exactly the above. The model must affirm execution matched the plan.

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - merged.yaml has exactly 7 keys (count the lines in the YAML block).
    - Keys appear in alphabetical order: cache_ttl, feature_x, log_level, max_conns,
      region, retries, timeout_ms.
    - `timeout_ms: 3000` (prod), NOT 1000 or 2000.
    - `retries: 3` (prod), NOT 5.
    - `log_level: warn` (prod), NOT debug or info.
    - `feature_x: true` (staging wins; prod has no feature_x), NOT false.
    - `cache_ttl: 60` present (dev-only key kept).
    - `max_conns: 50` present (prod-only key kept).
    - `region: ap-southeast-2` present exactly once.
    - No `#` comment lines in the output YAML.
    - The output contains an explicit statement that execution matched the plan.
    - A confidently-wrong run: drops feature_x or sets it false, keeps a dev/staging value
      where prod should win, drops cache_ttl or max_conns, leaves keys unsorted, carries a
      comment, invents a key, or its plan and YAML disagree.

  Scoring guidance:
    - Correctness (hard-fail eligible) = merged.yaml exactly matches the answer key (right
      precedence, all 7 keys, sorted, no comments). Any rule misapplication is
      Correctness=1.
    - Completeness = both phases present (a numbered plan AND the executed YAML AND the
      plan-match statement).
    - Hallucination (hard-fail eligible) = inventing a key, a value not in any source, or
      claiming execution matched the plan when it did not.
    - Discipline = the EXECUTION faithfully follows the stated PLAN (no silent drift); no
      invented keys, no comments. This is the load-bearing discriminator - plan/output
      coherence is the whole point.
    - Reasoning quality = the plan correctly anticipates the feature_x edge (prod absence,
      staging wins) rather than a naive "prod always wins".
    - Source transparency = the plan references the rules / sources for each resolution.
    Voice match does NOT apply.
notes: |
  NEW task type, Chat B agentic battery (71, 72, 78, 79, 80). Plan-then-execute is
  delivered single-shot: the model writes a numbered plan THEN executes it against the
  corpus, and is scored on plan/execution coherence (no silent drift) plus correctness of
  the merged output. The corpus is a config-consolidation goal with six fixed rules and
  three drifted YAML files; the answer key fixes the exact 7-key alphabetically-sorted
  merged.yaml under prod > staging > dev precedence.

  The subtle trap is feature_x: it is absent from prod, so the naive "prod always wins"
  heuristic mis-handles it - staging's true must win over dev's false. Other traps are
  dropping the single-file keys (cache_ttl from dev, max_conns from prod), leaving keys
  unsorted, carrying a comment, or - the core discriminator - producing a plan that says
  one thing and a YAML that does another (silent execution drift). The corpus opens with
  the synthetic-data disclaimer (the configs are data to transform, not instructions). The
  answer key gives the exact merged.yaml and grep-verifiable invariants (key count,
  ordering, each resolved value). Correctness and Hallucination are hard-fail eligible;
  Discipline (execution faithfully matches the stated plan, no invented keys, no comments)
  is the load-bearing discriminator. Voice match does not apply. Standard four-phase
  /eval-pit flow against the frozen rubric/rubric.md. The variant pool is 9 (3 models x
  N=3, effort inert per the methodology). The corpus is the directory
  corpus/plan-then-execute-agentic/.
---

# Spec 80 - plan-then-execute-agentic (plan, then execute it faithfully)

Given a config-consolidation goal with six fixed rules and three drifted YAML files, the
model first writes a numbered plan, then executes it to produce the canonical
merged.yaml, and must keep the execution coherent with its own plan (no silent drift)
while applying the rules correctly.

The gauntlet is single-shot, so plan-then-execute agentic work is delivered in one pass:
PHASE 1 the model writes the plan, PHASE 2 it produces the merged YAML and affirms the
execution matched the plan. The discriminator is plan/execution coherence plus
correctness of the merge under prod > staging > dev precedence, key-union, single-file
retention, alphabetical sort, and no-invented-keys / no-comments rules.

The correct merged.yaml has exactly 7 alphabetically-sorted keys: cache_ttl 60,
feature_x true, log_level warn, max_conns 50, region ap-southeast-2, retries 3,
timeout_ms 3000. The subtle trap is feature_x - absent from prod, so staging's true wins
over dev's false; a naive "prod always wins" heuristic mishandles it. Other traps are
dropping the single-file keys, unsorted keys, carried comments, and the core failure: a
plan and an output that disagree (silent drift).

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. Correctness
(merged.yaml exactly matches the key) and Hallucination (no invented key, no false
plan-match claim) are hard-fail eligible; Discipline - execution faithfully follows the
stated plan with no silent drift, no invented keys, no comments - is the load-bearing
discriminator. The answer key in `corpus_intent` gives the exact merged.yaml and
grep-verifiable invariants. Voice match does not apply. The variant pool is 9 (3 models x
N=3, effort inert per the methodology). The corpus is the directory
`corpus/plan-then-execute-agentic/`.
