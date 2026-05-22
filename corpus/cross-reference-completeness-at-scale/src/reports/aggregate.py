"""Aggregation helpers for Northwind Relay reports.

Clean module - groups and counts delivery events. No reference to the
deprecated renderer.
"""


def bucket_by_channel(events):
    buckets = {}
    for ev in events:
        buckets.setdefault(ev.get("channel", "unknown"), []).append(ev)
    return buckets


def summarise_counts(buckets):
    return {channel: len(items) for channel, items in buckets.items()}
