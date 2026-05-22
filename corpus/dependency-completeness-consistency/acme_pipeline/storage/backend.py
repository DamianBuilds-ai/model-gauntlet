"""acme_pipeline.storage.backend - storage backend factory."""

from acme_pipeline.vendor import kvstore


def open_backend(kind):
    if kind == "memory":
        return kvstore.MemoryStore()
    raise ValueError(f"unknown backend kind: {kind}")
