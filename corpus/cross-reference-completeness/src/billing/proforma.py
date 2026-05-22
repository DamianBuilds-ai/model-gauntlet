"""Proforma (quote) generation for Acme Ledger.

This module imports the deprecated function under an ALIAS and calls it through
the alias, so a search for the literal name "legacy_compute_tax" at the call
site will NOT find it - the call site reads "_calc_tax". This is an indirect
reference. Both the aliased import line and the aliased call site reference the
deprecated function and must migrate.
"""

from decimal import Decimal

from src.tax.legacy import legacy_compute_tax as _calc_tax


def build_proforma(cart, region):
    lines = []
    for entry in cart:
        net = Decimal(entry["unit_price"]) * entry["qty"]
        # Aliased call - this IS legacy_compute_tax under the name _calc_tax.
        tax = _calc_tax(net, region)
        lines.append({"description": entry["description"], "net": net, "tax": tax})
    return {"kind": "proforma", "lines": lines}
