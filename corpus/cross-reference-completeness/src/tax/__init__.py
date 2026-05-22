"""Tax package for Acme Ledger.

Re-exports the public tax surface. NOTE: this re-export of legacy_compute_tax is
itself an INDIRECT reference - downstream code that does `from src.tax import
legacy_compute_tax` depends on this line, so the migration must update it too.
"""

from src.tax.engine import TaxEngine
from src.tax.legacy import legacy_compute_tax  # re-export of the deprecated fn

__all__ = ["TaxEngine", "legacy_compute_tax"]
