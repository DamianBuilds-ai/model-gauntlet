# Synthetic source for the cross-language-migration eval.
# Task: port this Python module to idiomatic Go. Fully synthetic - a small
# inventory-reservation helper for a fictional "Acme" store.

from dataclasses import dataclass
from typing import Optional


@dataclass
class Item:
    sku: str
    on_hand: int
    reserved: int

    def available(self) -> int:
        return self.on_hand - self.reserved


class Inventory:
    def __init__(self) -> None:
        self._items: dict[str, Item] = {}

    def add(self, sku: str, on_hand: int) -> None:
        if on_hand < 0:
            raise ValueError("on_hand must be non-negative")
        self._items[sku] = Item(sku=sku, on_hand=on_hand, reserved=0)

    def reserve(self, sku: str, qty: int) -> bool:
        """Reserve qty units of sku. Returns True on success, False if not enough
        available or the sku is unknown. qty must be positive."""
        if qty <= 0:
            raise ValueError("qty must be positive")
        item = self._items.get(sku)
        if item is None:
            return False
        if item.available() < qty:
            return False
        item.reserved += qty
        return True

    def release(self, sku: str, qty: int) -> None:
        """Release a previously reserved qty. Clamps at zero - never goes negative."""
        item = self._items.get(sku)
        if item is None:
            return
        item.reserved = max(0, item.reserved - qty)

    def available(self, sku: str) -> Optional[int]:
        item = self._items.get(sku)
        return item.available() if item else None
