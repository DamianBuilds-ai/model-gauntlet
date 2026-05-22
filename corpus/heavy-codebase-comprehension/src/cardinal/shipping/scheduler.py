"""Shipment scheduling for Cardinal. Distractor - downstream of reserve_stock.

schedule_shipment is CALLED BY run_checkout after payment. It reads reservations
that were already placed but does not itself call reserve_stock.
"""

from cardinal.shipping.carrier import book_carrier


def schedule_shipment(order_id, lines, customer):
    address = customer.get("address", {})
    carrier = book_carrier(address.get("country", "US"), lines)
    return {
        "order_id": order_id,
        "carrier": carrier["name"],
        "eta_days": carrier["eta_days"],
        "lines": len(lines),
    }


def cancel_shipment(order_id):
    return {"order_id": order_id, "status": "cancelled"}
