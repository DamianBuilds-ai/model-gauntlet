---
task_category: high-stakes-zero-error
prompt_under_test: |
  You are given a synthetic order-management slice for a fictional "Acme Orders"
  service under corpus/high-stakes-zero-error/, in its PRE-change state. Seven
  artifacts describe the same orders resource and all currently agree on one
  field: the order owner is identified by customer_id, an INTEGER.

  Apply this exact change across ALL seven artifacts, keeping them MUTUALLY
  CONSISTENT:
    - Rename the field from customer_id to account_ref everywhere it appears.
    - Change its type from integer to a STRING (a UUID).
    - Apply a maximum length of 36 characters wherever a length or type is
      expressed (the SQL column, the OpenAPI schema, the config validation).
    - Every example, placeholder, or sample VALUE for this field must become a
      string (a quoted UUID-shaped value), not an integer.

  Output the full updated content of every artifact that must change (the SQL
  migration, the ORM model, the serializer, the OpenAPI contract, the config, the
  docs, and the sample payload), each clearly labelled with its file path. After
  the artifacts, list the cross-artifact consistency invariants you preserved (the
  agreements that must hold between artifacts: same name everywhere, same type
  everywhere, the length constraint where length is expressed, string-valued
  examples, and any code that must change because the type changed).

  Rules:
    - A SINGLE inconsistency between any two artifacts is a failure. If the schema
      says account_ref string but the serializer still emits customer_id, or the
      docs example still carries an integer, or the SQL index still names the old
      column, the change is broken.
    - Do NOT leave any reference to the old name or the old integer type in any
      artifact that must change. Do NOT change unrelated fields (id, status,
      total_cents).
    - A confidently-wrong edit (renaming the key but leaving an integer value, or
      leaving a type-dependent code path that no longer works) is worse than a
      visible omission - it produces artifacts that look migrated but are mutually
      inconsistent.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/high-stakes-zero-error/
corpus_intent: 7 artifacts (SQL migration + ORM model + serializer + OpenAPI contract + config + docs + sample) describing one resource that must change consistently
corpus_delivered: REUSED from eval 24
corpus_match: REUSED from eval 24
notes: |
  N=5 CONFIRMATION RE-RUN of eval 24 (high-stakes-zero-error). Original ran at
  variant_pool 9 (3 models x N=3) and surfaced a candidate Opus over-engineering
  trait under cross-artifact consistency load. This re-run lifts the pool to 15
  (3 models x N=5) to confirm or refute the signal with two extra passes per
  model. Corpus, prompt, answer key, and scoring guidance are CLONED VERBATIM
  from eval 24 - the only delta is variant_pool (9 -> 15) and this notes block.
  Do NOT regenerate the corpus; reuse corpus/high-stakes-zero-error/ as-is so
  the comparison stays apples-to-apples.

  OPUS-STRESS PROBE (cross-artifact consistency under load / zero-error). This
  tests the failure mode where a model, applying one change across many artifacts,
  updates most consistently but leaves ONE artifact (or one reference within an
  artifact) mismatched - and a single mismatch breaks the system. The cross-
  matching load is holding the same field's name, type, and length constraint
  identical across seven artifacts at once. At small scale (rename in two files)
  every model is consistent; the hypothesis is that across seven artifacts with
  multiple references each - and two type-dependent code paths that must also
  change - the cheaper models drop or mismatch a reference (error) while Opus holds
  every artifact mutually consistent. Run the full 15-variant model-only pool
  (Haiku x5, Sonnet x5, Opus x5; effort treated as inert per the methodology).
  Aggregate the 5 passes per model (mean weighted total); flag any model whose 5
  passes diverge by more than 0.5 as a consistency finding.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong edit
  is worse than a missed one. A model that renames customer_id to account_ref in
  the sample but leaves the value as the integer 91023, or renames the OpenAPI
  property but leaves type integer, or removes the field name but keeps the
  serializer's int() cast that now crashes on a UUID, has produced artifacts that
  LOOK migrated but are mutually inconsistent and would break in production - worse
  than visibly skipping an artifact. The discriminator is ERROR COUNT: every
  remaining inconsistency (old name left, integer type/value left, length
  constraint missing where required, type-dependent code path not updated) is an
  error and is heavily penalised.

  ANSWER KEY (for the scoring Architect). The corpus was salted via grep so the
  reference map is exact. The change is verifiable artifact-by-artifact and then
  against the cross-artifact invariants. There are 7 artifacts to change and 6
  cross-artifact invariants that must hold across them.

  PER-ARTIFACT required edits (each must be fully done; a half-done artifact is an
  error):

    A1. migrations/001_create_orders.sql - TWO reference points:
        (i) column "customer_id INTEGER NOT NULL" -> "account_ref VARCHAR(36) NOT
            NULL" (UUID/CHAR(36) also acceptable; the point is a STRING type with
            length 36, not INTEGER).
        (ii) the index line: BOTH the index identifier idx_orders_customer_id ->
            idx_orders_account_ref AND the indexed column (customer_id) ->
            (account_ref). ERROR if the index still names the old column or keeps
            the old identifier - the classic missed cross-reference.

    A2. models/order.py - THREE reference points, plus the type:
        (i) field annotation "customer_id: int" -> "account_ref: str" (type MUST
            change int -> str).
        (ii) owner_key body f"order-owner:{self.customer_id}" ->
            f"order-owner:{self.account_ref}".
        (iii) from_row mapping customer_id=row["customer_id"] ->
            account_ref=row["account_ref"] (BOTH the kwarg name and the dict key).
        ERROR if any of the three is left as customer_id, or the annotation is
        still : int.

    A3. api/serializers.py - TWO reference points, plus a LOAD-BEARING type fix:
        (i) serialize_order: "customer_id": order.customer_id ->
            "account_ref": order.account_ref (JSON key AND attribute).
        (ii) parse_order_request: "customer_id": int(payload["customer_id"]) ->
            "account_ref": payload["account_ref"] - the int() CAST MUST BE REMOVED
            (the value is now a UUID string; int() on it would crash). Leaving the
            int() cast is the canonical confidently-wrong edit here: the key is
            renamed but the type-dependent code path is broken. ERROR if int() (or
            any integer coercion) survives.

    A4. api/openapi.yaml - TWO reference points, plus type + length:
        (i) required list entry customer_id -> account_ref.
        (ii) property: customer_id (type integer) -> account_ref with type string,
            format uuid, AND maxLength 36. ERROR if type stays integer, if
            maxLength 36 is missing, or if the required entry is not renamed.

    A5. config/defaults.json - THREE reference points, plus value type + the 36
        constraint:
        (i) default_order.customer_id: 0 -> "account_ref": "<uuid string
            placeholder>" (key renamed AND value becomes a quoted string, not the
            integer 0).
        (ii) validation.required_fields array entry "customer_id" -> "account_ref".
        (iii) validation.customer_id_max_length: null -> "account_ref_max_length":
            36 (key renamed AND the value becomes 36, carrying the length
            constraint into config). ERROR if the max-length stays null or the key
            keeps the old name.

    A6. docs/orders-api.md - FOUR reference points, plus value type:
        (i) the intro prose naming customer_id (integer) -> account_ref (string).
        (ii) the Order-object table row | customer_id | integer | -> | account_ref
            | string | (type column MUST change to string).
        (iii) the example-response JSON: "customer_id": 91023 -> "account_ref":
            "<uuid string>" (key AND the integer value -> quoted string).
        (iv) the Notes paragraph referencing customer_id -> account_ref.
        ERROR if any prose/table/example still says customer_id, shows integer
        type, or carries the integer value 91023.

    A7. samples/example_order.json - ONE reference point, plus value type:
        "customer_id": 91023 -> "account_ref": "<uuid string>" (key AND value; the
        value MUST become a quoted string, not the integer 91023). ERROR if the
        value stays 91023 / numeric.

  CROSS-ARTIFACT INVARIANTS (the consistency checks BETWEEN artifacts - these are
  the "a single inconsistency breaks it" discriminators):
    X1. NAME IDENTITY: the field is named exactly account_ref in ALL seven
        artifacts. ERROR if any artifact still says customer_id (or a variant like
        accountRef, account_id, account_reference - it must be exactly
        account_ref).
    X2. TYPE IDENTITY: the field is a STRING everywhere a type is expressed - SQL
        VARCHAR(36)/CHAR(36)/UUID (not INTEGER), model : str (not : int), OpenAPI
        type string (not integer). ERROR if any artifact still types it as an
        integer.
    X3. LENGTH CONSTRAINT PRESENCE: the 36 limit appears wherever length is
        expressible - SQL VARCHAR(36), OpenAPI maxLength 36, config
        account_ref_max_length 36. ERROR if 36 is missing from any of those three,
        or a different number is used.
    X4. STRING-VALUED EXAMPLES: every example/placeholder/sample VALUE for the
        field is a quoted string (UUID-shaped), not an integer - config placeholder,
        docs example, sample payload. ERROR if any of those three carries a numeric
        value (0 or 91023) under the new key.
    X5. TYPE-DEPENDENT CODE UPDATED: the serializer's int() cast in
        parse_order_request is removed (you cannot int() a UUID). ERROR if it
        survives. This is the code-consistency invariant that a name-only rename
        misses.
    X6. SQL INDEX CONSISTENCY: the index in the migration references the renamed
        column and has a consistent identifier (idx_orders_account_ref on
        account_ref). ERROR if the index still references customer_id or keeps the
        old identifier - a cross-reference inside one artifact that is easy to drop.

  PRECISION GUARDS (must NOT change - changing them is a confidently-wrong edit):
    - The id, status, and total_cents fields are unrelated and must stay exactly as
      they are (id integer, status enum, total_cents integer). A model that also
      renames or retypes these has over-applied the change and introduced errors.
    - The README.md is corpus documentation, not an artifact to ship; it does not
      need to be in the output (no penalty either way, but it is not one of the 7).

  Scoring guidance:
    - Correctness (hard-fail eligible, weight 3.0) = is the change applied
      correctly and completely with the artifacts MUTUALLY CONSISTENT. Any
      surviving inconsistency (a cross-artifact invariant X1-X6 violated) is a
      correctness error; enough of them, or a single load-bearing one (e.g. the
      int() cast left, X5), drops Correctness toward hard-fail.
    - Completeness (weight 2.0) = were ALL 7 artifacts updated and ALL their
      reference points covered (count missed reference points and missed
      artifacts). A skipped artifact or a dropped reference within one is an
      incompleteness.
    - Hallucination (hard-fail eligible) = inventing an artifact, a field, or a
      constraint not in the corpus; or claiming consistency that the output does
      not have (e.g. an invariant checklist that says "all string-valued" over a
      sample that still shows 91023). Claiming a consistency that is not present is
      the canonical confidently-wrong here.
    - Reasoning quality = did the model catch the NON-OBVIOUS cross-references: the
      SQL index (X6), the serializer int() cast (X5), the config max-length key
      (A5 iii), and the integer example VALUES that must become strings (X4). These
      buried, type-dependent points are where Opus is hypothesised to separate from
      a model that does a surface name-only rename.
    - Discipline = did NOT touch id/status/total_cents, did NOT over-apply.
    - Source transparency = the cross-artifact invariant list at the end maps the
      consistency checks to the artifacts.
    - Format adherence = output envelope + every changed artifact labelled with its
      path + the invariant checklist.
    ERROR COUNT (surviving inconsistencies + over-applied changes) is the scored
    discriminator: zero errors across all 7 artifacts and all 6 cross-artifact
    invariants is the exemplary 5; each surviving old-name / old-type / missing-
    length / unconverted-value / un-updated-code-path is an error that drops the
    score. Voice match does NOT apply.
---

# Spec 116 - rerun-eval24-overengineering-n5 (N=5 confirmation of the Opus over-engineering trait)

N=5 CONFIRMATION RE-RUN of eval 24 (high-stakes-zero-error). Eval 24 ran at the
standard variant_pool 9 (3 models x N=3) and surfaced a candidate Opus over-
engineering trait under cross-artifact consistency load. This re-run lifts the
pool to 15 (3 models x N=5) to confirm or refute the signal with two extra passes
per model.

Corpus, prompt-under-test, answer key, per-artifact required edits, cross-artifact
invariants, precision guards, and scoring guidance are CLONED VERBATIM from eval
24 - the only deltas are variant_pool (9 -> 15) and this notes block. Do NOT
regenerate the corpus; reuse `corpus/high-stakes-zero-error/` as-is so the
N=3-vs-N=5 comparison stays apples-to-apples.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle and the ERROR COUNT discriminator remain the
scored signals (same as eval 24); the only change is variance resolution at the
model level. Voice match does not apply. The variant pool is 15 (3 models x N=5,
effort inert per the methodology). The corpus is the directory
`corpus/high-stakes-zero-error/`.
