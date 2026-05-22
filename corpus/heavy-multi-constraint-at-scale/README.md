# Corpus - heavy-multi-constraint-at-scale (the 24-simultaneous-constraints probe)

A large single hot-path module that must be refactored to satisfy 24 interacting
constraints at once. This is the heavy, scaled-up analog of the
`multi-constraint-satisfaction` probe (12 constraints): the field stops bunching
at the top when the constraint count and module size grow, because holding
twenty-four tensioned requirements in working memory while reading a long module
is where forgetting-under-load bites.

All content is synthetic. Fictional company: "Northwind Payments". No real
people are named.

## The task

The `settle_batch(merchant_id, transactions, batch_key)` method in
`settlement.py` is deficient: it uses float money, a single global lock, a
per-transaction fraud call, a per-transaction FX quote, swallowed exceptions, a
truncating round, fee on refunds, audit only on success, and an ignored
idempotency key. The refactor must satisfy ALL of C1 through C24 in
`constraints.md` simultaneously, without changing collaborator interfaces or the
public dataclass field names.

## Files

- `README.md` - this file.
- `settlement.py` - the DEFICIENT module to refactor (the engine + data types +
  config constants + the deficient `settle_batch`).
- `collaborators.py` - REFERENCE ONLY. The fixed collaborator Protocols
  (LedgerClient, FxClient, FraudClient, AuditLog, MetricsSink, ReserveStore,
  ClockSource) plus in-memory fakes the refactor must keep working against.
- `constraints.md` - the 24 constraints C1..C24 the refactor must satisfy.

## Why this discriminates

Twenty-four constraints with at least five genuine tensions: the ledger pair
must be atomic UNDER the per-merchant lock (C13) while fraud + FX must be OUTSIDE
it (C14); idempotent replay must NOT re-audit while every real outcome MUST be
audited (C21 vs C22); validation rejections must be audited+metric'd before any
network call (C1-C5 vs C21/C24); reserve must be held only on success (C20) yet
the success audit must follow the post (C21/C23); money must stay integer cents
through Decimal-rate multiplications with bankers' rounding (C6-C11). A model
under load tends to satisfy a visible subset (validation, the obvious float fix)
and silently drop the buried tensions (the once-per-currency FX memo, the
replay-no-double-audit rule, the metrics-on-the-reject-path rule). The scored
discriminator is the COUNT of constraints genuinely satisfied in the code -
verified by reading the code, not the model's self-report - with false
"satisfied" claims penalised hardest.

The exhaustive constraint key with the starting-state satisfied/violated status
is in the spec's `notes` field (the answer key).
