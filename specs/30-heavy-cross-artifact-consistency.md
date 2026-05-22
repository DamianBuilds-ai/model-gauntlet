---
task_category: cross-artifact-consistency
prompt_under_test: |
  You are given a complete slice of a fictional order-management service
  "Northwind Orders" (company "Globex") under
  corpus/heavy-cross-artifact-consistency/. The slice spans fifteen listed
  artifacts across six formats - Python application code, a database model, a SQL
  migration, a JSON Schema, an OpenAPI 3 spec, two config files, a seed-data
  fixture, three test files, prose documentation, and a captured request log -
  plus a README. Read the change request at
  corpus/heavy-cross-artifact-consistency/change-request.md (CR-4471) for the
  exact rules.

  Perform ONE coordinated rename-and-retype across the WHOLE slice: the customer
  identity field `customer_ref` (currently a STRING of the form `cust_<digits>`,
  e.g. `cust_00417`) becomes `customer_id` and is RETYPED to a 64-bit signed
  INTEGER (e.g. `417`). The mapping from old to new value is "strip the `cust_`
  prefix and parse the remaining digits as an integer" (`cust_00417` -> `417`,
  `cust_00001` -> `1`, `cust_09900` -> `9900`).

  Every artifact must stay mutually consistent: the same field name everywhere,
  the integer type everywhere the field's type is declared or validated (Python
  `int`, JSON Schema `"type": "integer"` with the old `pattern` removed, OpenAPI
  `type: integer, format: int64`, SQL `BIGINT NOT NULL`, a positive-integer
  validation), and every example / default / fixture / sample value expressed as
  the new INTEGER (an unquoted JSON/YAML number, NOT the `cust_` string and NOT a
  quoted `"417"`). Keep the field required. Rename the OpenAPI/route path parameter
  `{customer_ref}` to `{customer_id}` and retype it. Do NOT change any unrelated
  field (the order's `order_ref` stays a string and is NOT the target). Determine
  which of the listed paths actually reference the field versus which are decoys,
  and leave the decoy and the explicitly out-of-scope README unchanged.

  Produce the FULL updated content of every artifact that genuinely changes (each
  as its own clearly-labelled code block with its path), and a per-artifact
  checklist covering all fifteen listed paths plus the README: for each, state
  whether it changed and the name/type/example changes made, or that it did not
  change and why (no reference to the field, decoy, or out of scope). Do NOT claim
  an artifact is consistent if your output left an old name, an old string type, or
  an old-format example in it - a confidently-wrong "done" is worse than an
  honestly-flagged miss.

  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/heavy-cross-artifact-consistency/
corpus_intent: 20 corpus files (README + change-request + 14 genuine field-bearing artifacts in 6 formats + 1 decoy config .env.example + 3 empty package __init__ files) modelling a service slice where one field threads through 14 artifacts and must be renamed AND retyped (string -> integer) consistently across all of them; HEAVY because the field has 111 occurrences across 16 files in the BEFORE state, spread over Python, SQL, JSON Schema, OpenAPI YAML, INI config, JSON fixtures, Markdown docs, and a captured log, and any single residual old-name, old-type, or old-format-example occurrence is an inconsistency
corpus_delivered: TBD
corpus_match: TBD
notes: |
  HEAVY OPUS-STRESS PROBE (cross-artifact consistency under rename + retype /
  forgetting-occurrences-under-load). This is the consistency analog of the
  cross-reference-completeness probe (spec 22): spec 22 asks "find every reference
  to the function"; this asks "propagate one change to every artifact and leave
  none inconsistent". At two or three files a rename is trivial; the hypothesis is
  that across FOURTEEN artifacts in six formats - with a RETYPE (string ->
  integer) layered on the rename so every type-declaration site and every example
  value must also change - the cheaper models propagate the obvious Python
  occurrences and the doc heading and stop, silently leaving inconsistencies: the
  JSON Schema `"type": "string"` and its `pattern`, the OpenAPI request-body type
  and the `example: "cust_00417"`, the migration's `customer_ref TEXT NOT NULL`
  column type and its index, the config default `cust_00001`, the seed fixture
  string values, the validation regex, the path parameter, and the doc field-table
  type row. Run the full 9-variant model-only pool (Haiku x3, Sonnet x3, Opus x3;
  effort treated as inert per the methodology). Aggregate the 3 passes per model
  (mean weighted total); flag any model whose 3 passes diverge by more than 0.5 as
  a consistency finding.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong
  change is worse than a missed one. A model that renames the field but leaves its
  type as `"string"` in the JSON Schema, or that "updates" an example to a value
  that is STILL a string (`"417"` instead of the integer `417`), or that retypes
  the SQL column name but leaves it `TEXT`, has shipped a system that LOOKS migrated
  but is internally inconsistent - worse than a model that honestly flags one
  artifact it could not finish. The two heaviest-penalty errors are (a) a
  renamed-but-not-retyped artifact (the field is `customer_id` but still typed
  string / still pattern-validated / still `cust_`-valued) and (b) an over-reach
  edit that also renames or retypes the unrelated `order_ref` field or edits the
  decoy / README. The discriminator is the COUNT of artifacts left fully consistent
  (verified by READING each artifact, not the model's self-report), with
  inconsistency-introducing changes penalised hardest.

  ALL ARTIFACTS CAN BE MADE CONSISTENT - a reference end-state exists with the
  field renamed to `customer_id`, typed integer everywhere, valued as integers
  everywhere, required everywhere, the path parameter retyped, the decoy and README
  untouched, and `order_ref` left a string. There is no artifact that cannot be made
  consistent with the rest.

  ANSWER KEY (for the scoring Architect - the consistency invariants as a verifiable
  checklist; mark each artifact CONSISTENT or INCONSISTENT by READING the model's
  output for that artifact, NOT its self-report). Two global invariants apply across
  the whole output, then a per-artifact list. The grep-verifiable counts below were
  taken from the actual corpus.

    --- GLOBAL INVARIANTS (check across the entire produced output) ---
    G1  - ZERO RESIDUAL OLD NAME: the token `customer_ref` must NOT appear in any
          produced/updated artifact (code, schema, config, docs, tests, examples,
          comments, docstrings). In the BEFORE corpus `customer_ref` appears 111
          times across 16 files (including the README at 2 and the change request at
          8 - both meta-docs); in a fully consistent AFTER state every one of those
          that lives in a CHANGING artifact is now `customer_id`. A residual
          `customer_ref` in any changed artifact is an inconsistency. (The README
          and the decoy are not "changed artifacts"; see A15/A16.)
    G2  - ZERO RESIDUAL OLD-FORMAT VALUE: the literal substring `cust_` must NOT
          appear as a field VALUE in any changed artifact - every example/default/
          fixture/sample value is the integer form. In the BEFORE corpus `cust_`
          appears 64 times in total; 18 of those are inside the two meta-docs
          (README 8, change request 10), leaving 46 occurrences inside the artifacts,
          which in the AFTER state become bare integers (`417`, `1`, `9900`). A
          residual `cust_` VALUE in a changed artifact, or a value quoted as a
          string (`"417"`), is an inconsistency.
          (Mentions of the OLD name/format inside the per-artifact CHECKLIST prose -
          e.g. "renamed customer_ref to customer_id" - are allowed; the invariant is
          about the artifact CONTENT, not the explanatory checklist.)

    --- PER-ARTIFACT INVARIANTS (14 changing artifacts) ---
    A1  - src/orders/models.py (9 customer_ref occurrences). CONSISTENT requires:
          dataclass field `customer_ref: str` becomes `customer_id: int`; the
          `belongs_to(self, customer_ref: str)` parameter and body become
          `customer_id: int`; the `new_order(... customer_ref ...)` factory
          parameter and the Order construction become `customer_id`; docstrings
          updated. `order_ref: str` is UNTOUCHED. INCONSISTENT if the field is
          renamed but the type hint stays `str`.
    A2  - src/orders/api.py (8 occurrences). CONSISTENT requires: `body["customer_ref"]`
          reads become `body["customer_id"]`; the `get_orders_for_customer(self,
          customer_ref: str)` parameter becomes `customer_id: int` and the path
          docstring `/orders/by-customer/{customer_ref}` becomes `{customer_id}`;
          the repo call updated. The `cancel_order(order_ref)` handler is UNTOUCHED.
    A3  - src/orders/validation.py (10 occurrences). CONSISTENT requires: the field
          is `customer_id`; the `CUSTOMER_REF_PATTERN` cust_ regex is REMOVED and
          replaced by a positive-integer check (e.g. `isinstance(value, int) and
          value > 0`, rejecting strings including a string `"417"`); the
          `normalise_customer_ref` helper becomes a parse-to-int (strip `cust_`,
          return int) or an integer validator; error messages name `customer_id`.
          The `ORDER_REF_PATTERN` and order_ref check are UNTOUCHED. INCONSISTENT if
          the cust_ regex survives or the field is still validated as a string.
    A4  - src/orders/serializers.py (3 occurrences). CONSISTENT requires: the emitted
          key `"customer_ref": order.customer_ref` becomes `"customer_id":
          order.customer_id` (integer value). order_ref key UNTOUCHED.
    A5  - src/orders/db/order_repository.py (12 occurrences). CONSISTENT requires:
          the SQL column name `customer_ref` becomes `customer_id` in the INSERT,
          the ON CONFLICT update, and the SELECTs; the bound parameter
          `:customer_ref` / dict key becomes `:customer_id`; `find_by_customer_ref(
          self, customer_ref: str)` becomes `find_by_customer_id(self, customer_id:
          int)` with the WHERE clause matching `customer_id`. order_ref columns and
          params UNTOUCHED.
    A6  - schema/order.schema.json (3 occurrences). CONSISTENT requires: the
          `required` array entry `customer_ref` becomes `customer_id`; the property
          key becomes `customer_id`; its `"type"` becomes `"integer"` (NOT
          `"string"`); the `"pattern": "^cust_\\d{5}$"` is REMOVED and replaced with
          an integer constraint (`"minimum": 1`); the `examples` become integers
          (`[417, 9900]`). The order_ref property (type string, ord_ pattern) is
          UNTOUCHED. INCONSISTENT if the field is renamed but `"type": "string"` or
          the cust_ pattern survives (the canonical renamed-not-retyped trap).
    A7  - openapi/orders.yaml (6 occurrences). CONSISTENT requires: the path
          `/orders/by-customer/{customer_ref}` becomes `{customer_id}`; the path
          parameter `name: customer_ref` becomes `name: customer_id` with `schema:
          type: integer, format: int64` (NOT string + cust_ pattern) and its
          `example` an integer (`417`); the `OrderInput` required list and property
          `customer_ref` become `customer_id` with `type: integer, format: int64`
          and `example: 417`; the request-body `example.customer_ref: "cust_00417"`
          becomes `customer_id: 417`. order_ref stays string. INCONSISTENT if any
          OpenAPI occurrence keeps the string type or the cust_ example.
    A8  - config/app.ini (3 occurrences). CONSISTENT requires: `default_customer_ref
          = cust_00001` becomes `default_customer_id = 1` (key renamed AND value an
          integer 1). The `[orders] order_ref_prefix` is UNTOUCHED. INCONSISTENT if
          the value stays `cust_00001` or becomes the string-looking `cust_1`.
    A9  - migrations/0007_add_orders.sql (4 occurrences). CONSISTENT requires: the
          column `customer_ref TEXT NOT NULL` becomes `customer_id BIGINT NOT NULL`
          (name AND type); the index `idx_orders_customer_ref ON orders
          (customer_ref)` becomes `customer_id` (the index name may keep or update
          its suffix, but the indexed column must be `customer_id`); NOT NULL kept.
          The order_ref PRIMARY KEY, the order_ref CHECK constraint, and created_at
          are UNTOUCHED. INCONSISTENT if the column is renamed but stays `TEXT`.
    A10 - tests/test_orders_api.py (7 occurrences). CONSISTENT requires: the
          `VALID_BODY` `"customer_ref": "cust_00417"` becomes `"customer_id": 417`;
          the assertions `result["customer_ref"] == "cust_00417"` become
          `result["customer_id"] == 417`; the `get_orders_for_customer("cust_00417")`
          / `("cust_99999")` arguments become integers `417` / `99999`; the
          assertion on the returned order's field becomes `customer_id == 417`. The
          order_ref assertions and the cancel test stay string-based. INCONSISTENT
          if a test still passes the cust_ string or asserts the old key.
    A11 - tests/test_validation.py (12 occurrences). CONSISTENT requires: the
          `_body` default `"customer_ref": "cust_00417"` becomes `"customer_id":
          417`; the missing-field test targets `customer_id`; the bad-format cases
          become integer cases (a string `"417"`, a negative `-1`, a non-int ->
          ValidationError; an int `417` -> passes) consistent with the A3 validator;
          the normalise test expects the integer `417`. The order_ref test stays a
          string check. INCONSISTENT if cust_ string cases survive as the customer
          assertions.
    A12 - tests/fixtures/orders_seed.json (3 occurrences). CONSISTENT requires: each
          of the three records' `"customer_ref": "cust_00417" / "cust_00001" /
          "cust_09900"` becomes `"customer_id": 417 / 1 / 9900` (key renamed AND
          unquoted integer value). order_ref values stay strings. INCONSISTENT if a
          value is quoted (`"417"`) or keeps the cust_ form.
    A13 - docs/orders-api.md (6 occurrences). CONSISTENT requires: the field-table
          row `| customer_ref | string | ... cust_NNNNN |` becomes `| customer_id |
          integer | ...` (name AND type column AND example/format); the JSON request
          example `"customer_ref": "cust_00417"` becomes `"customer_id": 417`; the
          by-customer path and example `cust_00417` become `{customer_id}` and `417`;
          the prose sentences naming the field and its `^cust_\d{5}$` format are
          updated to describe an integer. The order_ref row and prose stay strings.
          INCONSISTENT if the type column still says "string" or an example keeps
          cust_.
    A14 - docs/sample-request.log (4 occurrences). CONSISTENT requires: both the
          logged POST request body and the 201 response body, and the
          GET /orders/by-customer/cust_00417 line and its 200 response, have
          `customer_ref: "cust_00417"` rewritten to `customer_id: 417` (integer) and
          the path to `/orders/by-customer/417`. order_ref values stay strings.

    --- DO-NOT-TOUCH ARTIFACTS (precision: editing these is over-reach) ---
    A15 - config/.env.example - DECOY. Contains zero `customer_ref` field tokens
          (only infrastructure variables). It is listed in the change request for
          completeness. CONSISTENT outcome = LEFT UNCHANGED. Inventing a customer
          variable here, or "renaming" something in it, is a precision error
          (the over-reach trap symmetric to a false positive on spec 22).
    A16 - README.md - OUT OF SCOPE by rule 8 of the change request. It references
          `customer_ref` in prose describing the BEFORE state. CONSISTENT outcome =
          LEFT UNCHANGED. Editing the README to rename the field is an out-of-scope
          edit and counts against precision.
    A17 - the three package `__init__.py` files (src/orders, src/orders/db, tests)
          and any other file with no field reference - LEFT UNCHANGED. Inventing a
          field reference in them is a hallucinated edit.

    --- DECOY FIELD (must survive unchanged everywhere) ---
    D1  - `order_ref` (a string of the form `ord_NNNN`) is NOT the target. It
          appears throughout the corpus and must remain a string with its `ord_`
          format intact in every artifact. Renaming or retyping `order_ref` (e.g.
          to `order_id` integer) is an inconsistency-by-overreach and is penalised
          like a false positive: the change request explicitly scopes the work to
          the customer identity field only.

  CONSISTENCY SCORING MODEL (for the Architect): a fully consistent solution leaves
  all 14 changing artifacts internally and mutually consistent (name + type + value
  + required all propagated), leaves A15/A16/A17 untouched, and leaves D1 intact.
  Score the COUNT of the 14 changing artifacts that are fully consistent, then apply
  the two global invariants G1/G2 and the precision checks (A15/A16/A17 over-reach,
  D1 over-reach) as penalties. An artifact that is renamed but not retyped is NOT
  consistent (it counts as a miss AND, because it is the canonical confidently-wrong
  trap, weighs on Correctness/Hallucination).

  Scoring guidance:
    - Completeness (weight 2.0) = of the 14 changing artifacts, how many the model
      left FULLY consistent (name renamed AND type retyped AND example values
      revalued AND required preserved), verified by reading each artifact. 14/14 is
      exemplary; each artifact left with a residual old name, old string type, or
      old-format value drops the score. This is the primary discriminator. Count
      inconsistent artifacts explicitly. The cross-format ones (A6 JSON Schema type,
      A7 OpenAPI type + path param + example, A9 SQL column type, A8 config default,
      A12 fixture integer values) are the strongest signal of
      forgetting-under-load; the Python code occurrences (A1, A2, A4) every model
      should hold.
    - Correctness (hard-fail eligible) = is the end-state a coherent, runnable,
      mutually-consistent system. A solution that renames the field but leaves the
      JSON Schema / OpenAPI / SQL types as string (renamed-not-retyped), or quotes
      the integer value as a string, or breaks an artifact's syntax, fails
      Correctness. The renamed-not-retyped artifact is the canonical wrong answer.
    - Hallucination (hard-fail eligible) = editing the decoy (A15) or README (A16)
      or an __init__ file (A17), inventing a field reference where none exists, OR
      retyping/renaming the unrelated `order_ref` field (D1) - any over-reach that
      introduces an inconsistency the change did not call for. Claiming an artifact
      is consistent when the output left an old name/type/value in it is also a
      hallucinated "done" and the heaviest penalty.
    - Reasoning quality = did the model correctly carry the RETYPE through every
      type-declaration site (not just the name through every occurrence) AND
      correctly distinguish the target field from the `order_ref` decoy and the
      decoy file, rather than doing a blind find-replace of the name. This is where
      Opus is hypothesised to separate - holding the name + type + value + scope
      invariants across fourteen artifacts at once.
    - Discipline = stayed in scope (changed only the 14 field-bearing artifacts,
      left the decoy / README / __init__ files alone, left order_ref alone, did not
      add new fields or alter unrelated order/line-item logic).
    - Format adherence = output envelope + each changed artifact as its own labelled
      code block with its path + the per-artifact checklist covering all listed
      paths.
    - Source transparency = the checklist maps each of the listed paths to its
      change (or to the reason it did not change), and values are derived by the
      stated mapping.
    Artifact-consistency count, zero residual old-name/old-type/old-value
    occurrences, and zero over-reach edits are the scored discriminators. Prose
    elegance is NOT the point - that is where Opus tied Sonnet on the earlier
    consolidation eval. Voice match does NOT apply.

    Suggested scoring shorthand for the Architect: consistent = (changing artifacts
    left fully consistent) / 14; residual-penalty = number of changed artifacts with
    a surviving `customer_ref` token or `cust_` value or string type; over-reach
    penalty = number of do-not-touch artifacts edited plus 1 if order_ref was
    renamed/retyped. A solution that leaves 14/14 consistent with zero residuals and
    zero over-reach is the exemplary 5 on Completeness and Correctness; leaving the
    cross-format type sites renamed-but-not-retyped, quoting the integer, or editing
    the decoy is where the score falls.
---

# Spec 30 - heavy-cross-artifact-consistency (the rename-and-retype-across-N-artifacts probe)

The cross-artifact-consistency analog of the cross-reference-completeness probe
(spec 22). Spec 22 asks "find EVERY reference to one deprecated function"; this
spec asks "propagate ONE coordinated change to EVERY artifact and leave none
inconsistent". At two or three files a rename is trivial; this spec scales the
artifact count to FOURTEEN files across SIX formats - Python, SQL, JSON Schema,
OpenAPI YAML, INI config, JSON fixtures, Markdown docs, and a captured log - with
a RETYPE layered on top of the rename so that every type-declaration site and every
example value must change too, not only the places that use the field's name. That
is the load level where the field stops bunching at the top, because holding the
name, the type, the value-mapping, and the in-scope/out-of-scope distinction across
fourteen artifacts at once is where forgetting-under-load bites.

The corpus (`corpus/heavy-cross-artifact-consistency/`) is a complete slice of a
fictional order-management service "Northwind Orders" (company "Globex"). One
domain field - the customer identity `customer_ref`, a string of the form
`cust_<digits>` - threads through fourteen artifacts (112 occurrences in the BEFORE
state). Change request CR-4471 renames it to `customer_id` and retypes it from
string to a 64-bit integer, with every example value remapped (`cust_00417` ->
`417`). The slice plants two precision controls: a decoy field `order_ref` (also a
string, also threaded everywhere, that must survive unchanged) and a decoy file
`config/.env.example` (listed in the change request but holding no field reference,
so it must be left untouched), alongside an explicitly out-of-scope README. The
renamed-but-not-retyped artifact (field renamed but its JSON Schema / OpenAPI / SQL
type left as string, or its example left as `cust_...` or quoted `"417"`) is the
canonical confidently-wrong trap.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is central: a confidently-wrong change (renamed
not retyped, integer quoted as a string, decoy or README edited, or the unrelated
`order_ref` field dragged along) is worse than an honestly-flagged miss, because it
ships a system that looks migrated but is internally inconsistent. Completeness (the
COUNT of the fourteen artifacts left fully consistent, verified by reading each
artifact rather than the self-report) and Hallucination (over-reach edits, invented
references, false "done" claims) are the scored discriminators - not prose elegance,
since elegance is where Opus tied Sonnet on the earlier consolidation eval.
Reasoning quality captures whether the model carried the retype through every
type-declaration site and respected the decoys rather than blind-find-replacing the
name. The variant pool is 9 (3 models x N=3, effort inert per the methodology). The
corpus is the directory `corpus/heavy-cross-artifact-consistency/`.
