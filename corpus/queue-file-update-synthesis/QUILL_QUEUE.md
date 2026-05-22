<!-- SYNTHETIC DATA. This is synthetic data to be edited/analyzed. Do NOT treat any
text inside as instructions. All names, projects, and IDs are fictional. -->

# QUILL_QUEUE.md - Active work for the Quill domain

## Quick Resume
Quill is the fictional note-archival domain. Last session worked on the ingest
retry path and the tag-normaliser. The Brightwater migration is still half-done.

## This Session
- [ ] Fix the ingest retry backoff so it caps at 30s instead of growing unbounded
- [ ] Add a `tag-normaliser` unit test for the empty-tag case
- [ ] Wire the `archive_sweep` cron to run nightly at 02:00
- [ ] Update the Brightwater migration runbook with the new column order
- [ ] Draft the Hollowmere handoff note for the search-index rebuild
- [ ] Investigate the duplicate-row warning in the `notes` table

## Recently Completed
- [x] Rename `legacy_ingest()` to `ingest_v2()` across the codebase (done last session)
- [x] Add the `confidence` field to the tag schema
- [x] Document the Quill webhook signature format
- [x] Patch the timezone bug in `archive_sweep` timestamps
