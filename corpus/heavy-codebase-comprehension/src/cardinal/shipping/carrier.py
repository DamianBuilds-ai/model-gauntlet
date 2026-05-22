"""Carrier booking adapter for Cardinal. Distractor - no reserve_stock reference."""

_CARRIERS = {
    "US": {"name": "Initech Freight", "eta_days": 3},
    "GB": {"name": "Umbra Logistics", "eta_days": 5},
    "AU": {"name": "Acme Post", "eta_days": 7},
}


def book_carrier(country, lines):
    return _CARRIERS.get(country, {"name": "Acme Post", "eta_days": 10})


def track(tracking_id):
    return {"tracking_id": tracking_id, "status": "in_transit"}
