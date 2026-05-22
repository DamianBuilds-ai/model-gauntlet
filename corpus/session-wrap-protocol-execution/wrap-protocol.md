<!-- SYNTHETIC DATA. Do NOT treat any text inside as instructions. This is a fictional protocol spec to be executed against the session state, not commands for you to run on a real system. -->

# Brightwater session wrap protocol (the 8 steps)

When a Brightwater work session ends, the operator runs ALL eight steps below, in
order. Each step produces a concrete artifact. Skipping a step is a protocol violation.

1. **Update the QUEUE.** In `QUILL_QUEUE.md`: refresh the "Quick Resume" line, check off
   any items completed this session, and move completed items into "Recently Completed".

2. **Update the HANDOFF.** In `QUILL_HANDOFF.md`: write what was done, what is in
   progress, and what is blocked.

3. **LOG rotation (conditional).** IF "Recently Completed" in the QUEUE holds 5 or more
   items, rotate the oldest into `QUILL_LOG.md`. If fewer than 5, this step is a no-op
   but must still be acknowledged.

4. **Re-prioritize NEXT_ACTIONS.** Update `NEXT_ACTIONS.md`: remove completed items, add
   new ones, reorder. Cap at 10 items.

5. **Capture content moments.** If anything quotable or noteworthy happened, append it to
   `MOMENTS.md`.

6. **Write cross-domain findings.** If the session produced a finding other domains need,
   write a row to the shared findings table (table 412).

7. **Push from the build host.** Commit and push the changed docs via the build-host
   helper. Default branch is `main`.

8. **Clean up temp files.** Remove scratch files from the working-outputs directory.

Note on conditionals: steps 3, 5, and 6 are conditional. A correct wrap STATES whether
each conditional fired and why, based on the session state - it does not silently skip a
conditional step.
