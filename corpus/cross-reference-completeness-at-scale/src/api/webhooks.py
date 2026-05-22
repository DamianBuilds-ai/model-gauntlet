"""Inbound webhook handlers for Northwind Relay.

When an upstream system posts an event, we render an immediate acknowledgement
body and enqueue downstream notifications. The ack render is on the hot path.
"""

from ..templates.legacy import legacy_render_template
from ..relay.queue import NotificationQueue


def handle_event(event, queue: NotificationQueue):
    payload = event.get("payload", {})
    locale = event.get("locale", "en-US")
    ack_body = legacy_render_template(payload, locale)
    queue.push({"channel": event.get("channel"), "payload": payload,
                "locale": locale, "ack": ack_body})
    return {"accepted": True, "ack": ack_body}
