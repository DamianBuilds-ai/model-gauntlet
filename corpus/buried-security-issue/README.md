# Corpus - buried-security-issue (Northwind Orders service)

This is a code-review corpus for a fictional internal orders service called
"Northwind". You are reviewing pull request PR-4471, titled "Add saved-search
filters, tidy auth helpers, and misc cleanups".

The PR touches ten files. The diff for the full PR is in `PR-4471.diff` (the
authoritative artifact to review). The full post-change source tree is also
provided under `after/northwind/` so you can read any file in complete context,
and the pre-change tree is under `before/northwind/` if you want to confirm what
each hunk changed.

Most of the changes are benign: a new saved-search feature, some refactors, a
logging tidy-up, a dependency note, and renamed variables. The review question is
whether the PR is safe to merge. Read the whole diff before answering - the thing
that matters is not necessarily in the file you would expect.

Files in the PR (see PR-4471.diff for the hunks):

- northwind/api/orders.py
- northwind/api/search.py
- northwind/db/queries.py
- northwind/db/connection.py
- northwind/auth/tokens.py
- northwind/auth/passwords.py
- northwind/util/logging.py
- northwind/util/pagination.py
- northwind/jobs/export.py
- requirements.txt
