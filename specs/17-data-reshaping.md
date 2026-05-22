---
task_category: data-reshaping
prompt_under_test: |
  You are given a flat CSV at corpus/data-reshaping/orders.csv. Each row is a single
  order LINE ITEM. The data is one-to-many in two levels: a customer has many orders,
  and an order has many line items, so the same customer and the same order repeat
  across rows.

  CSV columns (header row included):
    customer_id, customer_name, customer_email, order_id, order_date, line_no, sku,
    product_name, quantity, unit_price_cents, discount_code

  Transform the flat CSV into the following nested JSON shape EXACTLY. Output a single
  JSON array of customer objects. Use these keys, in this order, and no others:

    [
      {
        "customer_id": string,
        "name": string,
        "email": string,
        "orders": [
          {
            "order_id": string,
            "order_date": string,
            "order_total_cents": integer,
            "line_items": [
              {
                "line_no": integer,
                "sku": string,
                "product_name": string,
                "quantity": integer,
                "unit_price_cents": integer,
                "line_total_cents": integer,
                "discount_code": string | null
              }
            ]
          }
        ]
      }
    ]

  Documented rules and edge cases:
    1. GROUPING: group line items under their order, and orders under their customer.
       Each customer appears once; each order appears once under its customer. Preserve
       first-seen order for customers, orders, and line items (the order they first
       appear in the file).
    2. line_total_cents = quantity * unit_price_cents for that line item.
    3. order_total_cents = the sum of line_total_cents across that order's KEPT line
       items (see rule 5).
    4. MISSING OPTIONAL FIELD: discount_code is optional. When the CSV cell is empty,
       the JSON value MUST be null (JSON null, not the empty string "").
    5. ONE MALFORMED ROW TO SKIP: exactly one line item has a non-numeric quantity and
       cannot be parsed. SKIP that single line item and add a short note (outside the
       JSON array) naming the order_id and line_no you skipped and why. Do NOT skip the
       whole order it belongs to - keep that order's other valid line items, and
       compute order_total_cents from the kept lines only. Do NOT coerce, guess, or
       invent a quantity for the malformed line.
    6. quantity, unit_price_cents, line_total_cents, order_total_cents, and line_no are
       integers. customer_id, order_id, sku, product_name, name, email are strings.

  Output the JSON array first. Then, OUTSIDE the JSON, append the skip note and the
  required output envelope (schemaVersion, tier, status, tool_budget_used) on separate
  lines. No em dashes (spaced hyphens). No emojis. Do not add keys the schema does not
  list.
variant_pool: 9
corpus: corpus/data-reshaping/
corpus_intent: |
  One flat CSV (corpus/data-reshaping/orders.csv): 15 data rows (plus a header),
  representing 6 customers, with one-to-many nesting at two levels (customer -> orders
  -> line items). Contains deliberate edge cases: several empty discount_code cells (the
  optional field that must become JSON null), and exactly one malformed row (order
  O1011, line_no 2, quantity literal "two") that must be skipped-with-note WITHOUT
  dropping the rest of its order.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a reshaping that LOOKS valid
  but mis-groups, drops the wrong rows, or coerces the malformed value is WORSE than an
  honest, slightly-incomplete one. The two confidently-wrong traps:
    (a) The malformed line. A weaker model may "helpfully" coerce quantity "two" -> 2 and
        silently include it, producing a clean-looking JSON with a FABRICATED quantity
        and an inflated order_total_cents for O1011. OR it may drop the ENTIRE O1011
        order because one line is bad, silently losing the valid line 1 (4 x Red Widget)
        and corrupting customer C003's data. Both produce confident, well-formed JSON
        that a downstream system would trust and that is wrong. The correct behaviour is
        surgical: skip only line 2, keep line 1, note the skip, and compute O1011's total
        from the kept line.
    (b) The empty discount_code. Emitting "" (empty string) instead of null is a subtle
        distortion: a consumer testing `discount_code === null` would mis-route every
        such order. The honest, correct value is JSON null.
  Reward exact grouping, exact shape, true totals, JSON null for missing, and the
  surgical malformed-line skip with a note. Penalise hardest the plausible-but-wrong
  output: a coerced quantity, a whole-order drop, an inflated total, or "" for null.
  An output that is correct on grouping/nesting/null/skip but, say, omits the skip NOTE
  is incomplete-but-honest and beats a tidy output with a fabricated quantity.

  ANSWER KEY (for the scoring Architect - computed from the corpus).

  Counts: 15 data rows. 14 valid line items kept. 1 malformed row SKIPPED:
  order_id O1011, line_no 2, quantity "two" (non-numeric). 6 customers. 9 orders total.

  Per customer (first-seen order; line_total_cents = quantity * unit_price_cents;
  order_total_cents = sum of kept line totals):

    C001 Ada Lovelace, ada@example.com - 2 orders:
      O1001 (2026-03-01) total 5200: line1 SKU-RED qty2 unit1500 line_total 3000
        discount "SPRING10"; line2 SKU-BLU qty1 unit2200 line_total 2200 discount
        "SPRING10".
      O1042 (2026-03-14) total 4000: line1 SKU-GRN qty5 unit800 line_total 4000
        discount null (empty cell).
    C002 Alan Turing, alan@example.com - 1 order:
      O1003 (2026-03-02) total 7850: line1 SKU-RED qty1 unit1500 line_total 1500
        discount null; line2 SKU-YLW qty3 unit650 line_total 1950 discount "WELCOME5";
        line3 SKU-BLU qty2 unit2200 line_total 4400 discount "WELCOME5".
    C003 Grace Hopper, grace@example.com - 2 orders:
      O1007 (2026-03-05) total 8000: line1 SKU-GRN qty10 unit800 line_total 8000
        discount "BULK20".
      O1011 (2026-03-09) total 6000: line1 SKU-RED qty4 unit1500 line_total 6000
        discount null. (line2 is the MALFORMED row - skipped, NOT counted; O1011 keeps
        line1 and totals 6000, NOT dropped, NOT 12000.)
    C004 Edsger Dijkstra, edsger@example.com - 1 order:
      O1015 (2026-03-11) total 13800: line1 SKU-BLK qty1 unit9900 line_total 9900
        discount null; line2 SKU-YLW qty6 unit650 line_total 3900 discount "SPRING10".
    C005 Katherine Johnson, katherine@example.com - 2 orders:
      O1020 (2026-03-12) total 8200: line1 SKU-BLU qty3 unit2200 line_total 6600
        discount null; line2 SKU-GRN qty2 unit800 line_total 1600 discount null.
      O1031 (2026-03-13) total 9900: line1 SKU-BLK qty1 unit9900 line_total 9900
        discount "VIP15".
    C006 Margaret Hamilton, margaret@example.com - 1 order:
      O1040 (2026-03-16) total 10500: line1 SKU-RED qty7 unit1500 line_total 10500
        discount null.

  The single highest-signal correctness check is O1011: correct = keep line1, skip
  line2, total 6000, plus a skip note. Confidently-wrong = total 12000 (coerced "two"
  to 2) OR O1011 absent entirely (whole-order drop, C003 then shows only O1007).

  Scoring guidance:
    - Correctness (hard-fail eligible): grouping (6 customers, 9 orders, correct
      nesting), totals (every order_total_cents matches above), and the malformed-line
      handling. A coerced quantity, an inflated O1011 total, a dropped O1011, or wrong
      grouping is Correctness=1 territory (confidently wrong, well-formed but false).
    - Completeness: all 6 customers, all 9 orders, all 14 kept line items present, and
      the skip note included.
    - Format adherence: exact key set and key ORDER at all three levels, correct types
      (integers vs strings), JSON null (not "") for empty discount_code, valid JSON
      array, envelope outside the JSON.
    - Hallucination (hard-fail eligible): inventing a quantity for the malformed row, an
      extra order, a discount code that is not in the file, or a customer not present.
    - Discipline: did it follow "skip only the bad line, note it, do not coerce" exactly,
      rather than improvising a coercion or a whole-order drop?
    - Reasoning quality: if it shows reasoning, is the skip decision and the partial-order
      handling explained correctly?
    - Source transparency: does the skip note correctly name O1011 / line_no 2 / "two"?
    Voice match does NOT apply.
notes: |
  New task type. Tests deterministic data reshaping under a strict target schema with a
  two-level one-to-many nesting (customer -> orders -> line items), plus exact handling
  of two documented edge cases: a missing optional field (empty discount_code -> JSON
  null) and a single malformed row (non-numeric quantity) that must be skipped surgically
  with a note while preserving the rest of its order.

  The eval is built so a weaker model can be CONFIDENTLY WRONG, not just incomplete. The
  malformed row is the trap: the "helpful" failure is to coerce quantity "two" -> 2 and
  emit clean JSON with a fabricated value and an inflated O1011 total (12000 instead of
  6000); the "overcautious" failure is to drop the entire O1011 order and silently lose
  its valid line 1, corrupting customer C003. Both look well-formed and would be trusted
  downstream. The correct answer is surgical: skip only the bad line, keep the rest, note
  the skip, total from kept lines. The empty-cell trap (emit "" instead of null) is the
  second, subtler confidently-wrong path. See corpus_intent for the full computed answer
  key (6 customers, 9 orders, 14 kept line items, every order total).

  Correctness and Hallucination are hard-fail eligible (a coerced/invented quantity or a
  mis-grouping is a wrong answer, and fabricating a quantity for the unparseable row is a
  hallucination). Format adherence is load-bearing (exact key order at three nesting
  levels, integer-vs-string types, JSON null vs empty string). The single highest-signal
  check is the O1011 order. Voice match does not apply. The corpus is the directory
  corpus/data-reshaping/.
---

# Spec 17 - data-reshaping (flat CSV to nested JSON)

Transform the flat CSV at `corpus/data-reshaping/orders.csv` (15 data rows, one row per
order line item) into a strict nested JSON shape - an array of customers, each holding
their orders, each holding their line items - defined exactly in the prompt. Standard
four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`.

The data is one-to-many at two levels (customer -> orders -> line items), so the core
skill is correct grouping plus exact-shape adherence (key set, key order, and types at
all three levels, and JSON null - not an empty string - for the missing optional
discount_code). Two documented edge cases carry the differentiation: the empty
discount_code cells (must become JSON null) and a single malformed row (order O1011,
line 2, quantity literal "two") that must be skipped surgically with a note while keeping
the rest of that order intact.

This is the correctness-first quality principle: a well-formed JSON that coerces "two"
to 2 (inflating O1011's total) or drops the whole O1011 order (losing its valid line and
corrupting customer C003) is CONFIDENTLY WRONG and worse than an honest output that is
slightly incomplete but mis-groups nothing and invents nothing. Correctness and
Hallucination are hard-fail eligible; Format adherence is load-bearing. The highest-signal
correctness check is the O1011 order (correct total 6000 with a skip note, versus the
12000-coerced or order-dropped failures). Voice match does not apply. The corpus is the
directory `corpus/data-reshaping/`.
