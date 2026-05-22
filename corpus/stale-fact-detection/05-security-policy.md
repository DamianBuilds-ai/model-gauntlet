# Cardinal Logistics - Security Policy

Baseline security controls for the platform. Reviewed twice yearly.

## Access

All gateway access requires a bearer token. There are no anonymous endpoints.
Just-in-time elevation for production access is granted for a maximum of 2 hours
and requires a second engineer's approval.

## Log retention

Hot logs are retained for 15 days (CL-2026-011), after which they roll to cold
storage. Distributed traces are retained for 7 days. The audit trail is retained
for 3 years for compliance. These windows are independent of one another.

## Secrets

Service certificates are valid for 24 hours and rotate automatically. Customer JWTs
are valid for 60 minutes; refresh tokens for 30 days. Never commit a secret to a
repository.

## Deploy freeze

Production deploys are frozen from Friday 12:00 local to Monday 09:00 local to
protect the weekend. A proposal to widen this window (ADR-028) was reviewed and
rejected, so the Friday-to-Monday window stands. Emergency deploys during a freeze
require a Director's sign-off.

## Rate limiting

The gateway enforces 600 requests per minute per key (CL-2026-009). Exhausting the
quota returns a 429. This is a security control as much as a capacity one.
