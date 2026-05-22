#!/usr/bin/env python3
"""
Verifier for the dependency-completeness-consistency answer key.

Computes two closures of acme_pipeline.transform.normalizer:
  1. STATIC closure - follows only top-of-file `from acme_pipeline... import`
     and `import acme_pipeline...` lines (ignores commented lines). This is what
     a naive static scan finds. It MISSES the dynamic plugin edge.
  2. TRUE closure - the static closure PLUS the one dynamic edge from
     normalizer to plugins.rounding (resolved from the config default string)
     and everything reachable through it.

The difference between the two closures is exactly the buried subtree:
  acme_pipeline.transform.plugins.rounding, acme_pipeline.common.precision.

Run: python3 verify_closure.py
No em dashes. Neutral fictional names only.
"""

import ast
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
PKG = "acme_pipeline"


def module_to_path(mod):
    """Map a dotted module name to a file path under ROOT. Returns the .py file
    if it exists, else the package __init__.py, else None."""
    parts = mod.split(".")
    p = os.path.join(ROOT, *parts) + ".py"
    if os.path.isfile(p):
        return p
    pinit = os.path.join(ROOT, *parts, "__init__.py")
    if os.path.isfile(pinit):
        return pinit
    return None


def static_imports(path):
    """Return the set of acme_pipeline.* modules statically imported by the file
    at path (ignores commented lines automatically since ast skips comments)."""
    with open(path) as f:
        tree = ast.parse(f.read(), filename=path)
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith(PKG):
                for alias in node.names:
                    candidate = node.module + "." + alias.name
                    if module_to_path(candidate):
                        out.add(candidate)
                    else:
                        out.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith(PKG):
                    out.add(alias.name)
    return out


def closure(seed, extra_edges=None):
    """BFS the static-import graph from seed module. extra_edges is a dict of
    module -> set(modules) for non-static edges to inject (the dynamic one)."""
    extra_edges = extra_edges or {}
    seen = set()
    stack = [seed]
    while stack:
        mod = stack.pop()
        if mod in seen:
            continue
        seen.add(mod)
        path = module_to_path(mod)
        deps = set()
        if path:
            deps |= static_imports(path)
        deps |= extra_edges.get(mod, set())
        for d in deps:
            if d not in seen:
                stack.append(d)
    seen.discard(seed)
    return seen


if __name__ == "__main__":
    seed = "acme_pipeline.transform.normalizer"

    static_closure = closure(seed)

    # The single dynamic edge: normalizer -> plugins.rounding (config default).
    dynamic = {seed: {"acme_pipeline.transform.plugins.rounding"}}
    true_closure = closure(seed, extra_edges=dynamic)

    buried = true_closure - static_closure

    print("=== STATIC closure (naive scan finds these) ===")
    for m in sorted(static_closure):
        print("  ", m)
    print(f"  ({len(static_closure)} modules)")

    print("\n=== TRUE closure (includes the dynamic edge) ===")
    for m in sorted(true_closure):
        print("  ", m)
    print(f"  ({len(true_closure)} modules)")

    print("\n=== BURIED subtree (the separator: in TRUE, missed by STATIC) ===")
    for m in sorted(buried):
        print("  ", m)
    print(f"  ({len(buried)} modules)")
