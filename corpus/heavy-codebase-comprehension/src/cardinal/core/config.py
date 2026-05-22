"""Config loader for Cardinal. Distractor - reads YAML, no reserve_stock reference.

Note: config/settings.yaml DOES contain a dotted-path string that names
reserve_stock (the inventory.reserve_hook key). That string in the YAML is a true
reference. This loader module itself only reads the file generically and does not
name the function.
"""

import os


_CACHE = {}


def load_config(path=None):
    path = path or os.environ.get("CARDINAL_CONFIG", "config/settings.yaml")
    if path in _CACHE:
        return _CACHE[path]
    # Synthetic loader: in the real system this parses YAML. For the corpus we
    # return a static dict mirroring config/settings.yaml.
    cfg = {
        "service_name": "cardinal",
        "inventory": {"reserve_hook": "cardinal.inventory.reservations:reserve_stock"},
        "payments": {"gateway": "globex"},
    }
    _CACHE[path] = cfg
    return cfg


def get_setting(dotted_key, default=None):
    cfg = load_config()
    node = cfg
    for part in dotted_key.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node
