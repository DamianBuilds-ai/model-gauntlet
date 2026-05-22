"""Append-only ledger for Cardinal inventory + payment events.

Distractor for the reserve_stock trace. reserve_stock CALLS write_ledger_entry,
but write_ledger_entry does NOT call reserve_stock - the dependency points the
other way. No reserve_stock reference lives here.
"""

import time

_LEDGER = []


def write_ledger_entry(action, *, sku, quantity, order_id):
    entry = {
        "ts": time.time(),
        "action": action,
        "sku": sku,
        "quantity": quantity,
        "order_id": order_id,
    }
    _LEDGER.append(entry)
    return entry


def read_ledger(sku=None):
    if sku is None:
        return list(_LEDGER)
    return [e for e in _LEDGER if e["sku"] == sku]


def ledger_balance(sku):
    bal = 0
    for e in read_ledger(sku):
        if e["action"] in ("reserve", "release", "restock"):
            sign = 1 if e["action"] == "restock" else -1
            bal += sign * (e["quantity"] or 0)
    return bal
