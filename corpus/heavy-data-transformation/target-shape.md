# Target shape - expense ledger rollup (heavy-data-transformation)

You are transforming the flat ledger `transactions.csv` (310 data rows) into a single
nested JSON document that rolls expenses up by entity, then department, then project,
and quarantines every malformed row with a precise reason. All entities, departments,
projects, people, and figures are fictional.

This file documents the EXACT target shape, the field rules, the FX table, and the
malformed-row rules. Follow them precisely - the transform is scored against a computed
answer key, so an off-by-one count, a wrong rounding, or a mis-categorised malformed
row is a Correctness error.

---

## 1. The input columns (transactions.csv)

`txn_id, entity, department, project_code, category, currency, amount, status, date`

- One header row, then 310 data rows.
- Rows appear in arbitrary order. Malformed rows are interleaved throughout, not
  clustered at the end.

## 2. The output (one JSON object, this exact shape)

```json
{
  "entities": [
    {
      "entity": "<entity name>",
      "departments": [
        {
          "department": "<department>",
          "projects": [
            {
              "project_code": "<project code>",
              "total_usd": <number, 2 decimal places>,
              "approved_count": <integer>,
              "pending_count": <integer>,
              "rejected_count": <integer>
            }
          ]
        }
      ]
    }
  ],
  "quarantine": [
    { "txn_id": "<id>", "reason": "<one of the reason codes>" }
  ],
  "_meta": {
    "total_rows_in_csv": <integer>,
    "valid_rows": <integer>,
    "quarantined_rows": <integer>
  }
}
```

Ordering for determinism:
- `entities` sorted by entity name (ascending, case-sensitive A-Z).
- `departments` within an entity sorted by department name ascending.
- `projects` within a department sorted by project_code ascending.
- `quarantine` sorted by reason ascending, then txn_id ascending.
- Only include an entity / department / project node if at least one VALID row landed
  in it. Do not emit empty branches.

## 3. The FX table (settle every amount to USD)

| currency | rate to USD |
|----------|-------------|
| USD | 1.00 |
| EUR | 1.08 |
| GBP | 1.27 |
| AUD | 0.66 |

`amount_usd = round(amount * rate, 2)` using round-half-up at 2 decimal places. Any
currency NOT in this table makes the row malformed (reason `unknown_currency`).

## 4. What counts toward totals and counts

- `total_usd` sums `amount_usd` for VALID rows whose `status` is exactly `approved`.
  Pending and rejected rows do NOT contribute to `total_usd`.
- `approved_count`, `pending_count`, `rejected_count` count VALID rows in that project
  by status. Malformed rows are NOT counted in any of these - they go only to
  `quarantine`.

## 5. Malformed-row rules (quarantine, never silently drop, never sum)

A row is malformed if ANY of the conditions below hold. When more than one applies,
use the FIRST match in this priority order and emit exactly one quarantine entry for
that row:

1. `missing_entity` - the `entity` field is empty / whitespace only.
2. `invalid_status` - `status` is not exactly one of `approved`, `pending`, `rejected`
   (case-sensitive, lowercase).
3. `invalid_date` - `date` is not `YYYY-MM-DD` with month 01-12 and day 01-31.
4. `duplicate_txn_id` - a `txn_id` that appears more than once in the file. The FIRST
   occurrence is processed normally (if otherwise valid); every LATER occurrence with
   the same id is quarantined as `duplicate_txn_id` regardless of its other fields.
5. `unparseable_amount` - `amount` is empty, contains any character other than digits,
   a single optional leading minus, and at most one decimal point (so `$1,250.00`,
   `two hundred`, and `` are all unparseable), or otherwise cannot be parsed as a
   number.
6. `negative_amount` - `amount` parses to a number less than 0 (this is an
   expense-only ledger; refunds do not belong here).
7. `unknown_currency` - `currency` is not in the FX table above.
8. `project_department_mismatch` - the `project_code` does not belong to the stated
   `department` per the project map below.

Priority note: the order above is the tie-break order. For example a row that is both a
later duplicate AND has a bad amount is quarantined as `duplicate_txn_id` (rule 4 beats
rule 5). A row missing its entity AND with a bad date is `missing_entity` (rule 1 beats
rule 3).

## 6. The project -> department map (for rule 8)

| department | valid project_codes |
|------------|---------------------|
| engineering | ENG-API, ENG-WEB, ENG-DATA |
| marketing | MKT-BRAND, MKT-PERF |
| operations | OPS-WARE, OPS-FLEET |
| research | RES-CORE, RES-LABS |

A row whose `project_code` is not in its `department`'s list is
`project_department_mismatch` (e.g. `ENG-API` under `marketing`).

## 7. Output discipline

- Emit ONE JSON object exactly matching the shape in section 2. A fenced ```json block
  is fine; no prose commentary inside the JSON.
- Numbers: `total_usd` is a JSON number with 2-decimal precision (e.g. `41768.76`,
  `25950.0` is acceptable for a whole-dollar-ending value). Counts are integers.
- Do NOT invent rows, do NOT merge rows, do NOT drop a malformed row silently - every
  one of the 310 data rows is either summed/counted in a project OR present in
  `quarantine`. `valid_rows + quarantined_rows` must equal `total_rows_in_csv`.
