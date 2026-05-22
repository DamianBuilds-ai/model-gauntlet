---
task_category: heavy-data-transformation
prompt_under_test: |
  You are given a large flat expense ledger at
  corpus/heavy-data-transformation/transactions.csv (one header row plus 310 data
  rows) and a documented target shape at
  corpus/heavy-data-transformation/target-shape.md.

  Transform the CSV into ONE nested JSON document exactly matching the shape and rules
  in target-shape.md. In summary:
    1. Roll valid rows up by entity -> department -> project_code. For each project
       emit total_usd (sum of amount_usd for APPROVED rows only, FX-converted to USD
       and rounded half-up to 2dp), plus approved_count, pending_count, rejected_count
       over the valid rows in that project.
    2. Convert every amount to USD using the fixed FX table in target-shape.md
       (USD 1.00, EUR 1.08, GBP 1.27, AUD 0.66). Round half-up to 2 decimal places.
    3. Quarantine every malformed row into a quarantine array of
       {txn_id, reason}, using the eight reason codes and the FIRST-match priority
       order documented in target-shape.md. Never silently drop a malformed row and
       never let it contribute to a total or a count.
    4. Sort entities, departments, projects, and the quarantine list exactly as
       target-shape.md specifies. Emit only non-empty branches.
    5. Include the _meta block (total_rows_in_csv, valid_rows, quarantined_rows);
       valid_rows + quarantined_rows must equal total_rows_in_csv.

  Output ONLY the single JSON object (a fenced json block is fine; no prose inside the
  JSON). After the JSON, append the required output envelope (schemaVersion, tier,
  status, tool_budget_used) as separate lines OUTSIDE the JSON. No em dashes (spaced
  hyphens). No emojis.
variant_pool: 9
corpus: corpus/heavy-data-transformation/
corpus_intent: one large CSV ledger of 310 expense rows (300 valid, 10 malformed across 8 distinct malformed types) plus a target-shape.md documenting the nested entity->department->project rollup, the FX table, and the malformed-row rules
corpus_delivered: TBD
corpus_match: TBD
notes: |
  HEAVY DATA-TRANSFORMATION (exact-transform-at-scale). The corpus is large on purpose:
  310 data rows the model must read in full, FX-convert, roll up into a 3-level nested
  shape, AND triage 10 interleaved malformed rows into the right quarantine bucket
  without dropping or mis-summing any. The discriminator is exactness under volume - a
  model that skims, mis-rounds one currency, mis-prioritises an overlapping malformed
  condition, or quietly drops a bad row produces a confidently-wrong document a
  downstream finance system would trust. Volume + nesting + the malformed triage are
  what push context and stress consistency.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a transform that silently
  drops a malformed row, or sums a row it should have quarantined, or rounds EUR/GBP/AUD
  the wrong way, has produced wrong financial totals that look authoritative. That is
  WORSE than an honest "I could not classify TXxxxx" note. Reward exact totals + exact
  quarantine classification. Penalise the plausible-but-wrong number hardest (a total
  that is off by one row's amount, a count off by one, a malformed row summed into a
  project). Correctness and Hallucination are hard-fail eligible: inventing a row,
  inventing a project node with no valid rows, or fabricating a total are
  hallucinations.

  ANSWER KEY (computed deterministically by the corpus generator at
  corpus/heavy-data-transformation/.provenance/generate.py; reproduced here verbatim
  for the scoring Architect). 310 data rows -> 300 valid, 10 quarantined. Every entity
  below received valid rows in exactly the department/project combos shown (the row
  distribution is deterministic, so not every entity touches every department). The
  exact expected JSON:

    entities (sorted by entity name):

      Acme:
        engineering / ENG-DATA: total_usd 40978.80, approved 18, pending 3, rejected 4
        operations  / OPS-WARE: total_usd 50782.89, approved 18, pending 4, rejected 3
      Cardinal:
        marketing / MKT-PERF: total_usd 40284.31, approved 17, pending 4, rejected 4
        research  / RES-LABS: total_usd 25134.56, approved 18, pending 4, rejected 3
      Globex:
        marketing / MKT-PERF: total_usd 44388.45, approved 18, pending 3, rejected 4
        research  / RES-LABS: total_usd 27487.12, approved 18, pending 4, rejected 3
      Initech:
        marketing / MKT-PERF: total_usd 43054.10, approved 18, pending 4, rejected 3
        research  / RES-LABS: total_usd 25950.00, approved 18, pending 3, rejected 4
      Northwind:
        engineering / ENG-API: total_usd 41768.76, approved 18, pending 4, rejected 3
        operations  / OPS-WARE: total_usd 54306.52, approved 18, pending 3, rejected 4
      Umbra:
        engineering / ENG-WEB: total_usd 38204.28, approved 18, pending 4, rejected 3
        operations  / OPS-WARE: total_usd 43683.63, approved 18, pending 3, rejected 4

    quarantine (10 entries, sorted by reason then txn_id):
      TX1001 - duplicate_txn_id            (second occurrence of TX1001; the first is valid)
      TX9007 - invalid_date                (date 2026-13-40)
      TX9006 - invalid_status              (status "APPROVED?")
      TX9005 - missing_entity              (entity empty)
      TX9002 - negative_amount             (amount -300.00)
      TX9004 - project_department_mismatch (ENG-API under marketing)
      TX9003 - unknown_currency            (JPY, not in FX table)
      TX9001 - unparseable_amount          ("$1,250.00")
      TX9009 - unparseable_amount          (empty amount)
      TX9010 - unparseable_amount          ("two hundred")

    _meta: total_rows_in_csv 310, valid_rows 300, quarantined_rows 10

  THE PLANTED PRECISION TRAPS (where a weaker model goes confidently wrong):
    - TX9001 "$1,250.00" - the comma + dollar sign make it unparseable per the rule.
      A model that "helpfully" strips them to 1250.00 and SUMS it has broken the rule
      and inflated Globex/engineering/ENG-API. It must be quarantined, not cleaned.
    - TX9002 -300.00 - a negative on an expense-only ledger. A model that sums it
      (reducing a total) or treats it as valid is wrong; it is negative_amount.
    - TX9003 JPY - no FX rate, so it cannot convert. A model that invents a JPY rate
      has hallucinated; correct is unknown_currency.
    - TX9004 ENG-API under marketing - the project does not belong to that department.
      A model that files it under engineering/ENG-API (ignoring the stated department)
      or under marketing as if valid is wrong; it is project_department_mismatch.
    - TX9005 empty entity - missing_entity. A model that buckets it under "" or drops
      it silently is wrong.
    - TX9006 "APPROVED?" - not a valid status. invalid_status. A model that
      normalises it to approved and sums it is confidently wrong.
    - TX9007 2026-13-40 - month 13, day 40. invalid_date.
    - TX1001 duplicate - the duplicate carries DIFFERENT field values, but rule 4
      (duplicate) beats every other rule, so the SECOND TX1001 is quarantined as
      duplicate_txn_id regardless of its other fields. A model that processes both
      TX1001 rows double-counts; a model that quarantines the duplicate under a
      different reason (e.g. by its currency) has mis-prioritised.
    - TX9009 empty amount and TX9010 "two hundred" - both unparseable_amount.

  Scoring guidance:
    - Correctness (hard-fail eligible, weight 3.0) = do the 12 project totals match to
      the cent AND do all 12 project count-triples match AND are all 10 quarantine
      entries present with the RIGHT reason code? The cent-exact totals and the
      first-match priority on the overlapping malformed rows (especially TX1001
      duplicate and the three unparseable_amount rows) are the load-bearing checks. A
      single summed-malformed-row or mis-rounded-currency total is a Correctness miss.
    - Completeness (weight 2.0) = all 12 project nodes present, all 10 quarantine
      entries present, _meta arithmetic (valid + quarantined = total) holds. Count
      DROPPED projects or DROPPED quarantine entries explicitly.
    - Hallucination (hard-fail eligible, weight 2.5) = inventing a project node that
      received no valid rows, inventing an FX rate for JPY, fabricating a total, or
      emitting an entity/department combo that never appears in the data.
    - Reasoning quality (weight 2.5) = did the model apply the FIRST-match priority
      correctly on overlapping conditions (the duplicate-beats-amount and the
      missing-entity-beats-date cases), and resist the "clean the dollar sign and sum
      it" temptation, rather than ad-hoc handling each odd row.
    - Format adherence (weight 1.5) = exact nested shape, required key set, sort order,
      non-empty-branches-only, _meta present, output envelope appended outside the JSON.
    - Discipline (decision/judgment, weight 1.25) = honoured "quarantine, never silently
      drop, never sum a malformed row". A model that drops the hard rows to make the
      output look clean is penalised.
    - Source transparency applies weakly (single CSV + the documented rules). Voice
      match does NOT apply.

  Suggested shorthand for the Architect: totals_correct = (project totals matching to
  the cent) / 12; counts_correct = (count-triples matching) / 12; quarantine_recall =
  (correct {txn_id,reason} entries) / 10. An exemplary 5 on Correctness has 12/12
  totals, 12/12 counts, 10/10 quarantine with right reasons, and the _meta arithmetic
  holds. The score falls on any summed-malformed row, any mis-rounded total, any
  mis-prioritised malformed reason, or any dropped/duplicated row.

  Run the full 9-variant model-only pool (Haiku x3, Sonnet x3, Opus x3; effort inert
  per the methodology). Aggregate the 3 passes per model (mean weighted total); flag any
  model whose 3 passes diverge by more than 0.5 as a consistency finding - exactness on
  a large transform is exactly where per-run variance and forgetting-under-load show up.
---

# Spec 34 - heavy-data-transformation (exact transform at scale)

A heavy transform eval. The corpus is a large flat expense ledger
(`corpus/heavy-data-transformation/transactions.csv`, 310 data rows) plus a documented
nested target shape (`corpus/heavy-data-transformation/target-shape.md`). The model must
read every row, FX-convert each amount to USD against a fixed rate table, roll the valid
rows up into a three-level nested document (entity -> department -> project) with a
cent-exact `total_usd` over approved rows and a status count-triple per project, and
triage 10 deliberately malformed rows - interleaved throughout the file, not clustered -
into a quarantine list with the correct reason code under a documented first-match
priority order.

The malformed rows are the precision traps: a dollar-and-comma amount that must NOT be
cleaned-and-summed, a negative on an expense-only ledger, an un-FX-able currency, a
project filed under the wrong department, a missing entity, a corrupt status, an
impossible date, a duplicate txn_id whose later occurrence must lose to the duplicate
rule regardless of its other (overlapping) defects, and two unparseable amounts. A model
that "helpfully" repairs and sums any of these produces a confidently-wrong financial
total a downstream system would trust, which is worse than an honest quarantine.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
answer key is computed deterministically (generator under the corpus `.provenance/`
folder) and reproduced verbatim in the spec notes, so Correctness scores objectively to
the cent: 12 project totals, 12 status count-triples, and 10 quarantine entries with the
right reason. Correctness and Hallucination are hard-fail eligible; Reasoning quality
(first-match priority + trap resistance) and Format adherence (exact nested shape + sort
order) are the load-bearing differentiators. Voice match does not apply. The variant
pool is 9 (3 models x N=3, effort inert per the methodology). The corpus is the
directory `corpus/heavy-data-transformation/`.
