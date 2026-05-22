"""
acme_pipeline.transform.normalizer

The normalization stage of the Acme data pipeline. This is the TARGET module
for the dependency-completeness task: the question asks for every module in the
acme_pipeline package that this module transitively depends on.

Most dependencies are declared as ordinary top-of-file imports below. ONE
dependency is reached only at runtime through a dynamically resolved plugin
(see _load_rounding_plugin), so a scan of the static import lines alone will
miss it and everything reachable only through it.
"""

import importlib

from acme_pipeline.common import config
from acme_pipeline.common import units
from acme_pipeline.storage import cache

# from acme_pipeline.transform import enricher  # DEAD CODE: enrichment was
# removed in revision 3. This commented-out import is NOT a live dependency.
# A model that lists transform.enricher as a dependency has treated dead code as
# live and made a precision error.


def _load_rounding_plugin():
    """Resolve the rounding plugin named in configuration and import it at
    runtime. The plugin module path is a dotted string in config, so this edge
    does not appear as a static import. The configured default is
    "acme_pipeline.transform.plugins.rounding".
    """
    plugin_path = config.get("normalizer.rounding_plugin",
                             default="acme_pipeline.transform.plugins.rounding")
    module = importlib.import_module(plugin_path)
    return module


def normalize_record(record):
    """Normalize a single record: convert units, round, and cache the result."""
    converted = units.to_canonical(record["value"], record["unit"])
    rounding = _load_rounding_plugin()
    rounded = rounding.round_canonical(converted)
    cache.put(record["id"], rounded)
    return rounded


def normalize_batch(records):
    return [normalize_record(r) for r in records]
