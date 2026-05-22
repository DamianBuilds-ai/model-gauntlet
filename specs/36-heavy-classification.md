---
task_category: heavy-classification
prompt_under_test: |
  You are given a large batch of inbound support messages at
  corpus/heavy-classification/messages.csv (one header row plus 302 message rows; each
  row is an id and a message) and a documented taxonomy with explicit classification
  rules at corpus/heavy-classification/taxonomy.md.

  Classify EVERY message into exactly ONE of the eight categories defined in
  taxonomy.md (SEC, BILL, AUTH, BUG, PERF, FEAT, DOCS, HOW) by applying the precedence
  rules in that document.

  Requirements:
    1. Read taxonomy.md and apply its eight rules in the documented PRECEDENCE order -
       first match wins (SEC > BILL > AUTH > BUG > PERF > DOCS > FEAT > HOW). Many
       messages contain signals for more than one category; only the first-matching rule
       gives the correct label.
    2. Assign exactly one category to every message. Do not skip any message, do not
       invent categories, do not assign two categories to one message.
    3. Output ONLY a single JSON array. Each element is an object with exactly two keys
       in this order: {"id": "<id from CSV>", "category": "<one of the eight codes>"}.
       Categories are uppercase exactly as written in taxonomy.md. One object per
       message, in the SAME ORDER as the CSV rows.

  After the JSON array, append the required output envelope (schemaVersion, tier,
  status, tool_budget_used) as separate lines OUTSIDE the JSON. No em dashes (use spaced
  hyphens). No emojis.
variant_pool: 9
corpus: corpus/heavy-classification/
corpus_intent: one large CSV of 302 inbound support messages plus a taxonomy.md documenting 8 categories and an 8-rule first-match precedence; 30 of the messages are deliberately borderline (match 2+ categories so only the precedence rule resolves them), the rest are single-signal clean items balanced across the 8 categories. Per-item answer key + borderline rationale under .provenance.
corpus_delivered: TBD
corpus_match: TBD
notes: |
  HEAVY CLASSIFICATION (accuracy-and-consistency-at-volume). The corpus is large on
  purpose: 302 messages the model must read in full and label one at a time, holding the
  same 8-category taxonomy and its first-match precedence in working memory across the
  whole batch. This is the eval-22 completeness-under-load mechanism applied to
  classification: under volume, weaker models drift - they apply the precedence cleanly
  on the first dozen items, then start labelling by surface keyword later in the batch
  (calling a "hacked account, refund my charge" message BILL instead of SEC because they
  stopped re-checking the security rule), or they skip items, or they emit two labels.
  A strong model applies the same precedence uniformly to item 1 and item 300.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong label is
  worse than a flagged uncertainty. A model that labels an account-compromise message
  BILL because it saw the word "charged", or that calls a slow-but-not-erroring page a
  BUG because it saw "load", has produced wrong triage that a downstream routing system
  would trust (a security incident sent to the billing queue is the worst case). Reward
  correct rule-application, especially on the borderline items. Penalise the
  plausible-but-wrong label hardest. Correctness and Hallucination are hard-fail eligible
  (inventing a category code not in the taxonomy, or labelling messages that do not exist,
  is a hallucination).

  ANSWER KEY (computed deterministically by the corpus generator at
  corpus/heavy-classification/.provenance/generate.py): the per-item correct label is in
  corpus/heavy-classification/.provenance/answer_key.json (id -> category for all 302
  items, plus per-category counts), and the WHY for each of the 30 borderline items is in
  corpus/heavy-classification/.provenance/borderline-rationale.md. The clean items each
  carry exactly one category signal; the 30 borderline items each carry two or more, and
  the documented precedence resolves them. The load-bearing checks:

    - OVERALL ACCURACY: (items labelled correctly) / 302 against answer_key.json. The
      clean items establish the floor; a model that loses many clean items is drifting
      under volume.
    - BORDERLINE ACCURACY (the primary discriminator): (borderline items labelled
      correctly) / 30. These are where the precedence rule, not the surface keyword,
      decides. The classic traps: "hacked account + refund" must be SEC not BILL
      (security beats billing); "billing page shows error 500" must be BUG not BILL (a
      broken control beats a money signal when the ask is the breakage); "reports time
      out with a 504" must be BUG (explicit error) while "reports so slow they eventually
      time out, no error" must be PERF (slowness leads); "there is no bulk-delete, please
      add it" must be FEAT while "how do I bulk-delete, I just cannot find it" must be
      HOW. A model that labels by keyword rather than precedence misses these.
    - CONSISTENCY-AT-VOLUME: does the model apply the SAME rule the same way early and
      late in the 302-row batch? Compare accuracy on the first third vs the last third of
      the items; a large drop late is the forgetting-under-load signal.
    - COMPLETENESS: all 302 items present, in CSV order, exactly one label each, no
      skipped items, no duplicate ids, no extra ids. Count any missing, duplicated, or
      extra ids explicitly.

  Scoring guidance:
    - Correctness (hard-fail eligible, weight 3.0) = overall accuracy against
      answer_key.json, weighted by the borderline items (they are the rule-application
      test). A model with high clean accuracy but poor borderline accuracy is classifying
      by keyword, not by the documented precedence - that is the central failure this
      eval detects. A SEC item mislabelled BILL (security incident to billing queue) is
      the worst single error.
    - Completeness (weight 2.0) = all 302 ids present exactly once, in order, each with
      one valid category. Count dropped, duplicated, or extra ids.
    - Reasoning quality (weight 2.5) = evidence the model applied the FIRST-MATCH
      precedence rather than picking the most salient keyword, and resisted the
      keyword traps on the borderline items, rather than ad hoc labelling.
    - Hallucination (hard-fail eligible, weight 2.5) = inventing a category code outside
      the eight, labelling an id that is not in the CSV, or fabricating items.
    - Format adherence (weight 1.5) = a single clean JSON array, two keys per object in
      the right order, uppercase codes, CSV order preserved, output envelope appended
      OUTSIDE the JSON.
    - Discipline (decision/judgment, weight 1.25) = honoured "exactly one label, classify
      every message, do not invent categories". A model that emits two labels for a hard
      item, or quietly skips items it found hard, is penalised.
    - Source transparency applies weakly (CSV + the documented rules). Voice match does
      NOT apply.

  Suggested shorthand for the Architect: overall_accuracy = correct / 302;
  borderline_accuracy = correct-of-borderline / 30 (the headline discriminator);
  early_vs_late = accuracy(first 100) vs accuracy(last 100) to surface drift. An
  exemplary 5 on Correctness has high overall accuracy AND near-perfect borderline
  accuracy AND no early/late drift, with all 302 ids present exactly once. The score
  falls on keyword-over-precedence errors (especially SEC mislabelled as BILL/AUTH),
  on late-batch drift, and on any skipped, duplicated, or two-labelled item.

  Run the full 9-variant model-only pool (Haiku x3, Sonnet x3, Opus x3; effort inert per
  the methodology). Aggregate the 3 passes per model (mean weighted total); flag any
  model whose 3 passes diverge by more than 0.5 as a consistency finding - accuracy drift
  across a 302-item batch is exactly where per-run variance and forgetting-under-load show
  up.
---

# Spec 36 - heavy-classification (accuracy and consistency at volume)

A heavy classification eval. The corpus is a large batch of 302 inbound support messages
(`corpus/heavy-classification/messages.csv`) plus a documented taxonomy and rule set
(`corpus/heavy-classification/taxonomy.md`) defining eight categories (SEC, BILL, AUTH,
BUG, PERF, FEAT, DOCS, HOW) and an eight-rule first-match precedence
(SEC > BILL > AUTH > BUG > PERF > DOCS > FEAT > HOW). The model must label every message
with exactly one category by applying that precedence - not by picking the most salient
surface keyword.

The discriminator is accuracy and consistency under volume. The clean items each carry
one category signal and set the accuracy floor; thirty deliberately borderline items each
carry two or more signals, so only the documented precedence resolves them - a hacked
account that also mentions a refund is a security ticket, not a billing one; a billing
page that throws an error 500 is a bug, not a billing dispute; a request to slowly time
out with no error is performance, while an explicit 504 is a bug; "there is no bulk-delete,
please add it" is a feature request while "how do I bulk-delete, I just cannot find it" is
a how-to. This is the eval-22 completeness-under-load mechanism applied to classification:
under the volume of 302 items, weaker models apply the precedence cleanly early then drift
to keyword-matching late, or skip items, or emit two labels - a model that mis-routes a
security incident to the billing queue has produced confidently-wrong triage a downstream
system would trust.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The answer
key is computed deterministically (generator under the corpus `.provenance/` folder) and
stored per item in `answer_key.json` (id -> category for all 302 items), with the
rationale for each of the thirty borderline items in `borderline-rationale.md`, so
Correctness scores objectively: overall accuracy weighted by the borderline items, plus
an early-vs-late drift check. Correctness and Hallucination are hard-fail eligible;
Reasoning quality (first-match precedence over keyword) and Completeness (all 302 items
present exactly once) are the load-bearing differentiators. Voice match does not apply.
The variant pool is 9 (3 models x N=3, effort inert per the methodology). The corpus is
the directory `corpus/heavy-classification/`.
