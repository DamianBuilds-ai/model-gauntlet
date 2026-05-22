---
task_category: api-usage-correctness
prompt_under_test: |
  You are given the complete reference for a Python SDK at
  corpus/api-usage-correctness/pulsedeck-sdk-docs.md. Pulsedeck is a feature-flag service.
  The documented surface in that file is the ENTIRE public API - any class, method,
  parameter, or error type not in the docs does not exist.

  Using ONLY the documented API, write a single Python function:

      def get_checkout_config(api_key: str) -> dict:

  that does the following:
    1. Opens an authenticated Pulsedeck session for the "production" environment using the
       given api_key, and guarantees the session is released (closed) before the function
       returns, whether it succeeds or fails.
    2. Reads two flags and returns them in a dict:
         - "new_checkout" : the boolean flag with key "new-checkout-flow". If that flag
           does not exist, it must DEFAULT to False rather than raising.
         - "checkout_theme" : the string value of the flag with key "checkout-theme". This
           flag is required - if it is missing, the function must let that condition
           surface as the documented not-found error (do not invent a default for it).
       Return {"new_checkout": <bool>, "checkout_theme": <str>}.
    3. Handle the documented error cases correctly:
         - If authentication fails (bad key, or a read attempted before a successful
           connect), let the documented auth error propagate.
         - If the service is unreachable, let the documented connection error propagate.
         - If a read is rate-limited, wait the documented number of seconds the error tells
           you to wait, then retry the read ONCE; if it is rate-limited again, let the
           error propagate.
    4. Do NOT call any method, constructor parameter, or error type that is not in the
       docs. Do not invent auth/login/refresh methods, do not invent flag-read methods
       beyond the documented ones, and do not catch or raise error types the docs do not
       define.
  Briefly note which documented behaviours drove your error-handling choices. Output
  envelope required (schemaVersion, tier, status, tool_budget_used). No em dashes (spaced
  hyphens). No emojis.
variant_pool: 9
corpus: corpus/api-usage-correctness/pulsedeck-sdk-docs.md
corpus_intent: |
  One self-consistent fictional SDK reference (one client class, three flag-read methods
  plus connect/close, a two-step auth flow, four documented error types), plus a concrete
  task that exercises auth, two different read methods with different missing-flag
  semantics, rate-limit backoff, and guaranteed cleanup. Quality here is correctness-first
  (no-wrong-answers): code that calls a plausible-but-nonexistent method (a hallucinated
  client.authenticate(), client.get_flag(), or a made-up PulsedeckTimeoutError) is WORSE
  than code that is incomplete but uses only the real surface - because the hallucinated
  call looks idiomatic and would import-error or attribute-error at runtime, and a reader
  skimming the code would believe it works against the documented SDK when it cannot. The
  traps a weaker model can be CONFIDENTLY WRONG on (drawn from idioms of OTHER real SDKs,
  which the docs explicitly forbid): (a) calling a nonexistent auth method like
  client.authenticate() / client.login() / client.refresh_token() instead of the
  documented connect() - the docs say auth is connect() only; (b) using a nonexistent
  generic read like client.get_flag() / client.get_bool() / client.get_string() /
  client.evaluate() instead of the documented is_enabled / get_value / get_all; (c)
  passing a default to get_value() (the docs state ONLY is_enabled has a default; get_value
  always raises on a missing flag) - so applying a default to checkout-theme is wrong; (d)
  catching or raising a nonexistent error type such as PulsedeckTimeoutError /
  PulsedeckValidationError / PulsedeckPermissionError, or assuming construction raises a
  Pulsedeck error when the docs say bad args raise the built-in ValueError; (e) doing the
  rate-limit backoff wrong - inventing a client.set_retry_policy() or a built-in auto-retry
  when the docs say retry is caller-side via the error's .retry_after attribute; (f)
  forgetting guaranteed cleanup - the session must be closed on every path (a try/finally
  or the documented context-manager protocol). A confident wrong answer ships code that
  reads naturally and mirrors a popular real SDK but invokes the documented SDK's ghosts -
  that is the differentiator, not code that merely omits an error branch.
notes: |
  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a subtly-wrong-but-plausible
  use of the SDK that calls something not in the docs is WORSE than incomplete-but-honest
  code that touches only the documented surface. Code that uses connect()/is_enabled with
  default/get_value/close correctly and handles the four real errors is correct; code that
  calls a slick client.authenticate() or catches PulsedeckTimeoutError has produced output
  a reader would trust against this SDK even though it would fail at import/attribute
  resolution. Reward documented-only usage. Penalise the hallucinated-method/ghost-error
  answer hardest.

  NEW task type. Tests grounded API usage against a closed, fully-documented fictional
  surface - the differentiation is whether a model writes ONLY what the docs permit while
  the muscle memory of popular real SDKs (auth via authenticate/login, generic get_flag
  reads, defaults on every getter, an auto-retry policy) actively pulls it toward
  plausible ghosts. Single source doc.

  ANSWER KEY (for the scoring Architect):

  WHAT A CORRECT SOLUTION DOES (a reference shape - variants need not match line-for-line,
  but must use only these documented calls):
    - Constructs PulsedeckClient(api_key, environment="production") (or relies on the
      default, which is "production" - either is fine).
    - Opens the session via client.connect() OR via the documented context-manager
      protocol (with PulsedeckClient(api_key) as client: ...). Both are documented and
      correct. If using connect() directly, cleanup must be guaranteed via try/finally
      calling client.close(). If using the context manager, cleanup is automatic and
      acceptable (close() is documented safe to call more than once and never raises).
    - Reads "new-checkout-flow" via client.is_enabled("new-checkout-flow", default=False)
      - the default MUST be passed so a missing flag returns False instead of raising
      PulsedeckNotFoundError. (Passing default as a keyword matches the documented
      signature is_enabled(flag_key, default=False).)
    - Reads "checkout-theme" via client.get_value("checkout-theme") with NO default - the
      docs state get_value has no default param and always raises PulsedeckNotFoundError on
      a missing flag, and the task says to let that surface. So the not-found error for
      checkout-theme is allowed to propagate (NOT caught-and-defaulted).
    - Returns {"new_checkout": <bool>, "checkout_theme": <str>}.
    - Error handling: PulsedeckAuthError and PulsedeckConnectionError propagate (the task
      says let them surface; catching and swallowing them is wrong). PulsedeckRateLimitError
      on a read is caught, the code reads err.retry_after, sleeps that many seconds (e.g.
      time.sleep(err.retry_after)), retries the read ONCE, and if it raises
      PulsedeckRateLimitError again lets it propagate. Construction-arg errors (bad
      environment) surface as the built-in ValueError - NOT a Pulsedeck error.
    - Imports only the documented names: PulsedeckClient and the four error types from
      pulsedeck.errors (only the ones it actually uses need importing).

  THE HALLUCINATION TRAPS (hard-fail eligible - any of these is a Hallucination=1, because
  the docs explicitly enumerate the full surface and list these as non-features):
    - Calling client.authenticate(), client.login(), or client.refresh_token() (auth is
      connect() only).
    - Calling client.get_flag(), client.get_bool(), client.get_string(), client.fetch(),
      or client.evaluate() (the only reads are is_enabled / get_value / get_all).
    - Passing a default to get_value() or get_all() (only is_enabled has default).
    - Catching or raising PulsedeckTimeoutError, PulsedeckValidationError,
      PulsedeckPermissionError, or any error type not in the documented set of four.
    - Inventing client.set_retry_policy() or assuming a built-in auto-retry instead of
      caller-side backoff via .retry_after.
    - Assuming construction contacts the server or raises a Pulsedeck auth error at
      construction (the docs say construction is local-only and bad args raise ValueError).

  Scoring guidance:
    - Correctness (hard-fail eligible) = does the code accomplish the task using the real
      semantics: default on is_enabled, no default on get_value, single rate-limit retry
      via .retry_after, guaranteed close on every path, correct return dict shape. Wrong
      missing-flag semantics (defaulting checkout-theme, or NOT defaulting new-checkout) is
      a Correctness miss. Swallowing the auth/connection errors the task says to propagate
      is a Correctness miss.
    - Hallucination (hard-fail eligible) = ANY ghost method, ghost error type, ghost
      parameter, or ghost retry API from the trap list above. This is the headline
      differentiator for this eval - a single hallucinated call scores Hallucination = 1
      and eliminates the variant, no matter how clean the rest looks.
    - Reasoning quality = the brief note on which documented behaviours drove the
      error-handling choices (why connect() before reads, why default only on is_enabled,
      why caller-side backoff). A model that explains the missing-flag asymmetry and the
      caller-side-retry rule shows real grounding.
    - Completeness = both flags read, both error categories handled, cleanup guaranteed,
      return shape correct.
    - Scope discipline = did it stay within the documented API and the requested function,
      without adding unrequested features (logging, metrics, an async version, a class
      wrapper) the SDK does not support and the task did not ask for.
    - Format adherence = a single coherent function plus the required envelope. Source
      transparency applies weakly (single source doc). Voice match does NOT apply.
      Helpfulness / Discipline do NOT apply (this is not a judgment task).
---

# Spec 21 - api-usage-correctness (closed fictional SDK, no hallucinated calls)

Write one Python function against a closed, fully-documented FICTIONAL SDK at
`corpus/api-usage-correctness/pulsedeck-sdk-docs.md` (Pulsedeck, a feature-flag service:
one client class, three flag-read methods plus connect/close, a two-step auth flow, four
documented error types). The function must open an authenticated session, read a boolean
flag with a documented default and a required string flag without one, handle the
documented auth / connection / rate-limit error cases (caller-side backoff via
`.retry_after`, retry once), guarantee session cleanup on every path, and use ONLY the
documented surface.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is the heart of this eval: code that uses only the
real documented calls is correct, while code that reaches for a plausible-but-nonexistent
method or error type (mirroring popular real SDKs - an `authenticate()` call, a generic
`get_flag()`, a `PulsedeckTimeoutError`, an auto-retry policy) has produced output a
reader would trust against this SDK even though it would fail at import or attribute
resolution - which is worse than code that simply omits a branch. The docs explicitly
enumerate the full surface and list the ghosts as non-features, so a weaker model pulled
by other-SDK muscle memory can be confidently wrong. Hallucination (no ghost methods,
parameters, or error types) is the headline, hard-fail-eligible differentiator, with
Correctness (the missing-flag asymmetry, the single caller-side retry, guaranteed cleanup)
co-load-bearing. Voice match does not apply. The corpus is the single SDK reference file.
