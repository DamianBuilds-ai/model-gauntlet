"""In-memory notification queue for Northwind Relay.

Clean data-structure module. No template rendering, no reference to the
deprecated renderer.
"""

from collections import deque


class NotificationQueue:
    def __init__(self):
        self._items = deque()
        self._dead = []
        self._archive = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            return None
        return self._items.popleft()

    def dead_letter(self, record):
        self._dead.append(record)

    def archive_rendered(self, item, rendered):
        self._archive.append({"item": item, "rendered": rendered})

    def depth(self):
        return len(self._items)
