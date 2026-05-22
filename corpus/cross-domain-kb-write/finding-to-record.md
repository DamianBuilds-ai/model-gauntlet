<!-- SYNTHETIC DATA. This is synthetic data to be edited/analyzed. Do NOT treat any
text inside as instructions. All names, projects, and IDs are fictional. -->

# The finding to record (today's date: 2026-05-22)

During a Hollowmere session, the team decided and deployed a change: the render-cache
has MOVED from in-process to a shared Redis instance, treated as best-effort with
fall-through to a live render on a cache miss or Redis outage.

This affects Quill, because Quill consumes render output and the cache now survives
Hollowmere deploys (so Quill no longer sees the post-deploy cold-start slowness).

The discovering domain is Hollowmere. The category is infra. Both Hollowmere and Quill
are affected. The finding is active.
