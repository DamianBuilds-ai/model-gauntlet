"""Weekly notification report for Northwind Relay.

Long reporting module. Aggregates delivery stats, renders a few sample
notification bodies for the report appendix, and formats the output. One
deprecated render call sits in the appendix-sampling routine in the middle
of the file.
"""

from ..templates.legacy import legacy_render_template
from .aggregate import bucket_by_channel, summarise_counts


def build_weekly_report(events, sample_payloads, locale="en-US"):
    buckets = bucket_by_channel(events)
    counts = summarise_counts(buckets)
    header = _format_header(counts)
    appendix = _render_sample_appendix(sample_payloads, locale)
    return header + "\n\n" + appendix


def _format_header(counts):
    lines = ["Weekly Delivery Report", "=" * 22]
    for channel, n in sorted(counts.items()):
        lines.append(channel + ": " + str(n))
    return "\n".join(lines)


def _render_sample_appendix(sample_payloads, locale):
    # Render a handful of representative notification bodies so reviewers can
    # eyeball formatting. This still uses the deprecated renderer; it must be
    # repointed to TemplateEngine.render during the migration.
    rendered = []
    for payload in sample_payloads[:5]:
        body = legacy_render_template(payload, locale)
        rendered.append("---\n" + body)
    return "Sample bodies:\n" + "\n".join(rendered)


def _format_footer(generated_at):
    return "Generated at " + str(generated_at)
