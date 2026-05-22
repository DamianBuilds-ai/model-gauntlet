"""acme_pipeline.storage.cache - result cache for normalized records."""

from acme_pipeline.storage import backend
from acme_pipeline.common import config

_store = backend.open_backend(config.get("cache.backend", default="memory"))


def put(key, value):
    _store.set(key, value)


def get(key):
    return _store.get(key)
