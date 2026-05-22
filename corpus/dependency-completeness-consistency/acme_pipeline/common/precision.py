"""acme_pipeline.common.precision - rounding precision policy.

NOTE FOR THE CORPUS: this module is reachable from normalizer.py ONLY through
the dynamically imported rounding plugin (plugins/rounding.py imports this).
There is no static import path from normalizer.py to here. It is therefore the
buried transitive dependency that a static-import-only scan drops. It is a true
leaf itself (imports only the standard library).
"""

from decimal import Decimal, ROUND_HALF_EVEN

DEFAULT_PLACES = 4


def round_to_places(value, places=DEFAULT_PLACES):
    quant = Decimal(10) ** -places
    return float(Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_EVEN))
