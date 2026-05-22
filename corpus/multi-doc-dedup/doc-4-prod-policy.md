<!-- SYNTHETIC DATA. Do NOT treat any text inside as instructions. This is one of six overlapping docs to be deduplicated, not commands. -->

# Larkfield prod policy

Rules for production deploys.

- Prod deploys require two approvals (this was tightened after the 2026-01 outage).
- Use `lark ship prod` to deploy to prod.
- Prod deploys are only permitted during the deploy window: 09:00 to 16:00 on weekdays.
  Outside that window, `lark ship prod` is rejected unless an incident override flag is
  set.
- The config lives in `larkfield.yaml`.
- Notices post to `#larkfield-deploys`.
