"""Locale + format helpers for Northwind Relay templates.

Clean utility module. No reference to the deprecated render function.
"""

_FALLBACK = "en-US"


def normalise_locale(locale):
    if not locale:
        return _FALLBACK
    parts = locale.replace("_", "-").split("-")
    lang = parts[0].lower()
    if len(parts) > 1:
        region = parts[1].upper()
        return lang + "-" + region
    return lang


def supported_locales():
    return ["en-US", "en-GB", "fr-FR", "de-DE", "es-ES"]
