---
task_category: migration-step-completeness
prompt_under_test: |
  You are given a single corpus file at
  corpus/migration-step-completeness/migration-context.md - the current schema
  (v3), target schema (v4), and change notes for a fictional production orders
  database ("Marlowe", orders ~4.2M rows, order_items ~11M rows).

  Your task: produce the COMPLETE ordered migration runbook to take the database
  from v3 to v4 with zero downtime and no data loss. The runbook must be a numbered
  ordered list of steps. Ordering matters - some steps are only safe in a specific
  sequence. Cover every schema change in the notes (N1-N6) and the application
  deploy.

  Output the numbered ordered runbook. For each step, state the operation and why
  its position in the order is required. Do NOT add steps the corpus does not
  support. Append the output envelope (schemaVersion, tier, status,
  tool_budget_used) as separate lines after the runbook. No em dashes (use spaced
  hyphens). No emojis.
variant_pool: 15
corpus: corpus/migration-step-completeness/
corpus_intent: |
  One corpus file (corpus/migration-step-completeness/migration-context.md): a v3->v4
  schema migration for a large live orders DB with change notes N1-N6. The eval
  measures whether a run produces a COMPLETE, CORRECTLY ORDERED runbook, including the
  buried easy-to-drop step: each NOT NULL column must be added NULLABLE first,
  BACKFILLED, and only THEN altered to NOT NULL. Dropping the backfill step (or
  ordering it after the NOT NULL) is the failure this task detects.

  QUALITY PRINCIPLE (completeness-first): the schema additions, the CHECK constraint,
  the index, and the app deploy are signposted. The scored signal is whether a run
  includes the three-part ordered sequence (add nullable -> backfill -> add NOT NULL)
  for BOTH NOT NULL columns (currency_code on orders, unit_price_cents on
  order_items), with backfill BEFORE the constraint. A runbook that adds a NOT NULL
  column directly on a 4.2M-row table (or adds a default to dodge the failure, writing
  wrong history) has dropped the buried step.

  ANSWER KEY (for the scoring Architect - the complete ordered runbook; minor wording
  varies but the ORDER and the presence of every step are checked):

    1. Add orders.region as NULLABLE (N2, no backfill, no ordering constraint).
    2. Add orders.currency_code as NULLABLE (NOT yet NOT NULL).  <-- buried step 1/3
    3. BACKFILL orders.currency_code = 'USD' for all existing rows (N1).  <-- buried
       step 2/3, the easy-to-drop one.
    4. ALTER orders.currency_code to NOT NULL (only safe AFTER step 3).  <-- buried
       step 3/3.
    5. Add order_items.unit_price_cents as NULLABLE.  <-- buried step 1/3 (second
       column).
    6. BACKFILL order_items.unit_price_cents from the price_history table joined on
       (order_id, sku) per N3 (NOT total_cents/sum(qty) - that is the wrong formula
       called out in N3).  <-- buried step 2/3.
    7. ALTER order_items.unit_price_cents to NOT NULL (only AFTER step 6).  <-- buried
       step 3/3.
    8. Add the status CHECK constraint using ADD CONSTRAINT ... NOT VALID, then
       VALIDATE CONSTRAINT separately (N4, avoids the long lock on 4.2M rows).
    9. Create idx_orders_status_created ON orders(status, created_at) (concurrently /
       online to avoid locking the live table).
    10. Deploy the new application version that writes currency_code, unit_price_cents,
        and constrained status (N5). It must deploy AFTER the columns exist (steps 2
        and 5) but the NOT NULL enforcement (steps 4 and 7) interacts with in-flight
        old writes - the safe pattern is: add columns + backfill + app deploy, then
        enforce NOT NULL once old writers are gone. (Credit runbooks that sequence app
        deploy after columns exist and before/around the NOT NULL enforcement with a
        stated rationale.)
    11. Document the reversible down-migration for each step (N6).

    The ABSOLUTE ordering invariants that must hold (the scored core):
      - currency_code: ADD NULLABLE  <  BACKFILL  <  ADD NOT NULL.
      - unit_price_cents: ADD NULLABLE  <  BACKFILL  <  ADD NOT NULL.
      - unit_price_cents backfill uses price_history join, NOT total_cents/sum(qty).
      - CHECK constraint uses NOT VALID + VALIDATE (not a direct validating add).

  GREP-VERIFIABLE INVARIANTS (for the Architect, against the run's output):
    - A correct run contains, for currency_code, a backfill step BETWEEN an add-
      nullable step and an add-NOT-NULL step. grep -i "backfill" present AND a
      currency_code NOT NULL step appearing AFTER it. MISSING the backfill step (or a
      NOT NULL added before any backfill) is the dropped buried item - the primary
      scored signal.
    - Same three-step ordering present for unit_price_cents.
    - A correct run names the price_history backfill source for unit_price_cents and
      does NOT use total_cents/sum(qty). grep -i "price_history" present; grep -i
      "sum(qty)\|total_cents / " used as the backfill formula is an error (N3 trap).
    - A correct run uses "NOT VALID" + "VALIDATE" for the CHECK constraint. grep -i
      "not valid" present.
    - PRECISION: the run does not invent steps the corpus does not support (e.g.
      dropping the customer_id index, partitioning, sharding).

  Scoring guidance:
    - Buried-item catch (load-bearing) = did the run include the backfill step in the
      correct position (nullable -> backfill -> NOT NULL) for BOTH NOT NULL columns?
      The single highest-signal bit.
    - Completeness = all schema changes (region, currency_code, unit_price_cents,
      CHECK, index, app deploy, rollback) present.
    - Ordering correctness = the absolute ordering invariants hold.
    - Precision (hallucination-eligible) = correct backfill source (price_history, not
      total_cents/sum(qty)); no invented steps.
    Voice match does NOT apply.
notes: |
  Chat A consistency-battery extension, eval 64 of 61-70. variant_pool 15 (3 models
  x N=5). THE SCORED SIGNAL IS WITHIN-FAMILY SPREAD across the 5 runs PLUS per-model
  buried-item catch-rate - NOT peak score. The question is whether one model family
  reliably includes the buried backfill step in the correct position (add nullable ->
  backfill -> add NOT NULL) for BOTH NOT NULL columns on ALL 5 runs, or whether some
  runs drop the backfill or add the NOT NULL column directly. Low spread with 5/5
  catch beats high variance with a stronger single run.

  The corpus (corpus/migration-step-completeness/migration-context.md) gives a v3->v4
  schema migration on a large live table. The obvious steps (add columns, add a CHECK
  constraint, add an index, deploy the app) are signposted in the change notes. The
  buried completeness item is the three-part ordered sequence for each NOT NULL
  column: add nullable, backfill existing rows, then add NOT NULL - dropping the
  middle backfill step fails on a non-empty table or writes wrong history. A second
  precision trap is the unit_price_cents backfill source (price_history join per N3,
  NOT total_cents/sum(qty), which N3 explicitly calls out as wrong). Standard
  four-phase /eval-pit flow against the frozen rubric/rubric.md. The corpus is the
  directory corpus/migration-step-completeness/.
---

# Spec 64 - migration-step-completeness

Given a fictional v3->v4 schema migration for a large live orders database (orders
~4.2M rows, order_items ~11M rows) with change notes, produce the COMPLETE ordered
migration runbook for a zero-downtime, no-data-loss migration.

This is a Chat A consistency-battery eval (variant_pool 15, N=5). The scored signal
is WITHIN-FAMILY SPREAD across the five runs plus per-model buried-item catch-rate,
not peak score. The discriminator is one easy-to-drop ordered step: each NOT NULL
column (currency_code on orders, unit_price_cents on order_items) must be added
NULLABLE first, BACKFILLED for all existing rows, and only THEN altered to NOT NULL.
A runbook that adds a NOT NULL column directly on a 4.2M-row table fails immediately
(every existing row violates the constraint), or - if it adds a default to dodge the
failure - silently writes wrong history. Dropping the backfill step, or reordering it
after the NOT NULL, is the failure this eval detects.

The other steps (the nullable region column, the status CHECK constraint via NOT
VALID + VALIDATE, the composite index, the application deploy, the rollback) are
signposted in the change notes and form the shallow completeness set. A second
precision trap is the unit_price_cents backfill source: note N3 specifies a
price_history join and explicitly calls out total_cents/sum(qty) as wrong. Standard
four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The answer key in
`corpus_intent` lists the complete ordered runbook, the absolute ordering invariants,
and grep-verifiable invariants. Voice match does not apply. The corpus is the
directory `corpus/migration-step-completeness/`.
