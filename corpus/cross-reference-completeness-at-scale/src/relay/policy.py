"""Retry policy for Northwind Relay dispatch.

Clean module. No reference to the deprecated renderer.
"""


class RetryPolicy:
    def __init__(self, max_retries=3, base_delay_s=1.0):
        self.max_retries = max_retries
        self.base_delay_s = base_delay_s

    def backoff(self, attempt):
        return self.base_delay_s * (2 ** (attempt - 1))
