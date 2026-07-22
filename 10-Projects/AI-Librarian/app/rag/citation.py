"""Citation generation helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Citation:
    source: str
    page: int | None = None
    line: int | None = None
