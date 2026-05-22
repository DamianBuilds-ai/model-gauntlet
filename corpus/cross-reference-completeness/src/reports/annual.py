"""Annual reporting for Acme Ledger.

Does NOT call legacy_compute_tax directly. Instead it calls the local wrapper
_apply_tax (from helpers.py), which forwards to the deprecated function. So the
call site here ("_apply_tax(...)") is an INDIRECT reference - whether it must
change depends on the migration strategy, but it is a true location that touches
the deprecated behaviour through the wrapper and must be listed (the strong
answer notes it is indirect-via-wrapper).
"""

from decimal import Decimal

from src.reports.helpers import _apply_tax


def annual_tax_collected(transactions, region):
    total = Decimal("0")
    for t in transactions:
        # Indirect: _apply_tax wraps the deprecated legacy_compute_tax.
        total += _apply_tax(t["amount"], region)
    return total


def build_annual_report(transactions, region):
    return {
        "year_tax": annual_tax_collected(transactions, region),
        "txn_count": len(transactions),
    }
