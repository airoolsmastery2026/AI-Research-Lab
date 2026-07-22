"""In-memory vector store backend."""

from __future__ import annotations

from typing import Any

from .base import BaseVectorStore, VectorRecord
from .errors import VectorStoreError
from .filters import FilterCriteria
from .search import SearchRequest, SearchResult
from .serializer import deserialize_record, serialize_record
from .similarity import cosine_similarity


class MemoryVectorStore(BaseVectorStore):
    """Simple in-memory store with basic search and filtering."""

    def __init__(self, namespace: str = "default") -> None:
        super().__init__(namespace)
        self._records: dict[str, VectorRecord] = {}

    def upsert(self, record_id: str, vector: list[float], metadata: dict[str, Any] | None = None) -> None:
        self._records[record_id] = VectorRecord(id=record_id, vector=vector, metadata=metadata or {})

    def get(self, record_id: str) -> VectorRecord | None:
        return self._records.get(record_id)

    def search(self, request: SearchRequest) -> list[SearchResult]:
        if request.top_k <= 0:
            raise VectorStoreError("top_k must be positive")

        if request.filters is None:
            request.filters = FilterCriteria(namespace=self.namespace)
        else:
            request.filters.namespace = self.namespace

        scored: list[tuple[float, SearchResult]] = []
        for record in self._records.values():
            if request.filters.metadata and not all(record.metadata.get(key) == value for key, value in request.filters.metadata.items()):
                continue
            score = cosine_similarity(request.query_vector, record.vector)
            scored.append((score, SearchResult(id=record.id, score=score, metadata=record.metadata)))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [result for _, result in scored[:request.top_k]]

    def delete(self, record_id: str) -> None:
        self._records.pop(record_id, None)

    def stats(self) -> dict[str, Any]:
        return {"count": len(self._records), "namespace": self.namespace, "backend": "memory"}

    def export_data(self) -> dict[str, Any]:
        return {"namespace": self.namespace, "items": [serialize_record(record) for record in self._records.values()]}

    def import_data(self, payload: dict[str, Any]) -> None:
        self._records = {item["id"]: deserialize_record(item) for item in payload.get("items", [])}
        self.namespace = payload.get("namespace", self.namespace)
