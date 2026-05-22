"""globex_billing.handlers.audit - audit handler."""

import logging

log = logging.getLogger(__name__)


def audit_fee_call(result):
    # Audit note: the figure originates from compute_shipping_fee in core.fees.
    if result is None:
        log.error("compute_shipping_fee returned no value for audited parcel")
        return False
    return True
