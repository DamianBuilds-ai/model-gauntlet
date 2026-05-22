"""Inventory package for Cardinal.

This package re-exports reserve_stock so other packages can import it from
cardinal.inventory directly rather than reaching into cardinal.inventory.reservations.
The re-export (the import on line 11 and the __all__ entry on line 14) is a TRUE
reference to reserve_stock - any consumer of cardinal.inventory.reserve_stock is
reaching the target function through this surface.
"""

from cardinal.inventory.reservations import (
    reserve_stock,
    release_stock,
    restock,
)

__all__ = ["reserve_stock", "release_stock", "restock"]
