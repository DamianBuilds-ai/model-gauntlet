---
task_category: heterogeneous-precision-battery
prompt_under_test: |
  You are given a single target file at
  corpus/heterogeneous-precision-interdependent/marlowe-orderbook.md - the
  Q3-26 orderbook reconciliation for the fictional Project Marlowe. It
  contains an orders markdown table, a public order-status prose blurb, a
  fenced JSON billing-config block, a warehouse pick-priority bullet list,
  a customer contact roster table, and a per-customer order-count summary
  list with a total line above it.

  Apply the following TEN independent change requirements to that file in
  a single pass. Each requirement is a precise deterministic edit; each
  has exactly one correct result. Apply ONLY what is listed. Do NOT
  reformat, reorder, re-align, normalise, or "improve" anything the
  requirements do not name.

  CHANGE REQUIREMENTS (apply all ten; the listed order is the requirement
  number, NOT a recommended order of operations - the correct end-state
  is fully specified and you must arrive at it):

    R1. FIELD RENAME (orders table). Rename the `status_flag` column
        header to `fulfilment_state`. Update ONLY the header; leave every
        row's value (`active`) unchanged.

    R2. ARITHMETIC GRAND TOTAL. The "Orderbook line total (dollars)"
        line currently reads `Orderbook line total (dollars): 0`. SET
        the number to the exact sum of the `line_total` column across
        the orders table.

    R3. DATE FORMAT CONVERSION (DD/MM/YYYY -> ISO YYYY-MM-DD). In the
        "Public order-status blurb" paragraph, convert all three dates
        (02/12/2026, 09/12/2026, 16/12/2026) from DD/MM/YYYY to ISO.

    R4. FORBIDDEN-WORD REMOVAL. In the "Public order-status blurb"
        paragraph, remove every occurrence of `clearly`, `basically`,
        and `honestly` (case-sensitive). Keep single spacing.

    R5. JSON FIELD RENAME. Rename the JSON key `legacy_invoice_path` to
        `legacy_invoice_enabled`. Leave its value (`true`) unchanged.

    R6. ORDERS TABLE DEDUPLICATION. The orders table contains duplicate
        rows (rows with the same `order_id` appearing more than once
        across the table). Remove the duplicate rows so that each
        `order_id` appears exactly once in the orders table, preserving
        the first-occurrence row for each unique `order_id`. Do NOT
        change any non-duplicate row's contents.

    R7. WAREHOUSE PICK-PRIORITY DEDUPLICATION. In the "Warehouse
        pick-priority list" bullet list, remove duplicate bullets so
        each MLW-XXXX appears exactly once, preserving first-occurrence
        order. Do NOT change the non-duplicate bullets.

    R8. SORT-ORDER REORDER (warehouse list). After R7's dedup, the
        warehouse pick-priority list must be reordered to sort
        ASCENDING by order_id (lexicographic). Do NOT change any
        bullet's text content - only the order.

    R9. PER-CUSTOMER ORDER COUNT. In the "Per-customer order count"
        list at the foot, update each bullet to show the customer's
        exact unique-order count (one count per unique order_id for
        that customer, based on the orders table after all applicable
        prior changes). The current bullets read
        `- northfield-co: 0 orders`, `- summerline-llp: 0 orders`,
        `- rivermouth-pty: 0 orders`. Replace each `0` with the
        correct count.

    R10. CUSTOMER CONTACT ROSTER FIELD RENAME. In the "Customer contact
         roster" table, rename the `primary_contact_email` column
         header to `contact_email`. Do NOT change any email value.

  Output the COMPLETE updated file content, from its first line to its
  last line, as a single fenced code block, with all ten requirements
  applied and nothing else altered. After the code block, append the
  required output envelope (schemaVersion, tier, status, tool_budget_used)
  as separate lines OUTSIDE the code block. No em dashes (spaced hyphens).
  No emojis. Do not add commentary inside the file content.
variant_pool: 15
corpus: corpus/heterogeneous-precision-interdependent/
corpus_intent: |
  ONE realistic fictional artifact (corpus/heterogeneous-precision-interdependent/marlowe-orderbook.md):
  the Q3-26 orderbook reconciliation for the fictional Project Marlowe.
  The artifact organically hosts ten unrelated precise edit surfaces - an
  orders markdown table, a public order-status prose blurb, a fenced
  JSON billing-config block, a warehouse pick-priority bullet list, a
  customer contact roster table, and a per-customer order-count summary
  - so the bundling feels like one recon-lead's pre-lock pass rather than
  a list of disconnected chores.

  THE HETEROGENEOUS-PRECISION INTERDEPENDENT PROBE. This is the third
  eval in the 101-105 battery. The gameplan flagged the design rule:
  "Hardness is in JUGGLING interacting requirements, not raw count.
  Calibrated so a model that does each op in isolation (no global
  ordering plan) produces a wrong final state even though each local
  edit looks right. Does a naive left-to-right pass produce a WRONG
  answer? It must, or there is no discrimination." The eval has 10
  requirements; THREE are wired so that the order of operations matters
  and a naive R1-to-R10 sequential apply yields a wrong final state.

  THE INTERDEPENDENCY WEB (the heart of the eval):
    - R2 depends on R6. R2 says "sum the line_total column"; R6 says
      "deduplicate the orders table." A model that applies R2 BEFORE
      R6 sums all 9 rows including duplicates -> 480+360+480+210+540
      +360+615+295+720 = 4060. A model that applies R6 first then sums
      gets 480+360+210+540+615+295+720 = 3220. The CORRECT R2 value is
      the post-dedup sum 3220.
    - R8 depends on R7. R8 says "sort ascending after R7's dedup." A
      naive sort of the unsorted-and-duplicated original list yields a
      different sequence than the correct (post-dedup, sorted) list.
    - R9 depends on R6. R9 says "show each customer's unique-order
      count (one count per unique order_id for that customer)." Per the
      orders table the unique order_ids per customer are: northfield-co
      = {MLW-1041, MLW-1045, MLW-1047} = 3; summerline-llp = {MLW-1042,
      MLW-1044} = 2; rivermouth-pty = {MLW-1043, MLW-1046} = 2. A model
      that counts rows BEFORE R6 (on the duplicated table) gets:
      northfield-co = 4 (MLW-1041 twice, 1045, 1047), summerline-llp =
      3 (MLW-1042 twice, 1044), rivermouth-pty = 2 - WRONG for two of
      the three.

  The discrimination signal: a model that processes the requirements
  strictly in listed order (R1 then R2 then ... then R10), recomputing
  nothing, produces wrong values for R2 and R9 and a wrong order for
  R8. A model that builds a global plan (notice R6/R7 are dedups that
  feed R2/R8/R9, do them first, then compute) is correct. This is the
  eval-48-beating design: difficulty from interaction, not from any
  single op being individually hard. Each individual op is trivial.

  QUALITY PRINCIPLE (correctness-first, drop-tracking + order-error
  detection). An apply that LOOKS done but silently produced the wrong
  R2 value (because the model summed pre-dedup) is WORSE than one that
  flagged the dependency and asked for clarification. The eval is
  scored binary-per-requirement: all ten correct = pass, any miss =
  fail, and the scoring Architect records WHICH requirement each
  failing run missed AND whether the miss looks like an ORDERING ERROR
  (R2 = 4060 or R9 counts the duplicated rows) or a different drop
  type.

  ANSWER KEY (for the scoring Architect - the exact end-state after
  applying R1-R10 with correct global ordering). Verify by line-by-line
  comparison against the original corpus file plus the grep invariants
  below.

    CORRECT GLOBAL ORDERING (the only ordering producing the right
    end-state): R6 BEFORE R2; R6 BEFORE R9; R7 BEFORE R8. A
    topologically-valid sequence is: R1, R10, R6, R2, R7, R8, R9, R3,
    R4, R5 (or any reordering that respects {R6 -> R2, R6 -> R9, R7
    -> R8}).

    WRONG FINAL STATES PRODUCED BY A NAIVE PASS (the scoring Architect
    flags these as ordering errors):
      - R2 = 4060 (sum of pre-dedup table; correct is 3220).
      - R9 northfield-co = 4 orders, summerline-llp = 3 orders (counts
        of pre-dedup rows; correct is 3 and 2).
      - R8 warehouse list ordered by sorting the pre-dedup-still-9-bullets
        list (correct is 7 bullets in ascending order MLW-1041 ...
        MLW-1047).

    R1 (orders header rename): the orders table header reads
       `| order_id   | customer_handle | line_total | fulfilment_state |`.
       `status_flag` appears 0 times; `fulfilment_state` appears
       exactly once (in that header).

    R2 (arithmetic total, POST DEDUP): the line reads exactly
       `Orderbook line total (dollars): 3220`. Sums of {480, 360, 210,
       540, 615, 295, 720} = 3220. `Orderbook line total (dollars):
       4060` (the naive pre-dedup sum) is an ORDERING-ERROR signal.
       `Orderbook line total (dollars): 0` is the unchanged state.

    R3 (date conversion): the prose paragraph contains `2026-12-02`,
       `2026-12-09`, `2026-12-16`. `02/12/2026`, `09/12/2026`,
       `16/12/2026` appear 0 times in the prose. The JSON `"lock_date":
       "30/09/2026"` is OUTSIDE the prose paragraph and STILL appears
       (scope discipline).

    R4 (forbidden-word removal): `clearly`, `basically`, `honestly`
       appear 0 times. Paragraph reads grammatically with single
       spacing.

    R5 (JSON rename): the JSON block contains `"legacy_invoice_enabled":
       true`. `legacy_invoice_path` appears 0 times.

    R6 (orders table dedup): the orders table has EXACTLY 7 data rows
       (down from 9). The unique order_ids in first-occurrence order
       are: MLW-1041, MLW-1042, MLW-1043, MLW-1044, MLW-1045, MLW-1046,
       MLW-1047. The two duplicate rows (the second occurrences of
       MLW-1041 and MLW-1042) are removed. Non-duplicate rows are
       byte-identical.

    R7 (warehouse list dedup): the warehouse list has EXACTLY 7
       bullets (down from 9). Each MLW-XXXX appears exactly once.

    R8 (warehouse list sort ASC): after R7, the warehouse list reads
       (top to bottom) MLW-1041, MLW-1042, MLW-1043, MLW-1044,
       MLW-1045, MLW-1046, MLW-1047.

    R9 (per-customer unique count): the per-customer summary list reads
       exactly:
         - northfield-co: 3 orders
         - summerline-llp: 2 orders
         - rivermouth-pty: 2 orders
       Wrong counts (4/3/2 from pre-dedup table) are an ORDERING-ERROR
       signal.

    R10 (contact roster header rename): the contact roster table header
        reads `| customer_handle  | contact_email                |` (or
        equivalent column-width-preserving form). `primary_contact_email`
        appears 0 times; `contact_email` appears exactly once.

    EVERYTHING ELSE in the file (other headings, blank lines, prose
    intro paragraphs, code-fence markers, the column alignment of the
    pre-existing non-duplicate rows, the JSON keys not renamed by R5,
    the JSON `lock_date` per R3's scope-discipline check, every email
    value in the contact roster) is BYTE-IDENTICAL to the original.

  GREP-VERIFIABLE INVARIANTS (for the Architect, one per requirement):
    - R1: `status_flag` appears 0 times; `fulfilment_state` appears 1
      time.
    - R2: `Orderbook line total (dollars): 3220` appears 1 time;
      `Orderbook line total (dollars): 4060` appears 0 times (ordering
      error); `Orderbook line total (dollars): 0` appears 0 times.
    - R3: `02/12/2026`, `09/12/2026`, `16/12/2026` appear 0 times in
      prose; `2026-12-02`, `2026-12-09`, `2026-12-16` each appear at
      least once. The JSON `"lock_date": "30/09/2026"` STILL appears.
    - R4: `clearly`, `basically`, `honestly` appear 0 times.
    - R5: `legacy_invoice_path` appears 0 times;
      `"legacy_invoice_enabled": true` appears 1 time.
    - R6: the orders table has exactly 7 data rows (MLW-1041 appears
      exactly once in the table data, MLW-1042 appears exactly once).
    - R7: the warehouse pick-priority list has exactly 7 bullets;
      MLW-1041 appears exactly once in the list, MLW-1042 once.
    - R8: the warehouse list bullets in file order read MLW-1041,
      MLW-1042, MLW-1043, MLW-1044, MLW-1045, MLW-1046, MLW-1047.
    - R9: the per-customer summary list reads exactly
      `- northfield-co: 3 orders`, `- summerline-llp: 2 orders`,
      `- rivermouth-pty: 2 orders`. Lines `- northfield-co: 4 orders`
      and `- summerline-llp: 3 orders` (the ordering-error signal)
      appear 0 times.
    - R10: `primary_contact_email` appears 0 times; `contact_email`
      appears 1 time.

  DROP-DISTRIBUTION TRACKING (mandatory, with ordering-error
  sub-category): for each failing run, the scoring Architect records
  the exact set of R-tags missed AND tags each miss as either
  `ORDERING-ERROR` (R2=4060 or R9 wrong counts or R8 wrong ordering of
  unsorted-and-duplicated list) or `OTHER-DROP`. Aggregate per family:
  if a family's failures cluster on ORDERING-ERROR misses, that is a
  global-planning weakness signal. If failures are OTHER-DROP types,
  that is a capacity signal.

  Scoring guidance:
    - All-requirements-correct (binary, primary): all 10 of R1-R10
      satisfied AND nothing else changed = pass; any miss = fail.
    - Mean requirements-satisfied (secondary): mean of (number of
      R1-R10 satisfied) across the 5 runs per family.
    - Drop distribution (secondary): per-requirement miss count.
    - Ordering-error rate (tertiary, the eval's headline insight):
      fraction of failures that are ORDERING-ERROR misses on R2, R8,
      or R9.
    - Correctness (hard-fail eligible) = all 10 applied AND nothing
      else changed.
    - Hallucination (hard-fail eligible) = inventing a row, dropping
      a non-duplicate row, fabricating an order count.
    - Format adherence = one fenced code block, envelope outside.
    - Discipline = applied ONLY the 10 named edits.
    - Reasoning quality = SKIP-eligible; surfacing the
      dedup-before-total / dedup-before-count ordering is a quality
      signal but not required for pass (the grep invariants gate it).
    - Source transparency applies weakly.
    Voice match does NOT apply.
notes: |
  Difficulty self-check (mint-N rule, eval-45-to-48 lesson): would a
  weak model (Haiku) genuinely produce a wrong final state via a naive
  left-to-right apply? Honest prediction: YES. The gameplan-specified
  test ("does a naive left-to-right pass produce a WRONG answer? It
  must") is satisfied: a model that processes R1, R2, R3, ..., R10 in
  listed order with no global plan computes R2 from the pre-dedup
  table (R6 has not been applied yet) and R9 from pre-dedup counts.
  The CORRECT order requires noticing that R6 must precede R2 and R9,
  and R7 must precede R8 - i.e. building a small dependency graph
  before applying.

  The interdependencies are NOT signposted in the prompt: the prompt
  presents R1-R10 as if independent ("ten independent change
  requirements"). The dependency must be inferred from the
  REQUIREMENT TEXT (R2 says "sum the line_total column"; if R6
  removes rows from that column, the sum changes - the model has to
  notice this).

  The gameplan also said: "If everyone passes at 8, that is the
  EXPECTED floor result; the signal is whether ANY family starts
  dropping here." For 103, the analogous prediction: if all three
  families nail the ordering and produce R2=3220, the
  global-planning hypothesis is weak. If Sonnet/Haiku frequently
  produce R2=4060 while Opus produces R2=3220, the eval has
  separated. If everyone produces R2=4060, the eval has uncovered a
  systemic global-planning weakness across the frontier (still a
  finding, just not the Opus-separation one).

  Third eval in 101-105 battery, the interdependency probe. Pool 15
  (3 models x N=5). Codename hygiene: Project Marlowe, northfield-co,
  summerline-llp, rivermouth-pty are neutral fictional names;
  northfield-co.example, summerline-llp.example, rivermouth-pty.example
  are fictional .example TLD per RFC 2606. Standard four-phase
  /eval-pit flow against the frozen rubric/rubric.md.
---

# Spec 103 - heterogeneous-precision-interdependent (the interdependency probe)

Given a single realistic artifact - the Project Marlowe Q3-26 orderbook
reconciliation - apply TEN independent change requirements in a single
pass, where THREE pairs of requirements are wired so that the order of
operations matters. R2 (sum the line_total column) depends on R6
(deduplicate the orders table); R9 (per-customer unique-order count)
depends on R6; R8 (sort the warehouse list) depends on R7 (deduplicate
the warehouse list). A naive left-to-right apply (R1, R2, R3, ..., R10)
produces a wrong end-state for R2, R8, and R9. The correct apply
requires building a small global plan: dedup first, then sum / count /
sort.

This is the interdependency probe of the 101-105 heterogeneous-precision
battery. Per the gameplan: "Hardness is in JUGGLING interacting
requirements, not raw count. ... Does a naive left-to-right pass
produce a WRONG answer? It must, or there is no discrimination." 10
requirements (down from 12 in eval 102) - the load knob is dialled
DOWN to isolate the interaction effect from the count effect. Each
individual op stays trivial per the eval-48 lesson; the only knob
turned is the wiring.

The artifact is ONE fictional orderbook reconciliation with six
distinct edit surfaces. The interdependencies are not signposted in the
prompt - the model must infer from requirement TEXT that R6 changes
what R2 sums and what R9 counts, and R7 changes what R8 sorts. The
corpus_intent enumerates all 10 requirements as independent
grep-verifiable invariants R1-R10 with the exact post-state for each,
plus the wrong-final-states a naive pass yields (R2=4060,
R9=4/3/2-wrong), and the ordering-error tracking subcategory in the
drop-distribution spec.

Standard four-phase `/eval-pit` flow against the frozen
`rubric/rubric.md`. Correctness and Hallucination are hard-fail
eligible; Discipline (apply ONLY the 10 named edits with correct global
ordering) is the load-bearing discriminator. Primary metric is the
all-requirements-correct rate per family across the 5 runs. Secondary
metrics are mean requirements-satisfied, drop-distribution per
requirement, AND the ordering-error rate (the eval's headline insight).
Voice match does not apply. The variant pool is 15 (3 models x N=5,
effort inert per the methodology). The corpus is the directory
`corpus/heterogeneous-precision-interdependent/`.
