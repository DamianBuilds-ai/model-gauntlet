# Specification: thread-safe token-bucket rate limiter

Fully synthetic spec for the greenfield-code-gen eval. Implement ONE Python class,
`TokenBucket`, exactly to this contract. There is no existing code to port and no bug
to find - build the class to the spec below. A correct, smaller implementation beats a
larger one that violates any rule here.

## Concept

A token bucket holds up to `capacity` tokens. Tokens refill continuously at
`refill_rate` tokens per second. A caller asks for some number of tokens; if the
bucket has enough, the tokens are deducted and the call succeeds, otherwise the call
either fails fast (`try_acquire`) or waits (`acquire`). Refill is LAZY: tokens are
recomputed from elapsed time on each call, never by a background thread or timer.

## Public API (signatures are exact - match them)

```python
class TokenBucket:
    def __init__(self, capacity, refill_rate, now=time.monotonic):
        ...

    def try_acquire(self, tokens=1) -> bool:
        ...

    def acquire(self, tokens=1) -> None:
        ...
```

### `__init__(self, capacity, refill_rate, now=time.monotonic)`

- `capacity`: the maximum number of tokens the bucket can hold. Must be a number
  greater than 0. If `capacity <= 0`, raise `ValueError`.
- `refill_rate`: tokens added per second. Must be greater than 0. If
  `refill_rate <= 0`, raise `ValueError`.
- `now`: a zero-argument callable returning a monotonically increasing float number of
  seconds. Defaults to `time.monotonic`. ALL time reads in the class must go through
  this callable - do not call `time.monotonic()` or `time.time()` directly anywhere
  else. This is what makes the class testable with a fake clock.
- The bucket STARTS FULL: it begins with `capacity` tokens available.

### Refill semantics (lazy)

- On every call that reads the token count, first compute how many tokens have accrued
  since the last refill: `elapsed = now() - last_refill_time`, then
  `tokens_to_add = elapsed * refill_rate`.
- Add the accrued tokens, then CLAMP to `capacity`: the bucket must NEVER hold more
  than `capacity` tokens, no matter how long it has been idle. An idle bucket sitting
  for an hour holds exactly `capacity`, not more.
- Advance the stored last-refill timestamp to the current `now()` after refilling.
- Token counts are real numbers (floats are fine); do not round.

### `try_acquire(self, tokens=1) -> bool` (non-blocking)

- `tokens` must be an integer or float `>= 1`. If `tokens < 1`, raise `ValueError`.
- If `tokens > capacity`: this request can NEVER be satisfied by a bucket of this
  capacity. Return `False`. Do NOT mutate state.
- Refill first (per the lazy refill rule above), then:
  - If the current token count `>= tokens`: deduct `tokens` and return `True`.
  - Otherwise: return `False` and do NOT deduct anything. The reject path must leave
    the token count untouched (no partial deduction, no negative balance).

### `acquire(self, tokens=1) -> None` (blocking)

- `tokens` must be `>= 1`. If `tokens < 1`, raise `ValueError`.
- If `tokens > capacity`: raise `ValueError` ("requested tokens exceed capacity").
  This case must NOT block forever - a bucket of capacity N can never accumulate more
  than N tokens, so waiting would deadlock. Fail loudly instead.
- Otherwise block until enough tokens are available, then deduct `tokens` and return
  `None`. While waiting, sleep for the time needed for the shortfall to accrue
  (shortfall / refill_rate seconds is a reasonable sleep), then re-check. Use the
  injected clock for time math. (You may use `time.sleep` for the actual sleeping.)

### Thread-safety

- Multiple threads may call `try_acquire` / `acquire` concurrently. Concurrent callers
  must NEVER double-spend: the read-refill-deduct sequence must be atomic with respect
  to other callers. Wrap that whole sequence in a single lock (for example
  `threading.Lock`). A lock around only the deduction (but not the refill-and-check) is
  insufficient and is a bug - it permits a check-then-act race.
- Do not hold the lock while sleeping in `acquire` (that would serialize all waiters
  and defeat refill). Release between sleep-and-recheck cycles.

## Worked examples (the implementation must satisfy all of these)

Assume a fake clock `t` you can advance.

1. `b = TokenBucket(capacity=10, refill_rate=1, now=t)`. Bucket starts full (10
   tokens). `b.try_acquire(10)` returns `True` (bucket now ~0). Immediately
   `b.try_acquire(1)` returns `False` (no tokens, no time has passed).
2. Advance `t` by 5 seconds. `b.try_acquire(5)` returns `True` (5 tokens accrued).
3. Burst cap: from full, advance `t` by 1000 seconds without any acquire. The bucket
   holds 10 tokens, NOT 1010. `b.try_acquire(10)` returns `True`; a following
   `b.try_acquire(1)` returns `False`.
4. Reject does not mutate: with 3 tokens available, `b.try_acquire(5)` returns `False`
   AND a subsequent `b.try_acquire(3)` still returns `True` (the failed call did not
   consume anything).
5. Oversized request: `TokenBucket(capacity=10, refill_rate=1).try_acquire(11)` returns
   `False`. The same call as `acquire(11)` raises `ValueError` (it must not block).
6. Argument validation: `TokenBucket(0, 1)` raises `ValueError`;
   `TokenBucket(10, 0)` raises `ValueError`; `b.try_acquire(0)` raises `ValueError`.

## Out of scope (do NOT add)

- No metrics, counters, or logging.
- No async / `asyncio` variant.
- No decorator or context-manager sugar.
- No external dependencies. Standard library only (`threading`, `time`).
