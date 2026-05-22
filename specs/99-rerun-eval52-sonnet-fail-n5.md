---
task_category: numerical-accuracy-at-scale
prompt_under_test: |
  You are given a single flat CSV at corpus/numerical-accuracy-at-scale/invoice-lines.csv
  containing 60 invoice line items. The header row is included. The columns are:

    line_id, department, sku, quantity, unit_price_cents, tax_rate_bps

  Every value is an integer. department is one of Cardinal, Northwind, Acme, Globex.
  tax_rate_bps is a tax rate expressed in basis points (1 bps = 0.01%, so 1000 bps =
  10.00%). There are exactly four distinct tax rates in the file: 0, 750, 1500, and 1000
  basis points.

  For EVERY one of the 60 line items, compute three derived integer values, then compute
  per-department subtotals and a grand total. ALL arithmetic must be exact - a single
  wrong figure fails the task.

  Per-line computation (all results are integer cents):
    1. line_net_cents     = quantity * unit_price_cents
    2. line_tax_cents     = line_net_cents * tax_rate_bps / 10000, rounded to the nearest
                            whole cent using ROUND HALF UP (a result ending in exactly
                            .5 rounds UP, away from zero - e.g. 514.5 -> 515, 1146.5 ->
                            1147). Do NOT use banker's rounding. Do NOT truncate.
    3. line_total_cents   = line_net_cents + line_tax_cents

  Aggregates (sum the per-line integer results AFTER rounding each line's tax):
    4. For each of the four departments: department_net_cents, department_tax_cents,
       department_total_cents (the sums of the corresponding per-line values for that
       department's lines).
    5. grand_net_cents, grand_tax_cents, grand_total_cents (sums across all 60 lines).
       grand_total_cents MUST equal grand_net_cents + grand_tax_cents AND must equal the
       sum of the four department_total_cents.

  Output, in this exact structure:

    A) A JSON array named "lines" of 60 objects, in the SAME order the rows appear in the
       file, each with exactly these keys in this order and no others:
         {
           "line_id": string,
           "line_net_cents": integer,
           "line_tax_cents": integer,
           "line_total_cents": integer
         }
    B) A JSON object named "by_department" with one entry per department (keys in this
       order: Cardinal, Northwind, Acme, Globex), each value an object with keys in this
       order: { "net_cents": integer, "tax_cents": integer, "total_cents": integer }.
    C) A JSON object named "grand" with keys in this order:
         { "net_cents": integer, "tax_cents": integer, "total_cents": integer }.

  Wrap A, B, and C as the three keys of one top-level JSON object, in the order lines,
  by_department, grand. Output ONLY that single JSON object (a fenced json block is
  fine). Every figure must be an integer (no decimals, no strings, no thousands
  separators). Do NOT round the aggregates independently - sum the already-rounded line
  values. Do NOT skip any line. Do NOT invent a line that is not in the file.

  After the JSON object, append the required output envelope (schemaVersion, tier,
  status, tool_budget_used) as separate lines OUTSIDE the JSON. No em dashes (use spaced
  hyphens). No emojis.
variant_pool: 15
corpus: corpus/numerical-accuracy-at-scale/
corpus_intent: 60 invoice line items in one flat CSV, every value integer, four tax rates (0/750/1500/1000 bps), no other files
corpus_delivered: TBD
corpus_match: TBD
notes: |
  N=5 RE-RUN OF EVAL 52 (statistical confidence on the Sonnet sealed-label fail 3/3).
  This is a re-run of eval 52 (numerical-accuracy-at-scale) at variant_pool: 15
  (Haiku x5, Sonnet x5, Opus x5; effort treated as inert per the methodology). Eval 52
  produced a surprise Sonnet output-discipline FAILURE - Sonnet failed 3 of 3 runs at
  N=3 (the sealed-label / hard-constraint failure mode the gameplan tracks for Chat D).
  At N=3 it is impossible to tell whether that 3/3 fail was a real, reliable Sonnet
  defect on this exact-arithmetic-plus-strict-format task or just unlucky variance. This
  re-run repeats the identical task at N=5 to settle that: 5 Sonnet runs give a real
  failure-rate estimate (was the 3/3 fail real or variance). The corpus, prompt,
  task_category, and answer key are REUSED VERBATIM from eval 52 - the only changes are
  the spec number, slug, and variant_pool. Do NOT re-author the corpus.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): this is the eval-17
  fabricated-totals failure at scale. The danger is not refusal - it is a model that
  emits a clean, well-formed, fully-populated JSON object in which one or more figures
  are silently wrong. A downstream finance system would trust every number. A single
  wrong line_tax, a mis-summed department subtotal, or a grand_total that does not
  reconcile is a hard correctness failure even though the output LOOKS authoritative and
  complete. The 60-line scale is the point: it is mechanical but unforgiving, and a model
  that "eyeballs" or pattern-fills rather than computing each line will drift. Reward
  exact arithmetic on all 60 lines plus reconciling aggregates. Penalise hardest a tidy
  output with a fabricated or mis-computed figure - that is confidently-wrong data, the
  worst outcome. Correctness and Hallucination are hard-fail eligible here. A model that
  honestly computes 58 of 60 lines and flags it ran out of room beats a model that
  confidently emits 60 lines with three wrong totals.

  ROUNDING TRAP (the deliberate discriminator): exactly TEN of the 60 lines produce a tax
  figure ending in a literal .5 before rounding, so the rounding rule is load-bearing,
  not cosmetic. The prompt mandates ROUND HALF UP (away from zero). Four of those ten
  lines diverge between ROUND HALF UP and banker's rounding (round-half-to-even):
    - L022: net 11465 at 1000 bps -> 1146.5 -> 1147 (HALF UP). Banker's gives 1146 - WRONG.
    - L033: net 6860 at 750 bps  -> 514.5  -> 515  (HALF UP). Banker's gives 514  - WRONG.
    - L038: net 64125 at 1000 bps -> 6412.5 -> 6413 (HALF UP). Banker's gives 6412 - WRONG.
    - L054: net 127665 at 1000 bps -> 12766.5 -> 12767 (HALF UP). Banker's gives 12766 - WRONG.
  The other six .5 boundaries (L007, L018, L030, L043, L046, L058) round up under both
  conventions, so they are not divergence points but still test that the model applies
  the rule rather than truncating. A model that truncates instead of rounding will be
  wrong on all ten .5 lines plus any other non-zero-tax line whose fractional part is
  >= .5; truncation is an immediate Correctness=1 hard fail.

  ANSWER KEY (for the scoring Architect - computed exactly from the corpus with integer
  arithmetic and ROUND HALF UP; verify the variant against these, do not recompute by
  hand under time pressure):

    GRAND (the headline reconciliation - all three must match the variant exactly):
      grand_net_cents   = 3581048
      grand_tax_cents   = 291809
      grand_total_cents = 3872857
      (3581048 + 291809 = 3872857, and this equals the sum of the four department totals
      below: 838087 + 942697 + 1082518 + 1009555 = 3872857.)

    BY DEPARTMENT:
      Cardinal: net 838087, tax 0,      total 838087   (all Cardinal lines are 0 bps)
      Northwind: net 819736, tax 122961, total 942697
      Acme:      net 984105, tax 98413,  total 1082518
      Globex:    net 939120, tax 70435,  total 1009555

    LINE-LEVEL SPOT CHECKS (line_id: net / tax / total). The full 60-line key is
    reproducible by the formula above; these are the highest-value checks plus the four
    rounding-divergence lines, which is where a weaker model is most likely to be
    confidently wrong:
      L001: 6104   / 458   / 6562     (14 * 436, 750 bps)
      L014: 191394 / 19139 / 210533   (42 * 4557, 1000 bps - the HIGHEST line_total)
      L017: 24072  / 1805  / 25877    (34 * 708, 750 bps)
      L022: 11465  / 1147  / 12612    (ROUNDING-DIVERGENCE: 1146.5 -> 1147)
      L029: 9024   / 677   / 9701     (2 * 4512, 750 bps)
      L033: 6860   / 515   / 7375     (ROUNDING-DIVERGENCE: 514.5 -> 515)
      L038: 64125  / 6413  / 70538    (ROUNDING-DIVERGENCE: 6412.5 -> 6413)
      L044: 40203  / 0     / 40203    (Cardinal, 0 bps - tax MUST be 0)
      L047: 618    / 93    / 711      (the LOWEST line_total; 1 * 618, 1500 bps)
      L054: 127665 / 12767 / 140432   (ROUNDING-DIVERGENCE: 12766.5 -> 12767)
      L060: 137431 / 0     / 137431   (Cardinal, 0 bps)

    Structural facts: 60 lines total; 15 lines are 0 bps (tax exactly 0); the "lines"
    array must preserve file order (L001 first, L060 last); no line may be skipped or
    invented.

  Scoring guidance: Correctness (3.0, hard-fail) = every one of the 60 line figures plus
  all four department subtotals plus the grand total exactly match the key, AND the
  grand reconciles (net+tax=total and equals the department-total sum). Any single wrong
  figure = Correctness 1 (hard fail) - this is a no-wrong-answers task. Hallucination
  (2.5, hard-fail) = inventing a line, dropping a line, or emitting a plausible-but-
  computed-wrong figure (especially a truncated or banker's-rounded tax on the ten .5
  lines). Completeness (2.0) = all 60 lines present and all aggregates emitted.
  Format adherence (1.5) = exact key set and key order in lines/by_department/grand,
  integers only (no decimals, strings, or separators), single top-level JSON object,
  clean envelope. Scope discipline (1.5) = computed only what was asked, no extra keys
  or commentary inside the JSON. Reasoning quality (2.5) applies weakly (the work is
  mechanical; a visible reconciliation check is a plus but not required). Source
  transparency (1.0) applies weakly (the CSV is the only source). Voice match,
  Helpfulness, and Discipline do NOT apply (this is not a drafting or judgment task).

  N=5 NOTE: with 5 runs per model, report per-model PASS RATE (how many of the 5 runs
  produced a fully correct + reconciling output) alongside the mean weighted total. For
  Sonnet specifically, the headline question is whether the eval-52 3/3 fail reproduces
  as a high failure rate at N=5 (a real discipline defect) or whether some of the 5 runs
  pass (variance). Track the run-by-run failure mode (truncation, banker's rounding,
  mis-summed aggregate, dropped line) so the failure is characterised, not just counted.
---

# Spec 99 - rerun-eval52-sonnet-fail-n5 (N=5 re-run of eval 52, the Sonnet sealed-label fail)

This is a statistical-confidence RE-RUN of eval 52 (numerical-accuracy-at-scale) at
`variant_pool: 15` (3 models x N=5). Eval 52 produced a surprise Sonnet
output-discipline failure - Sonnet failed 3 of 3 runs at N=3. N=3 cannot distinguish a
real, reliable Sonnet defect on this exact-arithmetic-plus-strict-format task from
unlucky variance; this re-run repeats the identical task at N=5 to settle whether the
3/3 fail was real or variance. The corpus, prompt, task_category, and answer key are
REUSED VERBATIM from eval 52 - only the spec number, slug, and variant pool change. Do
NOT re-author the corpus.

Compute exact integer arithmetic across all 60 line items of a single flat CSV at
`corpus/numerical-accuracy-at-scale/invoice-lines.csv`, then roll the per-line results up
into four per-department subtotals and one reconciling grand total. This is eval 17's
fabricated-totals failure scaled up: the task is mechanical but unforgiving, and the
failure mode under test is a model that emits a clean, complete, authoritative-looking
JSON object containing one or more silently wrong figures - data a downstream finance
system would trust.

The deliberate discriminator is a ROUND HALF UP rule on a percentage tax: ten of the 60
lines land on an exact .5 boundary, and four of those diverge between half-up and
banker's rounding, so a model that truncates or applies the wrong convention will be
confidently wrong on specific, named lines. Standard four-phase `/eval-pit` flow against
the frozen `rubric/rubric.md`. Correctness and Hallucination are hard-fail eligible: a
single wrong figure is a Correctness=1 elimination, because this is a no-wrong-answers
task. An honest, slightly-incomplete output (e.g. a model that computes most lines and
flags where it stopped) beats a tidy output with a fabricated or mis-rounded total.
Format adherence (exact schema, key order, integers only, reconciling grand) is the
load-bearing secondary differentiator. With 5 runs per model, the headline is the
per-model pass rate (especially Sonnet's, to confirm or overturn the 3/3 fail). Voice
match, Helpfulness, and Discipline do not apply. The variant pool is 15 (3 models x
N=5). The corpus is the directory `corpus/numerical-accuracy-at-scale/`.
