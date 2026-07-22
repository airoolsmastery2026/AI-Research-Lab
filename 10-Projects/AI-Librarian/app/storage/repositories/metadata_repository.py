"""Repository for metadata entries."""

from __future__ import annotations

from typing import Any

from ..database import DatabaseManager
from ..errors import StorageNotFoundError
from ..serializers.json_serializer import JsonSerializer


class MetadataRepository:
    """Repository for storing document metadata key/value pairs."""

    def __init__(self, database_manager: DatabaseManager) -> None:
        self.database_manager = database_manager

    def save(self, document_id: str, key_name: str, value: Any) -> None:
        with self.database_manager.transaction() as connection:
            connection.execute(
                "INSERT INTO metadata_entries (id, document_id, key_name, value_text) VALUES (?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET value_text=excluded.value_text",
                (f"{document_id}:{key_name}", document_id, key_name, JsonSerializer.dumps(value)),
            )

    def find_for_document(self, document_id: str) -> dict[str, Any]:
        with self.database_manager.get_connection() as connection:
            rows = connection.execute(
                "SELECT key_name, value_text FROM metadata_entries WHERE document_id = ?",
                (document_id,),
            ).fetchall()
        return {row["key_name"]: JsonSerializer.loads(row["value_text"]) for row in rows}
