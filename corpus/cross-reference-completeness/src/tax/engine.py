"""The new tax engine for Acme Ledger.

This is the replacement for legacy_compute_tax. It is the migration TARGET API,
not a reference to the deprecated function, so this file is a distractor for the
"find every reference to the OLD function" task - it contains no legacy call.
"""

from decimal import Decimal


class TaxEngine:
    """New tax computation. Replaces the deprecated legacy_compute_tax."""

    _RATES = {
        "AU": Decimal("0.10"),
        "NZ": Decimal("0.15"),
        "GB": Decimal("0.20"),
    }

    def compute(self, amount, region, *, inclusive=False):
        rate = self._RATES.get(region, Decimal("0.10"))
        base = Decimal(amount)
        if inclusive:
            return base - (base / (Decimal("1") + rate))
        return base * rate
