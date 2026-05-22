"""Admin preview endpoints for Northwind Relay.

Renders SHORT previews for the admin console. These use the separate
legacy_render_template_preview helper (a 120-char preview), NOT the
deprecated legacy_render_template. The preview helper is not being retired,
so nothing in this file is part of the migration.
"""

from ..templates.legacy import legacy_render_template_preview


def preview_notification(payload):
    # Uses the PREVIEW helper, a different function from the migration target.
    snippet = legacy_render_template_preview(payload)
    return {"preview": snippet}


def preview_batch(payloads):
    return [preview_notification(p) for p in payloads[:20]]
