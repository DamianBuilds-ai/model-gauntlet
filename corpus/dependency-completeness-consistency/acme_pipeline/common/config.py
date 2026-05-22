"""acme_pipeline.common.config - configuration access for the pipeline."""

from acme_pipeline.common import schema

_DEFAULTS = {
    "normalizer.rounding_plugin": "acme_pipeline.transform.plugins.rounding",
    "cache.backend": "memory",
}


def get(key, default=None):
    schema.validate_key(key)
    return _DEFAULTS.get(key, default)
