"""Shared error types for Cardinal. Distractor for the reserve_stock trace -
defines exceptions only, no reserve_stock reference."""


class CardinalError(Exception):
    """Base class for all Cardinal domain errors."""


class OutOfStockError(CardinalError):
    def __init__(self, sku, requested, available):
        self.sku = sku
        self.requested = requested
        self.available = available
        super().__init__(
            f"out of stock for {sku}: requested {requested}, available {available}"
        )


class PaymentDeclinedError(CardinalError):
    def __init__(self, order_id, reason):
        self.order_id = order_id
        self.reason = reason
        super().__init__(f"payment declined for {order_id}: {reason}")


class ShipmentError(CardinalError):
    pass


class InvalidOrderError(CardinalError):
    pass
