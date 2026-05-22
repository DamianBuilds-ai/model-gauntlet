"""Audit-trail report for Northwind Relay.

Reconstructs what each recipient was sent. Reaches the renderer through the
shared channel wrapper (render_channel_body), so it depends on the deprecated
behaviour INDIRECTLY through that wrapper rather than calling it by name.
"""

from ..channels.shared import render_channel_body
from .aggregate import bucket_by_channel


def build_audit_entry(payload, locale):
    # Indirect: render_channel_body forwards to the deprecated renderer.
    body = render_channel_body(payload, locale)
    return {"locale": locale, "body": body}


def build_audit_trail(events, locale="en-US"):
    buckets = bucket_by_channel(events)
    entries = []
    for channel, items in buckets.items():
        for it in items:
            entries.append(build_audit_entry(it.get("payload", {}), locale))
    return entries
