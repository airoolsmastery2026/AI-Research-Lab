"""Token-aware helpers for embedding chunking."""

from __future__ import annotations

import re


def count_tokens(text: str) -> int:
    """Estimate token count using a simple whitespace-based heuristic."""

    return max(1, len(re.findall(r"\S+", text)))
