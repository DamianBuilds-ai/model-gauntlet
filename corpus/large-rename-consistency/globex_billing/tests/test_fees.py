"""globex_billing.tests.test_fees - tests. Import line + two call sites that
must be renamed, plus a decoy call to compute_handling_fee that must NOT be."""

from globex_billing.core.fees import (
    compute_shipping_fee,
    compute_handling_fee,
)


def test_compute_shipping_fee_domestic():
    assert compute_shipping_fee(10, "domestic") > 0


def test_compute_shipping_fee_international():
    assert compute_shipping_fee(10, "international") > compute_shipping_fee(10, "domestic")


def test_compute_handling_fee_decoy():
    # decoy - different function, do not rename
    assert compute_handling_fee(3) == 2.25
