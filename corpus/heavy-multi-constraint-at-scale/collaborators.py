"""Northwind Payments - collaborator interfaces + in-memory fakes.

This file is REFERENCE ONLY for the refactor. It documents the exact
collaborator contracts the SettlementEngine depends on. The refactor in
settlement.py must NOT change any of these signatures. The in-memory fakes at
the bottom exist so the engine can be exercised in tests; the refactor must keep
working against both the Protocols and these fakes.

Money is integer minor units (cents) everywhere except the FX rate and the
reserve rate, which are Decimal multipliers.
"""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from decimal import Decimal
from typing import Protocol


# ---------------------------------------------------------------------------
# Protocols (the fixed contracts - DO NOT CHANGE)
# ---------------------------------------------------------------------------


class LedgerClient(Protocol):
    def get_merchant_balance(self, merchant_id: str) -> Decimal:
        """Network call. Returns the merchant's available balance in settlement
        currency minor units, as a Decimal that is an integer value."""
        ...

    def post_entry(self, entry) -> str:
        """Network call. Persists a LedgerEntry, returns a new entry_id string.
        May raise on transport failure - the caller must handle that."""
        ...

    def reverse_entry(self, entry_id: str) -> None:
        """Network call. Reverses a previously posted entry by id."""
        ...


class FxClient(Protocol):
    def quote(self, from_ccy: str, to_ccy: str) -> Decimal:
        """Network call. Returns the conversion rate from from_ccy to to_ccy as
        a Decimal. Upstream rate-limited - call once per distinct currency pair
        per batch, never per transaction."""
        ...


class FraudClient(Protocol):
    def screen(self, merchant_id: str, txn_ids: list[str]) -> dict:
        """Network call. Batch-screens the given txn ids for one merchant and
        returns {txn_id: approved_bool}. Call ONCE per batch with all ids."""
        ...


class AuditLog(Protocol):
    def record(self, event: dict) -> None:
        """Local append-only audit write. Must be called once per terminal
        outcome. Event dicts carry at least an 'outcome' and a 'ts'."""
        ...


class MetricsSink(Protocol):
    def incr(self, name: str, value: int = 1, tags: dict | None = None) -> None:
        """Local non-blocking counter. Called on every terminal path."""
        ...


class ReserveStore(Protocol):
    def get_reserve_rate(self, merchant_id: str) -> Decimal:
        """Local. Returns the reserve fraction (e.g. Decimal('0.05')) for the
        merchant."""
        ...

    def hold(self, merchant_id: str, amount: Decimal) -> None:
        """Local. Records a reserve hold. Called only on a successful settle."""
        ...


class ClockSource(Protocol):
    def now(self) -> datetime:
        """Returns the current tz-aware UTC time. Injectable for tests."""
        ...


# ---------------------------------------------------------------------------
# In-memory fakes (for exercising the engine - keep them working)
# ---------------------------------------------------------------------------


class FakeLedger:
    def __init__(self, balances: dict[str, int]):
        self._balances = {m: Decimal(b) for m, b in balances.items()}
        self._entries: dict[str, object] = {}
        self._seq = 0
        self._lock = threading.Lock()
        self.fail_next_post = False

    def get_merchant_balance(self, merchant_id: str) -> Decimal:
        return self._balances.get(merchant_id, Decimal(0))

    def post_entry(self, entry) -> str:
        if self.fail_next_post:
            self.fail_next_post = False
            raise RuntimeError("ledger transport failure")
        with self._lock:
            self._seq += 1
            entry_id = f"ent_{self._seq}"
            self._entries[entry_id] = entry
        return entry_id

    def reverse_entry(self, entry_id: str) -> None:
        self._entries.pop(entry_id, None)


class FakeFx:
    def __init__(self, rates: dict[tuple[str, str], str]):
        self._rates = {k: Decimal(v) for k, v in rates.items()}
        self.calls: list[tuple[str, str]] = []

    def quote(self, from_ccy: str, to_ccy: str) -> Decimal:
        self.calls.append((from_ccy, to_ccy))
        if from_ccy == to_ccy:
            return Decimal(1)
        return self._rates[(from_ccy, to_ccy)]


class FakeFraud:
    def __init__(self, declined: set[str] | None = None):
        self._declined = declined or set()
        self.calls = 0

    def screen(self, merchant_id: str, txn_ids: list[str]) -> dict:
        self.calls += 1
        return {t: (t not in self._declined) for t in txn_ids}


class FakeAudit:
    def __init__(self):
        self.events: list[dict] = []

    def record(self, event: dict) -> None:
        self.events.append(dict(event))


class FakeMetrics:
    def __init__(self):
        self.counters: dict[str, int] = {}

    def incr(self, name: str, value: int = 1, tags: dict | None = None) -> None:
        self.counters[name] = self.counters.get(name, 0) + value


class FakeReserves:
    def __init__(self, rate: str = "0.05"):
        self._rate = Decimal(rate)
        self.holds: list[tuple[str, Decimal]] = []

    def get_reserve_rate(self, merchant_id: str) -> Decimal:
        return self._rate

    def hold(self, merchant_id: str, amount: Decimal) -> None:
        self.holds.append((merchant_id, amount))


class FakeClock:
    def __init__(self, fixed: datetime | None = None):
        self._fixed = fixed or datetime(2026, 5, 22, tzinfo=timezone.utc)

    def now(self) -> datetime:
        return self._fixed
