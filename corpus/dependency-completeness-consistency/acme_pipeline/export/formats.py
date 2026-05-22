"""acme_pipeline.export.formats - DISTRACTOR leaf. Used by export.writer only.
Not in normalizer's closure."""


def to_csv(rows):
    return "\n".join(str(r) for r in rows)
