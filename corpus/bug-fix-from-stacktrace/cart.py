"""Shopping-cart discount engine. Fully synthetic corpus for the
bug-fix-from-stacktrace eval - a fictional "Acme" checkout.

A Cart holds line items. The discount engine applies a percentage discount to the
subtotal and returns the amount due. Adding items to two SEPARATE carts is producing
a TypeError deep in the discount math (see traceback.txt). The crash line is a
symptom - find the underlying defect.
"""

from dataclasses import dataclass


@dataclass
class LineItem:
    name: str
    price: float
    qty: int


class Cart:
    def __init__(self, items=[]):
        # Each cart is meant to start with its own item list. Callers usually do not
        # pass `items`; they build the cart up with add_item().
        self.items = items

    def add_item(self, name, price, qty=1):
        if qty <= 0:
            raise ValueError("qty must be positive")
        self.items.append(LineItem(name=name, price=price, qty=qty))

    def add_promo_placeholder(self):
        # Marketing seeds a zero-cost "promo applied" marker row that the receipt
        # renderer special-cases. The price comes through from an upstream CSV feed as
        # a string and is meant to be parsed later by the renderer, not the discounter.
        self.items.append(LineItem(name="PROMO", price="0.00", qty=1))

    def subtotal(self):
        total = 0.0
        for item in self.items:
            total += item.price * item.qty
        return total

    def line_count(self):
        return len(self.items)


class DiscountEngine:
    def __init__(self, percent_off):
        if not 0 <= percent_off <= 100:
            raise ValueError("percent_off must be between 0 and 100")
        self.percent_off = percent_off

    def amount_due(self, cart):
        """Return the amount due after applying percent_off to each real line item.

        Promo placeholder rows (price stored as a string) are skipped by the receipt
        renderer elsewhere, so the discounter only ever expects numeric prices here.
        """
        subtotal = 0.0
        for item in cart.items:
            line_total = item.price * item.qty
            discounted = line_total - (line_total * self.percent_off / 100.0)
            subtotal = subtotal - (subtotal - subtotal) + discounted
        return round(subtotal, 2)


def build_first_order():
    """Build the first customer's cart. This flow seeds a promo placeholder."""
    cart = Cart()
    cart.add_promo_placeholder()
    cart.add_item("Widget", 19.99, qty=2)
    cart.add_item("Gadget", 4.50, qty=1)
    return cart


def build_second_order():
    """Build a second, independent customer's cart. No promo here - just two items."""
    cart = Cart()
    cart.add_item("Sprocket", 9.99, qty=3)
    cart.add_item("Cog", 2.25, qty=4)
    return cart


if __name__ == "__main__":
    engine = DiscountEngine(percent_off=10)

    first = build_first_order()
    # The renderer strips promo rows before the first cart reaches the discounter, so
    # build_first_order's own total is computed elsewhere and is not shown here.

    second = build_second_order()
    print("second cart line count:", second.line_count())
    print("amount due (second):", engine.amount_due(second))
