"""Repository for embedding records."""

from __future__ import annotations

from typing import Any

from ..database import DatabaseManager
from ..models.embedding_record import EmbeddingRecord
from ..serializers.json_serializer import JsonSerializer


class EmbeddingRepository:
    """Repository for embedding records."""

    def __init__(self, database_manager: DatabaseManager) -> None:
        self.database_manager = database_manager

    def save(self, record: EmbeddingRecord) -> None:
        with self.database_manager.transaction() as connection:
            connection.execute(
                """
                INSERT INTO embeddings (id, document_id, vector_json, metadata_json)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    document_id=excluded.document_id,
                    vector_json=excluded.vector_json,
                    metadata_json=excluded.metadata_json
                """,
                (
                    record.id,
                    record.document_id,
                    JsonSerializer.dumps(record.vector),
                    JsonSerializer.dumps(record.metadata),
                ),
            )

    def list_for_document(self, document_id: str) -> list[EmbeddingRecord]:
        with self.database_manager.get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM embeddings WHERE document_id = ?",
                (document_id,),
            ).fetchall()
        return [self._row_to_record(row) for row in rows]

    def _row_to_record(self, row: Any) -> EmbeddingRecord:
        if hasattr(row, "keys"):
            row_data = {key: row[key] for key in row.keys()}
        else:
            columns = ["id", "document_id", "vector_json", "metadata_json"]
            row_data = dict(zip(columns, row))
        return EmbeddingRecord(
            id=row_data["id"],
            document_id=row_data["document_id"],
            vector=JsonSerializer.loads(row_data["vector_json"]),
            metadata=JsonSerializer.loads(row_data["metadata_json"]) if row_data["metadata_json"] else {},
        )
