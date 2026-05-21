# Synthetic codebase for the codebase-qa eval (file 3 of 3). The worker.

class Worker:
    def __init__(self, store):
        self.store = store

    def run_once(self):
        job = self.store.next_job()
        if job is None:
            return
        try:
            self._handle(job)
        except Exception:
            # On any handler error, hand the job back to the store, which decides
            # whether to retry based on max_retries.
            self.store.fail(job)

    def _handle(self, job):
        if job.kind == "send-email":
            send_email(job.payload)
        elif job.kind == "resize-image":
            resize_image(job.payload)
        else:
            raise ValueError("unknown job kind: " + job.kind)


def send_email(payload):
    # Pretend to send. Synthetic stub.
    return True


def resize_image(payload):
    # Pretend to resize. Synthetic stub.
    return True
