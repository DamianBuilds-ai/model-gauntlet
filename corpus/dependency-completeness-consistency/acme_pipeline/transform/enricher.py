"""acme_pipeline.transform.enricher - DEAD MODULE. Enrichment was removed in
revision 3. normalizer's only reference to this module is a COMMENTED-OUT
import, so it is NOT in normalizer's live dependency closure. It imports a leaf
of its own; listing enricher (or that leaf) as a normalizer dependency is a
precision error driven by reading dead code as live."""

from acme_pipeline.common import geo


def enrich(record):
    record["region"] = geo.region_for(record.get("zip"))
    return record
