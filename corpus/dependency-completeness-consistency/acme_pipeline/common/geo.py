"""acme_pipeline.common.geo - DISTRACTOR leaf. Used only by the dead enricher
module. Not in normalizer's closure."""

_REGIONS = {"1": "north", "2": "south"}


def region_for(zip_code):
    if not zip_code:
        return "unknown"
    return _REGIONS.get(str(zip_code)[0], "unknown")
