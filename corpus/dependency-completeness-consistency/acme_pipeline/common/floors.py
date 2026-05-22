"""acme_pipeline.common.floors - DISTRACTOR leaf. Used only by the alternate
truncating plugin, which normalizer does not load under the default config. Not
in normalizer's closure."""

import math


def floor_to_int(value):
    return int(math.floor(value))
