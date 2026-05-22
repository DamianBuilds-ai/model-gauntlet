"""Notification dispatch for Cardinal. Distractor - downstream of reserve_stock.

notify_order_confirmed is CALLED BY checkout at the end of the flow. It sends an
email/SMS and does not call reserve_stock.
"""

from cardinal.notifications.templates import render_confirmation


def notify_order_confirmed(order_id, customer, total):
    body = render_confirmation(order_id, customer.get("name", "customer"), total)
    channel = customer.get("preferred_channel", "email")
    return {"order_id": order_id, "channel": channel, "sent": True, "body": body}


def notify_order_cancelled(order_id, customer):
    return {"order_id": order_id, "channel": "email", "sent": True}
