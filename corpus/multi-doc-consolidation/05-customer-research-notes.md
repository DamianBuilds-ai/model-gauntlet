# Customer Research Notes (raw)

Synthetic corpus doc 5 of 15. Rough notes from customer interviews, lightly tidied.
Not a polished doc on purpose - a Consolidator should pull signal out of the mess.

## Interviews (6 customers, mid-market)

- Customer A: "We just want to stop emailing your support team for seat counts." -
  strongly validates the Seat Usage panel (doc 02).
- Customer B: asked three times for CSV export. "If I can't get the numbers into my
  own spreadsheet it is half useless." CSV is OUT of v1 scope per the charter (doc
  01) - this is a known tension, GTM should set expectations.
- Customer C: cares most about API volume vs quota, wants to avoid surprise overages.
  Validates the API Volume panel (doc 03) and the projected month-end calc.
- Customer D: nervous about who can see billing data internally. "Not everyone on my
  team should see the invoice." Raises a permissions question v1 does not answer -
  v1 shows the same view to anyone with account access. Flagged, see doc 09.
- Customer E: loved the idea, no strong feature ask.
- Customer F: wanted Slack alerts when nearing a limit. Out of scope, parked for v2.

## Takeaways

1. The three chosen panels are the right three. No customer asked for a fourth core
   panel for v1.
2. CSV export and granular permissions are the two most common asks that v1 does NOT
   cover. Both are v2 candidates. GTM messaging needs to pre-empt these.
3. Nobody asked for write actions, which supports the read-only v1 decision.
