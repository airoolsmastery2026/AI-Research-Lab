"""Similarity helpers for embedding vectors."""

from __future__ import annotations

import math
from typing import Sequence


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    """Compute cosine similarity between two vectors."""

    numerator = sum(x * y for x, y in zip(a, b))
    denom_a = math.sqrt(sum(x * x for x in a))
    denom_b = math.sqrt(sum(y * y for y in b))
    if denom_a == 0 or denom_b == 0:
        return 0.0
    return numerator / (denom_a * denom_b)


def dot_product(a: Sequence[float], b: Sequence[float]) -> float:
    """Compute the dot product between two vectors."""

    return sum(x * y for x, y in zip(a, b))
