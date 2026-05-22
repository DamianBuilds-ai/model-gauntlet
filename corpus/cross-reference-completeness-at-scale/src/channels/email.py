"""Email channel for Northwind Relay.

Builds an email body from a notification payload and dispatches it.
"""

from ..templates.legacy import legacy_render_template
from .transport import send_smtp


def build_email(payload, locale):
    subject = payload.get("subject", "")
    body = legacy_render_template(payload, locale)
    return {"subject": subject, "body": body}


def deliver_email(payload, locale, address):
    message = build_email(payload, locale)
    return send_smtp(address, message["subject"], message["body"])
