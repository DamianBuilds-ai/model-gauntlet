# Compliance Memo - Data Residency and Certifications

Synthetic corpus doc 9 of 16. Memo from Riverbend's compliance function. Riverbend
handles EU customer data, so this is a first-order constraint (doc 01).

## Requirement

EU customer data must be stored and processed in an EU region. Vendor must hold the
standard security certifications and support a data-processing agreement.

## Per-platform assessment

- **Lumen Cloud:** Offers an EU region (Frankfurt) and holds the required
  certifications. One caveat: some Lumen ADMINISTRATIVE metadata transits a non-EU
  control plane. Compliance reviewed this and judged it acceptable because no customer
  payload leaves the EU region - only operational metadata. Conditional pass,
  documented. This is a real but manageable nuance, not a blocker.
- **Strato DB:** Because Riverbend self-hosts, data residency is whatever Riverbend
  configures - run the cluster in an EU region and residency is fully satisfied.
  Strongest residency control of the three, BUT the certification burden shifts to
  RIVERBEND (you must certify your own deployment), which is more compliance work for
  the small team.
- **Beacon Analytics:** Here is the caveat the one-pager (doc 04) is quiet about.
  Beacon's EU region currently does NOT cover its built-in BI/dashboard layer - the
  warehouse data can sit in the EU, but dashboard rendering and the BI metadata layer
  run from a non-EU region today. For Riverbend's EU-data obligation this is a
  MATERIAL gap, not a minor nuance. Beacon has it on their roadmap but it is not
  available now.

## Compliance recommendation

Lumen: acceptable with documented caveat. Strato: strongest residency, heaviest
self-certification load. Beacon: the BI-layer residency gap is a current blocker for
EU data and should weigh heavily against it unless and until resolved.
