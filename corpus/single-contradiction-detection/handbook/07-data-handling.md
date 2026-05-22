# Data Handling

## Data classification

Globex classifies data into four tiers:

- Public: may be shared freely (marketing material, published rates).
- Internal: for staff only (runbooks, internal metrics).
- Confidential: limited distribution (contracts, salaries).
- Restricted: customer personal data and payment data.

Each tier has handling rules below. When in doubt, treat data as one tier more
sensitive than you think.

## Storage and encryption

Restricted and Confidential data are encrypted at rest and in transit. Restricted
data is stored only in approved systems. Customer order records (Restricted) are
retained for 24 months after the order is closed, then anonymised, to meet
contractual and tax obligations.

## Backups

Production databases are backed up every 6 hours. Backups are encrypted and
stored in a separate region. Backup restores are tested quarterly.

## Audit logs

System audit logs (authentication events, privileged actions, and data-access
records) are written to the central log platform and retained for 90 days, after
which they are automatically purged. This 90-day window is the standard log
retention period referenced throughout operations and incident response.

## Access to customer data

Access to Restricted customer data is granted per role and logged. Staff must not
copy customer data to personal devices or unapproved tools (see 05-remote-work.md
and 06-security-policy.md). Bulk export of customer data requires director
approval and is itself logged.

## Data subject requests

Requests from individuals to access or delete their data are handled by the
privacy lead within 30 days of a verified request.
