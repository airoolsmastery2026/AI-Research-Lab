"""Repository for storing and retrieving documents."""

from __future__ import annotations

from typing import Any

from app.core.logger import get_logger

from ..database import DatabaseManager
from ..errors import StorageError, StorageNotFoundError
from ..models.document_record import DocumentRecord
from ..serializers.json_serializer import JsonSerializer

logger = get_logger("storage.documents")


class DocumentRepository:
    """Repository for document records."""

    def __init__(self, database_manager: DatabaseManager) -> None:
        self.database_manager = database_manager

    def save(self, record: DocumentRecord) -> None:
        with self.database_manager.transaction() as connection:
            connection.execute(
                """
                INSERT INTO documents (id, document_id, title, file_path, extension, mime_type, size_bytes, sha256, created_at, updated_at, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(document_id) DO UPDATE SET
                    title=excluded.title,
                    file_path=excluded.file_path,
                    extension=excluded.extension,
                    mime_type=excluded.mime_type,
                    size_bytes=excluded.size_bytes,
                    sha256=excluded.sha256,
                    created_at=excluded.created_at,
                    updated_at=excluded.updated_at,
                    metadata_json=excluded.metadata_json
                """,
                (
                    record.id,
                    record.document_id,
                    record.title,
                    record.file_path,
                    record.extension,
                    record.mime_type,
                    record.size_bytes,
                    record.sha256,
                    record.created_at,
                    record.updated_at,
                    JsonSerializer.dumps(record.metadata),
                ),
            )

    def find_by_id(self, document_id: str) -> DocumentRecord:
        with self.database_manager.get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM documents WHERE document_id = ?",
                (document_id,),
            ).fetchone()
        if row is None:
            raise StorageNotFoundError(f"Document not found: {document_id}")
        return self._row_to_record(row)

    def list_all(self) -> list[DocumentRecord]:
        with self.database_manager.get_connection() as connection:
            rows = connection.execute("SELECT * FROM documents ORDER BY created_at").fetchall()
        return [self._row_to_record(row) for row in rows]

    def delete(self, document_id: str) -> None:
        with self.database_manager.transaction() as connection:
            cursor = connection.execute("DELETE FROM documents WHERE document_id = ?", (document_id,))
            if cursor.rowcount == 0:
                raise StorageNotFoundError(f"Document not found: {document_id}")

    def _row_to_record(self, row: Any) -> DocumentRecord:
        if hasattr(row, "keys"):
            row_data = {key: row[key] for key in row.keys()}
        else:
            columns = ["id", "document_id", "title", "file_path", "extension", "mime_type", "size_bytes", "sha256", "created_at", "updated_at", "metadata_json"]
            row_data = dict(zip(columns, row))
        return DocumentRecord(
            id=row_data["id"],
            document_id=row_data["document_id"],
            title=row_data["title"],
            file_path=row_data["file_path"],
            extension=row_data["extension"],
            mime_type=row_data["mime_type"],
            size_bytes=row_data["size_bytes"],
            sha256=row_data["sha256"],
            created_at=row_data["created_at"],
            updated_at=row_data["updated_at"],
            metadata=JsonSerializer.loads(row_data["metadata_json"]) if row_data["metadata_json"] else {},
        )
