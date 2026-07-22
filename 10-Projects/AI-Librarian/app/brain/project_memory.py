"""Project memory persistence for the Brain."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ProjectMemory:
    entries: list[dict[str, Any]] = field(default_factory=list)

    def add(self, key: str, value: Any) -> None:
        self.entries.append({"key": key, "value": value})

    def get(self, key: str) -> Any | None:
        for entry in self.entries:
            if entry["key"] == key:
                return entry["value"]
        return None
