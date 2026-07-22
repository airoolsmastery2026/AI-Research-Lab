"""Versioning helpers for the storage layer."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class VersionManager:
    """Tracks the storage schema version."""

    current_version: int = 1

    def bump(self) -> int:
        self.current_version += 1
        return self.current_version

    def is_compatible(self, version: int) -> bool:
        return version <= self.current_version
