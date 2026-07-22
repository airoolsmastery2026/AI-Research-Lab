"""Metadata filtering helpers for vector search."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class FilterCriteria:
    metadata: dict[str, Any] = field(default_factory=dict)
    namespace: str | None = None
