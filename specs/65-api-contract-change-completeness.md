---
task_category: api-contract-change-completeness
prompt_under_test: |
  You are given a single corpus file at
  corpus/api-contract-change-completeness/api-and-consumers.md - a slice of the
  fictional "Veldt API" GET /orders response schema, a field-rename change, and 8
  consumer code snippets that read this API.

  THE CHANGE: rename the response field `shipping_status` to `fulfilment_status`.
  Same type (string enum), same values - only the JSON key changes.

  Your task: enumerate EVERY consumer affected by this rename. For each affected
  consumer, name the module/file and explain HOW it depends on the field (literal
  read, struct JSON tag, dynamic key iteration, pass-through, etc.). Be complete -
  a missed consumer is the failure this task measures. Also state which consumers
  are NOT affected and why.

  Output a numbered list of affected consumers (with the dependency mechanism for
  each), then a short list of unaffected consumers. Do NOT mark a consumer as
  affected if it does not read the renamed field. Append the output envelope
  (schemaVersion, tier, status, tool_budget_used) as separate lines. No em dashes
  (use spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/api-contract-change-completeness/
corpus_intent: |
  One corpus file (corpus/api-contract-change-completeness/api-and-consumers.md): a
  Veldt API response schema, a field rename (shipping_status -> fulfilment_status),
  and 8 consumers. The eval measures whether a run enumerates the COMPLETE set of
  affected consumers, including one buried consumer that reads the field via a
  generic Object.keys iteration - there is NO literal "shipping_status" string in
  that file, so a grep-only audit misses it entirely.

  QUALITY PRINCIPLE (completeness-first): the literal-read consumers and the struct-
  with-JSON-tag consumer are findable by string search. The scored signal is whether
  a run catches the dynamic-key-iteration consumer (consumer 5, fieldLogger), which
  depends on the key name but contains no literal occurrence of it. A run that lists
  the grep-able consumers but misses fieldLogger has found the shallow set and
  dropped the dangerous silent breakage (a downstream dashboard pivot keyed on the
  old field name). Marking the two genuinely-unaffected consumers (orderCache,
  indexer) as affected is a precision error.

  ANSWER KEY (for the scoring Architect - the full enumerable list):

    AFFECTED consumers (grep-able literal/tag reads):
      C1. Dash/orderRow.tsx - literal read order.shipping_status in JSX.
      C2. Notify/shipMailer.js - literal read order.shipping_status in a comparison.
      C3. Report/dailyShipStats.py - literal subscript o["shipping_status"].
      C4. Sync/warehouseSync.go - struct field ShippingStatus bound via the JSON tag
          `json:"shipping_status"`. The tag must change to "fulfilment_status";
          findable by grepping the tag, but a reader scanning only Go field names
          (ShippingStatus) without checking the tag could mis-handle it.

    BURIED AFFECTED consumer (the discriminator):
      C5. Audit/fieldLogger.js - iterates Object.keys(order) and records each field
          keyed by the JSON key string. There is NO literal "shipping_status" in this
          file, so a grep for the field name does NOT find it, yet it DOES depend on
          the field name: a downstream dashboard pivots on the exact key
          "shipping_status", and after the rename this consumer silently emits
          "fulfilment_status" records, breaking saved pivots. THIS is the buried
          item - dynamic key iteration, no literal to grep.

    BORDERLINE AFFECTED (credit if listed, lower weight):
      C6. Webhook/outbound.js - forwards the whole order object verbatim to an
          external partner whose contract expects shipping_status. The forwarded
          payload key changes, so the external consumer is affected. Less subtle
          than C5; correct to list as affected.

    NOT AFFECTED (precision traps - marking these as affected is a false positive):
      C7. Cache/orderCache.js - reads only total_cents and created_at.
      C8. Search/indexer.py - reads only id, customer_ref, notes.

  GREP-VERIFIABLE INVARIANTS (for the Architect, against the run's output):
    - A correct run names the dynamic-iteration consumer: grep -i "fieldLogger\|
      Object.keys\|iterat.*key\|dynamic.*key\|generic.*field". MISSING any reference
      to the fieldLogger / Object.keys consumer is the dropped buried item - the
      primary scored signal.
    - A correct run names the four grep-able consumers: orderRow, shipMailer,
      dailyShipStats, warehouseSync (and notes the Go JSON tag for the last).
    - PRECISION: the run must NOT mark orderCache or indexer as affected. grep -i
      "orderCache\|indexer" listed AS affected is a false positive.

  Scoring guidance:
    - Buried-item catch (load-bearing) = did the run find the Object.keys dynamic-
      iteration consumer (C5)? The single highest-signal bit.
    - Completeness = C1-C4 present + C5 present (+ C6 credit).
    - Precision (hallucination-eligible) = orderCache and indexer correctly excluded;
      no invented consumer.
    - Reasoning quality = C5 is explained as depending on the key name despite having
      no literal occurrence of it (the silent dashboard-pivot breakage); C4 is
      explained via the Go JSON struct tag.
    Voice match does NOT apply.
notes: |
  Chat A consistency-battery extension, eval 65 of 61-70. variant_pool 15 (3 models
  x N=5). THE SCORED SIGNAL IS WITHIN-FAMILY SPREAD across the 5 runs PLUS per-model
  buried-item catch-rate - NOT peak score. The question is whether one model family
  reliably catches the buried dynamic-key-iteration consumer (C5, fieldLogger, no
  literal field name to grep) on ALL 5 runs, or whether some runs drop it. Low spread
  with 5/5 catch beats high variance with a stronger single run.

  The corpus (corpus/api-contract-change-completeness/api-and-consumers.md) is a Veldt
  API response schema, a field rename (shipping_status -> fulfilment_status), and 8
  consumers. Four consumers read the field literally (or via a Go JSON struct tag) and
  are grep-findable. ONE buried consumer iterates Object.keys(order) and depends on the
  key name without ever containing a literal occurrence of it, so a grep-only audit
  misses it while a downstream dashboard pivot breaks silently after the rename. Two
  consumers genuinely do not read the field (orderCache, indexer) and serve as
  precision traps; a borderline pass-through webhook consumer is correctly counted as
  affected. Standard four-phase /eval-pit flow against the frozen rubric/rubric.md. The
  corpus is the directory corpus/api-contract-change-completeness/.
---

# Spec 65 - api-contract-change-completeness

Given a fictional Veldt API response schema, a field rename (shipping_status ->
fulfilment_status), and 8 consumers that read the API, enumerate EVERY consumer
affected by the rename, with the dependency mechanism for each.

This is a Chat A consistency-battery eval (variant_pool 15, N=5). The scored signal
is WITHIN-FAMILY SPREAD across the five runs plus per-model buried-item catch-rate,
not peak score. The discriminator is one buried consumer: `Audit/fieldLogger.js`
iterates `Object.keys(order)` and records each field keyed by its JSON key, with NO
literal occurrence of `shipping_status` in the file. A grep-only audit never finds
it, yet it depends on the field name - a downstream dashboard pivots on the exact key
string, and after the rename the consumer silently emits the new key, breaking saved
pivots.

The four literal/tag-read consumers (orderRow, shipMailer, dailyShipStats, and the Go
warehouseSync via its `json:"shipping_status"` struct tag) are the shallow set every
run should catch; finding them is necessary but not sufficient. Two consumers
(orderCache, indexer) genuinely never read the field and are precision traps -
marking them affected is a false positive; a pass-through webhook consumer is
correctly counted as affected. Standard four-phase `/eval-pit` flow against the
frozen `rubric/rubric.md`. The answer key in `corpus_intent` lists every affected and
unaffected consumer plus grep-verifiable invariants. Voice match does not apply. The
corpus is the directory `corpus/api-contract-change-completeness/`.
