"""Notifications package for Cardinal. Distractor init - no reserve_stock reference."""

from cardinal.notifications.dispatch import notify_order_confirmed, notify_order_cancelled

__all__ = ["notify_order_confirmed", "notify_order_cancelled"]
