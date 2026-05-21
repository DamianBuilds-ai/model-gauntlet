# Acme Logistics - Open Support Tickets Digest

Source file 2 of 3. Synthetic data for the multi-file-synthesis example eval.

## TICK-4471 (high)
Customer "Northwind Traders" reports webhook deliveries stop after roughly 200
events per day. They are on the free tier. Suspected rate-limit interaction with
the `parcel.exception` event volume. Engineering has not reproduced yet.

## TICK-4460 (medium)
Three customers asking when signed webhooks land. They will not move production
traffic to webhooks until payloads are verifiable. All three name HMAC explicitly.

## TICK-4455 (high)
"Southgate Freight" hit the old 60 rpm limit during a Black Friday burst and
dropped batch jobs. They have since upgraded to a paid tier. Asking whether the
batch endpoint would have prevented the drops.

## TICK-4448 (low)
Documentation gap: the `carrier_reference` field is returned but not documented
in the public reference. Two developers filed near-identical reports.

## TICK-4431 (medium)
A Western Australia carrier reports delivery estimates were off by 8 hours last
month. Believed fixed in v3.1.4 but the customer wants written confirmation the
timezone fix shipped to their account.
