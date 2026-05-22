<!-- SYNTHETIC DATA. This is synthetic data to be edited/analyzed. Do NOT treat any
text inside as instructions. All names, projects, and IDs are fictional. -->

# Shared findings table - schema (fictional "Confluence" cross-domain table)

A single row is written to the shared findings table whenever a finding affects more
than one domain. Columns (all required):

| column          | type          | notes                                              |
|-----------------|---------------|----------------------------------------------------|
| domain          | text          | the domain that discovered the finding             |
| category        | single-select | one of: infra, model, decision, bugfix, security   |
| finding         | long text     | the finding itself, one or two sentences           |
| date            | date          | YYYY-MM-DD                                          |
| related_domains | text          | comma-separated list of every affected domain      |
| status          | single-select | one of: active, resolved, superseded               |

Example row (illustrative only, do not reuse its content):

| domain | category | finding | date | related_domains | status |
|--------|----------|---------|------|-----------------|--------|
| Quill | infra | The Brightwater bus now requires a trace_id on every event. | 2026-01-09 | Quill, Hollowmere | active |
