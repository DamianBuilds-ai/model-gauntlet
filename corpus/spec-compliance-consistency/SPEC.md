# ledgerfmt - Specification

Version 3.0. This document specifies the behaviour of `ledgerfmt`, a small
command-line tool that reads a plain-text ledger and emits a normalised,
validated, re-formatted ledger. The single entry point is the function
`format_ledger(raw_text: str) -> str`. Implement it to satisfy every requirement
below. Each numbered section is binding. A constraint stated in a sentence of
prose is binding exactly as much as one stated in a bullet.

---

## Section 1 - Precedence and general principles

`ledgerfmt` is a normaliser, not a calculator. It transforms each input
transaction into a fixed-width output row, validates the fields, and appends a
running balance. Most rules in this spec ADD or TRANSFORM a row. Where any
row-level rule (formatting, balance contribution, sorting) interacts with the
zero-suppression rule defined later in Section 9, the zero-suppression rule takes
PRECEDENCE: a suppressed transaction is removed before any formatting, sorting, or
balance computation considers it. Apply suppression at the point of parsing and
rounding, before the sort pass and before the balance pass.

Validation errors never abort the run (see Section 12). The tool is total: it
always returns a string, even for empty or all-invalid input (see Section 13).

---

## Section 2 - Input shape

Input is a single string of newline-separated lines. Each non-empty,
non-comment line is one transaction.

- A blank line (empty or only whitespace) is skipped. It is NOT a transaction and
  does NOT advance the line counter described in Section 12.
- A line whose first non-whitespace character is `#` is a comment. It is skipped,
  is NOT a transaction, and does NOT advance the line counter.
- Every other line is a candidate transaction and is processed by Sections 3-6.

---

## Section 3 - Field split

A candidate transaction line is split on the pipe character `|` into fields.

- A valid line has EXACTLY four fields: `DATE | PAYEE | CATEGORY | AMOUNT`.
- A line that splits into any number of fields other than four is a parse error
  with reason `bad field count` (see Section 12). The line is skipped but still
  counts (Section 12).

---

## Section 4 - DATE and PAYEE

- DATE must be an ISO calendar date in the form `YYYY-MM-DD` (four-digit year,
  two-digit month, two-digit day, hyphen separators). A value that does not match
  this form is a validation error with reason `bad date`. Valid dates are passed
  through unchanged - DATE is NOT reformatted.
- PAYEE is trimmed of leading and trailing whitespace, and any internal run of
  whitespace is collapsed to a single space. If PAYEE is empty after trimming,
  that is a validation error with reason `empty payee`.

---

## Section 5 - CATEGORY

- CATEGORY is upper-cased.
- The allowed categories are: `GROCERIES`, `RENT`, `UTILITIES`, `INCOME`,
  `TRANSFER`, `OTHER`.
- A CATEGORY that, after upper-casing, is not in the allowed set is NOT rejected.
  It is mapped to `OTHER`. (This is a normalisation, not an error.)

---

## Section 6 - AMOUNT and rounding

- AMOUNT is parsed as a decimal number. A value that cannot be parsed as a number
  is a parse error with reason `bad amount`.
- A parsed amount is rounded to exactly two decimal places using BANKER'S ROUNDING
  (round-half-to-even). This is NOT round-half-up. For example, `2.005` rounds to
  `2.00` (the digit before the half is even, so it stays), and `2.015` rounds to
  `2.02`. Use round-half-to-even for every amount.
- A negative amount is permitted; it represents an expense. A positive amount
  represents income or a credit. The sign is preserved in the output.

---

## Section 7 - Sort order

Output rows are sorted:

1. By DATE ascending (lexicographic on the ISO string is correct because the form
   is fixed-width).
2. Then, for rows with the same DATE, by PAYEE ascending, compared
   case-insensitively, as the tiebreak.
3. The sort is stable within an equal (DATE, PAYEE) pair: rows that tie on both
   keep their relative input order.

---

## Section 8 - Row formatting

Each surviving transaction is formatted as a single output row with fixed-width
columns, joined by exactly two spaces between columns:

- DATE: width 10, the ISO date as-is (it is already 10 characters).
- PAYEE: left-justified in width 20. If the normalised payee is longer than 20
  characters, TRUNCATE it to 20 characters with no ellipsis.
- CATEGORY: left-justified in width 10.
- AMOUNT: right-justified in width 12, two decimal places, a leading minus sign
  for negatives (see Section 11 for the thousands separator).

Columns are separated by two spaces. There is no leading or trailing space on a row
beyond the column padding itself.

---

## Section 9 - Running balance

A RUNNING BALANCE column is appended to every output row. The running balance is
the cumulative sum of all amounts up to and including the current row, computed in
OUTPUT (sorted) order - NOT input order. The balance starts at `0.00` before the
first row, and each row's balance reflects that row's amount added to the prior
balance.

The balance column is appended after the AMOUNT column, separated by two spaces,
right-justified in width 14, two decimal places, using the same thousands separator
and sign conventions as the AMOUNT column (Section 11).

A subtle but important consequence of the running-balance design is worth stating
plainly so implementers do not get it wrong: because the balance is a cumulative
sum, a transaction whose amount rounds to exactly 0.00 after the rounding in
Section 6 is a no-op and MUST be omitted from the output entirely, since it would
otherwise produce a visually duplicate balance line that adds no information,
though it still advances the line counter used in Section 12. In other words a
zero-rounding transaction produces NO row and contributes NOTHING to the balance,
but it is still counted as a transaction line for the purpose of the Section 12
counter. Treat the suppression as happening at parse/round time per the precedence
rule in Section 1: round the amount, and if it is exactly 0.00, drop the
transaction from the row set before sorting and before the balance pass, while
still incrementing the counter.

The balance is therefore the sum only of the surviving (non-suppressed, valid)
rows, in sorted order.

---

## Section 10 - Header

The output begins with a single header line, exactly:

```
DATE        PAYEE                 CATEGORY    AMOUNT        BALANCE
```

The header is then followed immediately by the formatted rows (Section 8 and 9),
one per line. There is NO blank line between the header and the first row, and NO
trailing blank line at the end of the output.

---

## Section 11 - Number formatting

- Amounts in both the AMOUNT and BALANCE columns use a comma as a thousands
  separator for the integer part. For example `1234.5` is rendered `1,234.50`, and
  `1000000` is rendered `1,000,000.00`.
- The minus sign for a negative value sits OUTSIDE the digit grouping, immediately
  before the first digit group: `-1,234.50`, never `1,-234.50`.
- Every amount and every balance shows exactly two decimal places.

---

## Section 12 - Errors and the line counter

- The LINE COUNTER N is 1-based and counts TRANSACTION LINES only. Per Section 2,
  blank lines and comment lines do NOT advance N. Per Section 9, a zero-rounding
  suppressed transaction DOES advance N (it was a transaction line; it was merely
  suppressed from the output).
- A parse or validation error (Sections 3-6) does NOT abort the run. The offending
  line is skipped and recorded, and processing continues with the next line.
- After all output rows, if any errors occurred, emit a section beginning with the
  literal line `ERRORS:` on its own line, followed by one diagnostic line per bad
  transaction, in input order, each formatted EXACTLY as:

  ```
  line {N}: {reason}
  ```

  where `{N}` is the 1-based counter for that line and `{reason}` is one of the
  fixed strings: `bad field count`, `bad date`, `empty payee`, `bad amount`.
- If there were no errors, the `ERRORS:` section is omitted entirely - do NOT emit
  an empty `ERRORS:` header.

---

## Section 13 - Empty and degenerate input

- If after processing there are ZERO surviving output rows (because the input was
  all comments, all errors, all suppressed zero-amount transactions, or empty),
  the output is the header line from Section 10 ONLY, followed by the `ERRORS:`
  section if any errors occurred. The tool NEVER returns an empty string.

---

## Section 14 - Output assembly summary

The returned string is, in order:

1. The header line (Section 10).
2. Zero or more formatted rows (Sections 7-9, 11), sorted per Section 7.
3. If any errors occurred, the `ERRORS:` block (Section 12).

Lines are joined by a single newline character. There is no trailing newline.
