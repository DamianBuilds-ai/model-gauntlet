"""Templates package for Northwind Relay.

Re-exports the public rendering surface. NOTE: this still re-exports the
deprecated legacy_render_template so older imports keep working - that
re-export must be removed as part of the migration.
"""

from .engine import TemplateEngine
from .legacy import legacy_render_template

__all__ = ["TemplateEngine", "legacy_render_template"]
