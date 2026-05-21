# Northwind Pulse - Project Charter

Synthetic corpus doc 1 of 15. Fictional company "Northwind", launching a new
product called "Northwind Pulse" (a self-serve analytics dashboard for Northwind's
existing customers). This doc set is scattered planning material a Consolidator must
fold into one plan. Docs cross-reference each other by name.

## What we are building

Northwind Pulse is a dashboard that lets Northwind's existing customers see usage
analytics on their own accounts without filing a support ticket. Today customers
email support to ask "how many seats are we using" and "what is our API call volume"
and support pulls it manually. Pulse self-serves that.

## Why now

Support volume for these manual data pulls has roughly tripled over the last two
quarters. The Pulse launch is meant to deflect that ticket load and double as a soft
upsell surface (customers who can see they are near a plan limit tend to upgrade).

## Scope for v1 (launch)

- Read-only dashboard. No write actions in v1.
- Three core panels: Seat usage, API call volume, Billing summary.
- Self-serve, no support involvement to view.

## Out of scope for v1

- Custom report builder (parked for v2).
- Data export to CSV (parked for v2, though see the customer notes - this comes up).
- Anything that mutates account state.

## Target launch

Target launch date is June 12. This is the date the exec sponsor has committed to
the board, so it is the anchor everything else is planned against. (Note: other docs
in this set may state this differently - that is real, planning drifted.)

## Sponsor and leads

- Exec sponsor: Dana (VP Product).
- Eng lead: Marcus.
- Design lead: Priya.
- Go-to-market lead: Sam.
