"""Legacy template rendering for Northwind Relay.

DEPRECATED MODULE. legacy_render_template is being retired in favour of
TemplateEngine.render in src/templates/engine.py. This module is kept only
until every caller has migrated. Do not add new callers.
"""

from .formats import normalise_locale


def legacy_render_template(payload, locale):
    """Render a notification body from a payload dict and a locale string.

    DEPRECATED. Use TemplateEngine.render(payload, locale, strict=True).
    The legacy path silently swallows missing-key errors and returns an
    empty string, which the new engine refuses to do under strict mode.
    """
    loc = normalise_locale(locale)
    body = payload.get("template", "")
    for key, value in payload.get("vars", {}).items():
        body = body.replace("{" + key + "}", str(value))
    return body


def legacy_render_template_preview(payload):
    """Render a TRUNCATED preview. DIFFERENT function, not the migration target.

    This is a separate helper (a 120-char preview for the admin UI). It does
    NOT take a locale and is NOT being retired. Its name is deliberately close
    to legacy_render_template; do not confuse the two.
    """
    body = payload.get("template", "")
    return body[:120]
