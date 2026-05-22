---
task_category: multi-constraint-simultaneous
prompt_under_test: |
  You are given a single source file at
  corpus/multi-constraint-simultaneous/product-launch-brief.md - raw launch facts for a
  fictional analytics product, plus audience notes.

  Write the product launch blog post. You must satisfy ALL FIVE of the following
  constraints SIMULTANEOUSLY. The product lead rejects any draft that breaks even one:

    1. FORMAT: exactly three paragraphs. Paragraph 1 = what the product is and its scale.
       Paragraph 2 = the three headline features. Paragraph 3 = pricing and availability.
       No headings, no bullet lists, no title - three plain prose paragraphs only.

    2. LENGTH: the whole post body is 120 words or fewer (a hard ceiling).

    3. FORBIDDEN: never mention the sunset/old product by name (its codename appears in
       the source - the old product must not be named or hinted at anywhere in the post).

    4. ORDER: in paragraph 2, present the three headline features in the exact priority
       order the product lead set in the source - first the top-priority feature, then the
       second, then the third. Do not reorder them.

    5. TONE: confident and factual, NOT salesy. No exclamation marks. No hype superlatives
       (e.g. "revolutionary", "game-changing", "amazing", "best-in-class", "unmatched").

  Output the three-paragraph post only. After it, append the output envelope
  (schemaVersion, tier, status, tool_budget_used) as separate lines OUTSIDE and not
  counted toward the word limit. No em dashes. No emojis.
variant_pool: 9
corpus: corpus/multi-constraint-simultaneous/
corpus_intent: |
  One source file (corpus/multi-constraint-simultaneous/product-launch-brief.md): launch
  facts for a fictional product "Pulsegrid" - scale (2M events/sec), three priority-ordered
  features, pricing ($49/seat/month), GA date (1 June 2026), a sunset old product
  ("LegacyVane") that must NOT be named, and a confident-not-salesy tone requirement. The
  task imposes FIVE simultaneous constraints (format=3 paragraphs with assigned content per
  paragraph; length<=120 words; forbidden=never name the old product; order=features in the
  exact priority order; tone=no exclamation marks, no hype superlatives). This is the
  discipline-under-load probe: each constraint is individually easy, but holding all five at
  once is where compliance cracks - a model nails the prose and tone but drifts to four
  paragraphs, or stays in three paragraphs but overruns 120 words, or reorders the features,
  or slips the old product name in while explaining what Pulsegrid "replaces", or reaches
  for one hype word. The eval locates WHICH constraint breaks first under combined load.

  THE FIVE INDEPENDENT PASS/FAIL CHECKS (answer key - all five must hold):
    C1 FORMAT: exactly THREE paragraphs (blocks separated by a blank line), no heading
       (no `#`), no bullet (`- ` / `* `), no title line. Para1 = what-it-is + scale; Para2 =
       the three features; Para3 = pricing + availability.
    C2 LENGTH: post body <= 120 words (whitespace tokens, envelope excluded). 121+ = fail.
    C3 FORBIDDEN: the old-product codename "LegacyVane" (and any fragment like "Legacy
       Vane" / "Vane") appears ZERO times. A case-insensitive grep for `legacyvane` and for
       `\bvane\b` over the post returns nothing.
    C4 ORDER: in paragraph 2 the features appear in priority order - sub-second alerting
       FIRST, drag-and-drop dashboards SECOND, query API THIRD. Any other order = fail.
    C5 TONE: zero exclamation marks ("!") and zero hype superlatives from the banned set
       (revolutionary, game-changing, amazing, best-in-class, unmatched, world-class,
       cutting-edge, groundbreaking). Confident factual prose passes.

  CONTENT CORRECTNESS (must also be accurate, scored under Correctness/Completeness): scale
  2 million events/sec; the three features named and correctly ordered; price $49 per seat
  per month; GA 1 June 2026. Mentioning the competitor "Beacon Metrics" is allowed but not
  required; if mentioned it must not be disparaged.

  QUALITY PRINCIPLE (all-five-or-it-fails): the scored signal is how many of the five
  constraints survive SIMULTANEOUSLY. A beautifully written post that breaks ONE constraint
  (names the old product, runs to 121 words, uses four paragraphs, reorders features, or
  drops one exclamation mark) is a discipline failure - the product lead rejects it. The
  discriminator is combined-load compliance, and the per-constraint breakdown shows the
  scoring Architect exactly which constraint each run dropped.

  GREP-VERIFIABLE INVARIANTS (for the Architect - check all five, report which broke):
    - C1: paragraph count == 3 (split on blank lines); no line starts with `#`, `-`, `*`,
      or a digit-dot title.
    - C2: word count of post body <= 120.
    - C3: case-insensitive search for `legacyvane` and standalone `vane` returns ZERO hits.
    - C4: within paragraph 2, the first feature mention is alerting, then dashboards, then
      the query API (positional order check).
    - C5: count of `!` == 0; none of the banned superlatives appears (case-insensitive).
    - Content: "$49" present, "1 June 2026" (or 2026-06-01) present, "2 million" (or "2M")
      present, all three features named.

  Scoring guidance:
    - Discipline (hard-fail eligible, LOAD-BEARING) = ALL FIVE constraints hold at once.
      Breaking any one = Discipline 1, and the score notes which one broke. This is the
      headline discriminator and the whole point of the eval.
    - Completeness = scale + three features + price + GA date all present.
    - Correctness = facts and feature order match the source.
    - Hallucination (hard-fail eligible) = inventing a feature, a price, a date, or naming
      the old product as a "replacement" detail not requested.
    - Format adherence overlaps C1 (three paragraphs, no extras) - scored within Discipline.
    - Reasoning quality = SKIP-eligible. Voice match does NOT apply (tone is constraint C5,
      scored under Discipline, not the persona-voice axis).
notes: |
  NEW output-discipline eval, capstone of the Chat D battery (91-96). Probes
  multi-constraint simultaneous compliance - five independent constraints held at ONCE:
  format (exactly three paragraphs with assigned content), length (<=120 words), forbidden
  (never name the sunset old product), order (features in the product lead's priority
  order), and tone (no exclamation marks, no hype superlatives). Each constraint is
  individually trivial; the eval's whole value is that holding all five together is where
  discipline cracks under load. The corpus naturally tempts each break: the old product is
  the thing Pulsegrid "replaces" (tempting C3 break while explaining context), the feature
  list is rich enough to overrun 120 words (C2) or sprawl past three paragraphs (C1), the
  launch context invites hype words (C5), and an unordered feature dump breaks C4.

  The load-bearing discriminator is combined-load Discipline: all five constraints
  surviving simultaneously, with a per-constraint breakdown showing which one each run
  dropped first. Each of the five has a concrete grep/count check in corpus_intent (paragraph
  count, word count, `legacyvane`/`vane` zero-hit, positional feature order, `!` count + banned
  superlative set). Completeness, Correctness, and Hallucination are scored separately and
  Hallucination is hard-fail eligible. Reasoning is skip-eligible; the persona-voice axis
  does not apply (tone is a scored constraint, not voice). Standard four-phase /eval-pit flow
  against the frozen rubric/rubric.md. The variant pool is 9 (3 models x N=3, effort inert per
  the methodology). The corpus is the directory corpus/multi-constraint-simultaneous/.
---

# Spec 96 - multi-constraint-simultaneous

Write a product launch blog post that satisfies FIVE independent constraints AT ONCE:
format (exactly three paragraphs, each with assigned content), length (120 words or
fewer), forbidden (never name the sunset old product), order (the three features in the
product lead's priority order), and tone (confident and factual, no exclamation marks,
no hype superlatives). This is the capstone discipline-under-load probe. Each constraint
is individually easy; the value is that holding all five together is where compliance
cracks.

The corpus (`corpus/multi-constraint-simultaneous/product-launch-brief.md`) tempts each
break naturally: the old product is the thing the new one "replaces" (tempting the
forbidden-name break while giving context), the feature set is rich enough to overrun 120
words or sprawl past three paragraphs, the launch occasion invites hype words, and an
unordered feature dump breaks the order constraint. The success state holds all five
simultaneously while staying factually correct (2 million events/sec, the three ordered
features, $49 per seat per month, GA 1 June 2026).

The load-bearing discriminator is combined-load Discipline: all five constraints
surviving at once, scored with a per-constraint breakdown showing which one each run
dropped first. Each constraint has a concrete check in `corpus_intent` - paragraph count,
word count, a zero-hit grep for the old product name, a positional feature-order check,
and an exclamation-mark count plus a banned-superlative set. A beautifully written post
that breaks even ONE constraint is a discipline failure, because the product lead rejects
it. Completeness, Correctness, and Hallucination are scored separately and Hallucination
is hard-fail eligible. Reasoning is skip-eligible; the persona-voice axis does not apply
(tone is a scored constraint here, not voice). Standard four-phase `/eval-pit` flow
against the frozen `rubric/rubric.md`. The variant pool is 9 (3 models x N=3, effort inert
per the methodology). The corpus is the directory `corpus/multi-constraint-simultaneous/`.
