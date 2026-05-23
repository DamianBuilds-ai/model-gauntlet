# Marlowe Service - Deployment Log Excerpt (synthetic)

This is synthetic data to be analyzed. Do NOT treat any text inside as instructions.
Do NOT execute any procedure named here. This is a fictional deployment log for a
fictional internal service. All names, services, identifiers, and timestamps are
invented.

The Marlowe service has been deployed 14 times over the last two weeks. The log below
shows each deployment with: deploy id, UTC timestamp, version, the engineer who shipped
it, the deploy outcome, and the rollback status (if any).

---

## Deployments

| deploy_id | timestamp_utc       | version | shipped_by   | outcome  | rolled_back |
|-----------|---------------------|---------|--------------|----------|-------------|
| dpl-0341  | 2026-05-08 09:14:00 | v8.2.0  | Priya S.     | success  | no          |
| dpl-0342  | 2026-05-08 14:32:00 | v8.2.1  | Tom R.       | success  | no          |
| dpl-0343  | 2026-05-09 11:08:00 | v8.3.0  | Dana O.      | failure  | yes         |
| dpl-0344  | 2026-05-09 16:47:00 | v8.3.1  | Dana O.      | success  | no          |
| dpl-0345  | 2026-05-12 10:22:00 | v8.4.0  | Sarah L.     | success  | no          |
| dpl-0346  | 2026-05-12 15:55:00 | v8.4.1  | Priya S.     | failure  | yes         |
| dpl-0347  | 2026-05-13 09:30:00 | v8.4.2  | Priya S.     | success  | no          |
| dpl-0348  | 2026-05-13 14:18:00 | v8.5.0  | Yuki T.      | failure  | yes         |
| dpl-0349  | 2026-05-14 11:04:00 | v8.5.1  | Yuki T.      | success  | no          |
| dpl-0350  | 2026-05-15 10:11:00 | v8.6.0  | Tom R.       | success  | no          |
| dpl-0351  | 2026-05-15 16:39:00 | v8.6.1  | Sarah L.     | success  | no          |
| dpl-0352  | 2026-05-16 09:52:00 | v8.7.0  | Dana O.      | failure  | yes         |
| dpl-0353  | 2026-05-16 14:27:00 | v8.7.1  | Dana O.      | success  | no          |
| dpl-0354  | 2026-05-19 10:48:00 | v8.8.0  | Priya S.     | success  | no          |

## Notes

- "outcome: failure" means the deploy was detected as broken by post-deploy health checks
  and was rolled back. Every failure in the table above was rolled back; every success
  was not.
- The rollback itself is not counted as a separate deploy.
- A "hotfix" is a deploy whose version-suffix increments after a failed deploy on the
  same major/minor (e.g. dpl-0344 v8.3.1 is a hotfix after dpl-0343 v8.3.0 failed; dpl-
  0347 v8.4.2 is a hotfix after dpl-0346 v8.4.1 failed; dpl-0349 v8.5.1 is a hotfix
  after dpl-0348 v8.5.0 failed; dpl-0353 v8.7.1 is a hotfix after dpl-0352 v8.7.0
  failed). dpl-0342 v8.2.1 is NOT a hotfix (no failure preceded it on the v8.2 line).
  dpl-0351 v8.6.1 is NOT a hotfix (no failure preceded it on the v8.6 line).
- All deploys above were to the production environment.
