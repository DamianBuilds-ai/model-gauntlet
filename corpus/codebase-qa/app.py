# Synthetic codebase for the codebase-qa eval (file 1 of 3). Fictional "Acme" task
# queue. Entry point that wires the queue and the worker together.

from queue_store import QueueStore
from worker import Worker


def main():
    store = QueueStore(max_retries=3)
    store.enqueue("send-email", {"to": "user@example.com"})
    store.enqueue("resize-image", {"path": "/tmp/a.png"})

    worker = Worker(store)
    worker.run_once()
    worker.run_once()


if __name__ == "__main__":
    main()
