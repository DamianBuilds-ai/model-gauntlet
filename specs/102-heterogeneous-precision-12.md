---
task_category: heterogeneous-precision-battery
prompt_under_test: |
  You are given a single target file at
  corpus/heterogeneous-precision-12/veldt-platform-audit.md - the Q3-26
  quarterly audit pack for the fictional Veldt platform. It contains a
  service-tier roster table, a public status-page blurb, a fenced JSON
  rate-card config block, a regional-rollout bullet list, a
  contact-extraction worksheet with free-form prose notes, a deduplication
  queue, a feature-flag matrix table, and a checksum-tally line.

  Apply the following TWELVE independent change requirements to that file
  in a single pass. Each requirement is a precise, deterministic edit;
  each has exactly one correct result. Apply ONLY what is listed. Do NOT
  reformat, reorder, re-align, normalise, or "improve" anything the
  requirements do not name. Do NOT touch any other line.

  CHANGE REQUIREMENTS (apply all twelve):

    R1. FIELD RENAME (table header). In the "Service-tier roster" table,
        rename the `tier_label` column header to `service_tier`. Update
        ONLY the header cell; leave every row's value (gold / silver /
        bronze) unchanged.

    R2. ARITHMETIC GRAND TOTAL. The "Grand total monthly requests
        (millions)" line currently reads `Grand total monthly requests
        (millions): 0`. SET the number to the exact sum of the
        `monthly_requests_millions` column across all eight rows of the
        roster.

    R3. DATE FORMAT CONVERSION (DD/MM/YYYY -> ISO YYYY-MM-DD). In the
        "Status-page blurb (public)" paragraph, convert all three dates
        from DD/MM/YYYY to ISO YYYY-MM-DD format. The dates are
        03/11/2026, 17/11/2026, 24/11/2026. Touch ONLY those three date
        strings; leave every other word in the paragraph unchanged.

    R4. FORBIDDEN-WORD REMOVAL. In the "Status-page blurb (public)"
        paragraph, remove every occurrence of the words `clearly`,
        `unsurprisingly`, and `genuinely` (case-sensitive). Remove only
        the word itself and the single adjacent space; keep the sentence
        grammatical with single spacing.

    R5. SORT-ORDER REORDER (regional rollout). The "Regional rollout
        (planned order)" bullet list is in the wrong phase order.
        Reorder the bullets so they read Phase 1, Phase 2, Phase 3,
        Phase 4, Phase 5 (top to bottom). Do NOT change any bullet's
        text content - only the order.

    R6. UNIT NORMALIZATION (millions -> billions in status blurb).
        The "Status-page blurb (public)" paragraph currently asserts
        Veldt processed "billions of requests" without a number. SET the
        sentence to read "processed N.NN billion requests" where N.NN is
        the grand total from R2 divided by 1000, rounded to two decimal
        places. Replace the word `billions` with the computed `N.NN
        billion`. Touch ONLY that phrase.

    R7. JSON FIELD RENAME. In the fenced JSON rate-card block, rename
        the key `legacy_invoice_format` to `legacy_invoice_enabled`.
        Leave its value (`true`) unchanged. Do NOT rename any other key.

    R8. CODENAME / SCOPE BOUNDARY FIX. In the "Status-page blurb
        (public)" paragraph, change the phrase `the upcoming Q4-26
        maintenance window` to `the scheduled Q4-26 maintenance window`.
        Touch ONLY that phrase; leave the rest of the paragraph
        unchanged.

    R9. REGEX EXTRACT (emails). In the "Contact-extraction worksheet"
        section, the prose blockquote notes contain eight customer-success
        contact emails. Extract every email address (any token matching a
        standard email pattern with a `.example` top-level domain) into
        the bullet list under "Extracted contact emails (one per line,
        alphabetical order):". Replace the placeholder bullet `- (to be
        populated)` with one bullet per email, in ALPHABETICAL order by
        the full email string. Do NOT modify the prose notes themselves;
        only populate the bullet list below them.

    R10. CHECKSUM / TALLY. The "Checksum-tally line" line at the foot of
         the document currently reads `Service tally: 0`. SET it to the
         exact count of distinct service_id values in the service-tier
         roster (R1's table). The count is the number of unique rows of
         the roster after R1's header rename.

    R11. DEDUPLICATION. In the "Deduplication queue" section, the "Raw
         incident IDs" bullet list contains duplicates. Produce the
         de-duplicated list under "De-duplicated incident IDs:",
         replacing the placeholder bullet `- (to be populated)` with one
         bullet per unique incident ID in first-occurrence order. Do NOT
         modify the raw-list bullets above; only populate the
         de-duplicated bullet list below them.

    R12. CONDITIONAL FLAG-FLIP. In the "Feature-flag matrix" table, for
         EVERY service whose service-tier roster row (post R1) is `gold`,
         set the `audit_logging_strict` cell to `on`. For every service
         whose row is NOT `gold`, the cell stays `off`. Apply the flip
         row-by-row based on each service's tier in the roster above.

  Output the COMPLETE updated file content, from its first line to its
  last line, as a single fenced code block, with all twelve requirements
  applied and nothing else altered. After the code block, append the
  required output envelope (schemaVersion, tier, status, tool_budget_used)
  as separate lines OUTSIDE the code block. No em dashes (spaced hyphens).
  No emojis. Do not add commentary inside the file content.
variant_pool: 15
corpus: corpus/heterogeneous-precision-12/
corpus_intent: |
  ONE realistic fictional artifact (corpus/heterogeneous-precision-12/veldt-platform-audit.md):
  the Q3-26 quarterly audit pack for the fictional Veldt platform. The
  artifact organically hosts twelve unrelated precise edit surfaces - a
  service-tier roster markdown table, a public status-page prose blurb, a
  fenced JSON rate-card block, a regional-rollout bullet list, a
  contact-extraction worksheet with prose notes and a populate-this bullet
  list, a deduplication queue with a populate-this bullet list, a
  feature-flag matrix table, and a checksum-tally line - so the bundling
  feels like one audit-lead's pre-lock pass rather than a list of
  disconnected chores.

  THE HETEROGENEOUS-PRECISION CORE PROBE (12 simultaneous unrelated ops).
  This is THE core probe of the 101-105 battery. The gameplan flagged 12
  as "calibrated so 12 exceeds a weak model's reliable working set: at 12
  ops Sonnet/Haiku should drop ~1 on some runs while Opus holds all 12
  (if the hypothesis is true). If even 12 is a ceiling tie, that is itself
  a strong falsification signal." The 12 ops are exactly the eight from
  eval 101 (R1-R8 mapped to R1-R8 here) plus the four gameplan adds: a
  regex-extract (R9), a checksum/tally (R10), a deduplication (R11), and
  a conditional flag-flip (R12). Each individual op stays trivial per the
  eval-48 lesson; hardness comes ONLY from the count of 12 and the
  cross-section interaction (R10 and R12 depend on the post-R1 state of
  the roster table; R6 depends on R2; R11 requires preserving
  first-occurrence order).

  QUALITY PRINCIPLE (correctness-first, drop-tracking). An apply that
  silently mutated an out-of-scope line is WORSE than one that honestly
  applied eleven of twelve and flagged the twelfth. The eval is scored
  binary-per-requirement: all twelve correct = pass, any miss = fail, and
  the scoring Architect records WHICH requirement each failing run missed
  so the drop distribution can be inspected.

  ANSWER KEY (for the scoring Architect - the exact end-state after
  applying R1-R12). Verify by line-by-line comparison against the original
  corpus file plus the grep invariants below.

    R1 (field rename): the roster table header reads
       `| service_id    | service_tier | monthly_requests_millions | sla_target_band |`.
       The string `tier_label` appears 0 times; `service_tier` appears
       exactly once (in that header).

    R2 (arithmetic grand total): the line reads exactly `Grand total
       monthly requests (millions): 826`. The eight values are
       142 + 87 + 203 + 34 + 96 + 178 + 22 + 64 = 826. NO other digit
       on that line.

    R3 (date conversion): the status-page paragraph contains the three
       dates `2026-11-03`, `2026-11-17`, `2026-11-24` (in prose order).
       The strings `03/11/2026`, `17/11/2026`, `24/11/2026` appear 0
       times anywhere in the output. Note the JSON `"effective_date":
       "01/10/2026"` is OUTSIDE the prose paragraph and must remain
       `"01/10/2026"` (scope-discipline check).

    R4 (forbidden-word removal): the words `clearly`,
       `unsurprisingly`, `genuinely` appear 0 times in the output. The
       status-page paragraph reads grammatically with single spacing.

    R5 (sort-order reorder): the regional rollout list reads in order
       Phase 1 us-east-1, Phase 2 us-west-2, Phase 3 ap-southeast-2,
       Phase 4 ap-northeast-1, Phase 5 eu-central-1 (top to bottom).
       Each bullet's text content unchanged; only positions reordered.
       The list still has exactly 5 bullets.

    R6 (unit normalization): the status-page paragraph contains the
       phrase `processed 0.83 billion requests` (826 millions / 1000 =
       0.826, rounded to two decimals = 0.83). The word `billions` (in
       the context "billions of requests") appears 0 times; the phrase
       `0.83 billion requests` appears exactly once. Note: R6 depends on
       R2 having computed 826 first.

    R7 (JSON field rename): the JSON block contains
       `"legacy_invoice_enabled": true`. The string
       `legacy_invoice_format` appears 0 times. Value `true` unchanged.

    R8 (scope-boundary phrase fix): the status-page paragraph contains
       the phrase `the scheduled Q4-26 maintenance window`. The phrase
       `the upcoming Q4-26 maintenance window` appears 0 times.

    R9 (regex extract emails, alphabetical): the "Extracted contact
       emails" bullet list contains exactly these 8 bullets in
       alphabetical order:
         - a.petrov@meridian-clients.example
         - b.osei@hollowmere-co.example
         - c.lindqvist@veldt-customer.example
         - d.ramos@meridian-clients.example
         - e.feldman@hollowmere-co.example
         - f.takagi@veldt-customer.example
         - g.adebayo@meridian-clients.example
         - h.silvestri@hollowmere-co.example
       The placeholder bullet `- (to be populated)` is GONE from the
       extracted-emails list. The prose blockquote notes above are
       BYTE-IDENTICAL (the emails STILL appear in the prose; only the
       list below is populated).

    R10 (checksum tally): the foot line reads exactly `Service tally:
        8` (the 8 unique service_id values in the roster). The line
        `Service tally: 0` appears 0 times.

    R11 (deduplication preserving first-occurrence order): the
        "De-duplicated incident IDs" list contains exactly these 6
        bullets in first-occurrence order:
          - INC-4421
          - INC-4422
          - INC-4435
          - INC-4470
          - INC-4488
          - INC-4501
        The placeholder `- (to be populated)` is GONE from the
        de-duplicated list. The raw-list bullets above are
        BYTE-IDENTICAL (the duplicates STILL appear in the raw list).

    R12 (conditional flag-flip per tier): the feature-flag matrix
        contains `on` for atlas-api, carbon-store, flux-stream (the
        gold-tier services). It contains `off` for brio-events,
        dune-relay, ember-search, grove-mailer, harvest-jobs (the
        non-gold services). The cell count of `on` in that table is
        exactly 3; the cell count of `off` is exactly 5.

    EVERYTHING ELSE in the file (other headings, blank lines, prose intro
    paragraphs, code-fence markers, column alignment of pre-existing
    rows, JSON keys not renamed by R7, the JSON `effective_date` per
    R3's scope-discipline check, the raw incident list and the prose
    notes per R11/R9's scope discipline) is BYTE-IDENTICAL to the
    original. No row reordered (except the regional list per R5), no
    column re-aligned, no extra JSON key renamed, no heading changed.

  GREP-VERIFIABLE INVARIANTS (for the Architect, one per requirement):
    - R1: `tier_label` appears 0 times; `service_tier` appears 1 time.
    - R2: `Grand total monthly requests (millions): 826` appears 1 time;
      `Grand total monthly requests (millions): 0` appears 0 times.
    - R3: `03/11/2026`, `17/11/2026`, `24/11/2026` appear 0 times in
      the prose paragraph; `2026-11-03`, `2026-11-17`, `2026-11-24`
      each appear at least once. The JSON `"effective_date":
      "01/10/2026"` STILL appears.
    - R4: words `clearly`, `unsurprisingly`, `genuinely` appear 0 times.
    - R5: regional list bullets in file order start with `Phase 1`,
      `Phase 2`, `Phase 3`, `Phase 4`, `Phase 5`.
    - R6: `0.83 billion requests` appears 1 time; `billions of requests`
      appears 0 times.
    - R7: `legacy_invoice_format` appears 0 times;
      `"legacy_invoice_enabled": true` appears 1 time.
    - R8: `the scheduled Q4-26 maintenance window` appears 1 time;
      `the upcoming Q4-26 maintenance window` appears 0 times.
    - R9: the extracted-emails bullet list has exactly 8 email bullets
      in strict alphabetical order; `- (to be populated)` appears once
      total in the file (the dedup placeholder, until R11 removes it -
      0 times after R11).
    - R10: `Service tally: 8` appears 1 time; `Service tally: 0`
      appears 0 times.
    - R11: the de-duplicated bullet list has exactly 6 bullets in the
      order INC-4421, INC-4422, INC-4435, INC-4470, INC-4488, INC-4501.
      The raw-list above still contains 12 bullets (unchanged).
    - R12: the feature-flag matrix has exactly 3 `on` cells (rows
      atlas-api, carbon-store, flux-stream) and 5 `off` cells.

  DROP-DISTRIBUTION TRACKING (mandatory): for each failing run, the
  scoring Architect records the exact set of R-tags missed (e.g. "run 2
  missed {R6, R12}"). Aggregate per family: same requirement missed by
  multiple runs (hard-requirement signal) vs random drops across R1-R12
  (working-set-capacity signal).

  Scoring guidance:
    - All-requirements-correct (binary, primary): all 12 of R1-R12
      satisfied AND nothing else changed = pass.
    - Mean requirements-satisfied (secondary): mean of (number of
      R1-R12 satisfied) across the 5 runs per family.
    - Drop distribution (secondary): per-requirement miss count.
    - Correctness (hard-fail eligible) = all 12 applied AND nothing
      else changed.
    - Hallucination (hard-fail eligible) = inventing an edit,
      mis-counting the dedup list, fabricating an email, dropping a
      requirement without flagging.
    - Format adherence = one fenced code block, envelope outside,
      same code-fence and table syntax as original.
    - Discipline = applied ONLY the 12 named edits.
    - Reasoning quality = SKIP-eligible.
    - Source transparency applies weakly.
    Voice match does NOT apply.
notes: |
  Difficulty self-check (mint-N rule, eval-45-to-48 lesson): would Haiku
  reliably hold all 12 of R1-R12 across 5 runs with zero drops? Honest
  prediction: NO. 12 simultaneous unrelated precise ops, with three
  interdependencies (R6 depends on R2; R10 and R12 depend on R1's
  post-rename roster state; R11 must preserve first-occurrence ordering
  for an ID list that includes near-collisions like INC-4421 / INC-4422),
  should bite a weaker working set. Sonnet might hold most, dropping
  R6's two-step arithmetic (computing 0.83 from R2's 826) or R12's
  per-row conditional flip. Haiku predicted to drop one of R9 (regex
  extract + sort), R11 (dedup with order-preservation), or R12
  (conditional flag-flip across rows). This is the gameplan's "core
  probe" - if even 12 ops produces a ceiling tie across all three
  families, the Opus heterogeneity hypothesis is severely weakened.

  If after the dry-run inspection the prediction is "Haiku reliably
  holds all 12," the gameplan instruction is to push to 14 before
  shipping. Author judgment after construction: 12 ops with three real
  dependencies feels harder than 12 independent ops; staying at 12 with
  the dependencies is the right read. If the run comes back clean, the
  next escalation is more dependencies, not more raw ops.

  Heterogeneity check: the 12 ops span 12 distinct cognitive operations
  (schema rename, arithmetic sum, format conversion, removal, reorder,
  unit conversion with derived computation, JSON schema rename, prose
  surgical replacement, regex extraction + sort, count tally,
  deduplication preserving order, conditional per-row flip). They span
  6 syntax surfaces (markdown table, prose paragraph, JSON block,
  bullet list, prose-with-populated-list, populated-list).

  Second eval in 101-105 battery, the gameplan's headline core probe.
  Pool 15 (3 models x N=5). Codename hygiene: Veldt platform and all
  service names (atlas-api, brio-events, etc.) are neutral fictional;
  meridian-clients.example, hollowmere-co.example, veldt-customer.example
  are fictional .example TLD domains per RFC 2606. Standard four-phase
  /eval-pit flow against the frozen rubric/rubric.md.
---

# Spec 102 - heterogeneous-precision-12 (the heterogeneous-precision core probe)

Given a single realistic artifact - the Veldt platform Q3-26 quarterly
audit pack - apply TWELVE independent precise change requirements in a
single pass: a field rename, an arithmetic grand total, a date-format
conversion, a forbidden-word removal, a sort reorder, a unit
normalization that DEPENDS on the arithmetic total, a JSON field rename,
a prose phrase fix, a regex extract + alphabetical sort of 8 email
addresses, a count tally, a deduplication preserving first-occurrence
order, and a per-row conditional flag-flip that DEPENDS on the post-
rename roster state.

This is the core probe of the 101-105 heterogeneous-precision battery,
positioned by the gameplan as "calibrated so 12 exceeds a weak model's
reliable working set." Eight ops repeat the 101 floor pattern (so the
floor-vs-core delta is the new 4 ops, R9-R12: regex extract,
checksum/tally, deduplication, conditional flip) plus three deliberate
cross-requirement dependencies (R6 -> R2, R10 -> R1, R12 -> R1). Each
individual op stays trivial per the eval-48 lesson; the only knobs
turned are the count (8 -> 12) and the wiring.

The artifact is ONE fictional quarterly audit document with eight
distinct edit surfaces (roster table, status-page prose, JSON rate
card, regional rollout list, contact-extraction prose + populate-this
list, deduplication raw + populate-this list, feature-flag matrix
table, checksum-tally foot line). The corpus_intent enumerates all 12
requirements as independent grep-verifiable invariants R1-R12 with the
exact post-state for each, plus the drop-distribution tracking spec.

Standard four-phase `/eval-pit` flow against the frozen
`rubric/rubric.md`. Correctness and Hallucination are hard-fail eligible;
Discipline is the load-bearing discriminator. Primary metric is the
all-requirements-correct rate per family across the 5 runs. Secondary
metrics are mean requirements-satisfied and the drop-distribution per
requirement. Voice match does not apply. The variant pool is 15 (3
models x N=5, effort inert per the methodology). The corpus is the
directory `corpus/heterogeneous-precision-12/`.
