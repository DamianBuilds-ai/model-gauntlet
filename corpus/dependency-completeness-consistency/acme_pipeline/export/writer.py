"""acme_pipeline.export.writer - DISTRACTOR. Imports storage.cache and a
formatting module. normalizer does NOT depend on export.writer. Listing it as a
dependency of normalizer is a precision error."""

from acme_pipeline.storage import cache
from acme_pipeline.export import formats


def export_all(keys):
    rows = [cache.get(k) for k in keys]
    return formats.to_csv(rows)
