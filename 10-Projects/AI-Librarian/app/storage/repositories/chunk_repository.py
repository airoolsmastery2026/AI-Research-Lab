"""Repository for chunk records."""

from __future__ import annotations

from typing import Any

from ..database import DatabaseManager
from ..errors import StorageNotFoundError
from ..models.chunk_record import ChunkRecord
from ..serializers.json_serializer import JsonSerializer


class ChunkRepository:
    """Repository for chunk records."""

    def __init__(self, database_manager: DatabaseManager) -> None:
        self.database_manager = database_manager

    def save(self, record: ChunkRecord) -> None:
        with self.database_manager.transaction() as connection:
            connection.execute(
                """
                INSERT INTO chunks (id, document_id, index_number, text_content, metadata_json)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    document_id=excluded.document_id,
                    index_number=excluded.index_number,
                    text_content=excluded.text_content,
                    metadata_json=excluded.metadata_json
                """,
                (
                    record.id,
                    record.document_id,
                    record.index_number,
                    record.text_content,
                    JsonSerializer.dumps(record.metadata),
                ),
            )

    def list_for_document(self, document_id: str) -> list[ChunkRecord]:
        with self.database_manager.get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM chunks WHERE document_id = ? ORDER BY index_number",
                (document_id,),
            ).fetchall()
        return [self._row_to_record(row) for row in rows]

    def _row_to_record(self, row: Any) -> ChunkRecord:
        if hasattr(row, "keys"):
            row_data = {key: row[key] for key in row.keys()}
        else:
            columns = ["id", "document_id", "index_number", "text_content", "metadata_json"]
            row_data = dict(zip(columns, row))
        return ChunkRecord(
            id=row_data["id"],
            document_id=row_data["document_id"],
            index_number=row_data["index_number"],
            text_content=row_data["text_content"],
            metadata=JsonSerializer.loads(row_data["metadata_json"]) if row_data["metadata_json"] else {},
        )
