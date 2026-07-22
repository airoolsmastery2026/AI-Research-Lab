"""Vector normalization helpers."""

from __future__ import annotations

import math
from typing import Sequence


def normalize_vector(vector: Sequence[float]) -> list[float]:
    """Normalize a vector to unit length."""

    magnitude = math.sqrt(sum(value * value for value in vector))
    if magnitude == 0:
        return [0.0 for _ in vector]
    return [value / magnitude for value in vector]
