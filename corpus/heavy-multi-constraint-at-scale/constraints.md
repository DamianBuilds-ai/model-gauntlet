# Northwind Payments - settlement engine refactor constraints

The `settle_batch(merchant_id, transactions, batch_key)` method in
`settlement.py` must be refactored so that ALL TWENTY-FOUR constraints below
(C1 through C24) hold SIMULTANEOUSLY. Several of them tension or near-conflict.
You must hold all of them at once - do NOT satisfy some at the expense of
others, and do NOT claim a constraint is satisfied when your code does not
actually satisfy it.

Do not change the collaborator interfaces (LedgerClient, FxClient, FraudClient,
AuditLog, MetricsSink, ReserveStore, ClockSource). Do not change the public
field names of SettlementResult, LedgerEntry, Transaction, or the
SettlementError subtypes. Output the complete refactored module as a single
Python code block, then a checklist mapping each constraint C1..C24 to the
line(s) or construct that satisfies it.

---

## Input + structural validation

**C1 - EMPTY BATCH.** An empty `transactions` list does not post a ledger entry.
Return a `SettlementResult` with `status == "skipped_empty"`, all money fields 0,
`entry_id == ""`, `txn_count == 0`. (Do NOT raise; skipped-empty is a normal
no-op outcome, not an error.)

**C2 - OVERSIZED BATCH.** A batch with more than `MAX_BATCH_SIZE` (500)
transactions raises `EmptyBatchError`? No - raises `SettlementError` (the base
type) with a message naming the limit. It must NOT silently truncate to 500.

**C3 - DUPLICATE TXN IDS.** If two transactions in the batch share a `txn_id`,
raise `SettlementError` before any network call. Duplicate ids would double-count
gross; reject the batch rather than dedup silently.

**C4 - MIXED-MERCHANT GUARD.** Every transaction's `merchant_id` must equal the
`merchant_id` argument. A transaction belonging to a different merchant raises
`SettlementError` before any network call.

**C5 - SETTLEMENT CURRENCY SUPPORTED.** If `self.settlement_currency` is not in
`SUPPORTED_SETTLEMENT_CCY`, raise `CurrencyMismatchError` before any work.

## Money correctness (integer cents, bankers' rounding)

**C6 - INTEGER CENTS THROUGHOUT.** Gross, fee, reserve, and net are integer
minor units (`int`) at every step. No `float` may touch a money value. The only
Decimal use is multiplying by the FX rate and the reserve rate, and each such
multiplication is immediately quantised back to integer minor units. VIOLATED if
any money field is computed via `float(...)` or stored as a float.

**C7 - BANKERS' ROUNDING ON FX.** Each FX conversion result is rounded to
integer minor units using `ROUND_HALF_EVEN` (bankers' rounding), not truncation
and not `round()` builtin (which is bankers' on floats but you are forbidden
floats by C6). Use `Decimal.quantize(Decimal(1), rounding=ROUND_HALF_EVEN)`.

**C8 - FEE ONLY ON SALES.** The percentage + fixed fee (`FEE_BPS` bps +
`FEE_FIXED_MINOR` cents) applies once per `kind == "sale"` transaction. A
`kind == "refund"` transaction carries NO fee. VIOLATED if refunds accrue fee.

**C9 - REFUNDS REDUCE GROSS.** A refund subtracts its converted amount from
gross (signed). Sales add. So gross is the signed sum of converted sale amounts
minus converted refund amounts. VIOLATED if refunds are added to gross or ignored.

**C10 - FEE FROM CONVERTED AMOUNT.** The 2.90% portion of the fee is computed on
the FX-converted (settlement-currency) sale amount, not the original-currency
amount. VIOLATED if the bps fee is taken on `amount_minor` before conversion.

**C11 - RESERVE ON NET.** Reserve = `reserve_rate` of net (gross minus fee),
integer cents, bankers' rounded. Net-after-reserve = net minus reserve. The
`SettlementResult.net_minor` field is the net-after-reserve figure. VIOLATED if
reserve is taken on gross, or net_minor excludes the reserve deduction.

## Concurrency + atomicity

**C12 - PER-MERCHANT LOCK.** Concurrent settle_batch calls for DIFFERENT
merchants proceed in parallel. There is no single global lock serialising all
merchants. Use a per-merchant lock (e.g. a dict of locks guarded by a small
meta-lock). VIOLATED if one shared `threading.Lock` guards every merchant.

**C13 - ATOMIC BALANCE-CHECK-THEN-POST.** For a single merchant, the balance
read (`get_merchant_balance`) and the dependent `post_entry` are atomic with
respect to other settle_batch calls for the SAME merchant - no other settlement
for that merchant can post between this balance read and this post. VIOLATED if
the balance is read outside the per-merchant lock then posted inside (TOCTOU).

**C14 - NO NETWORK UNDER LOCK EXCEPT THE LEDGER PAIR.** The fraud screen and ALL
FX quotes happen BEFORE the per-merchant lock is acquired. Only the
balance-read + post_entry (+ a reversal on failure) run under the lock. VIOLATED
if `fraud.screen` or `fx.quote` is called while the lock is held. (This is the
C13-vs-C14 tension: the ledger pair must be atomic under the lock, but the other
network calls must NOT be under it.)

## Network-call efficiency

**C15 - SINGLE FRAUD SCREEN.** `fraud.screen` is called EXACTLY ONCE for the
whole batch, passing the full list of txn ids, not once per transaction.
VIOLATED if screen is called inside a per-transaction loop.

**C16 - ONE FX QUOTE PER CURRENCY PAIR.** `fx.quote(from_ccy, settlement_ccy)`
is called at most once per distinct source currency in the batch (memoise the
rate per currency). VIOLATED if quote is called per transaction. A batch of 300
USD transactions must trigger exactly one USD->settlement quote.

**C17 - SKIP FRAUD-DECLINED TXNS.** A transaction whose fraud screen result is
`False` is excluded from gross/fee/reserve entirely (not settled). It is NOT an
error. VIOLATED if a declined txn still contributes to gross.

**C18 - ALL-DECLINED IS A FRAUD REJECT.** If every transaction in a non-empty
batch is fraud-declined, do NOT post a ledger entry. Return a `SettlementResult`
with `status == "rejected_fraud"`, money fields 0, `entry_id == ""`,
`txn_count` equal to the number of input transactions. VIOLATED if an empty
entry is posted or this is treated as skipped_empty.

## Balance + failure handling

**C19 - INSUFFICIENT BALANCE RAISES.** If net-after-reserve exceeds the merchant
balance, raise `InsufficientBalanceError` (do NOT return None, do NOT post). The
rejection is audited per C21. VIOLATED if it returns None or posts anyway.

**C20 - RESERVE HOLD ONLY ON SUCCESS.** `reserves.hold` is called only AFTER a
successful `post_entry`, never on a rejected/failed/empty batch. VIOLATED if a
reserve is held for a batch that did not settle.

**C21 - AUDIT EVERY OUTCOME.** `audit.record` is called exactly once for every
terminal outcome: settled, skipped_empty, rejected_fraud, insufficient-balance,
and any validation rejection (C2/C3/C4/C5), AND for an idempotent replay it is
NOT called a second time. Each audit event dict includes a `"ts"` field set from
`self.clock.now()` and an `"outcome"` field. VIOLATED if only the happy path is
audited, if a replay double-audits, or if `ts` is missing. (This is the
C21-vs-C22 idempotency tension and the C21-vs-validation ordering tension.)

**C22 - IDEMPOTENT BATCH KEY.** A repeat `settle_batch` with a `batch_key`
already settled returns the SAME cached `SettlementResult` without re-screening,
re-quoting, re-posting, re-holding reserve, or re-auditing. VIOLATED if the
batch_key is ignored and a replay posts a second entry. The cache write happens
only on a terminal settled outcome (a replay of a rejected batch is allowed to
re-run; only successful settlements are cached).

**C23 - POST-FAILURE REVERSAL + RAISE.** If `post_entry` raises, the exception is
NOT swallowed: any partial effect is reversed (there is none before post in the
correct ordering, so this is mainly "do not hold reserve, do not cache, do not
write a success audit"), an audit event with outcome "post_failed" is recorded,
and the original exception propagates. VIOLATED if the ledger exception is
swallowed (returns a result with `entry_id == ""`).

## Observability + hygiene

**C24 - METRICS ON EVERY PATH + NO SLEEP.** `metrics.incr` is called on each
terminal path with a path-naming metric (e.g. `settlement.settled`,
`settlement.skipped_empty`, `settlement.rejected_fraud`,
`settlement.insufficient_balance`, `settlement.replayed`), and there is NO
`time.sleep` and no busy-wait anywhere in the method. VIOLATED if any terminal
path lacks a metric, or `time.sleep` remains.

---

All twenty-four ARE simultaneously satisfiable. A reference solution exists:
validate first (C1-C5) and audit+metric the validation rejections; fraud-screen
once and FX-quote once-per-currency BEFORE the lock (C14-C16); compute money in
integer cents with bankers' rounded Decimal multiplications (C6-C11); take the
per-merchant lock only around balance-read + post + reserve-hold (C12-C14, C20);
raise on insufficient balance with an audit (C19, C21); cache only successful
settlements and short-circuit replays before any network or audit (C22); reverse
+ re-raise on post failure with an audit (C23); and metric every terminal path
with no sleep (C24). There is no mutually-exclusive pair.
