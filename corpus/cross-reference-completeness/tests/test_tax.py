"""Tests for Acme Ledger tax behaviour.

Imports the deprecated legacy_compute_tax and asserts on its output. Both the
import line and the call inside the test reference the deprecated function and
must migrate (the test will need to target TaxEngine.compute after the cutover).

Note: there is also a test for legacy_compute_taxonomy below - that one is NOT
part of the tax-money migration and must NOT be counted as a location to change.
"""

from decimal import Decimal

from src.tax.legacy import legacy_compute_tax, legacy_compute_taxonomy


def test_compute_tax_au():
    # References the deprecated function - must migrate to TaxEngine.compute.
    assert legacy_compute_tax(100, "AU") == Decimal("10.0")


def test_compute_tax_default_region():
    assert legacy_compute_tax(100, "ZZ") == Decimal("10.0")


def test_compute_taxonomy_is_unrelated():
    # This exercises legacy_compute_taxonomy - the precision trap. NOT part of
    # the tax-money migration. Do not count this as a migration location.
    class FakeProduct:
        category_id = 7

    assert legacy_compute_taxonomy(FakeProduct()) == "TAX-0007"
