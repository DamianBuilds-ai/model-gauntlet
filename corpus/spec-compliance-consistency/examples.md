# ledgerfmt - input/output examples

These examples are illustrative. They do NOT exhaust the spec - the spec in
SPEC.md is the contract. Implement to the spec, not merely to these examples. The
output blocks are given whole; diff them carefully against the inputs.

---

## Example A - mixed valid, comment, error, and a zero-rounding line

### Input

```
# Q1 ledger - partial
2026-01-05 | Whole Foods Market | groceries | -84.20
2026-01-03 | Landlord Pty Ltd | rent | -1850
2026-01-05 | acme payroll | income | 4200.00

2026-01-04 | Rounding Test Vendor | other | -0.004
2026-01-06 | Corner Store | snacks | -12.5
2026-01-02 | BadDate Co | utilities | not-a-date | -30
2026-13-40 | Impossible Date | other | -5.00
```

### Output

```
DATE        PAYEE                 CATEGORY    AMOUNT        BALANCE
2026-01-03  Landlord Pty Ltd      RENT            -1,850.00       -1,850.00
2026-01-05  acme payroll          INCOME           4,200.00        2,350.00
2026-01-05  Whole Foods Market    GROCERIES          -84.20        2,265.80
2026-01-06  Corner Store          OTHER              -12.50        2,253.30
ERRORS:
line 6: bad field count
line 7: bad date
```

### What this example demonstrates (read carefully)

- The comment line and the blank line are skipped and do NOT advance the counter.
- The transaction lines, in input order, are counter values 1 through 7:
  1 = Whole Foods, 2 = Landlord, 3 = acme payroll, 4 = Rounding Test Vendor,
  5 = Corner Store, 6 = BadDate Co (5 fields -> bad field count),
  7 = Impossible Date (13th month -> bad date).
- The line `2026-01-04 | Rounding Test Vendor | other | -0.004` is counter value
  4. Its amount rounds to 0.00 (banker's rounding of -0.004 to 2 dp is 0.00). It
  is therefore SUPPRESSED: it produces NO row and does NOT touch the balance - yet
  it still consumed counter value 4, which is why the two error lines below report
  `line 6` and `line 7` (not `line 5` and `line 6`). If you leave the Rounding
  Test Vendor row in the output, your output is WRONG, and your error line numbers
  will also be wrong.
- Sorting: rows are by date ascending, then payee case-insensitive. The two
  2026-01-05 rows tie on date; `acme payroll` sorts before `Whole Foods Market`
  case-insensitively.
- `snacks` is not an allowed category, so it maps to `OTHER`.
- The balance is cumulative in sorted order: -1850.00, then +4200.00 = 2350.00,
  then -84.20 = 2265.80, then -12.50 = 2253.30.

---

## Example B - all lines invalid or suppressed

### Input

```
# nothing valid here
2026-02-01 | Zero Vendor | other | 0.00
bad | line | with | too | many | fields
2026-02-02 | | utilities | -10.00
```

### Output

```
DATE        PAYEE                 CATEGORY    AMOUNT        BALANCE
ERRORS:
line 2: bad field count
line 3: empty payee
```

### What this example demonstrates

- Counter value 1 is the Zero Vendor line; its amount is exactly 0.00, so it is
  SUPPRESSED (no row, no balance) but it consumes counter value 1.
- Counter value 2 is the 6-field line -> bad field count.
- Counter value 3 is the empty-payee line -> empty payee.
- There are zero surviving rows, so per Section 13 the output is the header line
  only, followed by the ERRORS block. The output is NEVER empty.

---

## Example C - banker's rounding spot checks

These are not full runs, just the rounding rule (Section 6) in isolation:

- `2.005` -> `2.00` (round-half-to-even; the digit kept, 0, is even)
- `2.015` -> `2.02` (round-half-to-even; rounds up to the even 2)
- `2.025` -> `2.02` (round-half-to-even; the digit kept, 2, is even)
- `-0.004` -> `0.00` (rounds toward zero here; triggers suppression)
- `-0.005` -> `0.00` (round-half-to-even of -0.005 to 2 dp is -0.00 == 0.00; also
  suppressed)
- `1234.5` -> `1,234.50` (thousands separator + two decimals, Section 11)
