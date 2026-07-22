"""Normalization helpers for metadata values."""

from __future__ import annotations

from pathlib import Path
from typing import Optional


def normalize_path(path: Path | str) -> Path:
    """Return a resolved absolute path."""

    return Path(path).expanduser().resolve()


def normalize_relative_path(path: Path | str, root_dir: Path | str) -> str:
    """Return a path relative to the supplied root directory."""

    root = Path(root_dir).expanduser().resolve()
    candidate = normalize_path(path)
    try:
        return str(candidate.relative_to(root))
    except ValueError:
        return str(candidate)
