---
task_category: multi-file-synthesis
prompt_under_test: |
  You are given two source files under corpus/higher-n-multi-file-synthesis/:
  release-notes.md (what shipped and what is planned) and feedback.md (a user
  feedback digest) for a fictional "Acme" dev-tools product.

  Produce ONE structured product brief that:
    1. Connects each piece of user feedback to the relevant release-note item where a
       link exists (the value is the cross-file connection, not two separate lists).
    2. Surfaces the top 3 priorities by combined signal (shipped state + user demand +
       any flagged risk).
    3. Calls out one place the two files reinforce each other and one open question
       neither resolves.
    4. Ends with 3 to 5 recommended next actions, each tied to its evidence.
  Do not invent facts. Output envelope required (schemaVersion, tier, status,
  tool_budget_used). No em dashes (spaced hyphens). No emojis.
variant_pool: 12
N: 3
corpus: corpus/higher-n-multi-file-synthesis/
notes: |
  HIGHER-N RERUN (N: 3). Re-runs the stable multi-file-synthesis task type three
  times to crush the within-model noise floor - the same prompt + corpus is scored
  across 3 independent passes per variant so we can separate true model skill from
  single-run variance. This corpus is intentionally close in shape to the EXAMPLE eval
  (overlapping shipped/feedback/planned threads) so the rerun is comparable. Aggregate
  the 3 passes per variant (mean weighted total, flag any variant whose passes diverge
  by more than 0.5 - that is itself a finding about model consistency). Voice match
  does not apply.
---

# Spec 02 - rerun-multi-file-synthesis (N=3 noise-floor crush)

Higher-N rerun of the multi-file-synthesis task type. Corpus is the directory
`corpus/higher-n-multi-file-synthesis/`. Run each variant THREE times (N: 3) and
aggregate per the notes. Standard four-phase flow against the frozen rubric. The
point of the rerun is consistency measurement, not a new task class. Voice match
does not apply.
