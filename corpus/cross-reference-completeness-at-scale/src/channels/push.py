"""Push-notification channel for Northwind Relay.

Renders a push body. Reaches the renderer through the shared wrapper in
src/channels/shared.py rather than calling the deprecated function directly.
"""

from .shared import render_channel_body
from .transport import send_apns


def build_push(payload, locale):
    body = render_channel_body(payload, locale)
    title = payload.get("title", "")
    return {"title": title, "body": body}


def deliver_push(payload, locale, device_token):
    message = build_push(payload, locale)
    return send_apns(device_token, message["title"], message["body"])
