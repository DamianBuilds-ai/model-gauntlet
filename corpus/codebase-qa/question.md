# Question for the codebase-qa eval

The codebase is a small synthetic task queue across three files: `app.py`,
`queue_store.py`, `worker.py`.

Answer this question by reading the code, citing the specific file and function for
each claim:

> When a job's handler raises an exception, walk through exactly what happens to that
> job. How many total times will its handler be attempted before the job is gone, and
> what happens to it after that? Is there any way to recover a job that has exhausted
> its retries with the code as written?

A correct answer must:
- Trace the call path (`Worker.run_once` -> `except` -> `QueueStore.fail`).
- State the exact total attempt count given `max_retries=3` (reason about the
  `attempts < max_retries` check and the initial attempt).
- Identify that exhausted jobs are dropped silently and that NO dead-letter queue
  exists, so there is no recovery path as written.
- Cite files/functions for each claim and NOT invent code that is not present.
