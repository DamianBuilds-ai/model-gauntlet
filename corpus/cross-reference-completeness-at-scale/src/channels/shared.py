"""Shared channel helpers for Northwind Relay.

render_channel_body is a thin WRAPPER that forwards to the deprecated
legacy_render_template. Any channel that calls render_channel_body reaches
the deprecated behaviour indirectly through this wrapper.
"""

from ..templates.legacy import legacy_render_template


def render_channel_body(payload, locale):
    # Wrapper: forwards straight to the deprecated renderer.
    return legacy_render_template(payload, locale)


def channel_defaults():
    return {"retry": 3, "timeout_s": 10}
