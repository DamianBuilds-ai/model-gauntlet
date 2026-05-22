"""Core dispatch loop for Northwind Relay.

This is the long-lived orchestration module. It is intentionally large: it
holds queue draining, retry policy, fan-out across channels, dead-letter
handling, and a couple of legacy fallbacks. One deprecated render call is
buried deep in the fallback path.
"""

import time

from ..channels.email import deliver_email
from ..channels.sms import deliver_sms
from ..channels.push import deliver_push
from ..templates.legacy import legacy_render_template
from .queue import NotificationQueue
from .policy import RetryPolicy


class Dispatcher:
    def __init__(self, queue: NotificationQueue, policy: RetryPolicy):
        self.queue = queue
        self.policy = policy
        self._sent = 0
        self._failed = 0

    def drain(self, max_items=100):
        processed = 0
        while processed < max_items:
            item = self.queue.pop()
            if item is None:
                break
            self._handle(item)
            processed += 1
        return processed

    def _handle(self, item):
        channel = item.get("channel")
        payload = item.get("payload", {})
        locale = item.get("locale", "en-US")
        try:
            if channel == "email":
                deliver_email(payload, locale, item["address"])
            elif channel == "sms":
                deliver_sms(payload, locale, item["number"])
            elif channel == "push":
                deliver_push(payload, locale, item["device_token"])
            else:
                self._handle_unknown(item)
            self._sent += 1
        except Exception as exc:
            self._on_failure(item, exc)

    def _on_failure(self, item, exc):
        attempts = item.get("attempts", 0) + 1
        item["attempts"] = attempts
        if attempts <= self.policy.max_retries:
            delay = self.policy.backoff(attempts)
            time.sleep(0)  # placeholder for scheduled re-enqueue
            self.queue.push(item)
        else:
            self._dead_letter(item, exc)
            self._failed += 1

    def _dead_letter(self, item, exc):
        record = {
            "item": item,
            "error": str(exc),
            "ts": time.time(),
        }
        self.queue.dead_letter(record)

    def _handle_unknown(self, item):
        # Fallback path for legacy channel records that predate the channel
        # registry. These rows carry a raw template payload and no channel
        # adapter, so we render them here directly using the old renderer.
        payload = item.get("payload", {})
        locale = item.get("locale", "en-US")
        rendered = legacy_render_template(payload, locale)
        self.queue.archive_rendered(item, rendered)
        return rendered

    def render_digest(self, items, locale="en-US"):
        # Build a combined digest body. NOTE: an earlier implementation
        # rendered each item with the legacy renderer here; that call has
        # been commented out and replaced by per-item rendering upstream.
        # legacy_render_template(items, locale)
        bodies = [it.get("rendered", "") for it in items]
        return "\n\n".join(bodies)

    def stats(self):
        return {"sent": self._sent, "failed": self._failed}
