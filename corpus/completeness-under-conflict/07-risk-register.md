# Risk Register - Globex Insight

Maintained by the program manager.

## RISK-1 - Authentication method unresolved (HIGH)

The data-pipeline notes and the design notes describe DIFFERENT authentication methods
for the dashboard. The security review cannot start until this is settled (see the
security-review notes). Owner: unassigned. This is blocking.

## RISK-2 - Data retention figure inconsistent (HIGH, legal)

The activity-panel PRD displays 12 months of activity; the compliance memo states a
shorter mandated retention. Displaying longer than the compliance limit is a legal
exposure. Must be reconciled before launch. Owner: compliance + product.

## RISK-3 - Primary datastore ambiguity (MEDIUM)

The data-pipeline notes name PostgreSQL as the serving store; the migration plan names
the new vendor's columnar store. The two plans disagree on the primary store. Owner:
data eng + platform.

## RISK-4 - Budget exposure (MEDIUM)

The launch/GTM plan's projected spend may exceed the finance budget cap. Owner:
finance.

## RISK-5 - Endpoint tagging not done (MEDIUM)

The usage panel needs per-endpoint consumption tagging that is not yet built. Owner:
unassigned.
