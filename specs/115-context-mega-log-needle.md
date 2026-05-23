---
task_category: context-mega-log-needle
prompt_under_test: |
  You are given a single very large log file at
  corpus/context-mega-log-needle/service.log - approximately 300,000 tokens of
  structured request logs from a fictional API gateway called "Helix Routing
  Service" over a 24-hour window. Each line is one log record with a timestamp,
  level, request_id, route, upstream, http_status, latency, and status. Read the
  whole file.

  Somewhere in that log, ONE specific request_id misbehaves. The bug is subtle:
  the same request is logged with contradictory final outcomes by different
  components of the system. Find it.

  Answer ALL of the following, drawing ONLY on lines that appear in the log:

    (a) Which request_id is the anomalous one?
    (b) How many distinct log lines mention that request_id, and what are the
        timestamps of those lines (in the order they appear in the file)?
    (c) For each occurrence: in one sentence, state what the line records
        (forwarded, failed, succeeded, etc.) and quote the line verbatim so the
        source is verifiable.
    (d) The bug itself: explain in two to four sentences WHY this request_id is
        anomalous - what is the contradiction across the occurrences, which
        component recorded the contradictory event, and what is the operational
        consequence (i.e. what masks what).

  Do NOT scan only for ERROR lines and stop. The contradicting event is logged at
  INFO level by a downstream worker; a model that finds the start and the
  failure but misses the later mis-acknowledgement is wrong on (b), (c), and
  (d). If you cannot find all occurrences, say so honestly - do NOT guess.

  After your answer, append the required output envelope (schemaVersion, tier,
  status, tool_budget_used) as separate lines. No em dashes (use spaced
  hyphens). No emojis.
variant_pool: 9
corpus: corpus/context-mega-log-needle/
corpus_intent: |
  GENERATED CORPUS. corpus/context-mega-log-needle/service.log is produced
  deterministically by corpus/context-mega-log-needle/generate.py (seed=115). The
  file is ~1,200,000 chars (~300,000 tokens at ~4 chars/token), a fictional Helix
  Routing Service log of structured request lines. To regenerate byte-identically:
  cd into the corpus dir and run `python3 generate.py`. The script asserts the
  anomalous request_id appears EXACTLY 3 times and that each of the three
  distinguishing event substrings appears exactly once.

  WHAT THIS EVAL PROBES: very-long-context (~300k token) anomaly detection where
  the discriminating event is NOT the obvious failure but a later INFO-level
  mis-acknowledgement that contradicts the failure. A model that scans for ERROR
  lines and stops will catch the failure (event B) and miss the silent success-ack
  (event C). The eval tests whether the model reads the full window AND notices
  the contradiction, not just the loudest signal. This is the >300k-token gap on
  the gauntlet map beyond the 220k eval 75 and the 200k eval 14.

  QUALITY PRINCIPLE (full-recall + contradiction detection at extreme distance):
  the anomaly is not that a request failed (failures happen and are normal noise
  in the log). The anomaly is that a downstream audit-replay worker LATER recorded
  the same failed request as a SUCCESSFUL completion, silently masking the failure
  from any downstream consumer that trusts the audit log. A correct answer
  identifies all three occurrences AND identifies that the third (the success-ack)
  contradicts the second (the failure). A model that returns 2 of 3 events and
  declares the request "failed" - missing the mis-ack - has missed the bug
  entirely, even though both lines it found are real and quoted correctly. A
  model that fabricates a fourth occurrence or invents a retry-success line that
  is not in the file is confidently wrong.

  ANSWER KEY (the scoring Architect verifies by grep):
    The anomalous request_id is `req-7f3a91c4d0b2e` (this exact string).
    It appears EXACTLY 3 times in the file.

    Event A - START (at ~22% of file)
      Timestamp: 2026-04-01T02:14:08.122Z
      Level: INFO
      Verbatim signature: contains `forwarded_to=ledger-write attempt=1 status=forwarded`
      Meaning: the gateway accepted the request and forwarded it upstream to
      ledger-write on the first attempt.

    Event B - FAILURE (at ~48% of file)
      Timestamp: 2026-04-01T09:47:33.401Z
      Level: ERROR
      Verbatim signature: contains `http_status=500 ... status=failed retry_count=2`
      and the message `upstream returned 500 after 2 retries`.
      Meaning: the upstream ledger-write service returned HTTP 500 twice; the
      gateway marked the request failed and scheduled no further retry.

    Event C - MIS-ACKNOWLEDGEMENT (at ~81% of file) - THE LOAD-BEARING NEEDLE
      Timestamp: 2026-04-01T18:22:51.077Z
      Level: INFO
      Worker: audit-replay
      Verbatim signature: contains `worker=audit-replay ... status=success result=ok`
      and the message `treating absence-of-retry as completion; logged as successful`.
      Meaning: the audit-replay worker re-read the request, found no retry record,
      and (incorrectly) treated absence-of-retry as completion - logging the request
      as successful and masking the upstream failure.

    The bug: Event C contradicts Event B. The audit-replay worker treats
    absence-of-retry as success, which silently masks the real failure - any
    downstream consumer that trusts the audit log sees this request as completed
    successfully even though it never was.

  GREP-VERIFIABLE INVARIANTS (against the corpus and the model output):
    - In the corpus: `grep -c "req-7f3a91c4d0b2e" service.log` == 3.
    - `grep -c "forwarded_to=ledger-write attempt=1 status=forwarded" service.log` == 1.
    - `grep -c "upstream returned 500 after 2 retries" service.log` == 1.
    - `grep -c "treating absence-of-retry as completion" service.log` == 1.
    - A CORRECT model output contains the string `req-7f3a91c4d0b2e` (the anomalous
      id), all three timestamps (`02:14:08.122`, `09:47:33.401`, `18:22:51.077`),
      AND explicitly identifies the contradiction (event C masks event B; the
      audit-replay worker mis-acknowledged a failed request as successful).
    - A WRONG output identifies only 2 of 3 events (typically A and B, missing C),
      or names a different request_id, or invents a fourth event not in the log,
      or fails to flag that C contradicts B.

  Scoring guidance:
    - Correctness (hard-fail eligible) = correct request_id AND all three
      occurrences identified AND the contradiction (C masks B) named. Missing
      event C is Correctness=1 - the bug was missed even if the two found events
      were quoted accurately.
    - Completeness = all four answer parts (a)(b)(c)(d) addressed; all three
      occurrences listed with timestamps and verbatim quotes.
    - Hallucination (hard-fail eligible) = inventing a fourth occurrence, naming
      a request_id that does not appear three times, or asserting a line exists
      when it does not.
    - Discipline = answered ONLY from the log; honestly flagged any occurrence
      not found rather than guessing; did not stop scanning at the first ERROR.
    - Source transparency (load-bearing) = each occurrence quoted verbatim so
      recall is independently verifiable.
    - Reasoning quality = correctly diagnosed WHY C is the bug (it is an
      INFO-level mis-acknowledgement that masks a real failure; the contradiction
      is not the failure itself but the later success-ack of the failed request).
    Voice match does NOT apply.
notes: |
  Chat C gap-filler: the >300k-token long-context anomaly-detection dimension
  beyond eval 75 (220k) and eval 14 (sub-100k). The corpus is GENERATED (not
  hand-written) by a deterministic seeded Python script
  (corpus/context-mega-log-needle/generate.py, seed=115) that emits ~1,200,000
  chars (~300k tokens) of structured log lines and plants one specific request_id
  three times at ~22%, ~48%, ~81% of the file. The three events are: gateway
  accepts and forwards (INFO), upstream returns 500 and request is marked failed
  (ERROR), then later a downstream audit-replay worker mis-acknowledges the same
  request as successful (INFO). Regenerate byte-identically with `python3
  generate.py` in the corpus dir.

  The probe is recall-at-extreme-distance combined with contradiction detection:
  finding the failure is the obvious half (ERROR lines stand out); finding the
  later INFO success-ack that masks the failure is the discriminator. A weak
  model that scans only for ERROR lines and stops will return event B and miss
  the bug. The answer key names the request_id (req-7f3a91c4d0b2e), the three
  exact timestamps, and the contradicting verbatim quotes for the scoring
  Architect to grep against. Correctness and Hallucination are hard-fail
  eligible; source transparency (quoting each occurrence) is load-bearing.
  Reasoning quality is heavily weighted - the model must explicitly name that
  event C contradicts event B and that audit-replay is the bug location, not
  just list the three lines. Standard four-phase /eval-pit flow against the
  frozen rubric/rubric.md. The variant pool is 9 (3 models x N=3, effort inert
  per the methodology). The corpus is the directory corpus/context-mega-log-needle/.
---

# Spec 115 - context-mega-log-needle (the >300k-token anomaly-in-noise probe)

Hand a model a ~300,000-token synthetic API-gateway log and ask it to find the
one request_id whose three log lines tell a contradictory story across the full
window. The bug is not the failure (failures are normal noise) - it is a later
INFO-level mis-acknowledgement by a downstream worker that silently records the
failed request as successful. This fills the >300k-token blank on the gauntlet
map: eval 75 stops at ~220k tokens; eval 14 stops well under 100k.

The corpus is GENERATED, not hand-written.
`corpus/context-mega-log-needle/generate.py` (seed=115) emits `service.log`
(~1,200,000 chars, ~300k tokens) deterministically - re-running it produces
byte-identical output, and it asserts the anomalous request_id appears exactly
three times and that each of the three event signatures appears exactly once.
The three events are planted at roughly 22%, 48%, and 81% of the file: (A) the
gateway forwards the request, (B) the upstream returns HTTP 500 and the
request is marked failed, then (C) a downstream audit-replay worker
mis-acknowledges the same request as successful by treating
absence-of-retry-record as completion.

The discriminator is full recall at extreme distance combined with
contradiction detection. A model that scans for ERROR lines and stops will
catch event B and miss event C - and therefore miss the bug entirely. A model
that returns events A and B and declares the request "failed" has found the
loudest signal but missed the actual anomaly. The correct answer names all
three occurrences AND explains that the third contradicts the second - the
audit-replay worker silently masks the upstream failure. Each occurrence must
be quoted verbatim so the recall is independently verifiable.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`.
Correctness and Hallucination are hard-fail eligible; source transparency
(quoting each occurrence) is load-bearing; reasoning quality is heavily
weighted because the bug is the contradiction across occurrences, not the
existence of any single one. Voice match does not apply. The variant pool is
9 (3 models x N=3, effort inert per the methodology). The corpus is the
directory `corpus/context-mega-log-needle/`.
