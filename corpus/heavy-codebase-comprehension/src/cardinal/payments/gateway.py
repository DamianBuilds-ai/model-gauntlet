"""Payment gateway adapter for Cardinal (fictional 'Globex' gateway).

Distractor - external payment authorize/capture. No reserve_stock reference.
"""

import uuid
from decimal import Decimal


def authorize(token, amount):
    if amount <= Decimal("0"):
        return {"approved": False, "reason": "invalid_amount"}
    if token == "decline-card":
        return {"approved": False, "reason": "card_declined"}
    return {"approved": True, "auth_id": str(uuid.uuid4()), "amount": str(amount)}


def capture(auth_id, amount):
    return {"captured": True, "auth_id": auth_id, "amount": str(amount)}


def void(auth_id):
    return {"voided": True, "auth_id": auth_id}
