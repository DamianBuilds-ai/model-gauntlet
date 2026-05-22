# Corpus - edge-case-completeness (Cardinal billing allocate function)

This corpus specifies ONE function from a fictional billing platform called
"Cardinal". The function splits an integer amount of money (in cents) across a
list of weighted buckets (cost centers), distributing any indivisible remainder
deterministically.

Read both files:

- `spec.md` - the complete, authoritative behavioural specification of
  `allocate_cents(total_cents, weights)`. Every rule you need is here.
- `reference_impl.py` - a reference implementation that matches the spec. Use it to
  confirm exact behaviour on any case you are unsure about.

The spec is precise and self-contained. The task will ask you to enumerate the
edge cases this function must handle. The obvious cases are easy; the function has
several subtle, non-obvious edge cases that follow directly from the rounding and
remainder rules.
