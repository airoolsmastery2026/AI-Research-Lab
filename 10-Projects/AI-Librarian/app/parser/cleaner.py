"""Text cleaning utilities for parsed content."""

from __future__ import annotations

import re
import unicodedata


def clean_text(text: str) -> str:
    """Normalize and clean text for downstream processing."""

    normalized = unicodedata.normalize("NFKC", text)
    normalized = re.sub(r"[\u00a0\t]+", " ", normalized)
    normalized = re.sub(r"\r\n?", "\n", normalized)
    normalized = re.sub(r"[ ]{2,}", " ", normalized)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    normalized = re.sub(r"(?<!\n)\n(?!\n)", "\n", normalized)
    return normalized.strip()
