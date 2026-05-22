"""Webhook handlers for Acme Ledger.

Handles inbound payment-provider webhooks. No tax computation happens here - this
is a distractor file with no reference to the deprecated function. It mentions
"tax" only in a log string, not as a call.
"""

import json


def handle_payment_succeeded(payload):
    event = json.loads(payload)
    return {"recorded": event["id"], "note": "payment captured, tax already on invoice"}


def handle_refund_issued(payload):
    event = json.loads(payload)
    return {"refunded": event["id"]}
