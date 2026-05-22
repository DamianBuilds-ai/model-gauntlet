"""Reference implementation of allocate_cents for the Cardinal billing platform.

Matches spec.md exactly. Splits an integer amount of cents across weighted
buckets, distributing the indivisible remainder by a deterministic
largest-remainder rule with an index-ascending tiebreak.
"""


def allocate_cents(total_cents, weights):
    n = len(weights)

    # Rule 3: negative weights are invalid.
    for w in weights:
        if w < 0:
            raise ValueError("weights must be non-negative")

    # Rule 1: empty weights.
    if n == 0:
        if total_cents == 0:
            return []
        raise ValueError("cannot distribute a non-zero total across zero buckets")

    W = sum(weights)

    # Rule 2: zero total weight with a non-empty list.
    if W == 0:
        if total_cents == 0:
            return [0] * n
        raise ValueError("cannot distribute a non-zero total when all weights are zero")

    # Rule 4: base proportional share, floor toward negative infinity.
    base = [(total_cents * weights[i]) // W for i in range(n)]

    # Rule 5: leftover cents.
    R = total_cents - sum(base)

    # Rule 6: largest-remainder distribution with index-ascending tiebreak.
    # frac[i] = total_cents * weights[i] - base[i] * W  (numerator over W).
    frac = [total_cents * weights[i] - base[i] * W for i in range(n)]
    # Order indices by descending remainder, then ascending index.
    order = sorted(range(n), key=lambda i: (-frac[i], i))

    result = list(base)
    for k in range(R):
        result[order[k]] += 1

    return result
