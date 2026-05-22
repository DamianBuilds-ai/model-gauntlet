"""acme_pipeline.transform.plugins.truncating - an ALTERNATE rounding plugin
that is NOT the configured default. config names
"acme_pipeline.transform.plugins.rounding" as the default, so normalizer never
imports this one at runtime. It is a DISTRACTOR: present in the same plugins
package as the real plugin, imports a different leaf, but is not reachable from
normalizer under the default configuration. Listing it (or common.floors via
it) as a normalizer dependency is a precision error."""

from acme_pipeline.common import floors


def round_canonical(value):
    return floors.floor_to_int(value)
