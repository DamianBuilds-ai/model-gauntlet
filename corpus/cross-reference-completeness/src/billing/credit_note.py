"""Credit note generation for Acme Ledger.

A credit note reverses tax on a returned item. One direct, obvious call to the
deprecated legacy_compute_tax.
"""

from decimal import Decimal

from src.tax.legacy import legacy_compute_tax


def build_credit_note(original_line, region):
    net = Decimal(original_line["net"])
    # Direct call to deprecated function - must migrate to TaxEngine.compute.
    tax = legacy_compute_tax(net, region)
    return {
        "description": f"Credit: {original_line['description']}",
        "net": -net,
        "tax": -tax,
        "gross": -(net + tax),
    }
