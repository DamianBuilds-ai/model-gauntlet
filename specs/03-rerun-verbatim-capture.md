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
variant_pool: 9
corpus: corpus/higher-n-verbatim-capture/transcript.md
notes: |
  NOISE-FLOOR RERUN. This eval is about within-model consistency on the stable
  verbatim-capture task type. Under v1.5 the 9-variant model-only pool ALREADY runs each
  model x3 (3 models x N=3 - Haiku x3, Sonnet x3, Opus x3; effort treated as inert per
  the methodology), so the 3 reruns per model ARE the variance runs that tighten
  confidence on the finding by measuring single-run variance. Verbatim retrieval is a
  known Haiku-strong task type; the reruns sharpen that read. The failure mode this task
  probes is "helpful" paraphrasing - a model that rewords a quote fails on Correctness
  even if the meaning is preserved, because the task is verbatim. Score Correctness as
  exact-match fidelity. Aggregate the 3 passes per model (mean-of-3); flag any model
  whose fidelity is inconsistent across its passes. Reasoning quality is skipped (pure
  retrieval). Voice match does not apply.
---

# Spec 03 - rerun-verbatim-capture (noise-floor crush)

Noise-floor rerun of the verbatim-capture task type. Corpus is
`corpus/higher-n-verbatim-capture/transcript.md`. The v1.5 9-variant model-only pool
already runs each model three times (3 models x N=3 - Haiku x3, Sonnet x3, Opus x3), so
those 3 reruns per model ARE the variance runs; aggregate them mean-of-3 per the notes.
Standard four-phase flow against the frozen rubric. This is a pure-retrieval task:
Correctness means exact-match verbatim fidelity, Reasoning quality is excluded, and
Voice match does not apply.
---
