"""Registry helpers for storage indexes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class IndexRegistry:
    """Tracks known indexes and their metadata."""

    indexes: dict[str, dict[str, Any]] = field(default_factory=dict)

    def register(self, name: str, metadata: dict[str, Any] | None = None) -> None:
        self.indexes[name] = metadata or {}

    def get(self, name: str) -> dict[str, Any] | None:
        return self.indexes.get(name)
