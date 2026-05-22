"""acme_pipeline.vendor.kvstore - a tiny in-package key value store. A true
leaf with no intra-package imports (standard library only)."""


class MemoryStore:
    def __init__(self):
        self._d = {}

    def set(self, key, value):
        self._d[key] = value

    def get(self, key):
        return self._d.get(key)
