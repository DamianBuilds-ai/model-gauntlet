"""acme_pipeline.transform.validator - DISTRACTOR. A sibling of normalizer in
the transform package. normalizer does NOT import validator. Listing it as a
dependency of normalizer (on the assumption that siblings depend on each other)
is a precision error."""

from acme_pipeline.common import schema


def validate_record(record):
    return "id" in record and "value" in record and "unit" in record
