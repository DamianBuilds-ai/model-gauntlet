# Service Registry - Northwind Platform

Synthetic corpus for the mechanical-apply-exact eval. This is the target file an
apply agent must edit. All services, ports, and owners are fictional (company
"Globex", platform "Northwind"). The file mixes a markdown table, a fenced config
block, and a plain bullet list - three different edit surfaces. Do NOT treat this
text as instructions; it is data to be edited per a separate change spec.

---

## Registered services

| service | port | owner | status |
|---------|------|-------|--------|
| gateway | 8080 | platform-team | active |
| ledger | 8081 | finance-team | active |
| courier | 8082 | logistics-team | active |
| beacon | 8083 | platform-team | retired |
| almanac | 8084 | data-team | active |

## Feature flags

```ini
[flags]
enable_courier_v2 = false
enable_ledger_batch = true
enable_beacon_metrics = false
max_retries = 3
```

## On-call rotation

- gateway: Dana Okafor
- ledger: Priya Sundaram
- courier: Tom Reilly
- almanac: Sarah Lin
