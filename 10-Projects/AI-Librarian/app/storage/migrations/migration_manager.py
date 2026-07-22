"""Simple migration manager for the storage layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from ..errors import StorageMigrationError


@dataclass(slots=True)
class Migration:
    name: str
    operation: Callable[[], None]


@dataclass(slots=True)
class MigrationManager:
    migrations: list[Migration] = field(default_factory=list)

    def register(self, migration: Migration) -> None:
        self.migrations.append(migration)

    def apply(self) -> None:
        for migration in self.migrations:
            try:
                migration.operation()
            except Exception as exc:
                raise StorageMigrationError(f"Migration failed: {migration.name}") from exc
