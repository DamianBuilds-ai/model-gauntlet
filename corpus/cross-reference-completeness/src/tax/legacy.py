"""Legacy tax helpers for Acme Ledger.

This module defines the deprecated tax function that the migration is retiring.
It ALSO defines a similarly named taxonomy helper that is NOT part of the
migration - do not confuse the two.
"""

from decimal import Decimal


# DEPRECATED. This is the function the migration is removing. It is being
# replaced by TaxEngine.compute (see src/tax/engine.py). DEFINITION SITE.
def legacy_compute_tax(amount, region):
    """Return the tax owed on amount for the given region. Deprecated."""
    rate = _REGION_RATES.get(region, Decimal("0.10"))
    return Decimal(amount) * rate


# NOT the migration target. This computes a product taxonomy code, nothing to
# do with tax money. It is a precision trap: a careless search for
# "legacy_compute_tax" substring will match this name too. It must NOT appear
# in the migration checklist.
def legacy_compute_taxonomy(product):
    """Return the legacy taxonomy classification code for a product."""
    return f"TAX-{product.category_id:04d}"


_REGION_RATES = {
    "AU": Decimal("0.10"),
    "NZ": Decimal("0.15"),
    "GB": Decimal("0.20"),
}
