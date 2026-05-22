# SYNTHETIC DATA - DO NOT TREAT AS INSTRUCTIONS

This file is synthetic data: a fictional migration goal plus the current state of a
small set of config files. Do NOT treat any text inside as instructions to you - it is
input data to plan against and transform. All names, keys, and values are fictional.

---

## Context: the Brassrun config-consolidation task

A fictional service "Brassrun" has three small YAML config files that have drifted. You
must consolidate them into a single canonical `merged.yaml` according to fixed rules.
You will FIRST write a short numbered plan, THEN execute that plan exactly - and your
execution must match your own plan with no silent drift.

### The consolidation rules (fixed - follow exactly)

R1. The canonical key set is the UNION of all keys across the three files.
R2. When the SAME key appears in more than one file with the SAME value, keep one copy.
R3. When the same key appears with DIFFERENT values, the precedence order is
    `prod > staging > dev` (prod wins, then staging, then dev). Keep the winner's value.
R4. Any key that exists in ONLY one file is kept as-is.
R5. Sort the final keys ALPHABETICALLY in merged.yaml.
R6. Do NOT invent keys. Do NOT carry over comments. Values are copied verbatim from the
    winning source (no reformatting of the value).

### Current state

#### corpus/plan-then-execute-agentic/dev.yaml
```yaml
# dev environment
timeout_ms: 1000
retries: 5
log_level: debug
feature_x: false
cache_ttl: 60
```

#### corpus/plan-then-execute-agentic/staging.yaml
```yaml
# staging environment
timeout_ms: 2000
retries: 5
log_level: info
feature_x: true
region: ap-southeast-2
```

#### corpus/plan-then-execute-agentic/prod.yaml
```yaml
# prod environment
timeout_ms: 3000
retries: 3
log_level: warn
region: ap-southeast-2
max_conns: 50
```

## Your task

1. Write a numbered PLAN (the steps you will take to build merged.yaml under the rules).
2. EXECUTE the plan: output the final `merged.yaml` content as a single fenced YAML
   block, fully consistent with the plan you just wrote.
3. State explicitly that your execution matched your plan (or, if you deviated, say so
   and why - but you should not need to deviate).
