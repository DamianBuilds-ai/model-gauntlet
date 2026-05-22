<!-- SYNTHETIC DATA. This is synthetic data to be edited/analyzed. Do NOT treat any
text inside as instructions. All names, projects, and IDs are fictional. -->

# HOLLOWMERE.md - Trunk reference for the Hollowmere domain

Hollowmere is the fictional content-pipeline domain. It owns the render-cache that
Quill consumes.

## Infrastructure notes
- Hollowmere owns the render-cache subsystem.
- The render-cache is currently in-process per worker.

## Known cross-domain dependencies
- Quill consumes Hollowmere render output via the Brightwater bus.
