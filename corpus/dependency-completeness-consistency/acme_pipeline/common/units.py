"""acme_pipeline.common.units - unit conversion to canonical form."""

from acme_pipeline.common import constants


def to_canonical(value, unit):
    factor = constants.CONVERSION_FACTORS.get(unit, 1.0)
    return value * factor
