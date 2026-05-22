"""Notification templates for Cardinal. Distractor - no reserve_stock reference."""


def render_confirmation(order_id, name, total):
    return f"Hi {name}, your order {order_id} is confirmed. Total: {total}."


def render_cancellation(order_id, name):
    return f"Hi {name}, your order {order_id} was cancelled."
