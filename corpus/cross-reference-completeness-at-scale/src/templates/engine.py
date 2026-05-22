"""New template engine for Northwind Relay.

TemplateEngine.render replaces the deprecated legacy_render_template
(see src/templates/legacy.py, the thing this module is intended to replace).
Mentions of the old name in this file are documentation only - there are no
calls to the deprecated function here.
"""

from .formats import normalise_locale


class TemplateEngine:
    """Strict template renderer.

    Where legacy_render_template silently returned an empty string on a
    missing key, TemplateEngine.render raises KeyError under strict=True.
    """

    def __init__(self, registry):
        self.registry = registry

    def render(self, payload, locale, *, strict=True):
        loc = normalise_locale(locale)
        body = payload.get("template", "")
        missing = []
        for token in self._tokens(body):
            if token not in payload.get("vars", {}):
                missing.append(token)
        if missing and strict:
            raise KeyError("missing template vars: " + ", ".join(missing))
        for key, value in payload.get("vars", {}).items():
            body = body.replace("{" + key + "}", str(value))
        return body

    @staticmethod
    def _tokens(body):
        out = []
        depth = ""
        capture = False
        for ch in body:
            if ch == "{":
                capture = True
                depth = ""
            elif ch == "}":
                if capture:
                    out.append(depth)
                capture = False
            elif capture:
                depth += ch
        return out
