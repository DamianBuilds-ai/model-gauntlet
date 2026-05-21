# Synthetic codebase for the codebase-qa eval (file 2 of 3). The queue store.

class Job:
    def __init__(self, kind, payload):
        self.kind = kind
        self.payload = payload
        self.attempts = 0


class QueueStore:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries
        self._jobs = []

    def enqueue(self, kind, payload):
        self._jobs.append(Job(kind, payload))

    def next_job(self):
        if not self._jobs:
            return None
        return self._jobs.pop(0)

    def fail(self, job):
        # Re-enqueue the job for retry unless it has exhausted max_retries.
        job.attempts += 1
        if job.attempts < self.max_retries:
            self._jobs.append(job)
        # else: dropped silently. (Note: no dead-letter queue exists.)
