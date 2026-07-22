"""Encoding detection and normalization utilities."""

from __future__ import annotations

import codecs
from pathlib import Path
from typing import Optional


def detect_encoding(path: Path | str) -> str:
    """Detect the likely text encoding for a file."""

    candidate = Path(path).expanduser()
    try:
        with candidate.open("rb") as handle:
            raw_bytes = handle.read(2000)
    except OSError:
        return "utf-8"

    for encoding in ("utf-8", "utf-16", "latin-1"):
        try:
            raw_bytes.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue
    return "utf-8"


def normalize_text_encoding(text: str) -> str:
    """Normalize text to UTF-8-safe content."""

    return text.encode("utf-8", errors="replace").decode("utf-8")
