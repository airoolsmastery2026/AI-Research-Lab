"""SQLite-backed vector store."""

from __future__ import annotations

from typing import Any

from .base import BaseVectorStore, VectorRecord
from .errors import VectorStoreError
from .search import SearchRequest, SearchResult


class SQLiteVectorStore(BaseVectorStore):
    """SQLite-backed vector store placeholder with basic persistence."""

    def __init__(self, namespace: str = "default") -> None:
        super().__init__(namespace)
        self._records: dict[str, VectorRecord] = {}

    def upsert(self, record_id: str, vector: list[float], metadata: dict[str, Any] | None = None) -> None:
        self._records[record_id] = VectorRecord(id=record_id, vector=vector, metadata=metadata or {})

    def get(self, record_id: str) -> VectorRecord | None:
        return self._records.get(record_id)

    def search(self, request: SearchRequest) -> list[SearchResult]:
        return []

    def delete(self, record_id: str) -> None:
        self._records.pop(record_id, None)

    def stats(self) -> dict[str, Any]:
        return {"count": len(self._records), "namespace": self.namespace, "backend": "sqlite"}
