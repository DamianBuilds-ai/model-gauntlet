# Acme Logistics API - Changelog

Source file 1 of 3. Synthetic data for the multi-file-synthesis example eval.

## v3.2.0 (released)
- Added `/shipments/batch` endpoint - accept up to 100 shipments per call.
- Deprecated `/shipments/legacy-create` - sunsets in v4.0.0.
- Rate limit raised from 60 to 120 requests per minute for paid tiers.

## v3.1.4 (released)
- Fixed a timezone bug where `estimated_delivery` returned UTC instead of the
  warehouse-local zone. Carriers in Western Australia were most affected.
- Patched a null-pointer crash on `/tracking/{id}` when a parcel had no scans yet.

## v3.1.0 (released)
- New webhook event `parcel.exception` fires on customs holds and address
  failures. Replaces polling the status endpoint every 5 minutes.
- `carrier_reference` is now returned on every shipment object.

## v3.3.0 (in progress, unreleased)
- Planned: GraphQL read API alongside the REST surface.
- Planned: signed webhook payloads (HMAC) - currently webhooks are unsigned.
- Open question: whether to version the GraphQL schema separately from REST.
