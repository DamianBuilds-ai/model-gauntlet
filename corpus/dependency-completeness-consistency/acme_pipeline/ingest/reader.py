"""acme_pipeline.ingest.reader - DISTRACTOR. This module imports the normalizer
and several common modules, but normalizer does NOT depend on it (the edge runs
the other way: reader -> normalizer). A model that lists ingest.reader as a
dependency OF normalizer has reversed an edge and made a precision error."""

from acme_pipeline.transform import normalizer
from acme_pipeline.common import constants


def read_and_normalize(rows):
    records = [{"id": i, "value": v, "unit": constants.CANONICAL_UNIT}
               for i, v in enumerate(rows)]
    return normalizer.normalize_batch(records)
