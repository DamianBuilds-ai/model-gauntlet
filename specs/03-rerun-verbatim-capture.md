---
task_category: verbatim-capture
prompt_under_test: |
  You are given a meeting transcript at corpus/higher-n-verbatim-capture/transcript.md
  for a fictional "Acme" team. Extract the following, WORD-FOR-WORD (no paraphrasing,
  no cleanup, no summarizing), attributing each to the speaker:

    1. The exact statement that defines when the schema freeze starts and what it
       prohibits.
    2. The exact statement that defines the rollback plan.
    3. The exact statement describing the CI check that will be added.

  Reproduce each quote verbatim and name the speaker. Do not reword. If a quote spans
  two sentences, include both. Output envelope required (schemaVersion, tier, status,
  tool_budget_used). No em dashes (spaced hyphens). No emojis.
variant_pool: 12
N: 3
corpus: corpus/higher-n-verbatim-capture/transcript.md
notes: |
  HIGHER-N RERUN (N: 3). Re-runs the stable verbatim-capture task type three times to
  crush the within-model noise floor. Verbatim retrieval is a known Haiku-strong task
  type; the rerun tightens confidence on that finding by measuring single-run variance.
  The failure mode this task probes is "helpful" paraphrasing - a variant that rewords a
  quote fails on Correctness even if the meaning is preserved, because the task is
  verbatim. Score Correctness as exact-match fidelity. Aggregate the 3 passes per variant;
  flag any variant whose fidelity is inconsistent across passes. Reasoning quality is
  skipped (pure retrieval). Voice match does not apply.
---

# Spec 03 - rerun-verbatim-capture (N=3 noise-floor crush)

Higher-N rerun of the verbatim-capture task type. Corpus is
`corpus/higher-n-verbatim-capture/transcript.md`. Run each variant THREE times (N: 3)
and aggregate per the notes. Standard four-phase flow against the frozen rubric. This
is a pure-retrieval task: Correctness means exact-match verbatim fidelity, Reasoning
quality is excluded, and Voice match does not apply.
---
