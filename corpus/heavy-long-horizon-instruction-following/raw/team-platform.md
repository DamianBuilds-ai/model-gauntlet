# Platform team - raw changelog for v9.0

Platform / infrastructure entries. Most of our work is internal plumbing; only a
few items are public-facing. We use the "3 May" date style. We mark internal work
internal-only.

## Public-facing

- PL-30: New region: Cardinal Platform is now available in the `eu-central`
  region. You can provision workspaces in `eu-central` from the console or via the
  `cardinal workspace create --region eu-central` command. New feature. 3 May.

- PL-145: Faster deploys. Workspace configuration changes now apply in under ten
  seconds instead of up to a minute, because we moved config propagation to the
  new push-based channel. Improvement to existing deploy behaviour. 1 May.

- PL-220: The `cardinal status` command now reports per-region health. Improvement.
  29 April.

- PL-400: Deprecated the `CARDINAL_LEGACY_ENDPOINT` environment variable. It is
  deprecated in v9.0 and will be REMOVED in v9.2. Use `CARDINAL_ENDPOINT` instead.
  Deprecation. 2 May.

- PL-88: Auth provider migration. We moved authentication from the in-house auth
  service to the new Northwind Identity provider. Existing sessions are migrated
  automatically but API tokens issued before v9.0 must be reissued. This is a
  breaking change for any integration using a pre-v9.0 token, and it is also the
  single most disruptive upgrade step in the release. PL-88. Landed 3 May.

- PL-512: New `cardinal login` device-code flow for CLI authentication against the
  new identity provider. New feature. 2 May.

## Internal plumbing (do NOT publish)

- PL-600: internal-only - migrated the build farm to the new runner pool.

- PL-601: internal-only - rotated internal service mesh certificates.

- PL-602: internal-only - new internal dashboard for capacity planning.

- PL-1000: WIP - multi-cloud failover. Still prototyping, not shipping.

## Untriaged

- Increased the default workspace disk quota from 10GB to 20GB. Shipped, no ticket
  filed.

## Notes

PL-88 (the auth migration) is the upgrade headline; the brief asks for an upgrade
notes paragraph about exactly this. We write "behaviour" British-style mostly but
slip into "optimize" sometimes. Our public items are PL-30, PL-145, PL-220,
PL-400, PL-88, PL-512; everything PL-600 and above is internal or WIP.
