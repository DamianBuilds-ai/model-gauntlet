# Feature ticket INTERNAL-4471

**Title:** Add export to the dashboard

**Reporter:** Priya (Customer Success)
**Priority:** High - a few customers have asked and the QBR is in two weeks

---

## Description

Customers want to be able to export the dashboard so they can share it with
their own stakeholders and keep records. Right now there is no way to get the
data out of the product - they screenshot it, which looks bad and they have
complained about it on two calls this month.

Can we add an export button to the main analytics dashboard? It should let them
pull the data they are looking at. The big enterprise account (Northwind) asked
about this specifically and their renewal is the quarter after next, so it would
be good to have something to show them.

Sam from sales also mentioned a customer wanted to "get the dashboard into their
weekly report" but I am not sure exactly what they meant by that.

---

## Notes from the thread

- Priya: "Just needs to work, the customers aren't picky about the exact format."
- Sam: "Northwind has a LOT of data, they have been with us for years."
- Dev lead (async, last week): "We have the data layer already, this is mostly a
  front-end + an endpoint. Should be quick?"
- Priya: "Whatever is fastest to get in front of Northwind before the QBR."

---

## Acceptance criteria

- There is an export button on the dashboard.
- Customers can export their dashboard.
- It works for Northwind.
