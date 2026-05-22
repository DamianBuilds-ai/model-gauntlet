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
variant_pool: 9
corpus: corpus/higher-n-multi-file-synthesis/
notes: |
  NOISE-FLOOR RERUN. This eval is about within-model consistency: re-running the stable
  multi-file-synthesis task type enough times to crush the noise floor and separate true
  model skill from single-run variance. Under v1.5 the 9-variant model-only pool ALREADY
  runs each model x3 (3 models x N=3 - Haiku x3, Sonnet x3, Opus x3; effort treated as
  inert per the methodology), so the 3 reruns per model ARE the variance runs this eval
  is built on - the per-model score is the mean-of-3. This corpus is intentionally close
  in shape to the EXAMPLE eval (overlapping shipped/feedback/planned threads) so the
  comparison is clean. Aggregate the 3 passes per model (mean weighted total); flag any
  model whose 3 passes diverge by more than 0.5 - that divergence is itself the
  consistency finding this eval exists to surface. Voice match does not apply.
---

# Spec 02 - rerun-multi-file-synthesis (noise-floor crush)

Noise-floor rerun of the multi-file-synthesis task type. Corpus is the directory
`corpus/higher-n-multi-file-synthesis/`. The v1.5 9-variant model-only pool already
runs each model three times (3 models x N=3 - Haiku x3, Sonnet x3, Opus x3), so those
3 reruns per model ARE the variance runs; aggregate them mean-of-3 per the notes.
Standard four-phase flow against the frozen rubric. The point of the rerun is
consistency measurement, not a new task class. Voice match does not apply.
