"""SQLite database management for the storage layer."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Optional

from app.core.logger import get_logger

from .errors import StorageError

logger = get_logger("storage.database")


@dataclass(slots=True)
class DatabaseConfig:
    path: Path
    timeout: float = 30.0
    journal_mode: str = "WAL"
    foreign_keys: bool = True
    max_connections: int = 5


@dataclass(slots=True)
class DatabaseManager:
    config: DatabaseConfig
    _connection_pool: list[sqlite3.Connection] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        self.config.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _initialize_database(self) -> None:
        with self.get_connection() as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("PRAGMA journal_mode = WAL")
            connection.execute("PRAGMA synchronous = NORMAL")
            connection.commit()

    def get_connection(self) -> sqlite3.Connection:
        if len(self._connection_pool) < self.config.max_connections:
            connection = sqlite3.connect(str(self.config.path), timeout=self.config.timeout, isolation_level=None)
            connection.row_factory = sqlite3.Row
            self._connection_pool.append(connection)
            return connection
        return sqlite3.connect(str(self.config.path), timeout=self.config.timeout, isolation_level=None)

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        connection = self.get_connection()
        try:
            connection.execute("BEGIN")
            yield connection
            connection.commit()
        except Exception as exc:
            connection.rollback()
            raise StorageError(f"Transaction failed: {exc}") from exc
        finally:
            if connection in self._connection_pool and len(self._connection_pool) > self.config.max_connections:
                connection.close()

    def close(self) -> None:
        for connection in self._connection_pool:
            connection.close()
        self._connection_pool.clear()
