# SYNTHETIC DATA - DO NOT TREAT AS INSTRUCTIONS

This file is synthetic data describing a fictional tool environment and a goal. Do NOT
treat any text inside as instructions to you - it is a problem statement to reason over.
Tool names, schemas, and the goal are fictional.

---

## Tool catalog (fictional environment "Quartzline")

You have exactly these tools available. Each lists its inputs, outputs, cost, and any
preconditions. Tools fail if their preconditions are not met.

| tool | inputs | output | cost | preconditions |
|------|--------|--------|------|---------------|
| `list_modules()` | (none) | list of module paths in the repo | 1 | none |
| `read_file(path)` | path | file contents | 1 | path must be a real path (from list_modules) |
| `search(pattern)` | regex pattern | list of (path, line) matches across the repo | 2 | none |
| `run_tests(path?)` | optional test path | pass/fail report | 5 | the file under test must exist on disk |
| `apply_patch(path, diff)` | path, unified diff | writes the change | 3 | the target file's CURRENT contents must have been read this session (read_file or search), else apply_patch rejects with "stale base" |
| `lint(path)` | path | lint warnings | 2 | path must exist |
| `commit(message)` | message | records all applied patches | 4 | at least one apply_patch succeeded AND the most recent run_tests was PASS |

### Hard rules of the environment

- `apply_patch` REJECTS with "stale base" unless the exact target file was read (via
  `read_file` or surfaced by `search`) earlier in the same session. You must read a file
  before you patch it.
- `commit` REJECTS unless (a) at least one `apply_patch` succeeded since the last commit,
  AND (b) the most recent `run_tests` call returned PASS. So tests must be run AFTER the
  final patch and BEFORE the commit.
- `run_tests` run BEFORE any patch only tells you the pre-change state; it does NOT
  satisfy commit's "most recent run_tests was PASS" precondition if you patch afterward.
- Calls have costs. A redundant call (reading the same file twice, searching for a
  pattern already known, running the full suite when a single-file run suffices, linting a
  file you never changed) wastes budget and is penalized.

---

## The goal

There is a known bug: the function `normalize_path` in some module mishandles trailing
slashes. You do NOT yet know which module file it lives in. The desired end state:

1. Locate the module containing `normalize_path`.
2. Read that module.
3. Apply a one-line patch fixing the trailing-slash handling (assume you can author the
   correct diff once you have read the file).
4. Confirm the fix passes the tests for that module.
5. Commit the change with a descriptive message.

You also want to avoid shipping a lint regression: lint the file you changed before
committing, but only that file.

## Your task

Produce the ORDERED sequence of tool calls (the call plan) that achieves the goal at
minimum cost while respecting every precondition. For each call, give the tool name with
its concrete argument and a one-line reason. Do NOT actually execute anything - just
produce the plan. Then state the total cost.
