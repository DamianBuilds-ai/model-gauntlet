# Pulsedeck Python SDK - Reference (v2)

Synthetic corpus for the api-usage-correctness eval. Pulsedeck is a FICTIONAL feature-
flag and remote-config service; this is its complete, self-consistent Python SDK
reference. There is no real Pulsedeck. The documented surface below is the ENTIRE public
API - any class, method, parameter, or error type not listed here does not exist. A
correct solution uses ONLY what is documented here. All identifiers are fictional.

---

## Installation and import

```python
from pulsedeck import PulsedeckClient
from pulsedeck.errors import (
    PulsedeckAuthError,
    PulsedeckNotFoundError,
    PulsedeckRateLimitError,
    PulsedeckConnectionError,
)
```

That is the full set of importable names: one client class and four error types. There
are no other public classes, helpers, or submodules.

---

## Authentication flow

Pulsedeck uses a two-step auth handshake. You construct the client with an API key, then
explicitly open a session before making any flag calls.

1. Construct `PulsedeckClient(api_key, environment="production")`.
   - `api_key` (str, required): your project API key.
   - `environment` (str, optional, default "production"): one of "production",
     "staging", or "development". Any other value raises `ValueError` at construction.
   - Construction does NOT contact the server. It only validates arguments locally.

2. Call `client.connect()` to open an authenticated session.
   - `connect()` performs the network handshake and exchanges the API key for a session.
   - Returns `None` on success.
   - Raises `PulsedeckAuthError` if the API key is rejected.
   - Raises `PulsedeckConnectionError` if the service is unreachable.
   - You MUST call `connect()` successfully before calling any flag-read method. Calling a
     flag-read method before a successful `connect()` raises `PulsedeckAuthError`.

3. When finished, call `client.close()` to release the session.
   - `close()` returns `None`. It is safe to call more than once. It never raises.

The client also supports the context-manager protocol: using
`with PulsedeckClient(api_key) as client:` calls `connect()` on enter and `close()` on
exit automatically. Inside the `with` block the session is already open.

---

## `PulsedeckClient` methods

Beyond `connect()` and `close()` above, the client exposes exactly these flag-read
methods. No others exist.

### `client.is_enabled(flag_key, default=False) -> bool`

Returns whether a boolean flag is enabled.

- `flag_key` (str, required): the flag identifier.
- `default` (bool, optional, default False): the value to return if the flag is not found
  (see error semantics below).
- Returns a `bool`.
- Raises `PulsedeckNotFoundError` ONLY if `flag_key` does not exist AND no `default` was
  provided as a keyword. If `default` is provided, a missing flag returns `default`
  instead of raising.
- Raises `PulsedeckRateLimitError` if the per-minute read quota is exceeded.
- Raises `PulsedeckAuthError` if called before a successful `connect()`.

### `client.get_value(flag_key) -> str`

Returns the string value of a multivariate (string-valued) flag.

- `flag_key` (str, required): the flag identifier.
- Returns a `str`.
- There is NO default parameter on `get_value`. A missing flag ALWAYS raises
  `PulsedeckNotFoundError`.
- Raises `PulsedeckRateLimitError` if the per-minute read quota is exceeded.
- Raises `PulsedeckAuthError` if called before a successful `connect()`.

### `client.get_all() -> dict`

Returns a dict of every flag the current session can see, mapping `flag_key` (str) to its
current value. Boolean flags map to `bool`, string flags map to `str`.

- Takes no arguments.
- Returns a `dict`.
- Raises `PulsedeckRateLimitError` if the per-minute read quota is exceeded.
- Raises `PulsedeckAuthError` if called before a successful `connect()`.

---

## Error types (the complete set - four)

All four live in `pulsedeck.errors` and all subclass a common base `PulsedeckError`
(also in `pulsedeck.errors`, but you rarely catch the base directly).

- `PulsedeckAuthError` - the API key was rejected, OR a flag-read method was called before
  a successful `connect()`.
- `PulsedeckNotFoundError` - a requested `flag_key` does not exist (subject to the
  `default` semantics on `is_enabled`).
- `PulsedeckRateLimitError` - the per-minute read quota was exceeded. This error exposes
  one attribute, `.retry_after` (an int number of seconds to wait before retrying).
- `PulsedeckConnectionError` - the service could not be reached (network failure or
  timeout during `connect()` or a read).

There are no other error types. There is no "PulsedeckTimeoutError", no
"PulsedeckValidationError", no "PulsedeckPermissionError" - those do not exist. Argument
validation at construction raises the built-in `ValueError`, not a Pulsedeck error.

---

## Rate-limit guidance (documented behaviour)

When a read raises `PulsedeckRateLimitError`, the correct handling is to read its
`.retry_after` attribute and wait that many seconds before retrying. There is no
auto-retry built into the SDK - the caller is responsible for backoff. There is no
`client.set_retry_policy()` or similar; retry is entirely caller-side.

---

## What the SDK does NOT have (explicit non-features)

To be unambiguous, the following do NOT exist in this SDK. Using any of them is a usage
error:

- No `client.authenticate()`, `client.login()`, or `client.refresh_token()` - auth is
  `connect()` only.
- No `client.get_flag()`, `client.get_bool()`, `client.get_string()`,
  `client.fetch()`, or `client.evaluate()` - the only reads are `is_enabled`,
  `get_value`, and `get_all`.
- No async variant, no `await` API, no `PulsedeckAsyncClient`.
- No `default` parameter on `get_value` or `get_all` (only `is_enabled` has `default`).
- No batch/bulk read method beyond `get_all()`.
