"""Northwind Payments - merchant settlement engine (DEFICIENT starting state).

This module batches captured card transactions into per-merchant settlement
runs, applies fees, reserves, FX conversion, and writes ledger entries plus an
audit trail. It is the single largest hot-path module in the Northwind core and
it is currently wrong in many ways at once.

The refactor task (see constraints.md) is to make the settle_batch entry point
satisfy ALL of the listed constraints SIMULTANEOUSLY without changing the
collaborator interfaces (LedgerClient, FxClient, FraudClient, AuditLog,
MetricsSink, ReserveStore, ClockSource) and without changing the public shape of
the SettlementResult / SettlementError types.

The collaborators are injected. Their interfaces are fixed - do not change them:

    LedgerClient:
        get_merchant_balance(merchant_id) -> Decimal      # network call
        post_entry(entry: LedgerEntry) -> str             # returns entry_id, network call
        reverse_entry(entry_id) -> None                   # network call

    FxClient:
        quote(from_ccy, to_ccy) -> Decimal                # network call, the rate
        # NOTE: quote is rate-limited upstream; calling it per-transaction in a
        # tight loop will trip the upstream limiter. Quote once per currency pair.

    FraudClient:
        screen(merchant_id, txn_ids: list[str]) -> dict[str, bool]
        # network call, returns {txn_id: approved_bool}; batch-screen, do not call per txn

    AuditLog:
        record(event: dict) -> None                       # local, must be append-only

    MetricsSink:
        incr(name, value=1, tags=None) -> None            # local, non-blocking

    ReserveStore:
        get_reserve_rate(merchant_id) -> Decimal          # local
        hold(merchant_id, amount: Decimal) -> None        # local

    ClockSource:
        now() -> datetime                                 # injectable clock (tz-aware UTC)

The data types are defined below. Transaction amounts are in MINOR units
(integer cents) on input and must stay integer cents through fee/reserve maths -
floating point money is a defect. FX conversion is the one place a Decimal rate
is applied, and the result must be rounded to integer minor units using
bankers' rounding (ROUND_HALF_EVEN), then carried as integer cents again.
"""

from __future__ import annotations

import time
import threading
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


# ---------------------------------------------------------------------------
# Data types (public shapes - do not change field names)
# ---------------------------------------------------------------------------


@dataclass
class Transaction:
    txn_id: str
    merchant_id: str
    amount_minor: int          # integer cents in the transaction's own currency
    currency: str              # ISO 4217, e.g. "AUD", "USD"
    captured_at: datetime
    kind: str = "sale"         # "sale" or "refund"


@dataclass
class LedgerEntry:
    merchant_id: str
    amount_minor: int          # settlement currency minor units, signed
    currency: str              # the settlement currency
    memo: str
    source_txn_ids: list[str] = field(default_factory=list)


@dataclass
class SettlementResult:
    merchant_id: str
    settlement_currency: str
    gross_minor: int
    fee_minor: int
    reserve_minor: int
    net_minor: int
    entry_id: str
    txn_count: int
    status: str                # "settled", "skipped_empty", "rejected_fraud"


class SettlementError(Exception):
    """Base settlement failure. Subtypes below."""


class CurrencyMismatchError(SettlementError):
    pass


class InsufficientBalanceError(SettlementError):
    pass


class EmptyBatchError(SettlementError):
    pass


# ---------------------------------------------------------------------------
# Configuration (read-only constants - the refactor must honour these)
# ---------------------------------------------------------------------------

# Fee is 2.9% + 30 cents per SALE transaction, in the settlement currency, after
# FX. Refunds carry no fee but reverse gross. Fee maths must be integer cents.
FEE_BPS = 290               # 2.90% expressed in basis points
FEE_FIXED_MINOR = 30        # 30 cents fixed per sale txn, settlement currency

# Reserve is a percentage of NET (after fee) held back, rate per merchant from
# ReserveStore. Reserve is integer cents, bankers' rounded.
MAX_BATCH_SIZE = 500        # a single settle_batch must reject > 500 transactions

SUPPORTED_SETTLEMENT_CCY = {"AUD", "USD", "EUR", "GBP"}


# ---------------------------------------------------------------------------
# The engine (DEFICIENT - this is what gets refactored)
# ---------------------------------------------------------------------------


class SettlementEngine:
    def __init__(self, ledger, fx, fraud, audit, metrics, reserves, clock,
                 settlement_currency="AUD"):
        self.ledger = ledger
        self.fx = fx
        self.fraud = fraud
        self.audit = audit
        self.metrics = metrics
        self.reserves = reserves
        self.clock = clock
        self.settlement_currency = settlement_currency
        # single global lock guarding ALL merchants - a bottleneck defect
        self._lock = threading.Lock()
        # idempotency memory, currently declared but never consulted
        self._settled_batches: dict[str, SettlementResult] = {}

    def settle_batch(self, merchant_id, transactions, batch_key):
        """Settle a batch of captured transactions for one merchant.

        DEFICIENT. Known problems (non-exhaustive - see constraints.md):
          - no input validation (empty batch, oversized batch, wrong-currency
            settlement target, duplicate txn ids all slip through)
          - batch_key idempotency is ignored
          - FX quote is fetched inside the per-transaction loop (rate-limit risk)
          - fraud screen is called once per transaction instead of batched
          - money maths drift into float
          - a single global lock serialises every merchant
          - balance is read outside the lock then posted inside (TOCTOU)
          - audit only records the happy path
          - network post happens while the lock is held
          - refunds are treated identically to sales (fee wrongly applied)
          - no metrics on the reject/skip paths
          - exceptions from the ledger are swallowed
        """
        # PROBLEM: no validation at all. Empty, oversized, dup, bad-currency
        # batches all proceed.

        with self._lock:  # PROBLEM: global lock, and everything below is under it
            gross = 0.0   # PROBLEM: float money
            fee = 0.0
            screened = {}
            for txn in transactions:
                # PROBLEM: per-transaction fraud call
                screened.update(self.fraud.screen(merchant_id, [txn.txn_id]))
                if not screened.get(txn.txn_id, False):
                    continue
                # PROBLEM: per-transaction FX quote inside the loop
                rate = self.fx.quote(txn.currency, self.settlement_currency)
                converted = float(txn.amount_minor) * float(rate)  # PROBLEM: float
                gross += converted
                # PROBLEM: fee applied to refunds too
                fee += converted * (FEE_BPS / 10000.0) + FEE_FIXED_MINOR

            # PROBLEM: balance read here, outside any per-merchant guarantee,
            # and the comparison is float
            balance = float(self.ledger.get_merchant_balance(merchant_id))
            net = gross - fee
            reserve_rate = self.reserves.get_reserve_rate(merchant_id)
            reserve = net * float(reserve_rate)  # PROBLEM: float
            net_after_reserve = net - reserve

            if net_after_reserve > balance:
                # PROBLEM: swallowed - returns a half-built result instead of
                # raising, and never audits the rejection
                return None

            entry = LedgerEntry(
                merchant_id=merchant_id,
                amount_minor=int(net_after_reserve),  # PROBLEM: truncation not rounding
                currency=self.settlement_currency,
                memo="settlement",
                source_txn_ids=[t.txn_id for t in transactions],
            )
            try:
                # PROBLEM: network post under the lock
                entry_id = self.ledger.post_entry(entry)
            except Exception:
                # PROBLEM: swallowed exception, no audit, no reversal
                entry_id = ""

            self.reserves.hold(merchant_id, Decimal(str(reserve)))

            # PROBLEM: audits only success, with no timestamp from the clock
            self.audit.record({"event": "settled", "merchant": merchant_id})

            result = SettlementResult(
                merchant_id=merchant_id,
                settlement_currency=self.settlement_currency,
                gross_minor=int(gross),
                fee_minor=int(fee),
                reserve_minor=int(reserve),
                net_minor=int(net_after_reserve),
                entry_id=entry_id,
                txn_count=len(transactions),
                status="settled",
            )
            # PROBLEM: idempotency cache never written, so replays re-post
            time.sleep(0)  # PROBLEM: leftover sleep placeholder
            return result
