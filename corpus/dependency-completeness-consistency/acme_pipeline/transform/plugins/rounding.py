"""acme_pipeline.transform.plugins.rounding - the default rounding plugin.

This module is imported at RUNTIME by normalizer._load_rounding_plugin via a
dotted-path string resolved from config, not by a static import in normalizer.
It in turn imports common.precision, so common.precision is in normalizer's
transitive dependency closure ONLY through this dynamic edge.
"""

from acme_pipeline.common import precision


def round_canonical(value):
    return precision.round_to_places(value, places=precision.DEFAULT_PLACES)
