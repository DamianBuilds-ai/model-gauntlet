# Design / UX Notes

Synthetic corpus doc 10 of 15. Priya's design notes for the Pulse shell and
navigation (the frame around the three panels).

## Navigation shell

- Left nav with the three panels: Seat Usage, API Volume, Billing.
- A persistent account-name header so multi-account users know which account they
  are viewing.
- Empty/loading states for when the aggregation service has no data yet for a new
  customer.

## Sign-in flow

The Pulse sign-in uses an email magic-link: the customer enters their work email,
receives a one-time link, and clicks through to their dashboard. This was chosen to
keep the first-run experience frictionless for customers whose admins have not set
up anything special.

(Note: the engineering pipeline notes, doc 06, record the auth decision as "use
existing SSO, no separate Pulse login." These two docs DISAGREE on the sign-in
method. This is a genuine unreconciled conflict in the planning record - a good
Consolidator must flag it explicitly rather than silently pick one, and should note
it needs an owner to resolve before build.)

## Visual states tied to data

- The seat utilisation amber/red band (doc 02) needs design tokens for the warning
  states - done.
- The billing panel needs a "data unavailable" state for when the Zentro adapter
  (doc 11) is not yet certified - done.

## Accessibility

All panels must meet the internal contrast standard. The amber warning band was
adjusted once to pass contrast. Noted as done.
