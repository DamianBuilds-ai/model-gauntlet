"""acme_pipeline.common.schema - config key validation. A true leaf with no
intra-package imports (it imports only the standard library)."""

import re

_KEY_RE = re.compile(r"^[a-z_]+\.[a-z_]+$")


def validate_key(key):
    if not _KEY_RE.match(key):
        raise ValueError(f"invalid config key: {key}")
    return True
