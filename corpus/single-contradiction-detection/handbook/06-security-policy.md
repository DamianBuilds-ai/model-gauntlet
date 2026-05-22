# Security Policy

## Purpose

This policy sets the baseline security controls for all Globex systems and staff.
It applies to every employee, contractor, and system that touches company or
customer data.

## Access control

Access to internal systems follows least privilege. Access is granted by role
through the identity provider and reviewed every quarter. Privileged (admin)
access additionally requires hardware multi-factor authentication and is reviewed
monthly. Dormant accounts with no sign-in for 45 days are automatically disabled
and must be re-requested.

## Authentication

All staff use single sign-on with multi-factor authentication. Session tokens
issued by the identity provider expire after 30 days of inactivity, after which
the user must re-authenticate. Passwords, where still used for legacy systems, are
a minimum of 14 characters and are rotated only on suspected compromise (no
forced periodic rotation).

## Endpoint security

Company laptops run full-disk encryption and the managed endpoint agent. Remote
staff additionally follow the connectivity rules in 05-remote-work.md. Personal
devices are not permitted to store customer data.

## Logging and audit trails

Every production system emits structured audit logs to the central log platform.
These audit logs capture authentication events, privileged actions, and data
access. Audit logs are retained for 180 days in the central log platform before
being purged, which the security team considers sufficient for investigation and
forensic review while keeping storage costs bounded. Access to the audit log
platform is itself logged and is restricted to the security team.

## Vulnerability management

Critical vulnerabilities are patched within 7 days of a fix being available; high
severity within 30 days. The security team runs an external scan monthly and an
internal scan weekly.

## Reporting

Suspected security incidents are reported immediately to the security team and
handled per 08-incident-response.md.
