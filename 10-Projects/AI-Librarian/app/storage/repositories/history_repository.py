"""Repository for history events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..database import DatabaseManager


@dataclass(slots=True)
class HistoryEntry:
    id: str
    document_id: str
    action: str
    created_at: str
    details: str | None = None


class HistoryRepository:
    """Repository for storing history entries."""

    def __init__(self, database_manager: DatabaseManager) -> None:
        self.database_manager = database_manager

    def save(self, entry: HistoryEntry) -> None:
        with self.database_manager.transaction() as connection:
            connection.execute(
                "INSERT INTO history (id, document_id, action, created_at, details) VALUES (?, ?, ?, ?, ?)",
                (entry.id, entry.document_id, entry.action, entry.created_at, entry.details),
            )

    def list_for_document(self, document_id: str) -> list[HistoryEntry]:
        with self.database_manager.get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM history WHERE document_id = ? ORDER BY created_at",
                (document_id,),
            ).fetchall()
        return [self._row_to_entry(row) for row in rows]

    def _row_to_entry(self, row: Any) -> HistoryEntry:
        if hasattr(row, "keys"):
            row_data = {key: row[key] for key in row.keys()}
        else:
            columns = ["id", "document_id", "action", "created_at", "details"]
            row_data = dict(zip(columns, row))
        return HistoryEntry(
            id=row_data["id"],
            document_id=row_data["document_id"],
            action=row_data["action"],
            created_at=row_data["created_at"],
            details=row_data["details"],
        )
