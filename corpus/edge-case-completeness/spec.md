# Specification - allocate_cents(total_cents, weights)

## Purpose

`allocate_cents` splits an integer amount of money (in cents) across a list of
weighted buckets (cost centers) so that:

1. The returned amounts are all integers (cents - money is never fractional).
2. The returned amounts sum EXACTLY to `total_cents` (no money is created or
   lost).
3. Each bucket's share is proportional to its weight, with any indivisible
   remainder distributed by a deterministic largest-remainder rule.

## Signature

```python
def allocate_cents(total_cents: int, weights: list[int]) -> list[int]:
    ...
```

- `total_cents`: an integer number of cents to distribute. May be zero. May be
  negative (representing a credit / refund to split).
- `weights`: a list of non-negative integer weights, one per bucket. The returned
  list has the same length and order as `weights`.

## Return value

A list of integers, same length and order as `weights`, that sums exactly to
`total_cents`, where each bucket receives its proportional share with remainder
distributed per the rules below.

## Allocation rules (precise)

Let `n = len(weights)` and `W = sum(weights)`.

1. **Empty weights.** If `weights` is empty (`n == 0`):
   - If `total_cents == 0`, return `[]` (empty list - nothing to distribute,
     nothing distributed; the sum-equals-total invariant holds trivially).
   - If `total_cents != 0`, raise `ValueError` (there is no bucket to receive a
     non-zero amount, so the sum-equals-total invariant cannot be satisfied).

2. **Zero total weight with non-empty list.** If `n > 0` but `W == 0` (every
   weight is zero):
   - If `total_cents == 0`, return a list of `n` zeros.
   - If `total_cents != 0`, raise `ValueError` (no bucket has any weight, so there
     is no proportional basis to distribute a non-zero amount).

3. **Negative weight.** If any weight is negative, raise `ValueError`. Weights
   must be non-negative.

4. **Base proportional share.** Otherwise (`W > 0`), for each bucket `i` compute
   the exact (rational) share `total_cents * weights[i] / W`, and take its FLOOR
   TOWARD NEGATIVE INFINITY to get the integer base share `base[i]`. (Floor toward
   negative infinity is mandated so the rule is well-defined for negative
   `total_cents`; this is Python's `//` on the product, i.e.
   `base[i] = (total_cents * weights[i]) // W`.)

5. **Remainder.** Let `R = total_cents - sum(base)`. Because each `base[i]` was
   floored toward negative infinity, `R` is an integer with `0 <= R < n_pos`,
   where `n_pos` is the number of buckets with a positive weight. `R` is the
   number of leftover cents (cents that the flooring did not assign) that must be
   handed out, one cent each, to `R` buckets.

6. **Largest-remainder distribution.** Distribute the `R` leftover cents one at a
   time to the buckets with the largest fractional remainders. The fractional
   remainder of bucket `i` is `frac[i] = total_cents * weights[i] - base[i] * W`
   (an integer numerator over the common denominator `W`; larger numerator =
   larger fractional part). Hand out one extra cent to each of the `R` buckets
   with the largest `frac[i]`.
   - **Tiebreak.** If two buckets have equal `frac[i]`, the bucket with the LOWER
     INDEX receives the extra cent first. (Deterministic, stable, index-ascending.)
   - A bucket with weight 0 has `frac[i] == 0` and base 0; it can only receive a
     leftover cent if `R` exceeds the count of positive-remainder buckets, which
     never happens because `R < n_pos` and every leftover cent goes to a
     positive-weight bucket first. In practice a zero-weight bucket always
     receives exactly 0.

7. **Result.** The result is `base[i]` plus one for each leftover cent that bucket
   received. It sums exactly to `total_cents` by construction.

## Invariants (must always hold for any input that does not raise)

- `len(result) == len(weights)`.
- `sum(result) == total_cents` EXACTLY.
- Every `result[i]` is an integer.
- A bucket with weight 0 receives exactly 0.
- The function is deterministic: the same inputs always produce the same output
  (the tiebreak makes remainder distribution order-independent of anything but
  index).

## Worked examples

- `allocate_cents(100, [1, 1, 1])` -> `[34, 33, 33]`. Base = [33, 33, 33], R = 1,
  remainders equal so the lowest index (bucket 0) gets the extra cent.
- `allocate_cents(100, [1, 1])` -> `[50, 50]`. Divides evenly, R = 0.
- `allocate_cents(10, [1, 1, 1])` -> `[4, 3, 3]`. Base = [3, 3, 3], R = 1, bucket
  0 gets it.
- `allocate_cents(5, [3, 1])` -> `[4, 1]`. Exact shares 3.75 and 1.25; base =
  [3, 1], R = 1; bucket 0 has the larger remainder (0.75 vs 0.25) and gets it.
- `allocate_cents(0, [5, 5])` -> `[0, 0]`.
- `allocate_cents(-100, [1, 1, 1])` -> `[-33, -33, -34]`. Base via floor toward
  negative infinity = [-34, -34, -34]? No: -100*1//3 = -34 (since -100//3 = -34),
  base = [-34, -34, -34], sum = -102, R = -100 - (-102) = 2, so TWO leftover cents
  go to the two largest-remainder buckets (indices 0 and 1), giving
  [-33, -33, -34]. (This is the subtle negative case - leftover cents are added,
  moving values toward zero, and there can be more than one of them.)
- `allocate_cents(100, [2, 0, 1])` -> `[67, 0, 33]`. Base = [66, 0, 33], R = 1,
  the zero-weight bucket has remainder 0; bucket 0 has the largest remainder and
  gets the extra cent. The zero-weight bucket stays at 0.
