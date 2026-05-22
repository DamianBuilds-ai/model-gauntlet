# Helios Design System Notes

Author: Noor (Design)
Status: working notes

## Visual language

Helios uses the Globex design system with an analytics-specific extension for charts.
Chart color palettes are colorblind-safe by default. Typography and spacing follow the
Globex tokens.

## Component inventory

- Dashboard canvas, widget cards, the field picker, the visualization picker.
- The plan-selection and usage-meter components for the billing surface (doc 04).
- The connector-setup wizard (doc 03).

## Accessibility

This design targets WCAG 2.1 level A at GA, with level AA as a fast-follow after
launch. The rationale is timeline: full AA conformance (contrast, focus management,
ARIA across every widget type) is more than the GA window allows, so the team proposes
A at GA and AA shortly after.

NOTE: the legal/compliance doc (doc 34) states that Helios MUST meet WCAG 2.1 level AA
at GA because it is a procurement requirement for public-sector and several enterprise
customers. That directly conflicts with this design doc's plan of A-at-GA, AA-as-
fast-follow. The accessibility level at GA (A vs AA) is therefore contested between
Design (doc 10) and Legal (doc 34). Risk register doc 12 tracks this as RISK-8.
