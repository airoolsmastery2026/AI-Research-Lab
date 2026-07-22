"""High-level vector store manager."""

from __future__ import annotations

from typing import Any

from .base import BaseVectorStore, VectorRecord
from .memory_store import MemoryVectorStore
from .search import SearchRequest, SearchResult


class VectorStoreManager:
    """Coordinate vector store operations with dependency injection."""

    def __init__(self, store: BaseVectorStore | None = None) -> None:
        self.store = store or MemoryVectorStore()

    def upsert(self, record_id: str, vector: list[float], metadata: dict[str, Any] | None = None) -> None:
        self.store.upsert(record_id, vector, metadata)

    def get(self, record_id: str) -> VectorRecord | None:
        return self.store.get(record_id)

    def search(self, request: SearchRequest) -> list[SearchResult]:
        return self.store.search(request)

    def delete(self, record_id: str) -> None:
        self.store.delete(record_id)

    def export_data(self) -> dict[str, Any]:
        if hasattr(self.store, "export_data"):
            return self.store.export_data()
        return {"namespace": self.store.namespace, "items": []}

    def import_data(self, payload: dict[str, Any]) -> None:
        if hasattr(self.store, "import_data"):
            self.store.import_data(payload)
