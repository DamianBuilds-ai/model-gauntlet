"""SMS channel for Northwind Relay.

Renders a short-form body. Imports the legacy renderer under an alias, so a
search for the literal function name will NOT find the call site below.
"""

from ..templates.legacy import legacy_render_template as _render
from .transport import send_gateway

MAX_SMS_LEN = 160


def build_sms(payload, locale):
    raw = _render(payload, locale)
    return raw[:MAX_SMS_LEN]


def deliver_sms(payload, locale, number):
    body = build_sms(payload, locale)
    return send_gateway(number, body)
