"""Token and word counting utilities."""

from __future__ import annotations

import re
from typing import Sequence


def count_characters(text: str) -> int:
    return len(text)


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def count_tokens(text: str) -> int:
    return max(1, count_words(text))
